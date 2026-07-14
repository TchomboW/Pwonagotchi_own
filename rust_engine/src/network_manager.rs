use crate::EngineError;
use std::process::Command;
use std::path::Path;

#[async_trait::async_trait]
pub trait NetworkService {
    async fn get_active_interface(&self) -> Result<String, EngineError>;
    async fn switch_to_wifi(&self) -> Result<(), EngineError>;
    async fn switch_to_ethernet(&self) -> Result<(), EngineError>;
}

pub struct NetworkManager;

impl NetworkManager {
    pub fn new() -> Self {
        Self
    }

    // This is the "Dongle Detection" logic. 
    // It checks if an ethernet device (potentially a dongle) has appeared in /sys/class/net/
    async fn detect_best_interface(&self) -> String {
        let mut interfaces = Vec::new();
        if let Ok(entries) = std::fs::read_dir("/sys/class/net") {
            for entry in entries.flatten() {
                let name = entry.file_name().into_string().unwrap_or_default();
                // We look specifically for 'eth' or 'enp' (standard Linux prefixes)
                if name.starts_with("eth") || name.starts_with("en") { // FIXED TYPO HERE
                    interfaces.push(name);
                }
            }
        }

        // If we found an ethernet interface, return the first one
        if !interfaces.is_empty() {
            return interfaces[0].clone();
        }

        "wlan0".to_string()
    }

    async fn check_carrier(&self, iface: &str) -> bool {
        let path = format!("/sys/class/net/{}/carrier", iface);
        if Path::new(&path).exists() {
            if let Ok(status) = std::fs::read_to_string(path) {
                return status.trim() == "1";
            }
        }
        false
    }

    fn run_cmd(&self, cmd: &str, args: &[&str]) -> Result<(), EngineError> {
        let status = Command::new(cmd)
            .args(args)
            .status()
            .map_err(|e| EngineError::ActionFailed(format!("Command failed to execute: {}", e)))?;

        if status.success() {
            Ok(())
        } else {
            Err(EngineError::ActionFailed(format!("Command '{} {:?}' exited with non-zero status", cmd, args)))
        }
    }
}

#[async_trait::async_trait]
impl NetworkService for NetworkManager {
    async fn get_active_interface(&self) -> Result<String, EngineError> {
        let best = self.detect_best_interface().await;
        if best != "wlan0" && self.check_carrier(&best).await {
            Ok(best)
        } else {
            Ok("wlan0".to_string())
        }
    }

    async fn switch_to_wifi(&self) -> Result<(), EngineError> {
        // Prioritize bringing up wlan0 for the Safety Loopback/Control UI
        self.run_cmd("ip", &["link", "set", "wlan0", "up"])?;
        Ok(())
    }

    async fn switch_to_ethernet(&self) -> Result<(), EngineError> {
        let target = self.detect_best_interface().await;
        if target == "wlan0" {
            return Err(EngineError::ActionFailed("No ethernet interface detected for dongle/switch.".into()));
        }
        self.run_cmd("ip", &["link", "set", &target, "up"])?;
        Ok(())
    }
}
