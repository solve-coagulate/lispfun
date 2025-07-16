import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lispfun.interpreter import standard_env
from lispfun.run import load_eval, load_toy, toy_run_file


BASIC_TEST = os.path.join(os.path.dirname(__file__), "..", "..", "lispfun", "hosted", "tests", "lisp", "basic.lisp")
LOOP_TEST = os.path.join(os.path.dirname(__file__), "lisp", "loops.lisp")
STRING_TEST = os.path.join(os.path.dirname(__file__), "lisp", "toy-strings.lisp")
REQUIRE_TEST = os.path.join(os.path.dirname(__file__), "lisp", "require-test.lisp")


def setup_env():
    env = standard_env()
    load_eval(env)
    load_toy(env)
    return env


def test_toy_run_basic():
    env = setup_env()
    result = toy_run_file(BASIC_TEST, env)
    assert result == [6, 4, 5, 7, 1, 1, [2, 3], [0, 1, 2, 3], [1, 2]]


def test_toy_run_loops():
    env = setup_env()
    result = toy_run_file(LOOP_TEST, env)
    assert result == [120, 15]


def test_toy_run_strings():
    env = setup_env()
    result = toy_run_file(STRING_TEST, env)
    assert result == [True, True]


def test_toy_require_module():
    env = setup_env()
    result = toy_run_file(REQUIRE_TEST, env)
    assert result == 1

