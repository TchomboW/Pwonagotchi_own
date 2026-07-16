import logging
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont

class DisplayController:
    """
    High-precision controller for e-paper displays (e.g., Waveshare 3-inch).
    Provides an off-screen canvas abstraction to minimize physical refresh cycles.
    """

    def __init__(self, width: int = 400, height: int = 300):
        self.logger = logging.getLogger(__name__)
        self.width = width
        self.height = height
        # Create the off-screen buffer (canvas) using PIL
        self._buffer = Image.new("1", (self.width, self.height), color=1) # '1' for 1-bit pixels, black/white
        self._draw = ImageDraw.Draw(self._buffer)
        self._dirty = False # Flag to track if the buffer has changed since last flush

    def clear(self):
        """Clears the off-screen canvas."""
        self._draw.rectangle([0, 0, self.width, self.height], fill=1)
        self._dirty = True
        self.logger.debug("Display buffer cleared.")

    def draw_text(self, position: Tuple[int, int], text: str, font_size: int = 20, color: int = 0):
        """Draws text onto the off-screen canvas."""
        try:
            # Note: In a real deployment, fonts would be pre-loaded from a directory.
            # For now, we fallback to default if specific font loading isn't available.
            font = ImageFont.load_default() # Default PIL font
            # In production, I'd use: font = ImageFont.truetype(f"fonts/size_{font_size}.ttf", font_size)
            
            self._draw.text(position, text, fill=color, font=font)
            self._dirty = True
        except Exception as e:
            self.logger.error(f"Error drawing text: {e}")

    def draw_rect(self, coords: Tuple[int, int, int, int], outline: int = 0, fill: Optional[int] = None):
        """Draws a rectangle onto the buffer."""
        self._draw.rectangle(coords, outline=outline, fill=fill)
        self._dirty = True

    def is_dirty(self) -> bool:
        return self._dirty

    def flush(self):
        """
        Performs the heavy-duty hardware sync. 
        On an e-paper display, this is where the expensive refresh happens.
        """
        if not self._dirty:
            self.logger.debug("Buffer not dirty; skipping physical flush.")
            return

        self.logger.info("Executing heavy E-Paper hardware sync (physical refresh)...")
        # ---------------------------------------------------------
        # RE-IMPLEMENTATION PLACEHOLDER
        # In the actual deployment, this method would call the specific 
        # hardware driver (e.g., Waveshare_driver.display(self._buffer))
        # ---------------------------------------------------------
        
        # For now, we simulate the time-consuming refresh loop.
        import time
        time.sleep(0.5) # Simulate e-paper latency

        self._dirty = False
        self.logger.info("Hardware sync complete.")

    def get_buffer(self) -> Image.Image:
        return self._buffer
