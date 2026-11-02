
use std::time::Duration;
use async_trait::async_trait;
use crate::{Target, ScanResult, EngineError, Scanner, tcp_connect_with_timeout};

pub struct SQLScanner;

impl SQLScanner {
    pub fn new() -> Self { Self }
}

#[async_trait]
impl Scanner for SQLScanner {
    async fn scan(&self, target: &Target) -> Result<ScanResult, EngineError> {
        let host = target.host();
        let default_ports = [3306, 5432, 1433, 27017]; // MySQL, PostgreSQL, MSSQL, MongoDB
        let mut results = Vec::new();

        let timeout = Duration::from_secs(8);

        for &port in &default_ports {
            match tcp_connect_with_timeout(&host, port, timeout, 256).await {
                Ok((latency, banner)) => {
                    let db_name = match port {
                        3306 => "MySQL",
                        5432 => "PostgreSQL",
                        1433 => "MSSQL",
                        27017 => "MongoDB",
                        _ => "Unknown DB",
                    };

                    let service_info = banner
                        .map(|b| format!("{}: {}", db_name, b.lines().next().unwrap_or("connected")))
                        .unwrap_or_else(|| format!("{} open", db_name));

                    results.push(ScanResult {
                        latency_ms: latency.as_millis() as u64,
                        success: true,
                        service_info: Some(service_info),
                        port: Some(port),
                    });
                }
                Err(_) => { /* port closed or timed out */ }
            }
        }

        if results.is_empty() {
            Ok(ScanResult {
                latency_ms: 0,
                success: false,
                service_info: Some("No common DB ports open".to_string()),
                port: None,
            })
        } else {
            // Return the most interesting result (first DB found)
            Ok(results.into_iter().next().unwrap())
        }
    }
}

impl Default for SQLScanner {
    fn default() -> Self {
        Self
    }
}
