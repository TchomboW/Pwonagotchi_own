use crate::{Scanner, Target, ScanResult, EngineError};
use std::time::Duration;
use async_trait::async_trait;

#[derive(Debug, Clone)]
pub struct SMBScanner { pub username: String, pub password: String }
impl SMBScanner { pub fn new(u: &str, p: &str) -> Self { Self { username: u.to_string(), password: p.to_string() } } }

#[async_trait]
impl Scanner for SMBScanner {
    async fn scan(&self, _t: &Target) -> Result<ScanResult, EngineError> {
        tokio::time::sleep(Duration::from_millis(10)).await; 
        Ok(ScanResult { latency: Duration::from_millis(5), success: true })
    }
}
