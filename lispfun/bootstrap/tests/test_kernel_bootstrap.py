import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from lispfun.interpreter import parse, eval_lisp, kernel_env
from run_hosted import load_eval


def test_kernel_basic_ops():
    env = kernel_env()
    assert eval_lisp(parse("(+ 1 2)"), env) == 3


def test_load_eval_in_kernel_env():
    env = kernel_env()
    load_eval(env)
    assert "eval2" in env
    assert "import" not in env
