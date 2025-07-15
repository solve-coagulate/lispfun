import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lispfun.interpreter import parse, parse_multiple, eval_lisp, standard_env

EVAL_FILE = os.path.join(os.path.dirname(__file__), "..", "lispfun", "evaluator.lisp")


def setup_env():
    env = standard_env()
    with open(EVAL_FILE) as f:
        code = f.read()
    for exp in parse_multiple(code):
        eval_lisp(exp, env)
    env['env'] = env
    return env


def eval_self(expr: str):
    env = setup_env()
    program = f"(eval2 (quote {expr}) env)"
    return eval_lisp(parse(program), env)


def test_self_add():
    assert eval_self("(+ 2 3)") == 5


def test_self_define_and_use():
    env = setup_env()
    eval_lisp(parse("(eval2 (quote (define y 7)) env)"), env)
    assert eval_lisp(parse("(eval2 (quote y) env)"), env) == 7


def test_self_lambda():
    env = setup_env()
    eval_lisp(parse("(eval2 (quote (define add (lambda (a b) (+ a b))) ) env)"), env)
    assert eval_lisp(parse("(eval2 (quote (add 1 2)) env)"), env) == 3


def test_self_if():
    env = setup_env()
    assert eval_lisp(parse("(eval2 (quote (if (> 3 2) 1 0)) env)"), env) == 1


def test_self_quote():
    assert eval_self("(quote hello)") == 'hello'
    assert eval_self("(quote (1 2))") == [1, 2]


def test_self_string_literal():
    assert eval_self('(quote "hello world")') == 'hello world'

def test_self_list_operations():
    env = setup_env()
    assert eval_lisp(parse("(eval2 (quote (list 1 2 3)) env)"), env) == [1, 2, 3]
    assert eval_lisp(parse("(eval2 (quote (car (list 1 2 3))) env)"), env) == 1
    assert eval_lisp(parse("(eval2 (quote (cdr (list 1 2 3))) env)"), env) == [2, 3]
    assert eval_lisp(parse("(eval2 (quote (cons 0 (list 1 2 3))) env)"), env) == [0, 1, 2, 3]
    assert eval_lisp(parse("(eval2 (quote (list? (list 1 2))) env)"), env)


def test_self_set_and_begin():
    env = setup_env()
    eval_lisp(parse("(eval2 (quote (define z 1)) env)"), env)
    assert eval_lisp(parse("(eval2 (quote (begin (set! z 4) z)) env)"), env) == 4


def test_self_cond():
    env = setup_env()
    expr = "(cond ((> 3 4) 0) ((< 3 4) 1) (else 2))"
    assert eval_lisp(parse(f"(eval2 (quote {expr}) env)"), env) == 1


def test_self_macro():
    env = setup_env()
    define = "(define-macro when (lambda (test expr) (list (quote if) test expr 0)))"
    eval_lisp(parse(f"(eval2 (quote {define}) env)"), env)
    assert eval_lisp(parse("(eval2 (quote (when (> 3 2) 42)) env)"), env) == 42


def test_self_list_utilities():
    env = setup_env()
    assert eval_lisp(parse("(eval2 (quote (null? (quote ())) ) env)"), env)
    assert eval_lisp(parse("(eval2 (quote (length (list 1 2 3))) env)"), env) == 3


def test_self_map_filter():
    env = setup_env()
    eval_lisp(parse("(eval2 (quote (define add1 (lambda (x) (+ x 1))) ) env)"), env)
    assert eval_lisp(parse("(eval2 (quote (map add1 (list 1 2 3))) env)"), env) == [2, 3, 4]
    expr = "(filter (lambda (x) (> x 2)) (list 1 2 3 4))"
    assert eval_lisp(parse(f"(eval2 (quote {expr}) env)"), env) == [3, 4]


