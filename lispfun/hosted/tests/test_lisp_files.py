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

# New parser functions may exist; fall back to Python versions if not
try:
    from lispfun.interpreter import parse_multiple_lisp, parse_lisp
except ImportError:  # pragma: no cover - parser not implemented yet
    parse_multiple_lisp = parse_multiple
    parse_lisp = parse

EVAL_FILE = os.path.join(os.path.dirname(__file__), "..", "evaluator.lisp")
BASIC_TEST = os.path.join(os.path.dirname(__file__), "lisp", "basic.lisp")
SELFTEST_FILE = os.path.join(os.path.dirname(__file__), "lisp", "selftest.lisp")
STRINGPARSE_FILE = os.path.join(os.path.dirname(__file__), "lisp", "stringparse.lisp")
STRINGUTILS_FILE = os.path.join(os.path.dirname(__file__), "lisp", "stringutils.lisp")
NUMERIC_FILE = os.path.join(os.path.dirname(__file__), "lisp", "numeric.lisp")
PRED_FILE = os.path.join(os.path.dirname(__file__), "lisp", "predicates.lisp")


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
    """Run a file using eval2 with code parsed by the Lisp parser."""
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


def test_basic_file_eval2():
    assert run_file_with_eval2(BASIC_TEST) == [6, 4, 5, 7, 1, 1, [2, 3], [0, 1, 2, 3], [1, 2]]


def test_selftest_script():
    assert run_file_with_eval2(SELFTEST_FILE) == 1


def test_basic_file_eval2_lisp_parser():
    assert run_file_with_eval2_lisp_parser(BASIC_TEST) == [6, 4, 5, 7, 1, 1, [2, 3], [0, 1, 2, 3], [1, 2]]


def test_selftest_script_lisp_parser():
    assert run_file_with_eval2_lisp_parser(SELFTEST_FILE) == 1


def test_stringparse_script():
    assert run_file_with_eval2(STRINGPARSE_FILE) == 1

def test_stringutils_script():
    assert run_file_with_eval2(STRINGUTILS_FILE) == 1


def test_numeric_script():
    assert run_file_with_eval2(NUMERIC_FILE) == 1


def test_predicates_script():
    assert run_file_with_eval2(PRED_FILE) == 1


