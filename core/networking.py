import asyncio
import subprocess
import logging
from typing import Optional

logger = logging.getLogger("pwonagotchi.networking")

class NetworkingManager:
    """
    Manages network state using modern Linux tooling (nmcli / ip).
    Designed to avoid the BCM43430/43436 firmware panics common in older
    pwnagotchi implementations by using safe, state-verified transitions.
    """

    def __init__(self, primary_iface: str = "wlan0"):
        self.primary_iface = primary_iface
        self.current_mode = "managed"

    async def _run_cmd(self, cmd: list[str], timeout: int = 10) -> tuple[bool, str]:
        """Wrapper for running system commands safely."""
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=timeout
            )
            return proc.returncode == 0, stdout.decode().strip()
        except asyncio.TimeoutError:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)

    async def get_active_ssids(self) -> list[str]:
        """Retrieve currently known/connected SSIDs via nmcli."""
        success, output = await self._run_cmd(["nmcli", "-t", "-f", "active,ssid", "device", "wifi", "list"])
        if success:
            return [line.split(":")[1] for line in output.split("\n") if line.startswith("yes:")]
        return []

    async def get_signal_strength(self) -> int:
        """Get raw signal strength percentage via nmcli."""
        success, output = await self._run_cmd(["nmcli", "-t", "-f", "strength", "device", "wifi"])
        if success and output:
            try:
                return int(output.split(":")[1])
            except (ValueError, IndexError):
                pass
        return 0

    async def is_connected(self) -> bool:
        """Verify actual internet connectivity (ping 8.8.8.8)."""
        success, _ = await self._run_cmd(["ping", "-c", "1", "-W", "2", "8.8.8.8"])
        return success

    async def toggle_interface(self, state: str) -> bool:
        """Toggle network interface up or down safely via 'ip' command."""
        success, output = await self._run_cmd(["ip", "link", state, self.primary_iface])
        if success:
            logger.info(f"Interface {self.primary_iface} set to {state}")
            return True
        else:
            logger.error(f"Failed to set {self.primary_iface} to {state}: {output}")
            return False

    async def get_mac_address(self) -> Optional[str]:
        """Retrieve the MAC address of the primary interface."""
        success, output = await self._run_cmd(["ip", "link", "show", self.primary_iface])
        if success:
            for line in output.split("\n"):
                if "link/ether" in line:
                    return line.split("link/ether")[1].strip().split()[0]
        return None

    async def reset_wifi_driver(self) -> bool:
        """
        Emergency reset: Toggle the interface down and back up to recover
        from SDIO bus errors or firmware hangs.
        """
        logger.warning("Executing emergency WiFi driver reset...")
        await self.toggle_interface("down")
        await asyncio.sleep(1)
        return await self.toggle_interface("up")

