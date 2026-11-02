pub mod network_manager;
pub mod wifi_scanner;
pub mod ssh_scanner;
pub mod ftp_scanner;
pub mod smb_scanner;
pub mod sql_scanner;

use std::net::IpAddr;
use std::str::FromStr;
use std::time::Duration;
use thiserror::Error;
use serde::{Serialize, Deserialize};

#[derive(Error, Debug, Clone)]
pub enum EngineError {
    #[error("Invalid target format: {0}")]
    InvalidTarget(String),
    #[error("Connection timeout after {0:?}")]
    Timeout(Duration),
    #[error("Scan failed: {0}")]
    ActionFailed(String),
    #[error("Network I/O error: {0}")]
    IoError(String),
    #[error("WiFi monitor mode unsupported")]
    MonitorModeUnavailable,
    #[error("pcap capture error: {0}")]
    PcapError(String),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum Target {
    Ip { address: IpAddr, port: Option<u16> },
    Hostname { name: String, port: Option<u16> },
}

impl Target {
    pub fn parse(raw: &str) -> Result<Self, EngineError> {
        let mut parts = raw.splitn(2, ':');
        let host_part = parts.next()
            .ok_or_else(|| EngineError::InvalidTarget("Empty hostname".into()))?;
        let port_part = parts.next();

        let port = match port_part {
            Some(p) => Some(
                p.parse::<u16>()
                    .map_err(|_| EngineError::InvalidTarget("Invalid port number".into()))?
            ),
            None => None,
        };

        if let Ok(ip) = IpAddr::from_str(host_part) {
            Ok(Target::Ip { address: ip, port })
        } else {
            Ok(Target::Hostname { name: host_part.to_string(), port })
        }
    }

    pub fn host(&self) -> String {
        match self {
            Target::Ip { address, .. } => address.to_string(),
            Target::Hostname { name, .. } => name.clone(),
        }
    }

    pub fn port(&self) -> Option<u16> {
        match self {
            Target::Ip { port, .. } | Target::Hostname { port, .. } => *port,
        }
    }
}

#[derive(Debug, PartialEq, Clone, Serialize, Deserialize)]
pub struct ScanResult {
    pub latency_ms: u64,
    pub success: bool,
    pub service_info: Option<String>,
    pub port: Option<u16>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WifiApResult {
    pub bssid: String,
    pub ssid: String,
    pub channel: u8,
    pub signal_dbm: i8,
    pub encryption: String,
    pub first_seen_ms: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HandshakeCapture {
    pub bssid: String,
    pub essid: String,
    pub timestamp_ms: u64,
    pub handshake_type: String,
    pub pcap_file: String,
}

#[async_trait::async_trait]
pub trait Scanner {
    async fn scan(&self, target: &Target) -> Result<ScanResult, EngineError>;
}

#[async_trait::async_trait]
pub trait WifiScanner {
    async fn set_monitor_mode(&self, iface: &str, enable: bool) -> Result<(), EngineError>;
    async fn scan_aps(&self, iface: &str, channels: &[u8]) -> Result<Vec<WifiApResult>, EngineError>;
    async fn capture_handshake(&self, iface: &str, target_bssid: &str, timeout_s: u64) -> Result<Option<HandshakeCapture>, EngineError>;
    async fn wifi_stats(&self, iface: &str) -> Result<String, EngineError>;
}

pub fn result_to_json(result: &ScanResult) -> String {
    serde_json::to_string(result).unwrap_or_else(|_| "{}".to_string())
}

pub async fn tcp_connect_with_timeout(
    addr: &str,
    port: u16,
    timeout: Duration,
    banner_bytes: usize,
) -> Result<(Duration, Option<String>), EngineError> {
    let start = std::time::Instant::now();
    let connect_addr = format!("{}:{}", addr, port);

    let mut tcp_stream = tokio::time::timeout(
        timeout,
        tokio::net::TcpStream::connect(&connect_addr),
    )
    .await
    .map_err(|_| EngineError::Timeout(timeout))?
    .map_err(|e| EngineError::IoError(e.to_string()))?;

    let latency = start.elapsed();

    let mut buf = vec![0u8; banner_bytes];
    let bytes_read = tokio::time::timeout(
        Duration::from_millis(500),
        tokio::io::AsyncReadExt::read(&mut tcp_stream, &mut buf),
    )
    .await
    .unwrap_or(Ok(0));

    let banner = match bytes_read {
        Ok(n) if n > 0 => {
            buf.truncate(n);
            let text = String::from_utf8_lossy(&buf);
            let trimmed = text.trim();
            if trimmed.is_empty() {
                None
            } else {
                Some(trimmed.to_string())
            }
        }
        _ => None,
    };

    // Drop tcp_stream explicitly to avoid leak warning
    drop(tcp_stream);
    Ok((latency, banner))
}

pub async fn run_cmd(cmd: &str, args: &[&str], timeout: Duration) -> Result<String, EngineError> {
    let output = tokio::time::timeout(
        timeout,
        tokio::process::Command::new(cmd)
            .args(args)
            .output(),
    )
    .await
    .map_err(|_| EngineError::Timeout(timeout))?
    .map_err(|e| EngineError::IoError(e.to_string()))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).trim().to_string())
    } else {
        let err_msg = String::from_utf8_lossy(&output.stderr).trim().to_string();
        Err(EngineError::ActionFailed(format!("cmd '{}' failed: {}", cmd, err_msg)))
    }
}

pub fn timestamp_ms() -> u64 {
    let now = chrono::Utc::now();
    now.timestamp_millis() as u64
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_parse_target_simple() {
        let t = Target::parse("127.0.0.1").unwrap();
        assert_eq!(t.host(), "127.0.0.1");
        assert_eq!(t.port(), None);
    }

    #[tokio::test]
    async fn test_parse_target_with_port() {
        let t = Target::parse("192.168.1.1:8080").unwrap();
        assert_eq!(t.host(), "192.168.1.1");
        assert_eq!(t.port(), Some(8080));
    }

    #[tokio::test]
    async fn test_parse_hostname() {
        let t = Target::parse("router.local").unwrap();
        assert_eq!(t.host(), "router.local");
    }

    #[tokio::test]
    async fn test_timestamp_ms_positive() {
        let ts = timestamp_ms();
        assert!(ts > 0);
        assert!(ts < 4_102_444_000_000);
    }
}
