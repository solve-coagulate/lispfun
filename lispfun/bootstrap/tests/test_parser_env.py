import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from lispfun.bootstrap.parser import kernel_parser_env, parser_env


def test_kernel_parser_env():
    p = kernel_parser_env()
    tokens = p['tokenize']('(add 1 2)')
    assert tokens == ['(', 'add', '1', '2', ')']
    ast = p['parse']('(add 1 2)')
    assert ast == ['add', 1, 2]


def test_parser_env_superset():
    base = kernel_parser_env()
    full = parser_env()
    for key in base:
        assert key in full
    assert 'parse-multiple' in full
    assert 'to-string' in full

