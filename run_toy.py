#!/usr/bin/env python
"""Run the toy interpreter implemented in Lisp."""
import sys
import os
from lispfun.bootstrap.interpreter import (
    standard_env,
    parse as py_parse,
    parse_multiple as py_parse_multiple,
    to_string,
)
from run_hosted import load_eval, eval_with_eval2

TOY_REPL_FILE = os.path.join(os.path.dirname(__file__), "toy", "toy-repl.lisp")
TOY_FILE = os.path.join(os.path.dirname(__file__), "toy", "toy-interpreter.lisp")


def load_toy(env):
    """Load the toy interpreter implemented in Lisp."""

    # Ensure all standard environment symbols are available when starting from
    # the minimal ``kernel_env``.
    for key, val in standard_env().items():
        env.setdefault(key, val)

    def process_expr(exp):
        if isinstance(exp, list) and exp and exp[0] == "import":
            path = str(exp[1])
            with open(path) as f:
                sub_code = f.read()
            for sub_exp in py_parse_multiple(sub_code):
                process_expr(sub_exp)
        else:
            eval_with_eval2(exp, env)

    with open(TOY_FILE) as f:
        code = f.read()
    for exp in py_parse_multiple(code):
        process_expr(exp)


def toy_run_file(filename, env):
    """Execute a Lisp script using the toy interpreter."""
    load_toy(env)
    program = py_parse(f'(run-file "{filename}")')
    return eval_with_eval2(program, env)



def lisp_toy_repl(env) -> None:
    """Run the toy REPL implemented entirely in Lisp."""
    toy_run_file(TOY_REPL_FILE, env)


def main() -> None:
    env = standard_env()
    load_eval(env)
    load_toy(env)
    if len(sys.argv) > 1:
        env["args"] = sys.argv[2:]
        toy_run_file(sys.argv[1], env)
    elif not sys.stdin.isatty():
        toy_run_file("/dev/stdin", env)
    else:
        env["args"] = []
        lisp_toy_repl(env)


if __name__ == "__main__":
    main()
