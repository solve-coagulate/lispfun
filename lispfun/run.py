import os
import sys
from .bootstrap.interpreter import (
    parse, parse_multiple, eval_lisp, standard_env, to_string,
)

# Enable command history and up-arrow navigation if readline is available
try:
    import readline  # type: ignore
    import atexit

    HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".lispfun_history")
    readline.parse_and_bind("tab: complete")
    try:
        readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError:
        pass
    atexit.register(readline.write_history_file, HISTORY_FILE)
except Exception:  # pragma: no cover - optional enhancement
    readline = None  # fallback when readline isn't available

EVAL_FILE = os.path.join(os.path.dirname(__file__), "hosted", "evaluator.lisp")
TOY_FILE = os.path.join(os.path.dirname(__file__), "..", "toy", "toy-interpreter.lisp")


def load_eval(env):
    with open(EVAL_FILE) as f:
        code = f.read()
    for exp in parse_multiple(code):
        eval_lisp(exp, env)
    env["env"] = env


def load_toy(env):
    """Load the toy interpreter implemented in Lisp."""
    with open(TOY_FILE) as f:
        code = f.read()
    for exp in parse_multiple(code):
        eval_with_eval2(exp, env)


def eval_with_eval2(exp, env):
    program = f"(eval2 (quote {to_string(exp)}) env)"
    return eval_lisp(parse(program), env)


def toy_run_file(filename, env):
    """Execute a Lisp script using the toy interpreter."""
    load_toy(env)
    program = parse(f'(run-file "{filename}")')
    return eval_with_eval2(program, env)


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
            if readline:
                readline.add_history(line)
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
        toy_run_file(sys.argv[1], env)
    else:
        repl(env)


if __name__ == "__main__":
    main()
