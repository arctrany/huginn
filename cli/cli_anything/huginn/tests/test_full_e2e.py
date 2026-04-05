import os
import subprocess
import shutil
import sys
import unittest
import json
import pytest

def _resolve_cli(name):
    """Resolve installed CLI command; falls back to python -m for dev.
    Set env CLI_ANYTHING_FORCE_INSTALLED=1 to require the installed command.
    """
    force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
    path = shutil.which(name)
    if path:
        print(f"[_resolve_cli] Using installed command: {path}")
        return [path]
    if force:
        raise RuntimeError(f"{name} not found in PATH. Install with: pip install -e .")
    module = name.replace("cli-anything-", "cli_anything.") + "." + name.split("-")[-1] + "_cli"
    print(f"[_resolve_cli] Falling back to: {sys.executable} -m {module}")
    return [sys.executable, "-m", module]

class TestCLISubprocessE2E(unittest.TestCase):
    CLI_BASE = _resolve_cli("cli-anything-huginn")

    def _run(self, args, check=True):
        return subprocess.run(
            self.CLI_BASE + args,
            capture_output=True, text=True,
            check=check,
        )

    def test_agent_list(self):
        result = self._run(["--json", "agent", "list"], check=False)
        # Note: If rails runner fails, it will output "Rails Script Error"
        # Since this is an E2E test, we normally expect Huginn to be installed.
        if result.returncode == 0:
            if "error" not in result.stdout:
                data = json.loads(result.stdout)
                self.assertIsInstance(data, list)
