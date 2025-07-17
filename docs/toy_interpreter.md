# Lisp Toy Interpreter

The toy interpreter demonstrates how a complete Lisp system can be built in Lisp itself. It includes:

- `toy-tokenizer.lisp` – converts source text into tokens.
- `toy-parser.lisp` – builds lists and atoms from the token stream.
- `toy-evaluator.lisp` – evaluates expressions using a simple environment.

`toy-interpreter.lisp` loads these pieces and exposes helper functions such as `run-file` and a small REPL. String literals are recognized so `(print "hi")` works as expected.

The evaluator supports `define-macro` so macros can be expanded when running code entirely in Lisp.

`toy-evaluator.lisp` also defines simple `while` and `for` macros so iterative
loops can be written without modifying the evaluator.

Basic predicates `number?` and `string?` are available and the tokenizer handles
quoted strings.
Additional helpers like `<=`, `>=`, `abs`, `max`, `min` and a Lisp
implementation of `apply` further reduce the reliance on Python.  Common string
utilities such as `string-length`, `string-slice`, `string-concat`,
`make-string`, `char-code`, `chr`, `make-symbol` and `digits->number` are now
provided directly from Lisp as simple wrappers. The interpreter still depends on
the host for low level I/O and environment manipulation.

Currently the following primitives are defined in Lisp:

- arithmetic operators `+`, `-`, `*`, `/`, comparisons and `apply`
- list helpers like `null?`, `length`, `map`, `filter`, `append`
- control flow macros `while` and `for`
- module loader `(require path)`
- string helpers `string-length`, `string-slice`, `string-concat`,
  `make-string`, `char-code`, `chr`, `make-symbol`, `digits->number`

Python still supplies the underlying string and file operations as well as
`read-line` and environment manipulation.
The `(require "file.lisp")` form loads a Lisp file only once so modules aren't
imported multiple times.
`(error "msg")` raises an exception and `(trap-error thunk handler)` can be
used to recover from runtime errors.

Example:

```lisp
(define n 3)
(define total 0)
(for i 1 n
  (set! total (+ total i)))
(print total) ; => 6
```

Run the interpreter with:

```bash
python -m lispfun toy/toy-interpreter.lisp [args...]
```
Arguments after the file name are stored in the `args` list for use by the Lisp
program. Inside the REPL you can execute scripts using `(run-file "path/to/file.lisp")`.
