#!/usr/bin/env python
"""Run the pure Python bootstrap interpreter."""
import sys
from lispfun.bootstrap.interpreter import (
    parse,
    parse_multiple,
    eval_lisp,
    standard_env,
    to_string,
)


def run_file(filename: str, env) -> None:
    """Execute expressions from *filename* using *env*."""
    with open(filename) as f:
        code = f.read()
    for exp in parse_multiple(code):
        eval_lisp(exp, env)


def repl(env) -> None:
    """Interactive REPL using the bootstrap interpreter."""
    while True:
        try:
            line = input("lispfun> ")
            if not line:
                continue
            val = eval_lisp(parse(line), env)
            if val is not None:
                print(to_string(val))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as e:
            print(f"Error: {e}")


def main() -> None:
    env = standard_env()
    if len(sys.argv) > 1:
        run_file(sys.argv[1], env)
    else:
        repl(env)


if __name__ == "__main__":
    main()
