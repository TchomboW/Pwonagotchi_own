import asyncio
import logging
from typing import List, Any, Dict, Optional
from core.event_bus import EventBus

class IntelligenceAgent:
    """
    Reactive cognitive entity for Pwonagotchi_own. 
    Uses EventBus for decoupled communication and implements safety checks
    for long-running intelligence cycles (Oxigotchi-inspired resilience).
    """

    def __init__(self, name: str, orchestrator: Any, memory_manager: Any, event_bus: EventBus, visual_engine: Optional[Any] = None):
        self.name = name
        self.orchestrator = orchestrator
        self.memory = memory_manager
        self.event_bus = event_bus
        self.visual_engine = visual_engine
        self.logger = logging.getLogger(f"intelligence.{name}")
        self.active_cycles: List[Any] = []
        self.current_profile = None
        self.is_alive = True

        # Register for system-wide events
        self.event_bus.subscribe("system.shutdown", self.on_system_shutdown)

    def add_cycle(self, cycle: Any):
        """Registers a new cognitive process (Intelligence Cycle) into the agent."""
        if self.current_profile:
            cycle.apply_parameters(self.current_profile.get_parameters())
        self.active_cycles.append(cycle)
        self.logger.info(f"Cycle '{cycle.name}' added to agent mapping.")

    def load_profile(self, profile_class: Any):
        """Loads a new intelligence profile and redistributes parameters to all cycles."""
        self.logger.info(f"Loading intelligence profile: {profile_class.__name__}")
        new_profile = profile_class(self.name)
        self.current_profile = new_profile
        params = new_profile.get_parameters()
        for cycle in self.active_cycles:
            cycle.apply_parameters(params)
        self.logger.info(f"Profile '{new_profile.name}' active with params: {params}")

    def start_all(self):
        """Starts all registered intelligence cycles."""
        self.logger.info("Starting all cognitive processes...")
        for cycle in self.active_cycles:
            cycle.start()
        self.logger.info("Intelligence engine is fully awake.")

    async def stop_all(self):
        """Safely shuts down all active cycles and notifies the event bus."""
        self.logger.info("Shutting down intelligence processes...")
        self.is_alive = False
        for cycle in self.active_cycles:
            await cycle.stop()
        await self.event_bus.publish("intelligence.stopped", {"agent": self.name})
        self.logger.info("Intelligence engine is offline.")

    def on_system_shutdown(self, data: Any):
        """EventBus callback to gracefully handle system-wide shutdown signals."""
        self.logger.warning("Received system shutdown signal!")
        self.is_alive = False

    async def pulse(self):
        """The fundamental heartbeat of the agent. 
        Iterates through all active cycles, performing an Observe-Reflect loop.
        Publishes state updates to the EventBus for other modules to consume.
        """
        if not self.is_alive:
            return

        for cycle in self.active_cycles:
            if not cycle.is_running():
                continue
            
            try:
                # Step 1: Observe (Sensor/Environment polling)
                observation = await cycle.observe()
                
                # Step 2: Reflect (Decision-making and reasoning-based state change)
                await cycle.reflect(observation)
            except Exception as e:
                self.logger.error(f"Cycle '{cycle.name}' crashed during pulse: {e}")
                # Self-healing: restart the specific cycle
                await cycle.stop()
                await cycle.start()

        # Step 3: Visual Synchronization
        if self.visual_engine:
            await self.visual_engine.sync_state(self)

        # Notify the system that a pulse has completed
        await self.event_bus.publish("agent.pulse_complete", {"agent": self.name, "cycles_active": len(self.active_cycles)})

    def learn(self, key: str, insight: Dict[str, Any]):
        """The primary mechanism for an agent to internalize new knowledge."""
        self.logger.info(f"Agent is learning: {key}")
        self.memory.save_state(key, insight)

    def recall(self, key: str) -> Dict[str, Any]:
        """Retrieves a previously learned piece of intelligence."""
        data = self.memory.get_state(key)
        self.logger.info(f"Agent recalled intelligence for '{key}'")
        return data

    def execute_action(self, category: str, action: str, **kwargs):
        """The bridge method to translate cognitive decisions into system actions via the orchestrator."""
        self.logger.info(f"Agent translating intelligence decision: [{category}.{action}]")
        return self.orchestrator.dispatch(category, action, **kwargs)
