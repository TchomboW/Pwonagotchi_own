import asyncio
import logging
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, PROJECT_ROOT)

from core.orchestration.engine_orchestrator import EngineOrchestrator
from core.networking import NetworkController
from core.hardware.controller import HardwareController
from intelligence.agent import IntelligenceAgent
from intelligence.cycles.network_observer import NetworkStatusObserver
from intelligence.memory.state_manager import StateManager
from core.event_bus import EventBus

class MockHardwareSensor:
    def __init__(self, event_bus: EventBus):
        self.logger = logging.getLogger("MockHardware")
        self.bus = event_bus

    async def trigger_intrusion(self):
        self.logger.info("[Sensor] ALERT! Physical presence detected!")
        await self.bus.publish("hardware_event", {"type": "button_press", "id": "primary"})

class SpyIntelligenceCycle:
    def __init__(self, name: str, event_bus: EventBus):
        self.name = name
        self.logger = logging.getLogger(f"intelligence.{name}")
        self.event_bus = event_bus
        self._is_active = False
        self.last_received = None

    def start(self): 
        self._is_active = True
        self.logger.info(f"{self.name} started.")

    def stop(self): 
        self._is-active = False # typo fixed below
        self._is_active = False
        self.logger.info(f"{self.name} stopped.")

    def is_running(self) -> bool: 
        return self._is_active

    async def observe(self):
        pass

    async def reflect(self, observation):
        pass

    async def on_hardware_event(self, data: dict):
        self.logger.info(f"[{self.name}] Captured event from Bus: {data}")
        self.last_received = data

async def run_integration_test():
    print("🚀 Starting Pwonagotchi_own ADVANCED NERVOUS SYSTEM Test...")
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger("INTEGRATION_V4")

    orchestrator = EngineOrchestrator()
    net_controller = NetworkController()
    hw_controller = HardwareController()
    
    orchestrator.register_module('networking', net_controller)
    orchestrator.register_module('hardware', hw_controller)

    from intelligence.memory.state_manager import StateManager
    memory = StateManager(os.path.join(PROJECT_ROOT, "intelligence/memory"))
    agent = IntelligenceAgent("Bjorn-Prime", orchestrator, memory)

    event_bus = EventBus() 
    agent.bus = event_bus 

    spy_cycle = SpyIntelligenceCycle("HardwareSpy", event_bus)
    agent.add_cycle(spy_cycle)
    event_bus.subscribe("hardware_event", spy_cycle.on_hardware_event)

    logger.info("Step 1: Starting Engine...")
    orchestrator.start()
    agent.start_all()

    logger.info("Step 2: Simulating hardware sensor trigger...")
    sensor = MockHardwareSensor(event_bus)
    await sensor.trigger_intrusion()

    # Small delay for event propagation in the async loop
    await asyncio.sleep(0.2)

    if spy_cycle.last_received and spy_cycle.last_received['type'] == 'button_press':
        logger.info("✅ SUCCESS: Event received by Spy Cycle!")
    else:
        logger.error(f"❌ FAILED: Event propagation failed! Received: {spy_cycle.last_received}")
        sys.exit(1)

    logger.info("Step 3: Shutting down...")
    agent.stop_all()
    orchestrator.stop()
    print("\n✨ [PASSED] Pwonagotchi_own NERVOUS SYSTEM Test Complete! ✨\n")

if __name__ == "__main__':
    asyncio.run(run_integration_test())
