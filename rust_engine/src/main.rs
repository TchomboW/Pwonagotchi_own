use pwon_core::network_manager::NetworkService;
use pwon_core::WifiScanner;
use pwon_core::Scanner;

#[tokio::main]
async fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: pwon_core <module> [args...]");
        eprintln!("Modules: network, wifi, scan, ssh, ftp, smb, sql");
        std::process::exit(1);
    }

    let module_name = &args[1];
    let timeout_str = std::env::var("PWN_TIMEOUT_SECS").unwrap_or_else(|_| "30".to_string());
    let timeout_secs: u64 = timeout_str.parse().unwrap_or(30);

    match module_name.as_str() {
        // ---- Network module ----
        "network" => {
            if args.len() < 3 {
                eprintln!("Usage: pwon_core network <wifi|eth>");
                std::process::exit(1);
            }
            let mode = &args[2];
            let nm = pwon_core::network_manager::NetworkManager::new();

            match mode.as_str() {
                "wifi" => {
                    if let Err(e) = nm.switch_to_wifi().await {
                        eprintln!("FAILURE|error:{}", e);
                        std::process::exit(1);
                    }
                    println!("SUCCESS|status:wifi_up");
                }
                "eth" => {
                    if let Err(e) = nm.switch_to_ethernet().await {
                        eprintln!("FAILURE|error:{}", e);
                        std::process::exit(1);
                    }
                    println!("SUCCESS|status:eth_up");
                }
                "stats" => {
                    if let Ok(iface) = nm.get_active_interface().await {
                        println!("SUCCESS|active_interface:{}", iface);
                    } else {
                        eprintln!("FAILURE|error:could not determine interface");
                        std::process::exit(1);
                    }
                }
                _ => {
                    eprintln!("Unknown network mode: {}", mode);
                    std::process::exit(1);
                }
            }
        }

        // ---- WiFi module ----
        "wifi" => {
            if args.len() < 3 {
                eprintln!("Usage: pwon_core wifi <scan|monitor_on|monitor_off|capture|stats> [args...]");
                std::process::exit(1);
            }
            let subcmd = &args[2];
            let iface = args.get(3).map(|s| s.as_str()).unwrap_or("wlan0");

            match subcmd.as_str() {
                "scan" => {
                    // Scan 2.4GHz channels: 1-11
                    let channels: [u8; 11] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
                    let wsc = pwon_core::wifi_scanner::WifiScanner::new();

                    match wsc.scan_aps(iface, &channels).await {
                        Ok(aps) => {
                            println!("SUCCESS|aps_detected:{}", aps.len());
                            for ap in &aps {
                                println!(
                                    "AP|bssid:{}|ssid:{}|ch:{}|signal:{}|enc:{}",
                                    ap.bssid, ap.ssid, ap.channel, ap.signal_dbm, ap.encryption
                                );
                            }
                        }
                        Err(e) => {
                            eprintln!("FAILURE|error:{}", e);
                            std::process::exit(1);
                        }
                    }
                }
                "monitor_on" => {
                    let wsc = pwon_core::wifi_scanner::WifiScanner::new();
                    match wsc.set_monitor_mode(iface, true).await {
                        Ok(_) => println!("SUCCESS|monitor:{}_on", iface),
                        Err(e) => {
                            eprintln!("FAILURE|error:{}", e);
                            std::process::exit(1);
                        }
                    }
                }
                "monitor_off" => {
                    let wsc = pwon_core::wifi_scanner::WifiScanner::new();
                    match wsc.set_monitor_mode(iface, false).await {
                        Ok(_) => println!("SUCCESS|monitor:{}_off", iface),
                        Err(e) => {
                            eprintln!("FAILURE|error:{}", e);
                            std::process::exit(1);
                        }
                    }
                }
                "capture" => {
                    // Usage: pwon_core wifi capture <iface> <bssid> [timeout]
                    if args.len() < 5 {
                        eprintln!("Usage: pwon_core wifi capture <iface> <bssid> [timeout_s]");
                        std::process::exit(1);
                    }
                    let target_bssid = &args[4];
                    let cap_timeout: u64 = args.get(5)
                        .and_then(|s| s.parse().ok())
                        .unwrap_or(timeout_secs);

                    let wsc = pwon_core::wifi_scanner::WifiScanner::new();
                    match wsc.capture_handshake(iface, target_bssid, cap_timeout).await {
                        Ok(Some(capture)) => {
                            println!("SUCCESS|handshake_captured:true");
                            println!("CAPTURE|bssid:{}|essid:{}|type:{}|file:{}",
                                capture.bssid, capture.essid, capture.handshake_type, capture.pcap_file);
                        }
                        Ok(None) => {
                            println!("SUCCESS|handshake_captured:false|note:no_eapol_frames");
                        }
                        Err(e) => {
                            eprintln!("FAILURE|error:{}", e);
                            std::process::exit(1);
                        }
                    }
                }
                "stats" => {
                    let wsc = pwon_core::wifi_scanner::WifiScanner::new();
                    match wsc.wifi_stats(iface).await {
                        Ok(stats) => println!("SUCCESS|stats:{}", stats),
                        Err(e) => {
                            eprintln!("FAILURE|error:{}", e);
                            std::process::exit(1);
                        }
                    }
                }
                _ => {
                    eprintln!("Unknown wifi subcommand: {}", subcmd);
                    std::process::exit(1);
                }
            }
        }

        // ---- Scanner modules (ssh/ftp/smb/sql) ----
        "ssh" | "ftp" | "smb" | "sql" => {
            if args.len() < 3 {
                eprintln!("Usage: pwon_core <module> <target:port>");
                std::process::exit(1);
            }
            let target_raw = &args[2];
            let target = match pwon_core::Target::parse(target_raw) {
                Ok(t) => t,
                Err(e) => {
                    eprintln!("Error parsing target: {}", e);
                    std::process::exit(1);
                },
            };

            // Read credentials from environment variables
            let env_prefix = match module_name.as_str() {
                "ssh" => "SSH",
                "ftp" => "FTP",
                "smb" => "SMB",
                "sql" => "SQL",
                _ => "UNKNOWN",
            };
            let user_env = format!("PWN_{}_USER", env_prefix);
            let pass_env = format!("PWN_{}_PASS", env_prefix);
            let user = std::env::var(&user_env).unwrap_or_else(|_| String::new());
            let pass = std::env::var(&pass_env).unwrap_or_else(|_| String::new());

            match module_name.as_str() {
                "ssh" => {
                    let scanner = pwon_core::ssh_scanner::SSHScanner::new(&user, &pass);
                    let result = scanner.scan(&target).await.unwrap_or_else(|e| {
                        pwon_core::ScanResult {
                            latency_ms: 0, success: false,
                            service_info: Some(format!("error:{}", e)), port: None,
                        }
                    });
                    println!("{}", pwon_core::result_to_json(&result));
                }
                "ftp" => {
                    let scanner = pwon_core::ftp_scanner::FTPScanner::new(&user, &pass);
                    let result = scanner.scan(&target).await.unwrap_or_else(|e| {
                        pwon_core::ScanResult {
                            latency_ms: 0, success: false,
                            service_info: Some(format!("error:{}", e)), port: None,
                        }
                    });
                    println!("{}", pwon_core::result_to_json(&result));
                }
                "smb" => {
                    let scanner = pwon_core::smb_scanner::SMBScanner::new();
                    let result = scanner.scan(&target).await.unwrap_or_else(|e| {
                        pwon_core::ScanResult {
                            latency_ms: 0, success: false,
                            service_info: Some(format!("error:{}", e)), port: None,
                        }
                    });
                    println!("{}", pwon_core::result_to_json(&result));
                }
                "sql" => {
                    let scanner = pwon_core::sql_scanner::SQLScanner::new();
                    let result = scanner.scan(&target).await.unwrap_or_else(|e| {
                        pwon_core::ScanResult {
                            latency_ms: 0, success: false,
                            service_info: Some(format!("error:{}", e)), port: None,
                        }
                    });
                    println!("{}", pwon_core::result_to_json(&result));
                }
                _ => unreachable!(),
            }
        }

        _ => {
            eprintln!("Unknown module: {}", module_name);
            eprintln!("Available: network, wifi, ssh, ftp, smb, sql");
            std::process::exit(1);
        }
    }
}
