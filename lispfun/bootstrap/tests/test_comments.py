import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from lispfun.interpreter import parse_multiple, eval_lisp, standard_env


def test_parse_comments():
    code = """; leading comment\n(+ 1 2) ; trailing comment\n"""
    env = standard_env()
    exprs = parse_multiple(code)
    result = None
    for exp in exprs:
        result = eval_lisp(exp, env)
    assert result == 3
