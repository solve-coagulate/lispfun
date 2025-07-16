#!/usr/bin/env python
"""Run the toy interpreter implemented in Lisp."""
import sys
import os
from lispfun.bootstrap.interpreter import (
    standard_env,
    parse,
    to_string,
    eval_lisp,
)
from lispfun.run import load_eval, load_toy, toy_run_file, eval_with_eval2

TOY_REPL_FILE = os.path.join(os.path.dirname(__file__), "toy", "toy-repl.lisp")




def python_toy_repl(env) -> None:
    """Interactive REPL implemented in Python using the toy interpreter."""
    while True:
        try:
            line = input("toy> ")
        except EOFError:
            print()
            break
        if line in {"", "exit"}:
            break
        try:
            expr = parse(line)
            result = eval_with_eval2(expr, env)
            if result is not None:
                print(to_string(result))
        except Exception as exc:  # pragma: no cover - exercise REPL manually
            print(f"Error: {exc}")


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
