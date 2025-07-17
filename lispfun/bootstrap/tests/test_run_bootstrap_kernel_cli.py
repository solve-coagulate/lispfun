import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
run_bootstrap = root / 'run_bootstrap.py'
basic_file = root / 'lispfun' / 'bootstrap' / 'tests' / 'lisp' / 'bootstrap.lisp'


def test_run_bootstrap_kernel_cli():
    proc = subprocess.run(
        [sys.executable, str(run_bootstrap), '--kernel', str(basic_file)],
        capture_output=True,
    )
    assert proc.returncode == 0

