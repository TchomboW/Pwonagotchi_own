import logging
from .base_cycle import BaseIntelligenceCycle

class NetworkStatusObserver(BaseIntelligenceCycle):
    """
    Observes the current state of the network through the orchestrator 
    and reacts when a threshold or state change is detected.
    """

    async def observe(self):
        # Fetch the current interface from the networking module via the orchestrator
        net = self.orchestrator.get_module('networking')
        if net:
            return net.get_active_interface()
        return "unknown"

    async def reflect(self, observation: str):
        self.logger.info(f"Observing network state: {observation}")
        # Logic: If we are in 'wifi' mode, maybe we want to log it or trigger a hardware action
        if observation == "wifi":
            self.logger.info("System is currently on WiFi. Maintaining persistence...")
        elif observation == "ethernet":
            self.logger.info("System has transitioned to high-speed Ethernet.")
