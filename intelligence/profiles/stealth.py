from .base_profile import BaseProfile

class StealthProfile(BaseProfile):
    """
    A high-privacy, low-footprint profile.
    Emphasizes minimizing network noise and avoiding detection.
    """

    def get_parameters(self) -> dict:
        return {
            "scan_interval": 60,       # Longer wait times between actions
            "noise_threshold": 0.1,    # Minimize radio/system activity
            "recon_depth": "light",     # Shallow scanning
            "stealth_mode": True
        }
