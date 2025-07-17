import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from lispfun.interpreter import (
    parse,
    parse_multiple,
    eval_lisp,
    standard_env,
    to_string,
)

from run_hosted import load_eval, eval_with_eval2

EVAL_FILE = os.path.join(os.path.dirname(__file__), "..", "evaluator.lisp")


def load_eval_using_eval2(target_env, runner_env):
    """Load evaluator.lisp into *target_env* using eval2 from *runner_env*."""
    with open(EVAL_FILE) as f:
        code = f.read()
    for exp in parse_multiple(code):
        program = f"(eval2 (quote {to_string(exp)}) target)"
        eval_lisp(parse(program), runner_env)
    target_env["env"] = target_env


def test_eval2_can_bootstrap_another_env():
    runner_env = standard_env()
    load_eval(runner_env)  # bootstrap eval2 using Python
    target_env = standard_env()
    runner_env["target"] = target_env
    load_eval_using_eval2(target_env, runner_env)
    assert eval_with_eval2(parse("(+ 1 2)"), target_env) == 3

