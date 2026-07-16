import logging
import subprocess
from typing import Dict, Any

class HardwareController:
    """
    High-performance hardware interaction layer optimized for Pi Zero W.
    Manages GPIO-based peripherals including Status LEDs and Input Buttons.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._is_initialized = False
        # Internal registry of current hardware states
        self._led_states: Dict[str, str] = {} 
        self._button_states: Dict[int, bool] = {}

    def initialize(self):
        """Prepares the GPIO pins and low-level drivers."""
        self.logger.info("Initializing hardware peripherals (GPIO/LED/Buttons)...")
        # In a real Pi-environment, we would do: import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM)
        self._is_initialized = True
        self.logger.info("Hardware layer ready for operational commands.")

    def set_led(self, name: str, state: bool, pattern: str = "solid"):
        """
        Controls a status LED.
        Args:
            name: The identifier of the LED (e.g., 'status', 'activity').
            state: True for ON, False for OFF.
            pattern: Optional visual pattern (e.g., 'blink', 'pulse').
        """
        if not self._is_initialized:
            self.logger.error("Cannot set LED: Hardware not initialized.")
            return

        self._led_states[name] = "on" if state else "off"
        self.logger.info(f"[LED] {name} is now {'ON' if state else 'OFF'} (Pattern: {pattern})")
        # FUTURE: Implement actual GPIO write calls here.

    def read_button(self, pin: int) -> bool:
        """Reads the current logical state of a physical button."""
        if not self._is_initialized:
            self.logger.error("Cannot read button: Hardware not initialized.")
            return False
        
        # For simulation/testing on MacOS, we return a dummy status
        # In production, this would be: return GPIO.input(pin) == GPIO.HIGH
        status = True # Mocked high-signal input
        self._button_states[pin] = status
        return status

    def get_hardware_status(self) -> Dict[str, Any]:
        """Returns a snapshot of all current hardware states."""
        return {
            "leds": self._led_states,
            "buttons": self._button_states,
            "initialized": self._is_initialized
        }

    def shutdown(self):
        """Cleans up GPIO pins and turns off all outputs."""
        self.logger.info("Shutting down hardware layer...")
        for led in self._led_states:
            self.logger.info(f"Turning off LED: {led}")
        self._led_states.clear()
        self._is_initialized = False
