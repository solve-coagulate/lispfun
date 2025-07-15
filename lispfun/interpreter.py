from functools import reduce
import operator as op
from typing import Any, List

Symbol = str
ListType = list


def tokenize(chars: str) -> List[str]:
    """Convert a string into a list of tokens."""
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def atom(token: str) -> Any:
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def read_from_tokens(tokens: List[str]) -> Any:
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def parse(program: str) -> Any:
    """Read a program into Python data structures."""
    return read_from_tokens(tokenize(program))


def parse_multiple(program: str) -> List[Any]:
    """Parse multiple expressions from a program string."""
    tokens = tokenize(program)
    expressions = []
    while tokens:
        expressions.append(read_from_tokens(tokens))
    return expressions


class Environment(dict):
    """An environment: a dict of {'var': val} pairs, with an optional outer env."""

    def __init__(self, params=(), args=(), outer=None):
        super().__init__(zip(params, args))
        self.outer = outer

    def find(self, var: Symbol) -> 'Environment':
        """Find the innermost Env where var appears."""
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            raise NameError(f"Undefined symbol: {var}")


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
        'symbol?': lambda x: isinstance(x, str),
        'apply': lambda f, args: f(*args),
        'map': lambda f, lst: [f(item) for item in lst],
    })
    # helpers for the self-hosted evaluator
    env.update({
        'env-get': lambda env, var: env.find(var)[var],
        'env-set!': lambda env, var, val: env.__setitem__(var, val),
        'make-procedure': Procedure,
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
        var, exp = args
        env[var] = eval_lisp(exp, env)
    elif op_ == 'set!':
        var, exp = args
        env.find(var)[var] = eval_lisp(exp, env)
    elif op_ == 'begin':
        val = None
        for exp in args:
            val = eval_lisp(exp, env)
        return val
    elif op_ == 'lambda':
        params, body = args
        return Procedure(params, body, env)
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


def to_string(exp: Any) -> str:
    if isinstance(exp, ListType):
        return '(' + ' '.join(map(to_string, exp)) + ')'
    else:
        return str(exp)
