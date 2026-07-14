#[tokio::main]
async fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: pwon_core <module> [arg]");
        std::process::exit(1);
    }

    let module_name = &args[1];

    match module_name.as_str() {
        "network" => {
            if args.len() < 3 {
                eprintln!("Usage: pwon_core network <wifi|eth>");
                std::process::exit(1);
            }
            let mode = &args[2];
            use pwon_core::network_manager::NetworkService; 
            let nm = pwon_core::network_manager::NetworkManager::new();

            match mode.as_str() {
                "wifi" => {
                    println!("Executing: Switch to WiFi...");
                    if let Err(e) = nm.switch_to_wifi().await {
                        eprintln!("FAILURE|error:{}", e);
                        std::process::exit(1);
                    }
                    println!("SUCCESS|status:wifi_up");
                }
                "eth" => {
                    println!("Executing: Switch to Ethernet...");
                    if let Err(e) = nm.switch_to_ethernet().await {
                        eprintln!("FAILURE|error:{}", e);
                        std::process::exit(1);
                    }
                    println!("SUCCESS|status:eth_up");
                }
                _ => {
                    eprintln!("Unknown network mode: {}", mode);
                    std::process::exit(1);
                }
            }
        }
        "ssh" | "ftp" | "smb" | "sql" => {
            if args.len() < 3 {
                eprintln!("Usage: pwon_core <module> <target>");
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

            match module_name.as_str() {
                "ssh" => execute_scan(&pwon_core::ssh_scanner::SSHScanner::new("a","p"), &target).await,
                "ftp" => execute_scan(&pwon_core::ftp_scanner::FTPScanner::new("u","p"), &target).await,
                "smb" => execute_scan(&pwon_core::smb_scanner::SMBScanner::new("u","p"), &target).await,
                "sql" => execute_scan(&pwon_core::sql_scanner::SQLScanner::new("u","p"), &target).await,
                _ => unreachable!(),
            }
        }
        _ => {
            eprintln!("Unknown module: {}", module_name);
            std::process::exit(1);
        }
    }
}

async fn execute_scan<S: pwon_core::Scanner>(s: &S, t: &pwon_core::Target) {
    match s.scan(t).await {
        Ok(r) => println!("SUCCESS|latency:{}|status:{}", r.latency.as_millis(), r.success),
        Err(e) => eprintln!("FAILURE|error:{}", e),
    }
}
