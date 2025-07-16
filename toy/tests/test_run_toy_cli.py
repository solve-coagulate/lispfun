import os
import sys
import subprocess
from pathlib import Path


def test_run_toy_from_stdin():
    root = Path(__file__).resolve().parents[2]
    run_toy = root / "run_toy.py"
    cmd = [sys.executable, str(run_toy), "/dev/stdin"]
    proc = subprocess.run(cmd, input='(print "Hello...")', text=True, capture_output=True, check=True)
    assert proc.stdout.strip() == "Hello..."
