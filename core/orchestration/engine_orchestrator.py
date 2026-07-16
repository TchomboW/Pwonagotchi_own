import logging
from typing import Dict, Any

class EngineOrchestrator:
    """
    The central nervous system of the Pwonagotchi_own engine.
    Responsible for registering core modules, managing their lifecycles,
    and dispatching high-level intelligence commands to specialized controllers.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._modules: Dict[str, Any] = {}
        self._is_running = False

    def register_module(self, name: str, module_instance: Any):
        """Registers a core module (e.g., Networking, Hardware) with the orchestrator."""
        self._modules[name] = module_instance
        self.logger.info(f"Module '{name}' registered in the Orchestrator.")

    def get_module(self, name: str):
        """Returns a registered module instance."""
        return self._modules.get(name)

    def start(self):
        """Initializes all registered modules and starts the engine loop."""
        self.logger.info("Starting Engine Orchestrator...")
        for name, module in self._modules.items():
            if hasattr(module, 'initialize'):
                try:
                    module.initialize()
                    self.logger.info(f"Successfully initialized module: {name}")
                except Exception as e:
                    self.logger.error(f"Failed to initialize module '{name}': {e}")
            else:
                self.logger.warning(f"Module '{name}' does not support formal initialization.")
        self._is_running = True
        self.logger.info("Engine Orchestrator is fully active.")

    def stop(self):
        """Gracefully shuts down all registered modules."""
        self.logger.info("Stopping Engine Orchestrator...")
        for name, module in self._modules.items():
            if hasattr(module, 'shutdown'):
                try:
                    module.shutdown()
                    self.logger.info(f"Module '{name}' shutdown successfully.")
                except Exception as e:
                    self.logger.error(f"Error during module '{name}' shutdown: {e}")
        self._is_running = False
        self.logger.info("Engine Orchestrator stopped.")

    def dispatch(self, category: str, action: str, **kwargs):
        """Dispatches a high-level command to a specific module category."""
        if not self._is_running:
            self.logger.error(f"Cannot dispatch '{action}' in '{category}': Engine is not running.")
            return False

        module = self.get_module(category)
        if not module:
            self.logger.error(f"Module category error: '{category}' not found in orchestrator registry.")
            return False

        try:
            method = getattr(module, action)
            if callable(method):
                result = method(**kwargs)
                self.logger.info(f"Dispatched: {category}.{action} -> Result: {result}")
                return result
            else:
                self.logger.error(f"Module '{category}' contains non-callable attribute '{action}'.")
                return False
        except Exception as e:
            self.logger.error(f"Dispatch failed for {category}.{action}: {e}")
            return False
