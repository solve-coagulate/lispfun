import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from lispfun.interpreter import parse, kernel_env
from run_hosted import load_eval, eval_with_eval2


def test_run_basic_with_kernel_env():
    env = kernel_env()
    load_eval(env)
    result = eval_with_eval2(parse("(+ 1 2)"), env)
    assert result == 3

