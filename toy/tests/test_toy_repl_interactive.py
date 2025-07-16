import os
import sys
import pty
import subprocess
from pathlib import Path


def run_interactive(expr: str) -> str:
    root = Path(__file__).resolve().parents[2]
    cmd = [sys.executable, str(root / 'run_toy.py')]
    master_fd, slave_fd = pty.openpty()
    proc = subprocess.Popen(
        cmd,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=subprocess.STDOUT,
        text=True,
    )
    os.close(slave_fd)

    out = ''
    while 'toy>' not in out:
        out += os.read(master_fd, 1024).decode()

    os.write(master_fd, (expr + '\nexit\n').encode())

    while True:
        try:
            chunk = os.read(master_fd, 1024)
        except OSError:
            break
        if not chunk:
            break
        out += chunk.decode()
    proc.wait(timeout=5)
    os.close(master_fd)
    return out


def test_toy_repl_interactive_prints_hi():
    output = run_interactive('(print "hi")')
    assert 'hi' in output
