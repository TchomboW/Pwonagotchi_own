# 🐉 Pwonagotchi (Optimized)

**CRITICAL ATTRIBUTION:** This project is a modified and enhanced version of **[Pwnagotchi by jayofelony](https://github.com/jayofelony/pwnagotchi)**. All original credit for the foundational code, core logic, and concept goes to them. 

My contributions (Pwonagotchi) include:
- 🚀 **Architecture Optimization**: Refactoring for Raspberry Pi Zero W efficiency in a modern 64-bit environment.
- 🛠️ **Intelligence Enhancement**: Implementing advanced trend-analysis and resource-guarding protocols.
- ✨ **Themed Interface**: Tailoring the ecosystem into the "Pwonagotchi" identity.

---

## 🔭 Project Overview

`Pwonagotci_own` is a high-performance evolution of the original Pwnagotchi ecosystem. This version is precision-tuned to extract maximum capability from the **Raspberry Pi Zero W** running a modern **64-bit OS**. It focuses on intelligent reconnaissance and automated signal intelligence.

### 🌟 Key Technical Upgrades:
- **Optimized Engine**: A high-speed Rust core (`rust_engine`) for intensive network tasks.
- **Cognitive Intelligence**: An asynchronous Python layer capable of pattern recognition (detecting trends in memory/CPU usage).
- **Survival Protocols**: Built-in "Circuit Breaker" logic to prevent system crashes during resource spikes.

## 🏗️ Core Architecture

The intelligence is organized into a high-integrity dual-layer structure:

1.  **High-Speed Engine (`rust_engine/`)**: A memory-safe Rust crate handling heavy-duty scanning and low-level connectivity.
2.  **Intelligence Orchestrator (`core/` & `intelligence/`)**: An asynchronous Python framework that manages the cognitive cycles and sensory feedback loops.

## 🚀 Installation & Deployment

### 1. Prerequisites
- A fresh installation of **Raspberry Pi OS (64-bit)** on your Raspberry Pi Zero W.

### 2. Quick Start (Local Development)

```bash
# Clone the repository
git clone https://github.com/TchomboW/Pwonagotci_own.git ~/Pwonagotci_own
cd ~/Pwonagotci_own

# Build the Rust core
cd rust_engine
cargo build --release
cd ..

# Run the main engine
python3 interface.py
```

## 🛠️ Hardware Requirements
- **Target**: Raspberry Pi Zero W (Optimized for ARM64/64-bit architecture).
- **Interface**: SPI protocol for high-precision hardware interaction.

---
*Built by TchomboW. Based on the amazing work of jayofelony.*
