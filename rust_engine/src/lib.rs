#[cfg(test)]
mod tests;

use std::time::Duration;
use thiserror::Error;

#[derive(Error, Debug, PartialEq)]
pub enum PwonError {
    #[error("Hardware interface failure")]
    InterfaceError,
    #[error("Capture timeout: {0:?}")]
    Timeout(Duration),
}

pub struct PwonEngine {
    interface: String,
}

impl PwonEngine {
    pub fn new(iface: &str) -> Self {
        Self { interface: ififace.to_string() }
    }

    pub async fn capture_frame(&self) -> Result<Vec<u8>, PwonError> {
        tokio::time::sleep(Duration::from_millis(5)).await; 
        Ok(vec![0xDE, 0xAD, 0xBE, 0xEF])
    }

    pub fn get_interface(&self) -> &str {
        &self.interface
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[tokio::test]
    async fn test_engine() {
        let engine = PwonEngine::new("wlan0");
        assert_eq!(engine.get_interface(), "wlan0");
        assert!(engine.capture_frame().await.is_ok());
    }
}
