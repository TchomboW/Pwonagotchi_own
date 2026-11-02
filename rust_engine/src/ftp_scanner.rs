
use std::time::Duration;
use async_trait::async_trait;
use crate::{Target, ScanResult, EngineError, Scanner, tcp_connect_with_timeout};

pub struct FTPScanner {
    pub username: String,
    pub password: String,
}

impl FTPScanner {
    pub fn new(username: &str, password: &str) -> Self {
        Self {
            username: username.to_string(),
            password: password.to_string(),
        }
    }
}

#[async_trait]
impl Scanner for FTPScanner {
    async fn scan(&self, target: &Target) -> Result<ScanResult, EngineError> {
        let host = target.host();
        let port = target.port().unwrap_or(21);
        let timeout = Duration::from_secs(10);

        let (latency, banner) = tcp_connect_with_timeout(&host, port, timeout, 512).await?;

        let is_ftp = banner.as_ref().is_some_and(|b| {
            let b_l = b.to_lowercase();
            b_l.contains("ftp") || b.starts_with("220") || b_l.contains("welcome")
        });

        let service_info = if is_ftp {
            banner.clone().map(|b| format!("FTP: {}", b.lines().next().unwrap_or("unknown")))
                .unwrap_or("FTP detected".to_string())
        } else {
            banner.map(|b| format!("Unknown service: {}", b.lines().next().unwrap_or("unknown")))
                .unwrap_or("Banner grabbed".to_string())
        };

        Ok(ScanResult {
            latency_ms: latency.as_millis() as u64,
            success: is_ftp,
            service_info: Some(service_info),
            port: Some(port),
        })
    }
}
