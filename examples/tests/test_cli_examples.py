import sys
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
run_bootstrap = root / 'run_bootstrap.py'
run_hosted = root / 'run_hosted.py'
run_toy = root / 'run_toy.py'
bootstrap_tests = root / 'examples' / 'bootstrap-tests.lisp'
hosted_tests = root / 'examples' / 'hosted-tests.lisp'
toy_tests = root / 'examples' / 'toy-tests.lisp'
run_script = root / 'run_example_tests.sh'


def run(cmd):
    return subprocess.run([sys.executable, str(cmd[0]), str(cmd[1])], capture_output=True)


def test_bootstrap_examples():
    proc = run([run_bootstrap, bootstrap_tests])
    assert proc.returncode == 0
    proc = run([run_bootstrap, hosted_tests])
    assert proc.returncode != 0
    proc = run([run_bootstrap, toy_tests])
    assert proc.returncode != 0


def test_hosted_examples():
    proc = run([run_hosted, bootstrap_tests])
    assert proc.returncode == 0
    proc = run([run_hosted, hosted_tests])
    assert proc.returncode == 0
    proc = run([run_hosted, toy_tests])
    assert proc.returncode != 0


def test_toy_examples():
    proc = run([run_toy, bootstrap_tests])
    assert proc.returncode == 0
    proc = run([run_toy, hosted_tests])
    assert proc.returncode == 0
    proc = run([run_toy, toy_tests])
    assert proc.returncode == 0


def test_run_example_tests_script():
    proc = subprocess.run(['bash', str(run_script)], capture_output=True)
    assert proc.returncode == 0

