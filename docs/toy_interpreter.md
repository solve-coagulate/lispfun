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
The `(require "file.lisp")` form loads a Lisp file only once so modules aren't
imported multiple times.

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
