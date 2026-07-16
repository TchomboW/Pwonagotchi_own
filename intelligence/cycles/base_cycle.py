import logging
from abc import ABC, abstractmethod

class BaseIntelligenceCycle(ABC):
    """
    The base interface for all intelligence-driven processes in Pwonagotchi_own.
    A cycle is responsible for observing the environment and performing reasoning 
    to trigger actions via an orchestrator.
    """

    def __init__(self, name: str, orchestrator: any):
        self.name = name
        self.orchestrator = orchestrator
        self.logger = logging.getLogger(f"intelligence.{name}")
        self._is_active = False
        self.parameters = {}

    @abstractmethod
    async def observe(self):
        """The primary method called to monitor the environment/state."""
        pass

    @abstractmethod
    async def reflect(self, observation: any):
        """Perform reasoning on the latest observation and decide on actions."""
        pass

    def apply_parameters(self, params: dict):
        """Injects profile-specific parameters into this cycle."""
        self.parameters.update(params)
        self.logger.info(f"Parameters updated for {self.name}: {params}")

    def start(self):
        self._is_active = True
        self.logger.info(f"Cycle '{self.name}' started.")

    def stop(self):
        self._is_active = False
        self.logger.info(f"Cycle '{self.name}' stopped.")

    @property
    def is_running(self) -> bool:
        return self._is_active
