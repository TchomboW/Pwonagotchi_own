use std::time::Duration;
use std::collections::HashSet;
use async_trait::async_trait;
use crate::{WifiApResult, HandshakeCapture, EngineError, run_cmd, timestamp_ms};

pub struct WifiScanner;

impl Default for WifiScanner {
    fn default() -> Self {
        Self
    }
}

impl WifiScanner {
    pub fn new() -> Self { Self }

    fn cmd_timeout() -> Duration { Duration::from_secs(30) }
}

#[async_trait]
impl crate::WifiScanner for WifiScanner {
    async fn set_monitor_mode(&self, iface: &str, enable: bool) -> Result<(), EngineError> {
        if enable {
            let _ = run_cmd("ip", &["link", "set", iface, "down"], Self::cmd_timeout()).await;

            match run_cmd("iw", &["dev", iface, "set", "type", "monitor"], Self::cmd_timeout()).await {
                Ok(_) => {
                    let _ = run_cmd("ip", &["link", "set", iface, "up"], Self::cmd_timeout()).await;
                    Ok(())
                }
                Err(_) => {
                    let mon_iface = format!("{}_mon", iface);
                    let _ = run_cmd(
                        "iw",
                        &["dev", iface, "interface", "add", &mon_iface, "type", "monitor"],
                        Self::cmd_timeout(),
                    ).await;
                    let _ = run_cmd(
                        "ip",
                        &["link", "set", &mon_iface, "up"],
                        Self::cmd_timeout(),
                    ).await;
                    Ok(())
                }
            }
        } else {
            let _ = run_cmd("ip", &["link", "set", iface, "down"], Self::cmd_timeout()).await;
            run_cmd("iw", &["dev", iface, "set", "type", "__automatic"], Self::cmd_timeout()).await?;
            Ok(())
        }
    }

    async fn scan_aps(&self, iface: &str, channels: &[u8]) -> Result<Vec<WifiApResult>, EngineError> {
        let mut results: Vec<WifiApResult> = Vec::new();

        for &ch in channels {
            let ch_str = ch.to_string();
            let _ = run_cmd(
                "iw",
                &["dev", iface, "set", "channel", &ch_str],
                Duration::from_secs(5),
            ).await;

            match run_cmd(
                "iw",
                &["dev", iface, "scan"],
                Duration::from_secs(15),
            ).await {
                Ok(output) => {
                    for line in output.lines() {
                        let trimmed = line.trim();

                        if trimmed.starts_with("BSS ") || trimmed.starts_with("BSS[") {
                            let bss_part = trimmed.trim_start_matches("BSS [").trim_start_matches("BSS ");
                            let bssid_end = bss_part.find(' ').unwrap_or(bss_part.len());
                            let bssid = bss_part[..bssid_end].trim().to_string();

                            if !bssid.is_empty() && bssid.len() >= 17 {
                                results.push(WifiApResult {
                                    bssid,
                                    ssid: String::new(),
                                    channel: ch,
                                    signal_dbm: 0,
                                    encryption: "unknown".to_string(),
                                    first_seen_ms: timestamp_ms(),
                                });
                            }
                        }

                        if trimmed.starts_with("\tSSID: ") {
                            let ssid = trimmed[6..].to_string();
                            if let Some(last) = results.last_mut() {
                                last.ssid = ssid;
                            }
                        }

                        if let Some(sig_str) = trimmed.strip_prefix("\tsignal:") {
                            let sig_str = sig_str.trim();
                            if let Ok(val) = sig_str.parse::<i8>() {
                                if let Some(last) = results.last_mut() {
                                    last.signal_dbm = val;
                                }
                            }
                        }
                    }
                }
                Err(_) => { /* skip channel */ }
            }

            tokio::time::sleep(Duration::from_millis(200)).await;
        }

        let mut seen = HashSet::new();
        results.retain(|ap| seen.insert(ap.bssid.clone()));

        Ok(results)
    }

    async fn capture_handshake(
        &self,
        iface: &str,
        target_bssid: &str,
        timeout_s: u64,
    ) -> Result<Option<HandshakeCapture>, EngineError> {
        let capture_dir = std::path::Path::new("/tmp/pwon_captures");
        let _ = std::fs::create_dir_all(capture_dir);

        let pcap_path = capture_dir.join(format!(
            "capture_{}.pcap",
            target_bssid.replace(':', "_")
        ));

        let pcap_str = pcap_path.to_string_lossy().to_string();
        let timeout_str = timeout_s.to_string();

        let tcpdump_cmd = format!(
            "timeout {} tcpdump -i {} -w {} -s 0 \'ether host {} and type mgt\' 2>/dev/null",
            timeout_str, iface, pcap_str, target_bssid
        );

        let tcpdump_cmd_ref = tcpdump_cmd.as_str();
        let _ = run_cmd("sh", &["-c", tcpdump_cmd_ref], Duration::from_secs(timeout_s + 30)).await;

        if pcap_path.exists() {
            let metadata = std::fs::metadata(&pcap_path).map_err(|e| EngineError::PcapError(e.to_string()))?;
            if metadata.len() > 100 {
                let check = format!(
                    "tcpdump -r {} -c 10 \'type mgt\' 2>/dev/null | grep -c EAPOL || true",
                    pcap_str
                );
                let check_ref = check.as_str();
                if let Ok(count) = run_cmd("sh", &["-c", check_ref], Duration::from_secs(10)).await {
                    let has_handshake = count.parse::<u32>().unwrap_or(0) > 0;

                    return Ok(if has_handshake {
                        Some(HandshakeCapture {
                            bssid: target_bssid.to_string(),
                            essid: String::new(),
                            timestamp_ms: timestamp_ms(),
                            handshake_type: "full_wpa".to_string(),
                            pcap_file: pcap_path.to_string_lossy().to_string(),
                        })
                    } else {
                        None
                    });
                }
            }
        }

        Ok(None)
    }

    async fn wifi_stats(&self, iface: &str) -> Result<String, EngineError> {
        let stats = format!("ip link show {}", iface);
        let stats_ref = stats.as_str();
        let output = run_cmd("sh", &["-c", stats_ref], Duration::from_secs(5)).await?;

        let mode_check = run_cmd(
            "iw",
            &["dev", iface, "info"],
            Duration::from_secs(5),
        ).await;

        let mode = match mode_check {
            Ok(info) => info.lines()
                .find(|l| l.contains("type"))
                .unwrap_or("unknown mode")
                .to_string(),
            Err(_) => "cannot query".to_string(),
        };

        Ok(format!("iface:{}|{}|mode:{}", iface, output.lines().next().unwrap_or(""), mode))
    }
}
