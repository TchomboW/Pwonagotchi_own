# ⚔️ Bjorn Reborn: High-Performance Intelligence Agent

Bjorn is an autonomous intelligence engine designed specifically for highly resource-constrained environments, such as the **Raspberry Pi Zero W (Pi OS 64-bit)**. It utilizes a high-performance hybrid architecture combining a **Rust core** for speed and safety with a **Python orchestration layer** for complex logic.

## 🧠 Intelligence Capability: The "Scout-and-Strike" Cycle

Unlike traditional scanners, Bjorn operates on an **Advanced Intelligence Cycle** (Perceive $\rightarrow$ Evaluate $\rightarrow$ Act):

1.  **Perception**: Constant monitoring of network state and hardware presence (e.g., USB-Ethernet dongles).
2.�  **Evaluation**: Analyzes current targets for high-value indicators.
3.   **Tactical Chaining**: If a target is identified, Bjorn automatically generates follow-up sub-tasks (e.g., probing specific service ports) to expand the reconnaissance scope.

## 🛡️ Tactical Profiles

Bjorn can operate under different tactical postures by adjusting its timing and noise signature:

| Profile | Behavior | Use Case |
| :--- | :--- | :--- |
| `stealth` | Long, randomized delays; low-frequency probing | Unobtrusive reconnaissance in high-security environments |
| `standard` | Moderate pacing; standard duty cycle | General intelligence gathering |
| `aggressive` | High-speed, rapid-fire scanning | Rapid/Tactical situational awareness |

## 🛠️ Architecture & Setup

### Core Components
- **Engine (Rust)**: `pwon_core` - Handles high-performance connectivity management and low-level scanner routines.
- **Orchestrator (Python)**: `BjornOrchestrator` - Man-in-the-middle controller managing the intelligence logic, profile switching, and target chaining.

### Hardware Requirements
- **Target**: Raspberry Pi Zero W (or any ARM64 Linux system).
- **OS**: Pi OS 64-bit (optimized for memory/CPU constraints).

### Quick Start (Local Development)
1. **Build the Engine**:
   ```bash
   cd rust_engine
   cargo build
   ```
2. **Run an Intelligence Cycle**:
   ```bash
   python3 src/interface.py --profile stealth
   ```

## 📡 Connectivity Management
Bjorn-reborn is designed for hardware that requires manual interface switching (e.g., USB-Ethernet dongles). The `NetworkManager` module handles:
- **Automatic Interface Detection**: Detects when an `eth0` or `enp...` device is connected.
- **Interface Switching**: Allows the orchestrator to flip between `wlan0` and `eth0` for optimal stability/speed.

---
*Built by TchomboW. Designed for high-integrity autonomous reconnaissance.*
