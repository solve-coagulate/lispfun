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

# helpers for error handling
def _trap_error(thunk, handler):
    try:
        return thunk()
    except Exception as e:
        return handler(str(e))

from .parser import (
    Symbol,
    String,
    ListType,
    parse,
    parse_multiple,
    to_string,
)
from .env import Environment


def kernel_env() -> Environment:
    """Return the minimal environment used during bootstrapping."""
    env = Environment()
    env.update({
        '+': lambda *x: sum(x),
        '-': lambda x, *rest: x - sum(rest) if rest else -x,
        '*': lambda *x: reduce(op.mul, x, 1),
        '/': lambda x, y: x / y,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'print': print,
        'list': lambda *x: list(x),
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'apply': lambda f, args: (
            eval_lisp(f.body, Environment(f.params, args, f.env))
            if isinstance(f, Procedure)
            else f(*args)
        ),
        'list?': lambda x: isinstance(x, list),
        'symbol?': lambda x: isinstance(x, Symbol),
        'env-get': lambda env, var: env.find(var)[var],
        'env-set!': lambda env, var, val: env.__setitem__(var, val),
        'make-procedure': Procedure,
    })
    return env


def standard_env() -> Environment:
    env = kernel_env()
    env.update({
        'abs': abs,
        'max': max,
        'min': min,
        # error handling primitives
        'error': lambda msg: (_ for _ in ()).throw(RuntimeError(str(msg))),
        'trap-error': lambda thunk, handler: _trap_error(thunk, handler),
        'list?': lambda x: isinstance(x, list),
        'null?': lambda x: x == [],
        'length': lambda lst: len(lst),
        'symbol?': lambda x: isinstance(x, Symbol),
        'number?': lambda x: isinstance(x, (int, float)),
        'string?': lambda x: isinstance(x, str),
        'map': lambda f, lst: [f(item) for item in lst],
        'filter': lambda pred, lst: [item for item in lst if pred(item)],
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
    """Evaluate an expression in an environment using an explicit stack."""
    task_stack: List[tuple] = [('eval', x, env)]
    value_stack: List[Any] = []

    while task_stack:
        op_, *data = task_stack.pop()

        if op_ == 'eval':
            expr, env = data
            if isinstance(expr, Symbol):
                value_stack.append(env.find(expr)[expr])
            elif isinstance(expr, String):
                value_stack.append(str(expr))
            elif not isinstance(expr, ListType):
                value_stack.append(expr)
            else:
                operator, *args = expr
                if operator == 'quote':
                    value_stack.append(args[0])
                elif operator == 'if':
                    test, conseq, alt = args
                    task_stack.append(('if-branch', conseq, alt, env))
                    task_stack.append(('eval', test, env))
                elif operator == 'define':
                    if len(args) < 2:
                        raise ValueError(
                            f'define expects at least 2 arguments, got {len(args)}: {args}'
                        )
                    var, exp, *rest = args
                    task_stack.append(('define-after', var, rest, env))
                    task_stack.append(('eval', exp, env))
                elif operator == 'set!':
                    var, exp = args
                    task_stack.append(('set-after', var, env))
                    task_stack.append(('eval', exp, env))
                elif operator == 'begin':
                    if not args:
                        value_stack.append(None)
                    else:
                        task_stack.append(('begin-next', args[1:], env))
                        task_stack.append(('eval', args[0], env))
                elif operator == 'cond':
                    task_stack.append(('cond-clauses', args, env))
                elif operator == 'let':
                    bindings, *body = args
                    vars = [var for var, _ in bindings]
                    exps = [exp for _, exp in bindings]
                    task_stack.append(('let-bindings', vars, body, env, len(exps)))
                    for b in reversed(exps):
                        task_stack.append(('eval', b, env))
                elif operator == 'lambda':
                    params, *body = args
                    body_expr = body[0] if len(body) == 1 else ['begin'] + list(body)
                    value_stack.append(Procedure(params, body_expr, env))
                else:
                    task_stack.append(('apply', len(args)))
                    for a in reversed(args):
                        task_stack.append(('eval', a, env))
                    task_stack.append(('eval', operator, env))

        elif op_ == 'if-branch':
            conseq, alt, env = data
            condition = value_stack.pop()
            task_stack.append(('eval', conseq if condition else alt, env))

        elif op_ == 'define-after':
            var, rest, env = data
            val = value_stack.pop()
            env[var] = val
            if rest:
                task_stack.append(('begin-next', rest[1:], env))
                task_stack.append(('eval', rest[0], env))
            else:
                value_stack.append(val)

        elif op_ == 'set-after':
            var, env = data
            val = value_stack.pop()
            env.find(var)[var] = val
            value_stack.append(None)

        elif op_ == 'begin-next':
            rest, env = data
            last_val = value_stack.pop()
            if not rest:
                value_stack.append(last_val)
            else:
                task_stack.append(('begin-next', rest[1:], env))
                task_stack.append(('eval', rest[0], env))

        elif op_ == 'cond-clauses':
            clauses, env = data
            if not clauses:
                value_stack.append(None)
            else:
                clause = clauses[0]
                rest = clauses[1:]
                test, *body = clause
                if test == 'else':
                    if not body:
                        value_stack.append(None)
                    else:
                        task_stack.append(('begin-next', body[1:], env))
                        task_stack.append(('eval', body[0], env))
                else:
                    task_stack.append(('cond-decision', body, rest, env))
                    task_stack.append(('eval', test, env))

        elif op_ == 'cond-decision':
            body, rest, env = data
            test_val = value_stack.pop()
            if test_val:
                if not body:
                    value_stack.append(test_val)
                else:
                    task_stack.append(('begin-next', body[1:], env))
                    task_stack.append(('eval', body[0], env))
            else:
                task_stack.append(('cond-clauses', rest, env))

        elif op_ == 'let-bindings':
            vars, body, env, count = data
            values = [value_stack.pop() for _ in range(count)][::-1]
            local_env = Environment(vars, values, env)
            if not body:
                value_stack.append(None)
            else:
                expr = body[0] if len(body) == 1 else ['begin'] + body
                task_stack.append(('eval', expr, local_env))

        elif op_ == 'apply':
            count = data[0]
            args = [value_stack.pop() for _ in range(count)][::-1]
            proc = value_stack.pop()
            if isinstance(proc, Procedure):
                task_stack.append(('eval', proc.body, Environment(proc.params, args, proc.env)))
            else:
                value_stack.append(proc(*args))

        else:
            raise ValueError(f'Unknown task {op_}')

    return value_stack.pop() if value_stack else None


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


