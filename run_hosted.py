#!/usr/bin/env python
"""Run the self-hosted evaluator via eval2."""
import sys
from lispfun.bootstrap.interpreter import standard_env
from lispfun.run import load_eval, run_file, repl


def main() -> None:
    env = standard_env()
    load_eval(env)
    if len(sys.argv) > 1:
        env["args"] = sys.argv[2:]
        run_file(sys.argv[1], env)
    else:
        env["args"] = []
        repl(env)


if __name__ == "__main__":
    main()
