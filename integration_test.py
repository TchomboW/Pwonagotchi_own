import asyncio
import logging
import sys
import os

# Absolute path logic
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)

from core.orchestration.engine_orchestrator import EngineOrchestrator
from core.networking import NetworkController
from core.hardware.controller import HardwareController
from intelligence.cycles.network_observer import NetworkStatusObserver

async def run_integration_test():
    print("🚀 Starting Pwonagotchi_own Intelligence Integration Test...")
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger("INTEGRATION_TEST")

    # 1. Initialize Orchestrator
    orchestrator = EngineOrchestrator()
    logger.info("Step 1: Initializing Orchestrator...")

    # 2. Register Modules
    logger.info("Step 2: Registering Core Modules (Networking & Hardware)...")
    net_controller = NetworkController()
    hw_controller = HardwareController()
    
    orchestrator.register_module('networking', net_controller)
    orchestrator.register_module('hardware', hw_controller)

    # 3. Start Engine (Lifecycle check)
    logger.info("Step 3: Starting the Engine...")
    orchestrator.start()
    
    if not orchestrator._is_running:
        logger.error("❌ FAILED: Engine failed to start.")
        sys.exit(1)

    # 4. Register & Start Intelligence Cycle
    logger.info("Step 4: Deploying Intelligence (NetworkStatusObserver)...")
    network_brain = NetworkStatusObserver("NetworkWatcher", orchestrator)
    network_brain.start() # This is the sync startup method we defined in base_cycle

    # 5. Test Dispatch: Networking State Change via Orchestrator
    logger.info("Step 5: Simulating-Network Transition (Switching to WiFi)...")
    net_result = orchestrator.dispatch('networking', 'switch_to_wifi')
    if not net_result:
        logger.error("❌ FAILED: Networking dispatch failed!")
        sys.exit(1)

    # 6. Test Cycle Observation & Reflection
    logger.info("Step 6: Running Intelligence Observation/Reflection loop...")
    current_state = await network_brain.observe()
    logger.info(f"Brain observed state: {current_state}")
    
    if current_state == "wifi":
        logger.info("✅ SUCCESS: Brain recognized the new network mode.")
        await network_brain.reflect(current_state)
    else:
        logger.error(f"❌ FAILED: Brain reported wrong state: {current_state}")
        sys.exit(1)

    # 7. Shutdown
    logger.info("Step 7: Shutting down Engine...")
    network_brain.stop()
    orchestrator.stop()

    if not orchestrator._is_running:
        logger.info("✅ SUCCESS: Engine shutdown verified.")
    else:
        logger.error("❌ FAILED: Engine failed to stop.")
        sys.exit(1)

    print("\n✨ [PASSED] Pwonagotchi_own Intelligence Integration Test Complete! ✨\n")

if __name__ == "__main__":
    try:
        asyncio.run(run_integration_test())
    except Exception as e:
        print(f"💥 UNEXPECTED ERROR IN TEST: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
