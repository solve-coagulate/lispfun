import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from lispfun.interpreter import parse, eval_lisp, standard_env
from lispfun.parser import Symbol


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

def test_quote():
    env = standard_env()
    assert eval_lisp(parse("(quote hello)"), env) == 'hello'
    assert eval_lisp(parse("(quote (1 2))"), env) == [1, 2]

def test_list_operations():
    env = standard_env()
    assert eval_lisp(parse("(list 1 2 3)"), env) == [1, 2, 3]
    assert eval_lisp(parse("(car (list 1 2 3))"), env) == 1
    assert eval_lisp(parse("(cdr (list 1 2 3))"), env) == [2, 3]
    assert eval_lisp(parse("(cons 0 (list 1 2 3))"), env) == [0, 1, 2, 3]
    assert eval_lisp(parse("(list? (list 1 2))"), env)


def test_string_literal_and_print(capsys):
    env = standard_env()
    eval_lisp(parse('(print "hello world")'), env)
    captured = capsys.readouterr()
    assert captured.out.strip() == 'hello world'
    assert eval_lisp(parse('(quote "hi there")'), env) == 'hi there'


def test_symbol_and_digits_helpers():
    env = standard_env()
    make_sym = env['make-symbol']
    digits_to_number = env['digits->number']
    sym = make_sym('foo')
    assert isinstance(sym, Symbol)
    assert env['symbol?'](sym)
    assert digits_to_number('123') == 123
    assert digits_to_number('3.14') == 3.14

