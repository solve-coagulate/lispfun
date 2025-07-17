import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lispfun.interpreter import kernel_env
from run_hosted import load_eval
from run_toy import load_toy

@pytest.mark.xfail(reason="toy interpreter not bootstrapped with kernel env yet")
def test_toy_kernel_env():
    env = kernel_env()
    load_eval(env)
    load_toy(env)

