# 🐉 Pwonagotchi_own (Pi Zero W Optimized Edition)

> **Autonomous Wi-Fi Intelligence Agent — Rust + Python Hybrid Architecture**
> Optimized for Raspberry Pi Zero W / Zero 2 W running 64-bit Raspberry Pi OS (Bookworm)

## ⚖️ License & Attribution

This project is a high-performance, optimized evolution of the **Bjorn** ecosystem.
All original credit for the foundational code, core-logic, and concept goes to the **infinition/Bjorn** project.
The original Bjorn license is included in the `LICENSE` file.

**Fork lineage:** Pwonagotchi_own diverges from the standard Pwnagotchi (evilsocket → jayofelony) lineage
by replacing the Python+Go+bettercap stack with a purpose-built Rust engine + Python intelligence orchestrator,
drawing architectural inspiration from [Oxigotchi](https://github.com/CoderFX/oxigotchi) (100% Rust, zero-crash firmware patching)
and [AngryOxide](https://github.com/Ragnt/AngryOxide) (validated capture pipeline).

---

## 🔭 Project Overview

`Pwonagotchi_own` is a high-performance evolution of the original Pwnagotchi ecosystem. This version is precision-tuned
for the **Raspberry Pi Zero W / Zero 2 W** running 64-bit OS. It focuses on intelligent reconnaissance, automated
signal intelligence, and extreme resource efficiency.

### 🌟 Key Technical Upgrades:

| Feature | Stock Pwnagotchi | Pwonagotchi_own |
|---------|-----------------|----------------|
| Core engine | Python + Go (bettercap) | Rust (`pwon_core`) + Python orchestrator |
| Memory footprint | ~80 MB | ~20 MB (target) |
| Capture validation | Requires post-processing (hashie-clean) | Planned: validated, hashcat-ready captures |
| Firmware crash resilience | Crashes every 2–5 min (BCM43436) | Planned: 6-layer self-healing watchdog |
| Language | Python + Go | Rust + Python (async) |
| Binary size | 150MB+ | ~5 MB (Rust release build) |
| SD card protection | Writes every capture | Planned: tmpfs capture pipeline |

### Architecture Highlights:
- **Optimized Rust Core**: `rust_engine` with trimmed `tokio` features to reduce binary size and memory footprint
- **Unified Async Architecture**: Async/sync mismatches resolved across Python orchestrator and Rust subprocess runtime
- **Survival Protocols**: Built-in Circuit Breaker logic to prevent system crashes during resource spikes on single-core CPU
- **Externalized Configuration**: Credentials managed via environment variables (`.env` file), never committed to source
- **Memory-Efficient Data**: Lightweight Python orchestration using standard library tools

---

## 🏗️ Core Architecture

```
┌─────────────────────────────────────────────────┐
│  IntelligenceAgent (Python Async Loop)           │
│  ┌─────────────┐ ┌─────────────┐ ┌────────────┐ │
│  │ Network     │ │ Visualizer  │ │ Future:    │ │
│  │ Observer    │ │ Cycle       │ │ BT Cycle   │ │
│  └──────┬──────┘ └──────┬──────┘ └─────┬──────┘ │
│         │               │              │        │
│  ┌──────▼──────────────▼──────────────▼──────┐  │
│  │         EventBus (async pub/sub)           │  │
│  └──────┬─────────────────────────────────────┘  │
│         │                                       │
│  ┌──────▼─────────────────────────────────────┐  │
│  │     EngineOrchestrator (module registry)    │  │
│  │  ┌───────────┐ ┌──────────┐ ┌───────────┐ │  │
│  │  │Networking │ │Hardware  │ │ State    │ │  │
│  │  │Manager    │ │Controller│ │ Manager  │ │  │
│  │  └────┬──────┘ └──────────┘ └───────────┘ │  │
│  └───────┼─────────────────────────────────────┘  │
└──────────┼────────────────────────────────────────┘
           │ subprocess (JSON IPC)
   ┌───────▼────────┐
   │  pwon_core     │  ← Rust Engine (tokio async)
   │  (Rust Binary) │
   │  ┌──────────┐  │
   │  │ Scanners │  │  SSH / FTP / SMB / SQL
   │  │ Network  │  │  WiFi / Ethernet toggle
   │  │ Manager  │  │
   │  └──────────┘  │
   └────────────────┘
```

### Component Breakdown:

1. **Rust Engine (`rust_engine/`)**: Memory-safe Rust crate handling network scanning, service detection, and low-level connectivity. Built with `--release` optimization.
2. **Intelligence Orchestrator (`core/` & `intelligence/`)**: Python 3.12+ async framework managing cognitive cycles, event-driven reactivity, and state persistence.
3. **Hardware Abstraction (`core/hardware/`)**: GPIO-based peripherals (e-ink display, status LEDs, input buttons) optimized for Pi Zero W.
4. **Memory System (`intelligence/memory/`)**: Persistent JSON-based state management with hot-reload capability.
5. **Profiles System (`intelligence/profiles/`)**: Swappable intelligence profiles (e.g., Stealth mode) that reconfigure all cycle parameters atomically.

---

## 🚀 Installation & Deployment

### System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| Hardware | Raspberry Pi Zero W | Raspberry Pi Zero 2 W (2024) |
| OS | Raspberry Pi OS Bookworm 64-bit (Debian 12) | Bookworm Lite 64-bit, Kernel 6.6+ |
| SD Card | 16 GB (Class 10) | 32 GB (UHS-I) |
| Display | None (headless) | Waveshare 2.13"” V2 e-ink |
| Rust | 1.70+ | 1.75+ (stable) |
| Python | 3.11 | 3.12 |

> **Note:** 32-bit OS is **NOT** supported. Pwonagotchi_own requires 64-bit ARM (`aarch64`).

### Option A: One-Command Automatic Install

```bash
curl https://raw.githubusercontent.com/TchomboW/Pwonagotchi_own/main/quick_setup.sh | bash
```

### Option B: Manual Step-by-Step Setup

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y git build-essential pkg-config libssl-dev python3-venv python3-pip

# 2. Install Rust
if ! command -v rustc &> /dev/null;
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source ~/.cargo/env
fi

# 3. Clone & setup
git clone https://github.com/TchomboW/Pwonagotchi_own.git
cd Pwonagotchi_own

# 4. Python environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Configure (COPY EXAMPLE — NEVER COMMIT REAL creds)
cp config.json.example config.json
nano config.json  # Edit with your settings

# 6. (Optional) Set credentials via .env
cp .env.example .env
nano .env  # Add real credentials here (gitignored)

# 7. Build Rust engine
cd rust_engine && cargo build --release && cd ..

# 8. Run
python3 interface.py
```

### Option C: Docker (Host Machine Development)

```bash
docker build -t pwonagotchi .
docker run --rm --network host pwonagotchi
```

---

## ⚙️ Configuration

### Environment Variables (Recommended)

Create a `.env` file (gitignored) with credentials:

```env
SSH_USER=root
SSH_PASS=your_password
FTP_USER=ftp
FTP_PASS=your_password
SMB_USER=admin
SMB_PASS=your_password
SQL_USER=sa
SQL_PASS=your_password
```

### config.json Structure

```json
{
    "engine": {
        "rust_binary_path": "rust_engine/target/release/pwon_core",
        "subprocess_timeout_seconds": 30,
        "max_crash_retries": 5
    },
    "intelligence": {
        "cycle_interval_seconds": 5,
        "history_file": "intelligence_accumulated.json",
        "seed_targets": ["127.0.0.1"]
    },
    "scanners": {
        "ssh": { "username": "${SSH_USER}", "password": "${SSH_PASS}" },
        "ftp": { "username": "${FTP_USER}", "password": "${FTP_PASS}" },
        "smb": { "username": "${SMB_USER}", "password": "${SMB_PASS}" },
        "sql": { "username": "${SQL_USER}", "password": "${SQL_PASS}" }
    },
    "logging": { "level": "INFO", "file": null }
}
```

> **Security:** Never commit `config.json` or `.env` to Git. They are in `.gitignore`.

### Intelligence Profiles

| Profile | Description | Use Case |
|---------|-------------|----------|
| `Stealth` | Low-footprint, minimal noise | Covert reconnaissance |
| *(Default)* | Standard balancing | General-purpose scanning |
| *(Planned: Aggressive)* | Maximum scan rate | Open test environments |
| *(Planned: RAGE)* | WiFi monitor + active attacks | Oxigotchi-style wardriving |

---

## 📡 Ecosystem Context (2025–2026)

The Pwnagotchi ecosystem has evolved significantly. Here's how Pwonagotchi_own fits:

| Project | Status | Approach | Notes |
|---------|--------|----------|-------|
| **evilsocket/pwnagotchi** | ❌ Archived (v1.5.5) | Python + bettercap | Original, abandoned |
| **jayofelony/pwnagotchi** | ✅ Active (v2.9.5.8) | Python + bettercap | Most active fork, 64-bit only |
| **infinition/Bjorn** | ✅ Active | Python + bettercap | Friendly fork, e-ink focus |
| **CoderFX/oxigotchi** | ✅ Active (v3.0) | **100% Rust + AngryOxide** | Zero crashes, firmware-patched, the gold standard |
| **Ragnt/AngryOxide** | ✅ Active | Rust 802.11 engine | Purpose-built WiFi attack tool, validated captures |
| **Pwonagotchi_own** | 🔥 This repo | **Rust + Python hybrid** | Bridges Bjorn AI with Rust performance |

### What Pwonagotchi_own Learns from the Ecosystem:

1. **Firmware crash prevention** (Oxigotchi): 6-layer self-healing with DWT hardware watchpoints — *planned integration*
2. **AngryOxide integration**: Replace placeholder scanners with real 802.11 attack engine — *planned*
3. **tmpfs capture pipeline**: Protect SD card from write wear — *planned*
4. **Bluetooth offensive capabilities**: BT tethering + attack modes — *future cycle*
5. **Web dashboard**: Remote monitoring — *planned*

---

## 🔧 Development

### Project Structure

```
├── core/                     # Core subsystems
│   ├── hardware/            # GPIO, display, LED, button drivers
│   ├── orchestration/       # Engine orchestrator (module registry)
│   ├── event_bus.py         # Async pub/sub event bus
│   └── networking.py        # nmcli/ip-based network management
├── intelligence/            # AI/agent layer
│   ├── agent.py             # IntelligenceAgent (pulse loop)
│   ├── cycles/              # Cognitive cycles (observe → reflect)
│   ├── memory/              # Persistent state management
│   └── profiles/            # Swappable behavior profiles
├── rust_engine/             # Rust engine (pwon_core)
│   ├── src/
│   │   ├── main.rs          # CLI entrypoint
│   │   ├── lib.rs           # Scanner trait, Target types
│   │   ├── ssh_scanner.rs   # SSH service detection
│   │   ├── ftp_scanner.rs   # FTP service detection
│   │   ├── smb_scanner.rs   # SMB/CIFS service detection
│   │   ├── sql_scanner.rs   # SQL service detection
│   │   └── network_manager.rs # WiFi/Ethernet toggle
│   └── Cargo.toml
├── config.json.example      # Configuration template
├── .env.example             # Environment variable template
├── interface.py             # Root entrypoint
├── quick_setup.sh           # Automated installer
└── requirements.txt         # Python dependencies
```

### Adding a New Scanner (Rust)

1. Create `rust_engine/src/<service>_scanner.rs`
2. Implement the `Scanner` trait from `lib.rs`
3. Expose the module in `lib.rs` and `main.rs`
4. Rebuild: `cd rust_engine && cargo build --release`

### Adding a New Intelligence Cycle (Python)

1. Create `intelligence/cycles/<name>_cycle.py`
2. Extend `BaseIntelligenceCycle`
3. Implement `observe()` and `reflect()`
4. Register in the agent via `agent.add_cycle(new_cycle)`

### Adding a New Profile

1. Create `intelligence/profiles/<name>.py`
2. Extend `BaseProfile`
3. Implement `get_parameters() → dict`
4. Load with `agent.load_profile(YourProfileClass)`

---

## 🛡️ Security Notes

- **Never commit `config.json`** — it contains scanner credentials
- **Use `.env` for secrets** — automatically gitignored
- **The `.gitignore` blocks**: `config.json`, `.env`, `*.key`, `*.pem`, compiled artifacts
- **Hardcoded credentials removed** — Rust scanners now read from config at runtime

---

## 📈 Roadmap

| Priority | Feature | Status | Ecosystem Inspiration |
|----------|---------|--------|----------------------|
| P0 | Real 802.11 WiFi scanning (AngryOxide integration) | Planned | Oxigotchi, AngryOxide |
| P0 | tmpfs capture pipeline (SD card protection) | Planned | Oxigotchi |
| P0 | Self-healing watchdog (6 recovery layers) | Planned | Oxigotchi v3.0 |
| P1 | Web dashboard for remote monitoring | Planned | Stock Pwnagotchi |
| P1 | Aggressive / RAGE intelligence profiles | Planned | Oxigotchi modes |
| P1 | Bluetooth tethering + offensive cycles | Planned | jayofelony bt-tether |
| P2 | Reinforcement learning (A2C) reward system | Planned | Stock Pwnagotchi AI |
| P2 | pwnagotchi Grid upload integration | Planned | jayofelony grid plugin |
| P2 | Hardware clock sync fallback (NTP-less) | Planned | Stock Pwnagotchi docs |

---

## 📚 References & Further Reading

- [Oxigotchi](https://github.com/CoderFX/oxigotchi) — Zero-crash Rust WiFi agent
- [AngryOxide](https://github.com/Ragnt/AngryOxide) — Rust 802.11 attack engine
- [Bjorn](https://github.com/infinition/Bjorn) — Friendly Pwnagotchi fork
- [jayofelony/pwnagotchi](https://github.com/jayofelony/pwnagotchi) — Most active community fork (v2.9.5.8)
- [Raspberry Pi OS Bookworm](https://www.raspberrypi.com/software/) — Supported OS baseline
- [Bettercap](https://www.bettercap.org/) — Network toolkit (future replacement target)
- [Pwnagotchi Docs](https://pwnagotchi.ai/) — Original documentation

---

*Last audited: 2026-01-06 | Checksum: 2026-01-06-Tony-Pwonagotchi_own-v2*