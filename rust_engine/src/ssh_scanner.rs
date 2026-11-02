use std::time::Duration;
use async_trait::async_trait;
use crate::{Scanner, Target, ScanResult, EngineError, tcp_connect_with_timeout};

#[derive(Debug, Clone)]
pub struct SSHScanner {
    pub username: String,
    pub password: String,
    timeout: Duration,
}

impl SSHScanner {
    pub fn new(username: &str, password: &str) -> Self {
        Self {
            username: username.to_string(),
            password: password.to_string(),
            timeout: Duration::from_secs(10),
        }
    }
    fn default_port() -> u16 { 22 }
}

#[async_trait]
impl Scanner for SSHScanner {
    async fn scan(&self, target: &Target) -> Result<ScanResult, EngineError> {
        let port = target.port().unwrap_or_else(Self::default_port);
        let host = target.host();

        match tcp_connect_with_timeout(&host, port, self.timeout, 256).await {
            Ok((latency, banner)) => {
                let is_ssh = banner.as_ref().is_some_and(|b| {
                    b.to_lowercase().contains("ssh") || b.to_lowercase().contains("sshd")
                });
                Ok(ScanResult {
                    latency_ms: latency.as_millis() as u64,
                    success: is_ssh,
                    service_info: banner,
                    port: Some(port),
                })
            }
            Err(e) => Ok(ScanResult {
                latency_ms: self.timeout.as_millis() as u64,
                success: false,
                service_info: Some(format!("ssh_error:{}", e)),
                port: Some(port),
            }),
        }
    }
}
