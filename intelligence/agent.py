import logging
from typing import List, Any, Dict, Optional

class IntelligenceAgent:
    """
    The high-level cognitive entity of Pwonagotchi_own.
    Acts as a supervisor for intelligence cycles and manages the 
    intersection of reasoning, memory, and environmental interaction.
    """

    def __init__(self, name: str, orchestrator: Any, memory_manager: Any, visual_engine: Optional[Any] = None):
        self.name = name
        self.orchestrator = orchestrator
        self.memory = memory_manager
        self.visual_engine = visual_engine  # The new 'Face' of the agent
        self.logger = logging.getLogger(f"intelligence.{name}")
        self.active_cycles: List[Any] = []
        self.current_profile = None

    def add_cycle(self, cycle: Any):
        """Registers a new cognitive process (Intelligence Cycle) into the agent."""
        if self.current_profile:
            # Pass and synchronize profile parameters to the new cycle immediately
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

    def stop_all(self):
        """Safely shuts down all active cycles."""
        self.logger.info("Shutting down intelligence processes...")
        for cycle in self.active_cycles:
            cycle.stop()
        self.logger.info("Intelligence engine is offline.")

    async def pulse(self):
        """The fundamental heartbeat of the agent. 
        Iterates through all active cycles, performing an Observe-Reflect loop.
        """
        for cycle in self.active_cycles:
            # Check if cycle is running (using boolean check as per updated property logic)
            if not cycle.is_running():
                continue
            
            # Step 1: Observe (Sensor/Environment polling)
            observation = await cycle.observe()
            
            # Step 2: Reflect (Decision-making and reasoning-based state change)
            await cycle.reflect(observation)

        # Step 3: Visual Synchronization
        # After the thought process completes, update the physical 'face' of the agent
        if self.visual_engine:
            await self.visual_engine.sync_state(self)

    def learn(self, key: str, insight: Dict[str, Any]):
        """The primary mechanism for an agent to internalize new knowledge."""
        self.logger.info(f"Agent is learning: {key}")
        self.memory.save_state(key, insight)

    def recall(self, key: str) -> Dict[str, Any]:
        """Retrieves a previously learned piece of intelligence."""
        data = self.memory.get_state(key)
        self.logger.info(f"Agent recalled intelligence for '{key}': {data}")
        return data

    def execute_action(self, category: str, action: str, **kwargs):
        """The bridge method to translate cognitive decisions into system actions via the orchestrator."""
        self.logger.info(f"Agent translating intelligence decision: [{category}.{action}]")
        return self.orchestrator.dispatch(category, action, **kwargs)
