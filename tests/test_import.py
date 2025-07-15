import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lispfun.interpreter import parse, eval_lisp, standard_env
from lispfun.run import load_eval, run_file

SUPPORT = os.path.join(os.path.dirname(__file__), "lisp", "import_support.lisp")
MAIN = os.path.join(os.path.dirname(__file__), "lisp", "import_main.lisp")


def test_import_function():
    env = standard_env()
    eval_lisp(parse(f'(import "{SUPPORT}")'), env)
    assert eval_lisp(parse('(inc 1)'), env) == 2


def test_import_in_file_eval2():
    env = standard_env()
    load_eval(env)
    result = run_file(MAIN, env)
    assert result == 42
