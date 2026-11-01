# 🐉 Pwonagotchi_own (Pi Zero W Optimized Edition)

## ⚖️ License & Attribution

This project is a high-performance, optimized evolution of the **Bjorn** ecosystem.
All original credit for the foundational code, core-logic, and concept goes to the **infinition/Bjorn** project.
The original Bjorn license is included in the `LICENSE` file.

---

## 🔭 Project Overview

`Pwonagotchi_own` is a high-performance evolution of the original Pwnagotchi ecosystem. This version is precision-tuned to extract maximum capability from the **Raspberry Pi Zero W** running a modern **64-bit OS**. It focuses on intelligent reconnaissance, automated signal intelligence, and extreme resource efficiency.

### 🌟 Key Technical Upgrades:
- **Optimized Rust Core**: A high-speed `rust_engine` with trimmed `tokio` features (`rt-multi-thread`, `macros`, `net`, `time`) to reduce binary size and memory footprint.
- **Unified Async Architecture**: Fully resolved async/sync mismatches across the Python orchestrator and Rust subprocess runtime.
- **Survival Protocols**: Built-in "Circuit Breaker" logic to prevent system crashes during resource spikes on the single-core CPU.
- **Externalized Configuration**: Credentials and engine parameters are managed via `config.json`, ensuring no secrets are committed to source control.
- **Memory-Efficient Data**: Lightweight Python orchestration using standard library tools where possible.

---

## 🏗️ Core Architecture

The intelligence is organized into a high-integrity dual-layer structure:

1.  **High-Speed Engine (`rust_engine/`)**: A memory-safe Rust crate handling heavy-duty scanning and low-level connectivity. Built with `release` optimization for the Pi Zero W.
2.  **Intelligence Orchestrator (`core/` & `intelligence/`)**: An asynchronous Python framework that manages the cognitive cycles and sensory feedback loops using non-blocking subprocess calls.

---

## 🚀 Installation & Deployment Guide (Raspberry Pi OS)

This guide assumes a fresh installation of **Raspberry Pi OS (Bookworm) 64-bit** on your Raspberry Pi Zero W.

### Option A: One-Command Automatic Install
Run this single command on your Pi. It will automatically install dependencies, clone the code, and build the engine:
```bash
curl https://raw.githubusercontent.com/TchomboW/Pwonagotchi_own/main/quick_setup.sh | bash
```

### Option B: Manual Step-by-Step Setup


Before cloning, ensure your system is updated:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git build-essential pkg-config libssl-dev
```

### 2. Install Rust (Rustup)

We use `rustup` to manage the Rust toolchain. This is required to build the optimized core.
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
# Follow the prompts, then:
source ~/.cargo/env 
```

### 3. Install Python Dependencies

Pwonagotchi uses an external display interface and standard networking tools. 
```bash
# Install required Python libraries from the requirements file
pip3 install -r requirements.txt
```

### 4. Clone & Configure

```bash
git clone https://github.com/TchomboW/Pwonagotchi_own.git ~/Pwonagotchi_own
cd ~/Pwonagotchi_own

# Configure the engine (edit config.json to set your specific targets/credentials)
# The file contains [REDACTED] placeholders for security.
nano config.json 
```

### 5. Build the Rust Core

Building on the Pi Zero W takes a few minutes due to the limited CPU, but the optimized `Cargo.toml` skips heavy features to speed this up.
```bash
cd rust_engine
cargo build --release
cd ..
```

### 6. Run the Engine

```bash
python3 interface.py
```

---

## 🛠️ Hardware Requirements

- **Target**: Raspberry Pi Zero W (Optimized for ARM64/64-bit architecture).
- **OS**: Raspberry Pi OS 64-bit (Bookworm/Bullseye).
- **Interface**: SPI protocol supported for high-precision hardware interaction (if using an attached e-ink display via Pillow).
- **Storage**: Minimum 8GB SD Card recommended.

---

## 📄 License
This project is licensed under the MIT License.
