import json
import logging
import os

class StateManager:
    """
    The persistent memory component of Pwonotagchi_own.
    Handles reading and writing of structured state/intelligence data to disk.
    """

    def __init__(self, storage_path: str):
        self.logger = logging.getLogger(__name__)
        self.storage_path = storage_path
        self._state = {}

    def load_all(self):
        self.logger.info(f"Loading state from {self.storage_path}...")
        try:
            for filename in os.listdir(self.storage_path):
                if filename.endswith(".json"):
                    with open(os.path.join(self.storage_path, filename), 'r') as f:
                        data = json.load(f)
                        key = filename.replace(".json", "")
                        self._state[key] = data
            self.logger.info(f"Loaded {len(self._state)} state files.")
        except Exception as e:
            self.logger.error(f"Failed to load states: {e}")

    def save_state(self, key: str, data: dict):
        try:
            file_path = os.path.join(self.storage_path, f"{key}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            self._state[key] = data
            self.logger.info(f"Saved state '{key}' to {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to save state '{key}': {e}")

    def get_state(self, key: str) -> dict:
        return self._state.get(key, {})

    def delete_state(self, key: str):
        if key in self._state:
            file_path = os.path.join(self.storage_path, f"{key}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            del self._state[key]
            self.logger.info(f"Deleted state '{key}'.")

    def get_all(self) -> dict:
        return self._state
