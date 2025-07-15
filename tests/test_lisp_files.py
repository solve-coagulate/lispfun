import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lispfun.interpreter import parse_multiple, eval_lisp, standard_env, to_string, parse

EVAL_FILE = os.path.join(os.path.dirname(__file__), "..", "lispfun", "evaluator.lisp")
LISP_TEST = os.path.join(os.path.dirname(__file__), "lisp", "basic.lisp")


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
    eval_lisp(parse(evaluator_code), env)
    env['env'] = env
    with open(file_path) as f:
        code = f.read()
    exprs = parse_multiple(code)
    result = None
    for exp in exprs:
        program = f"(eval2 (quote {to_string(exp)}) env)"
        result = eval_lisp(parse(program), env)
    return result


def test_lisp_file_base_eval():
    assert run_file_with_eval(LISP_TEST) == [6, 4, 7, 1]


def test_lisp_file_eval2():
    assert run_file_with_eval2(LISP_TEST) == [6, 4, 7, 1]
