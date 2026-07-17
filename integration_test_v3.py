import asyncio
import logging
import sys
import os

# Resolve absolute path for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, PROJECT_ROOT)

from core.orchestration.engine_orchestrator import EngineOrchestrator
from core.networking import NetworkController
from core.hardware.controller import HardwareController
from intelligence.agent import IntelligenceAgent
from intelligence.cycles.network_observer import NetworkStatusObserver
from intelligence.profiles.stealth import StealthProfile

async def run_integration_test():
    print("🚀 Starting Pwonagotchi_own ADVANCED NERVOUS SYSTEM Test...")
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger("INTEGRATION_V3")

    # 1. Setup Stack
    orchestrator = EngineOrchestrator()
    net_controller = NetworkController()
    hw_controller = HardwareController()
    
    orchestrator.register_module('networking', net_controller)
    orchestrator.register_module('hardware', hw_controller)

    # 2. Setup Intelligence Agent with Memory
    from intelligence.memory.state_manager import StateManager
    memory = StateManager(os.path.join(PROJECT_ROOT, "intelligence/memory"))
    agent = IntelligenceAgent("Pwonagotchi-Prime", orchestrator, memory)

    # 3. Inject Profile (and verify parameter injection logic)
    logger.info("Step 1: Loading 'Stealth' profile and injecting into cycles...")
    agent.load_profile(StealthProfile)
    
    # Add cycle after profile is loaded so it gets the current params
    observer = NetworkStatusObserver("NetworkWatcher", orchestrator)
    agent.add_cycle(observer)
    
    # Verify parameter sync (should match StealthProfile param: scan_interval=60)
    if observer.parameters.get('scan_interval') == 60:
        logger.info("✅ SUCCESS: Profile parameters successfully injected into cycle.")
    else:
        logger.error(f"❌ FAILED: Parameter mismatch! Expected 60, got {observer.parameters.get('scan_interval')}")
        sys.exit(1)

    # 4. Start the World
    logger.info("Step 2: Starting Engine and its cycles...")
    orchestrator.start()
    agent.start_all()

    # 5. Simulate Reality (The trigger)
    logger.info("Step 3: Simulating physical event (Network Switch to WiFi)...")
    net_result = orchestrator.dispatch('networking', 'switch_to_wifi')
    if not net_result:
        logger.error("❌ FAILED: Networking dispatch failed!")
        sys.exit(1)

    # 6. Intelligence Pulse (The Brain-Action loop)
    logger.info("Step 4: Triggering Intelligence Pulse...")
    await agent.pulse()

    # 7. Verification of Observation
    logger.info("Step 5: Verifying observation results...")
    current_state = await observer.observe()
    if current_state == "wifi":
        logger.info("✅ SUCCESS: Brain observed correct state matching physical reality.")
    else:
        logger.error(f"❌ FAILED: Observation mismatch! Expected 'wifi', got '{current_state}'")
        sys.exit(1)

    # 8. Cleanup
    logger.info("Step 6: Shutting down system stack...")
    agent.stop_all()
    orchestrator.stop()

    print("\n✨ [PASSED] Pwonagotchi_own ADVANCED NERVOUS SYSTEM Test Complete! ✨\n")

if __name__ == "__main__":
    asyncio.run(run_integration_test())
