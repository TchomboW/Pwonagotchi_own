import subprocess
import os

class PwonBridge:
    def __init__(self, repo_root):
        self.repo_root = repo_root
        self.engine_dir = os.path.join(repo_root, "rust_engine")

    def run_subcommand(self, cmd="cargo test"):
        result = subprocess.run([cmd], cwd=self.engine_dir, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
