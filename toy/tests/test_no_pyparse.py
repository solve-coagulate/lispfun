from lispfun.interpreter import standard_env
from run_hosted import load_eval
from run_toy import load_toy


def setup_env():
    env = standard_env()
    load_eval(env)
    load_toy(env)
    return env


def test_load_toy_does_not_define_py_parse():
    env = setup_env()
    assert 'py-parse' not in env
    assert 'parse' not in env
