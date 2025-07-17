import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lispfun.interpreter import kernel_env
from run_hosted import load_eval, eval_with_eval2
from run_toy import load_toy
from lispfun.interpreter import parse

def test_toy_kernel_env():
    env = kernel_env()
    load_eval(env)
    load_toy(env)
    result = eval_with_eval2(parse('(length (list 1 2 3))'), env)
    assert result == 3

