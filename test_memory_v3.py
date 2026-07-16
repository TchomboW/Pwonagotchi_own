import logging
import sys
import os

# Use absolute path for deterministic behavior
PROJECT_ROOT = os.path.abspath("/Users/tony/Pwonagotchi_own")
sys.path.insert(0, PROJECT_ROOT)

try:
    from intelligence.memory.state_manager import StateManager
    print("Import successful!")
except Exception as e:
    print(f"Import FAILED: {e}")
    sys.exit(1)

def run_test():
    print("🚀 Starting StateManager test...")
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    
    # Use the absolute path for the storage dir inside the project structure
    store = StateManager(os.path.join(PROJECT_ROOT, "intelligence/memory"))
    
    print("Step 1: Saving state...")
    store.save_state("test_key", {"status": "active", "value": 42})
    
    print("Step 2: Loading state...")
    retrieved = store.get_state("test_key")
    print(f"Retrieved: {retrieved}")
    
    if retrieved.get("status") == "active":
        print("\n✨ [PASSED] StateManager Verification Successful! ✨\n")
    else:
        print("\n❌ [FAILED] Data Mismatch.\n")

if __name__ == '__main__':
    run_test()
