from __future__ import annotations
from typing import Any, List

class Symbol(str):
    """Represents a Lisp symbol."""
    pass


class String(str):
    """Represents a Lisp string literal."""
    pass

ListType = list


def tokenize(chars: str) -> List[str]:
    """Convert a string into a list of tokens, keeping string literals intact."""
    tokens = []
    token = ''
    in_string = False
    i = 0
    while i < len(chars):
        c = chars[i]
        if in_string:
            token += c
            if c == '"':
                tokens.append(token)
                token = ''
                in_string = False
        else:
            if c.isspace():
                if token:
                    tokens.append(token)
                    token = ''
            elif c == '(' or c == ')':
                if token:
                    tokens.append(token)
                    token = ''
                tokens.append(c)
            elif c == '"':
                if token:
                    tokens.append(token)
                    token = ''
                token = '"'
                in_string = True
            else:
                token += c
        i += 1
    if token:
        tokens.append(token)
    return tokens


def atom(token: str) -> Any:
    """Numbers become numbers; quoted tokens become strings; everything else is a symbol."""
    if token.startswith('"') and token.endswith('"'):
        return String(token[1:-1])
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


def to_string(exp: Any) -> str:
    if isinstance(exp, ListType):
        return '(' + ' '.join(map(to_string, exp)) + ')'
    elif isinstance(exp, String):
        return '"' + str(exp) + '"'
    else:
        return str(exp)
