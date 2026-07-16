import asyncio
import logging
import sys
import os

# Absolute path injection
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from core.orchestration.engine_orchestrator import EngineOrchestrator
from core.networking import NetworkController
from core.hardware.controller import HardwareController
from intelligence.agent import IntelligenceAgent
from intelligence.cycles.network_observer import NetworkStatusObserver
from intelligence.memory.state_manager import StateManager

async def run_integration_test():
    print("🚀 Starting Pwonagotchi_own ADVANCED Agentic Integration Test...")
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger("INTEGRATION_V2")

    # 1. Setup Orchestrator and Modules
    orchestrator = EngineOrchestrator()
    net_controller = NetworkController()
    hw_controller = HardwareController()
    
    orchestrator.register_module('networking', net_controller)
    orchestrator.register_module('hardware', hw_controller)

    # 2. Setup Intelligence Agent and Memory
    memory = StateManager(os.path.join(PROJECT_ROOT, "intelligence/memory"))
    agent = IntelligenceAgent("Bjorn-Prime", orchestrator, memory)

    # 3. Add a Cycle (The Observer)
    observer = NetworkStatusObserver("NetworkWatcher", orchestrator)
    agent.add_cycle(observer)

    # 4. Start everything
    logger.info("Starting full system stack...")
    orchestrator.start()
    agent.start_all()

    # 5. Action: Simulate a Network Change (The Trigger)
    logger.info("Simulating event: Switching to WiFi...")
    net_result = orchestrator.dispatch('networking', 'switch_to_wifi')
    if not net_result:
        logger.error("❌ FAILED: Networking dispatch failed!")
        sys.exit(1)

    # 6. Intelligence Loop: Observe -> Learn -> Recall
    logger.info("Running Cognitive Cycle (Observe -> Learn -> Recall)...")
    
    # Observation phase
    current_state = await observer.observe()
    logger.info(f"Brain observed current state: {current_state}")

    # Learning phase: Intelligence agent internalizes the state into memory
    agent.learn("env_check", {"mode": current_state, "confidence": 0.95})
    
    # Recall phase: Verify we can pull it back from the persistent storage
    recalled_data = agent.recall("env_check")
    if recalled_data.get("mode") == "wifi":
        logger.info("✅ SUCCESS: Intelligence Cycle (Observe $\rightarrow$ Learn $\rightarrow$ Recall) verified!")
    else:
        logger.error(f"❌ FAILED: Memory retrieval error! Expected 'wifi', got '{recalled_data.get('mode')}'")
        sys.exit(1)

    # 7. Shutdown
    logger.info("Shutting down system stack...")
    agent.stop_all()
    orchestrator.stop()
    print("\n✨ [PASSED] Pwonagotchi_own ADVANCED Integration Test Complete! ✨\n")

if __name__ == "__main__":
    asyncio.run(run_integration_test())
