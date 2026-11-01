#!/bin/bash

# 🐉 Pwonagotchi_own Pi Zero W Automatic Installer
# This script automates cloning and setting up Pwonagotchi_own on Raspberry Pi OS (64-bit)
set -e # Exit immediately if a command exits with a non-zero status

echo "🔧 Starting Pwonagotchi Own Automated Setup..."

# 1. Update System Dependencies
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git build-essential pkg-config libssl-dev python3-venv

# 2. Install Rust Toolchain (if not present)
if ! command -v rustc &> /dev/null; then
    echo "🦀 Installing Rust toolchain..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source ~/.cargo/env
else
    echo "Rust is already installed."
    source ~/.cargo/env
fi

# 3. Clone Repository (if not present)
TARGET_DIR="$HOME/Pwonagotchi_own"
if [ ! -d "$TARGET_DIR/.git" ]; then
    echo "📂 Cloning repository..."
    git clone https://github.com/TchomboW/Pwonagotchi_own.git $TARGET_DIR
else
    echo "Repository already exists at $TARGET_DIR. Pulling latest changes..."
    cd $TARGET_DIR
    git pull origin main
fi

# 4. Set up Python Environment & Install Dependencies
cd $TARGET_DIR
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 5. Build Rust Engine
echo "🛠️ Compiling optimized Rust engine..."
cd rust_engine
cargo build --release
cd ..

# 6. Finalize Setup
echo "✅ Setup Complete!"
echo "To run Pwonagotchi Own manually:"
echo "  cd ~/Pwonagotchi_own"
echo "  source venv/bin/activate"
echo "  python3 interface.py"
