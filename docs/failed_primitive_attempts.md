# Failed Primitive Attempts

This note documents experiments to replace the remaining host provided
primitives with Lisp equivalents. Several attempts caused the interpreter
or tests to hang, so the changes were reverted.

## Environment helpers

A Lisp implementation of `env-get`, `env-set!` and `make-procedure` was
sketched. These functions manipulate the interpreter environment directly
from Python. When replaced with Lisp versions, bootstrapping failed
because the evaluator depends on these helpers before it is fully loaded.
The interpreter would loop indefinitely while importing modules. A more
careful staged boot process might avoid the issue but has not been
worked out yet.

## String helpers

`string-slice`, `string-concat` and `make-string` were also tried in
Lisp using simple loops over indices. Simple programs worked but the
interpreter later produced corrupted strings and some tests timed out.
The naive implementations are likely too inefficient and may interact
poorly with other parts of the system.

The host implementations have been restored until a more robust approach
can be designed.

## File I/O

`read-file` and `read-line` were attempted in Lisp using simple string accumulation and looping over `(read-char)` from an input port. However reading from the filesystem ultimately relies on Python file handles, so the Lisp versions still needed host primitives for the actual data retrieval. Until the interpreter gains a Lisp-level file abstraction that can delegate to the host, these remain implemented in Python.
