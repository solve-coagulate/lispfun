#!/usr/bin/env python
"""Run the toy interpreter implemented in Lisp."""
import sys
import os
from lispfun.bootstrap.interpreter import (
    standard_env,
    parse,
    parse_multiple,
    to_string,
)
from lispfun.bootstrap.parser import Symbol
from run_hosted import load_eval, eval_with_eval2

TOY_REPL_FILE = os.path.join(os.path.dirname(__file__), "toy", "toy-repl.lisp")
TOY_FILE = os.path.join(os.path.dirname(__file__), "toy", "toy-interpreter.lisp")


def load_toy(env):
    """Load the toy interpreter implemented in Lisp."""
    # Expose the host parser for use by the Lisp REPL
    env['py-parse'] = parse
    env['py-parse-multiple'] = parse_multiple
    def import_file(path: str):
        with open(str(path)) as f:
            code = f.read()
        for exp in parse_multiple(code):
            eval_with_eval2(exp, env)

    with open(TOY_FILE) as f:
        code = f.read()
    for exp in parse_multiple(code):
        if (
            "import" not in env
            and isinstance(exp, list)
            and len(exp) == 2
            and exp[0] == Symbol("import")
        ):
            import_file(exp[1])
            env["import"] = import_file
        else:
            eval_with_eval2(exp, env)


def toy_run_file(filename, env):
    """Execute a Lisp script using the toy interpreter."""
    load_toy(env)
    program = parse(f'(run-file "{filename}")')
    return eval_with_eval2(program, env)




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
