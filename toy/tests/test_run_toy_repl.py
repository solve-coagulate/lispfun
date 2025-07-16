import sys
from pathlib import Path
import subprocess


def test_run_toy_repl_pipe():
    root = Path(__file__).resolve().parents[2]
    cmd = [sys.executable, str(root / 'run_toy.py')]
    proc = subprocess.run(cmd, input='(print "Hello")\n', text=True, capture_output=True, check=True)
    assert 'Hello' in proc.stdout
