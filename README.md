# Pwonagotchi (Optimized High-Performance Edition)

This is a high-density, asynchronous optimization of the original pwnagotchi project, architected for edge devices like the Raspberry Pi Zero W.

## 🚀 Deployment Instruction

Install your optimized engine on your Raspberry Pi using this automated command:

```bash
curl -sSL https://raw.githubusercontent.com/TchomboW/Pwonagotchi_own/main/setup.sh | bash
```

### 🛠️ Manual Local Setup (For Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TchomboW/Pwonagotchi_own.git ~/pwonagotchi
   cd ~/pwonagotchi
   ```

2. **Build the Rust Core Engine:**
   ```bash
   cd rust_engine
   cargo build --release
   ```

3. **Start the Interface:**
   ```bash
   cd ..
   source venv/bin/activate
   python3 src/interface.py
   ```

## ⚖️ License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for more details.
