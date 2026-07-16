import asyncio
import logging
from typing import Any

class VisualizerCycle:
    """
    A specialized intelligence cycle dedicated to rendering the 
    agent's current state onto the high-precision display controller.
    """

    def __init__(self, name: str, event_bus: Any, visual_engine: Any):
        self.name = name
        self.logger = logging.getLogger(f"intelligence.{name}")
        self.event_bus = event_bus
        self.visual_engine = visual_engine
        self._is_active = False

    def start(self):
        self._is_active = True
        self.logger.info(f"{self.name} started.")

    def stop(self):
        self._is_active = False
        self.logger.info(f"{self.name} stopped.")

    def is_running(self) -> bool:
        return self._is_active

    async def observe(self):
        # This cycle doesn't 'observe' the environment, it observes the agent's state via pulses
        pass

    async def reflect(self, agent_state: Any):
        """
        Translates internal agent metadata into visual primitives and flushes them to hardware.
        """
        if not self.visual_engine:
            return

        # 1. Clear the canvas
        self.visual_engine.clear() # Assuming clear is implemented in DisplayController

        # 2. Draw Header (Identity)
        self.visual_engine.draw_text((10, 20), f"AGENT: {agent_state.name}", font_size=24)
        self.visual_engine.draw_line(0, 40, 400, 40) # Separator

        # 3. Draw Current Profile
        profile_name = agent_state.current_profile.name if agent_state.current_profile else "NONE"
        self.visual_engine.draw_text((10, 60), f"PROFILE: {profile_name}", font_size=20)

        # 4. Draw Active Cycles count
        self.visual_engine.draw_text((10, 90), f"CYCLES: {len(agent_state.active_cycles)}", font_size=18)

        # 5. Commit the drawing to hardware (The expensive part)
        await self.visual_engine.flush()
        self.logger.info(f"[{self.name}] Visual update completed.")

    async def update_ui(self, agent: Any):
        """Convenience method called during the agent's pulse to redraw everything."""
        await self.reflect(agent)
