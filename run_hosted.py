#!/usr/bin/env python
"""Run the self-hosted evaluator via ``eval2``."""
import os
import sys
from lispfun.bootstrap.interpreter import (
    parse,
    parse_multiple,
    eval_lisp,
    kernel_env,
    standard_env,
    to_string,
    Procedure,
)
from lispfun.bootstrap.parser import Symbol

# Path to the evaluator implemented in Lisp
EVAL_FILE = os.path.join(os.path.dirname(__file__), "lispfun", "hosted", "evaluator.lisp")
IMPORT_FILE = os.path.join(os.path.dirname(__file__), "lispfun", "hosted", "import.lisp")
LIST_UTILS = os.path.join(os.path.dirname(__file__), "lispfun", "hosted", "list_utils.lisp")
STRING_UTILS = os.path.join(os.path.dirname(__file__), "lispfun", "hosted", "string_utils.lisp")
EVAL_CORE = os.path.join(os.path.dirname(__file__), "lispfun", "hosted", "eval_core.lisp")


def load_eval(env):
    """Load ``eval2`` from :mod:`lispfun.hosted` into *env*.

    If ``import`` is missing, ``(import ...)`` forms are handled directly until
    the Lisp implementation defines it.
    """

    env["py-parse"] = parse
    env["py-parse-multiple"] = parse_multiple

    def import_file(path: str):
        with open(str(path)) as f:
            code = f.read()
        result = None
        exprs = parse_multiple(code)
        for exp in exprs:
            if "eval2" in env:
                program = f"(eval2 (quote {to_string(exp)}) env)"
                result = eval_lisp(parse(program), env)
            else:
                result = eval_lisp(exp, env)
        return result

    env["import"] = import_file

    for path in [IMPORT_FILE, LIST_UTILS, STRING_UTILS, EVAL_CORE]:
        import_file(path)
        env["import"] = import_file
    env["env"] = env
    if "eval2" in env:
        import_file(IMPORT_FILE)
    if not (isinstance(env.get("import"), Procedure) and "eval2" in env):
        env["import"] = import_file



def eval_with_eval2(exp, env):
    """Evaluate *exp* using ``eval2`` within *env*."""
    program = f"(eval2 (quote {to_string(exp)}) env)"
    return eval_lisp(parse(program), env)


def run_file(filename: str, env):
    """Execute Lisp code in *filename* using ``eval2``."""
    with open(filename) as f:
        code = f.read()
    exprs = parse_multiple(code)
    result = None
    for exp in exprs:
        result = eval_with_eval2(exp, env)
    return result


def repl(env) -> None:
    """Interactive REPL powered by ``eval2``."""
    while True:
        try:
            line = input("lispfun> ")
            if not line:
                continue
            val = eval_with_eval2(parse(line), env)
            if val is not None:
                print(to_string(val))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as e:
            print(f"Error: {e}")


def main() -> None:
    """Run the hosted evaluator with optional ``--kernel`` flag."""
    args = sys.argv[1:]
    use_kernel = False
    if args and args[0] == "--kernel":
        use_kernel = True
        args = args[1:]

    env = kernel_env() if use_kernel else standard_env()
    load_eval(env)

    if args:
        env["args"] = args[1:]
        run_file(args[0], env)
    else:
        env["args"] = []
        repl(env)


if __name__ == "__main__":
    main()
