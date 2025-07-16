#!/usr/bin/env python
"""Run the toy interpreter implemented in Lisp."""
import sys
from lispfun.interpreter import standard_env
from lispfun.run import load_eval, load_toy, toy_run_file, repl


def main() -> None:
    env = standard_env()
    load_eval(env)
    load_toy(env)
    if len(sys.argv) > 1:
        toy_run_file(sys.argv[1], env)
    else:
        repl(env)


if __name__ == "__main__":
    main()
