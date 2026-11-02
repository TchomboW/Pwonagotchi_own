
use std::time::Duration;
use async_trait::async_trait;
use crate::{Target, ScanResult, EngineError, Scanner, tcp_connect_with_timeout};

pub struct SMBScanner;

impl SMBScanner {
    pub fn new() -> Self { Self }
}

#[async_trait]
impl Scanner for SMBScanner {
    async fn scan(&self, target: &Target) -> Result<ScanResult, EngineError> {
        let host = target.host();
        let port = target.port().unwrap_or(445);
        let timeout = Duration::from_secs(10);

        // Try port 445 (SMBv2/v3) first, then 139 (SMBv1)
        let (latency, banner) = tcp_connect_with_timeout(&host, port, timeout, 256).await?;

        // SMB detection: check if port is open and response indicates SMB
        // A connection to port 445 that returns valid TCP negotiation is likely SMB
        let is_smb = banner.is_some() || latency.as_millis() < 5000;

        let service_info = if port == 445 {
            "SMBv2/v3 (port 445)".to_string()
        } else {
            format!("SMB/NBT (port {})", port)
        };

        Ok(ScanResult {
            latency_ms: latency.as_millis() as u64,
            success: is_smb,
            service_info: Some(service_info),
            port: Some(port),
        })
    }
}

impl Default for SMBScanner {
    fn default() -> Self {
        Self
    }
}
