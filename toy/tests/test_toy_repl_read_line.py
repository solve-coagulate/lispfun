import builtins
from lispfun.interpreter import standard_env
from run_hosted import load_eval
from run_toy import load_toy, python_toy_repl, lisp_toy_repl
import pytest


def setup_env():
    env = standard_env()
    load_eval(env)
    load_toy(env)
    return env


def test_python_toy_repl_reads_line(monkeypatch, capsys):
    """REPL implemented in Python should read a line and print it."""
    env = setup_env()
    inputs = iter(['(print (read-line))', 'hi', 'exit'])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))
    python_toy_repl(env)
    out, err = capsys.readouterr()
    assert 'hi' in out


def test_lisp_toy_repl_reads_line(monkeypatch, capsys):
    """Lisp REPL implemented in toy interpreter should echo a line read via read-line."""
    env = setup_env()
    inputs = iter(['(print (read-line))', 'hi', 'exit'])
    monkeypatch.setattr(builtins, 'input', lambda prompt='': next(inputs))
    lisp_toy_repl(env)
    out, err = capsys.readouterr()
    assert 'hi' in out
