import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "src" / "main.py"


class Stage2Tests(unittest.TestCase):
    def test_both_parameters_are_printed(self):
        result = subprocess.run(
            [
                sys.executable,
                str(MAIN),
                "--vfs", "./data/vfs",
                "--startup", "./scripts/startup_alt.txt",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertIn("VFS: ./data/vfs", result.stdout)
        self.assertIn(
            "Startup script: ./scripts/startup_alt.txt",
            result.stdout,
        )

    def test_missing_startup_script_is_reported(self):
        result = subprocess.run(
            [
                sys.executable,
                str(MAIN),
                "--vfs", "./data/vfs",
                "--startup", "./scripts/missing.txt",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("не найден", result.stderr)

if __name__ == "__main__":
    unittest.main()