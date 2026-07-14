#[cfg(test)]
mod tests;

pub mod network_manager;
pub mod ssh_scanner;
pub mod ftp_scanner;
pub mod smb_scanner;
pub mod sql_scanner;

use std::net::IpAddr;
use std::str::FromStr;
use std::time::Duration;
use thiserror::Error;

#[derive(Error, Debug, PartialEq, Clone)]
pub enum EngineError {
    #[error("Invalid target format: {0}")]
    InvalidTarget(String),
    #[error("Connection timeout after {0:?}")]
    Timeout(Duration),
    #[error("Scan failed: {0}")]
    ActionFailed(String),
}

#[derive(Debug, Clone, PartialEq)]
pub enum Target {
    Ip { address: IpAddr, port: Option<u16> },
    Hostname { name: String, port: Option<u16> },
}

impl Target {
    pub fn parse(raw: &str) -> Result<Self, EngineError> {
        let mut parts = raw.splitn(2, ':');
        let host_part = parts.next().ok_or_else(|| EngineError::InvalidTarget("Empty hostname".into()))?;
        let port_part = parts.next();

        let port = match port_part {
            Some(p) => Some(p.parse::<u16>().map_err(|_| EngineError::InvalidTarget("Invalid port number".into()))?),
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

#[derive(Debug, PartialEq)]
pub struct ScanResult {
    pub latency: Duration,
    pub success: bool,
}

#[async_trait::async_trait]
pub trait Scanner {
    async fn scan(&self, target: &Target) -> Result<ScanResult, EngineError>;
}
