import logging
from abc import ABC, abstractmethod

class BaseProfile(ABC):
    """
    The base interface for an intelligence profile.
    A profile defines unique operational parameters (intervals, intensity, etc.) 
    that dictate how the IntelligenceAgent behaves.
    """

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"intelligence.profile.{name}")

    @abstractmethod
    def get_parameters(self) -> dict:
        """Returns a dictionary of operational parameters specific to this profile."""
        pass

    def on_activate(self):
        """Hook called when the profile becomes active."""
        self.logger.info(f"Profile '{self.name}' is now active.")

    def on_deactivate(self):
        """Hook called when the profile is swapped out."""
        self.logger.info(f"Profile '{self.name}' has been deactivated.")
