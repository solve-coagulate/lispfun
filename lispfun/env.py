from __future__ import annotations
from .parser import Symbol

class Environment(dict):
    """An environment: a dict of {'var': val} pairs, with an optional outer env."""

    def __init__(self, params=(), args=(), outer: 'Environment | None' = None) -> None:
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
