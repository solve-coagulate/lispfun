import os
import sys
from .interpreter import (
    parse, parse_multiple, eval_lisp, standard_env, to_string
)

EVAL_FILE = os.path.join(os.path.dirname(__file__), "evaluator.lisp")


def load_eval(env):
    with open(EVAL_FILE) as f:
        code = f.read()
    for exp in parse_multiple(code):
        eval_lisp(exp, env)
    env["env"] = env


def eval_with_eval2(exp, env):
    program = f"(eval2 (quote {to_string(exp)}) env)"
    return eval_lisp(parse(program), env)


def run_file(filename, env):
    with open(filename) as f:
        code = f.read()
    exprs = parse_multiple(code)
    result = None
    for exp in exprs:
        result = eval_with_eval2(exp, env)
    return result


def repl(env):
    while True:
        try:
            line = input("lispfun> ")
            if not line:
                continue
            exp = parse(line)
            val = eval_with_eval2(exp, env)
            if val is not None:
                print(to_string(val))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    env = standard_env()
    load_eval(env)
    if len(sys.argv) > 1:
        run_file(sys.argv[1], env)
    else:
        repl(env)


if __name__ == "__main__":
    main()
