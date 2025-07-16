import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from lispfun.interpreter import (
    parse_multiple,
    eval_lisp,
    standard_env,
    to_string,
    parse,
)

try:
    from lispfun.interpreter import parse_multiple_lisp, parse_lisp
except ImportError:  # pragma: no cover - parser not implemented yet
    parse_multiple_lisp = parse_multiple
    parse_lisp = parse

EVAL_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "lispfun", "hosted", "evaluator.lisp")
TOY_RUNNER_FILE = os.path.join(os.path.dirname(__file__), "..", "toy-runner.lisp")


def run_file_with_eval2(file_path):
    env = standard_env()
    with open(EVAL_FILE) as f:
        evaluator_code = f.read()
    for exp in parse_multiple(evaluator_code):
        eval_lisp(exp, env)
    env['env'] = env
    with open(file_path) as f:
        code = f.read()
    exprs = parse_multiple(code)
    result = None
    for exp in exprs:
        program = f"(eval2 (quote {to_string(exp)}) env)"
        result = eval_lisp(parse(program), env)
    return result


def test_toy_runner_script():
    # Running the toy interpreter and all example programs should succeed
    assert run_file_with_eval2(TOY_RUNNER_FILE) is None

