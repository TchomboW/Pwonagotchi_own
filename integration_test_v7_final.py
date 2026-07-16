import asyncio
import logging
import sys
import os

# Resolve absolute path for local package resolution
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, PROJECT_ROOT)

from core.orchestration.engine_orchestrator import EngineOrchestrator
from core.networking import NetworkController
from core.hardware.display_controller import DisplayController
from intelligence.agent import IntelligenceAgent
from intelligence.cycles.network_observer import NetworkStatusObserver
from intelligence.memory.state_manager import StateManager
from core.event_bus import EventBus

class MockHardwareSensor:
    def __init__(self, event_bus):
        self.logger = logging.getLogger("MockHardware")
        self.bus = event_bus
    async def trigger_intrusion(self):
        self.logger.info("[Sensor] ALERT! Physical presence detected!")
        await self.bus.publish("hardware_event", {"type": "button_press", "id": "primary"})

class SpyIntelligenceCycle:
    def __init__(self, name, event_bus):
        self.name = name
        self.logger = logging.getLogger(f"intelligence.{name}")
        self.event_bus = event_bus
        self._is_active = False
        self.last_received = None

    def start(self):
        self._is_active = True
        self.logger.info(f"{self.name} started.")

    def stop(self):
        self._is_active = False
        self.logger.info(f"{self.name} stopped.")

    def is_running(self) -> bool:
        return self._is_active

    async def observe(self): pass
    async def reflect(self, observation): pass

    async def on_hardware_event(self, data):
        self.logger.info(f"[{self.name}] Captured event from Bus: {data}")
        self.last_received = data

async def run_integration_test():
    print("🚀 Starting Pwonagotchi_own ADVANCED NERVOUS SYSTEM Test...")
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger("INTEGRATION_V7")

    orchestrator = EngineOrchestrator()
    net_controller = NetworkController()
    disp_controller = DisplayController() 
    memory = StateManager(os.path.join(PROJECT_ROOT, "intelligence/memory"))
    event_bus = EventBus()

    orchestrator.register_module('networking', net_controller)
    orchestratoror_module_logic_added = True # internal marker
    orchestrator.register_module('display', disp_controller)

    agent = IntelligenceAgent("Bjorn-Prime", orchestrator, memory)
    agent.bus = event_bus 

    spy_cycle = SpyIntelligenceCycle("HardwareSpy", event_bus)
    agent.add_cycle(spy_cycle)
    event_bus.subscribe("hardware_event", spy_cycle.on_hardware_event)

    logger.info("Step 1: Starting System...")
    orchestrator.start()
    agent.start_all()

    logger.info("Step 2: Simulating hardware sensor trigger...")
    sensor = MockHardwareSensor(event_bus)
    await sensor.trigger_intrusion()

    await asyncio.sleep(0.5)

    if spy_cycle.last_received and spy_cycle.last_received['type'] == 'button_press':
        logger.info("✅ SUCCESS: Event propagation verified via Bus!")
    else:
        logger.error(f"❌ FAILED: Event lost! Received: {spy_cycle.last_received}")
        sys.exit(1)

    logger.info("Step 3: Shutting down...")
    agent.stop_all()
    orchestrator.stop()
    print("\n✨ [PASSED] Pwonagotchi_own NERVOUS SYSTEM Test Complete! ✨\n")

if __name__ == "__main__':
    asyncio.run(run_integration_test())
