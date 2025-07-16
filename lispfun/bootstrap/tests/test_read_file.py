import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from lispfun.interpreter import parse, eval_lisp, standard_env


def test_read_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello")
    env = standard_env()
    result = eval_lisp(parse(f'(read-file "{file_path}")'), env)
    assert result == "hello"
