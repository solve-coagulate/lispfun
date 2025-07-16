from functools import reduce
import operator as op
from typing import Any, List


def read_file(fname: str) -> str:
    """Return the contents of *fname* as a string."""
    with open(str(fname)) as f:
        return f.read()


def _read_line(prompt: str = "") -> str:
    """Read a line from stdin, returning an empty string on EOF."""
    try:
        return input(prompt)
    except EOFError:
        return ""

from .parser import (
    Symbol,
    String,
    ListType,
    parse,
    parse_multiple,
    to_string,
)
from .env import Environment


def standard_env() -> Environment:
    env = Environment()
    env.update({
        "+": lambda *x: sum(x),
        "-": lambda x, *rest: x - sum(rest) if rest else -x,
        "*": lambda *x: reduce(op.mul, x, 1),
        '/': lambda x, y: x / y,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'max': max,
        'min': min,
        'print': print,
        # list utilities
        'list': lambda *x: list(x),
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'list?': lambda x: isinstance(x, list),
        'symbol?': lambda x: isinstance(x, Symbol),
        'number?': lambda x: isinstance(x, (int, float)),
        'string?': lambda x: isinstance(x, str),
        'apply': lambda f, args: f(*args),
        'map': lambda f, lst: [f(item) for item in lst],
        'read-file': read_file,
        'read-line': _read_line,
        # string utilities
        'string-length': len,
        'string-slice': lambda s, start, end: s[start:end],
        'string-concat': lambda a, b: a + b,
        'make-string': String,
        'char-code': lambda s: ord(s[0]),
        'chr': chr,
        # primitives used by Lisp parsing code
        'make-symbol': lambda name: Symbol(str(name)),
        'digits->number': lambda s: int(s) if '.' not in s else float(s),
    })
    # helpers for the self-hosted evaluator
    env.update({
        'env-get': lambda env, var: env.find(var)[var],
        'env-set!': lambda env, var, val: env.__setitem__(var, val),
        'make-procedure': Procedure,
    })
    # ability to load additional Lisp files
    def import_file(fname: str):
        with open(str(fname)) as f:
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

    env.update({
        'import': import_file,
    })
    return env


class Procedure:
    """A user-defined Scheme procedure."""

    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        local_env = Environment(self.params, args, self.env)
        return eval_lisp(self.body, local_env)


global_env = standard_env()


def eval_lisp(x: Any, env: Environment = global_env) -> Any:
    """Evaluate an expression in an environment."""
    if isinstance(x, Symbol):
        return env.find(x)[x]
    elif isinstance(x, String):
        return str(x)
    elif not isinstance(x, ListType):
        return x
    op_, *args = x
    if op_ == 'quote':
        (exp,) = args
        return exp
    elif op_ == 'if':
        test, conseq, alt = args
        exp = (conseq if eval_lisp(test, env) else alt)
        return eval_lisp(exp, env)
    elif op_ == 'define':
        if len(args) < 2:
            raise ValueError(f'define expects at least 2 arguments, got {len(args)}: {args}')
        var, exp, *rest = args
        env[var] = eval_lisp(exp, env)
        val = None
        for extra in rest:
            val = eval_lisp(extra, env)
        return val
    elif op_ == 'set!':
        var, exp = args
        env.find(var)[var] = eval_lisp(exp, env)
    elif op_ == 'begin':
        val = None
        for exp in args:
            val = eval_lisp(exp, env)
        return val
    elif op_ == 'cond':
        for clause in args:
            test, expr = clause
            if test == 'else' or eval_lisp(test, env):
                return eval_lisp(expr, env)
        return None
    elif op_ == 'let':
        bindings, *body = args
        vars = [var for var, _ in bindings]
        vals = [eval_lisp(exp, env) for _, exp in bindings]
        local_env = Environment(vars, vals, env)
        val = None
        for exp in body:
            val = eval_lisp(exp, local_env)
        return val
    elif op_ == 'lambda':
        params, *body = args
        if len(body) == 1:
            body_expr = body[0]
        else:
            body_expr = ['begin'] + list(body)
        return Procedure(params, body_expr, env)
    else:
        proc = eval_lisp(op_, env)
        values = [eval_lisp(arg, env) for arg in args]
        return proc(*values)


def repl(prompt: str = 'lispy> '):
    """A prompt-read-eval-print loop."""
    while True:
        try:
            program = input(prompt)
            if not program:
                continue
            val = eval_lisp(parse(program))
            if val is not None:
                print(to_string(val))
        except (KeyboardInterrupt, EOFError):
            print()
            break
        except Exception as e:
            print(f"Error: {e}")


