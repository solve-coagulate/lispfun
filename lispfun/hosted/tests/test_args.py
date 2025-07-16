import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

from lispfun.interpreter import (
    parse_multiple,
    eval_lisp,
    standard_env,
    to_string,
    parse,
)

EVAL_FILE = os.path.join(os.path.dirname(__file__), "..", "evaluator.lisp")
ARGS_FILE = os.path.join(os.path.dirname(__file__), "lisp", "args.lisp")


def run_file_with_args(file_path, args_list):
    env = standard_env()
    with open(EVAL_FILE) as f:
        evaluator_code = f.read()
    for exp in parse_multiple(evaluator_code):
        eval_lisp(exp, env)
    env["env"] = env
    env["args"] = args_list
    with open(file_path) as f:
        code = f.read()
    exprs = parse_multiple(code)
    result = None
    for exp in exprs:
        program = f"(eval2 (quote {to_string(exp)}) env)"
        result = eval_lisp(parse(program), env)
    return result


def test_args_variable():
    assert run_file_with_args(ARGS_FILE, ["one", "two"]) == ["one", "two"]
