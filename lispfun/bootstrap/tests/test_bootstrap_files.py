import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

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

EVAL_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "hosted", "evaluator.lisp")
BOOTSTRAP_TEST = os.path.join(os.path.dirname(__file__), "lisp", "bootstrap.lisp")


def run_file_with_eval(file_path):
    env = standard_env()
    with open(file_path) as f:
        code = f.read()
    exprs = parse_multiple(code)
    result = None
    for exp in exprs:
        result = eval_lisp(exp, env)
    return result


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


def run_file_with_eval2_lisp_parser(file_path):
    env = standard_env()
    with open(EVAL_FILE) as f:
        evaluator_code = f.read()
    for exp in parse_multiple_lisp(evaluator_code):
        eval_lisp(exp, env)
    env["env"] = env
    with open(file_path) as f:
        code = f.read()
    exprs = parse_multiple_lisp(code)
    result = None
    for exp in exprs:
        program = f"(eval2 (quote {to_string(exp)}) env)"
        result = eval_lisp(parse_lisp(program), env)
    return result


def test_bootstrap_file_base_eval():
    assert run_file_with_eval(BOOTSTRAP_TEST) == [6, 4, 7, 1, [1, 2]]


def test_bootstrap_file_eval2():
    assert run_file_with_eval2(BOOTSTRAP_TEST) == [6, 4, 7, 1, [1, 2]]


def test_bootstrap_file_eval2_lisp_parser():
    assert run_file_with_eval2_lisp_parser(BOOTSTRAP_TEST) == [6, 4, 7, 1, [1, 2]]

