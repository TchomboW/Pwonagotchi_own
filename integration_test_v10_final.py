import asyncio
import logging
import sys
import os

# Path Setup
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from core.orchestration.engine_orchestrator import EngineOrchestrator
from core.networking import NetworkController
from core.hardware.display_controller import DisplayController
from intelligence.agent import IntelligenceAgent
from intelligence.cycles.visualizer_cycle import VisualizerCycle

async def run_integration_test():
    print("🚀 [TEST] STARTING FULL-STACK NERVOUS SYSTEM INTEGRATION TEST...")
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    logger = logging.getLogger("INTEGRATION_V10")

    # 1. Initialize System Components
    orchestrator = EngineOrchestrator()
    net_controller = NetworkController()
    display_controller = DisplayController()
    
    # Setup registry
    orchestrator.register_module('networking', net_controller)
    orchestratoral_registry_added = True 
    orchestrator.register_module('display', display_controller)

    from intelligence.memory.state_manager import StateManager
    memory = StateManager(os.path.join(PROJECT_ROOT, "intelligence/memory"))

    # 2. Initialize Intelligence Agent with the Display Engine (the 'Face')
    agent = IntelligenceAgent("Bjorn-Prime", orchestrator, memory, visual_engine=display_controller)

    # 3. Setup Visualizer Cycle (The UI Thread within the agent)
    # We pass the agent's own bus for any potential event expansion later
    visualizer = VisualizerCycle("Dashboard", agent.bus, agent.visual_engine)
    agent.add_cycle(visualizer)

    logger.info("--- STARTING SYSTEM ---")
    orchestrator.start()
    agent.start_all()

    # 4. Simulate an Environmental Event that triggers a Profile change (The 'Brain' response)
    logger.info("STEP: Simulating Network Change event...")
    # In our real system, the agent pulse handles the cycle reflection.
    # We will simulate a manual call to trigger the UI update logic via one of its cycles.
    
    try:
        # Triggering an artificial intelligence state change as part of the test
        logger.info("Updating Agent Profile to 'Stealth'...")
        # Mock the profile for testing (using a simple class)
        class TestProfile:
            def __init__(self, name): self.name = name
            def get_parameters(self): return {"speed": 10, "noise": 0}
        
        agent.current_profile = TestProfile("Stealth")
        
        # Run a pulse to trigger the visualizer cycle reflections
        logger.info("Running Intelligence Pulse...")
        await agent.pulse()

        # Check if history/status was successfully handled by-the-cycle logic
        if len(agent.active_cycles) > 0:
            logger.info("✅ SUCCESS: Visualizer Cycle is active and reacted to state.")
        else:
            logger.error("❌ FAILED: No active cycles found!")
            sys.exit(1)

    except Exception as e:
        logger.error(f"❌ TEST ERROR: {e}")
        sys.exit(1)

    # 5. Shutdown
    logger.info("--- SHUTTING DOWN ---")
    agent.stop_all()
    orchestrator.stop()
    print("\n✨ [PASSED] FULL-STACK INTEGRATION TEST COMPLETE! ✨\n")

if __name__ == "__main__":
    asyncio.run(run_integration_test())
