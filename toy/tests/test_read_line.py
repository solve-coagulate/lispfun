import os, sys
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lispfun.interpreter import standard_env, parse
from run_hosted import load_eval, eval_with_eval2
from run_toy import load_toy


def setup_env():
    env = standard_env()
    load_eval(env)
    load_toy(env)
    return env


def test_read_line_returns_input(monkeypatch):
    env = setup_env()
    monkeypatch.setattr('builtins.input', lambda prompt='': 'hi')
    result = eval_with_eval2(parse('(read-line "foo> ")'), env)
    assert result == 'hi'


def test_read_line_eof(monkeypatch):
    env = setup_env()
    def raise_eof(prompt=''):
        raise EOFError
    monkeypatch.setattr('builtins.input', raise_eof)
    result = eval_with_eval2(parse('(read-line)'), env)
    assert result == ''


def test_run_toy_script_reads_line(tmp_path):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    script = tmp_path / 'readline.lisp'
    script.write_text('(print (read-line))')
    cmd = [sys.executable, os.path.join(root, 'run_toy.py'), str(script)]
    proc = subprocess.run(cmd, input='Hello\n', text=True, capture_output=True, check=True)
    assert proc.stdout.strip() == 'Hello'

