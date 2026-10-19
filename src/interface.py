import asyncio
import os
import json
import time
import logging

logger = logging.getLogger("pwonagotchi.interface")

class IntelligenceResult:
    """Standardized intelligence observation container."""
    def __init__(self, source_module, target, data, confidence=0.5):
        self.source_module = source_module
        self.target = target
        self.data = data
        self.confidence = confidence

    def to_dict(self):
        return {
            "module": self.source_module,
            "target": self.target,
            "data": self.data,
            "confidence": self.confidence
        }

class PwonagotchiOrchestrator:
    """
    Crash-resilient orchestrator bridging Python intelligence logic with the Rust core engine.
    Implements exponential backoff and subprocess timeouts similar to Oxigotchi/AngryOxide.
    """
    def __init__(self, bin_path: str, history_file: str = "intelligence_accumulated.json"):
        self.bin_path = os.path.abspath(bin_path)
        self.history_file = history_file
        if not os.path.exists(self.bin_path):
            raise FileNotFoundError(f"Rust engine binary not found at {self.bin_path}")
        
        self.active_interface = "unknown"
        self.intelligence_log = []
        self.crash_count = 0
        self.backoff_delay = 5  # Start at 5 seconds
        self.max_backoff = 300  # Cap at 5 minutes (Oxigotchi standard)

    async def _execute(self, args: list, timeout: int = 30) -> tuple[bool, str]:
        """Execute Rust engine with timeout and decode output."""
        cmd = [self.bin_path] + args
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
            out = stdout.decode().strip()
            err = stderr.decode().strip()

            if process.returncode == 0:
                self.crash_count = 0  # Reset backoff on success
                return True, out
            else:
                return False, f"{err} {out}".strip()
        except asyncio.TimeoutError:
            return False, "Engine subprocess timed out"
        except Exception as e:
            return False, f"Subprocess execution error: {e}"

    async def _get_with_retry(self, args: list, timeout: int = 10) -> tuple[bool, str]:
        """Attempt execution with exponential backoff if the engine is unstable."""
        success, output = await self._execute(args, timeout)
        if not success and self.crash_count < 5:
            self.crash_count += 1
            logger.warning(f"engine failed (attempt {self.crash_count}). waiting {self.backoff_delay}s")
            await asyncio.sleep(self.backoff_delay)
            self.backoff_delay = min(self.backoff_delay * 2, self.max_backoff)
            return await self._execute(args, timeout)
        return success, output

    async def get_network_state(self) -> str:
        success, output = await self._get_with_retry(["network", "wifi"])
        self.active_interface = "wlan0" if success else "eth0"
        return self.active_interface

    async def switch_network(self, mode: str) -> bool:
        logger.info(f"Initiating network switch to [{mode}]...")
        success, output = await self._get_with_retry(["network", mode])
        if success:
            self.active_interface = "wlan0" if mode == "wifi" else "eth0"
            logger.info(f"Network transition successful. Current: {self.active_interface}")
            return True
        else:
            logger.error(f"Network transition failed! -> {output}")
            return False

    async def connectivity_heartbeat(self) -> bool:
        if self.active_interface == "unknown":
            return False
        return True

    async def emergency_fallback(self):
        logger.warning("Emergency Protocol Triggered! Reverting to Safety Loopback (WiFi)...")
        await self.switch_network("wifi")

    async def perform_scan(self, module: str, target: str) -> dict:
        logger.info(f"Scanning {module} on {target}...")
        success, output = await self._get_with_retry([module, target])
        if not success:
            return {"status": "error", "message": output}

        try:
            parts = output.split("|")
            data_payload = {
                "latency_ms": int(parts[1].split(":")[1]), 
                "scanned": parts[2].split(":")[1].lower() == "true"
            }
            intel = IntelligenceResult(module, target, data_payload)
            self.intelligence_log.append(intel.to_dict())
            return {"status": "success", **intel.to_dict()}
        except (IndexError, ValueError):
            return {"status": "error", "message": f"Parse error: {output}"}

    async def load_intelligence_history(self):
        logger.info("Loading historical intelligence data...")
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.intelligence_log = json.load(f)
                logger.info(f"Loaded {len(self.intelligence_log)} historical records.")
            except Exception as e:
                logger.error(f"Failed to load history: {e}")
        else:
            logger.info("No history file found. Starting fresh intelligence state.")

    async def save_intelligence_history(self):
        logger.info(f"Persisting {len(self.intelligence_log)} intelligence records to disk...")
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.intelligence_log, f, indent=4)
            logger.info("History persistence complete.")
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    async def run_intelligence_cycle(self, seed_targets: list[str], iterations: int = 3):
        logger.info("STARTING ADVANCED INTELLIGENCE CYCLE")
        await self.get_network_state()

        for i in range(iterations):
            logger.info(f"Cycle {i+1}/{iterations}: Assessing environment...")
            if not await self.connectivity_heartbeat():
                await self.emergency_fallback()

            target = seed_targets[i % len(seed_targets)]
            result = await self.perform_scan("ssh", target)
            if result["status"] == "success":
                logger.info(f"High-Value Target Detected on {target}")
                if "127.0.0" in target:
                    new_chain = [f"{target}:80", f"{target}:443"]
                    logger.info(f"Chaining new assets: {new_chain}")
                    seed_targets.extend(new_chain)
                await asyncio.sleep(0.5)
            else:
                logger.info("No actionable intelligence found.")

        logger.info("INTELLIGENCE CYCLE COMPLETE")

if __name__ == "__main__":
    import sys

    async def main_test():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Point to release binary as per standard Oxigotchi production builds
        engine_path = os.path.join(current_dir, "..", "rust_engine", "target", "release", "pwon_core")
        engine_path = os.path.abspath(engine_path)

        orchestrator = PwonagotchiOrchestrator(engine_path)
        await orchestrator.load_intelligence_history()
        await orchestrator.run_intelligence_cycle(["127.0.0.1"])
        await orchestrator.save_intelligence_history()

    asyncio.run(main_test())
