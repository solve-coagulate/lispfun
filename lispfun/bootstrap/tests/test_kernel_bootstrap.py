import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from lispfun.interpreter import parse, eval_lisp, kernel_env
from run_hosted import load_eval


def test_kernel_basic_ops():
    env = kernel_env()
    assert eval_lisp(parse("(+ 1 2)"), env) == 3


@pytest.mark.xfail(reason="kernel env missing 'import' for self-hosted evaluator")
def test_load_eval_fails_in_kernel_env():
    env = kernel_env()
    load_eval(env)
