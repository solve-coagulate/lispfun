import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from lispfun.interpreter import parse, eval_lisp, standard_env


def eval_prog(expr: str):
    env = standard_env()
    return eval_lisp(parse(expr), env)


def test_add():
    assert eval_prog("(+ 1 2 3)") == 6


def test_define_and_use():
    env = standard_env()
    eval_lisp(parse("(define x 4)"), env)
    assert eval_lisp(parse("x"), env) == 4


def test_lambda_call():
    env = standard_env()
    eval_lisp(parse("(define add2 (lambda (a b) (+ a b)))"), env)
    assert eval_lisp(parse("(add2 3 4)"), env) == 7


def test_if_expression():
    env = standard_env()
    assert eval_lisp(parse("(if (> 3 2) 1 0)"), env) == 1
