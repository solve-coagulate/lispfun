# Lisp Toy Interpreter

The toy interpreter demonstrates how a complete Lisp system can be built in Lisp itself. It includes:

- `toy-tokenizer.lisp` – converts source text into tokens.
- `toy-parser.lisp` – builds lists and atoms from the token stream.
- `toy-evaluator.lisp` – evaluates expressions using a simple environment.

`toy-interpreter.lisp` loads these pieces and exposes helper functions such as `run-file` and a small REPL.

The evaluator supports `define-macro` so macros can be expanded when running code entirely in Lisp.

Run the interpreter with:

```bash
python -m lispfun examples/toy-interpreter.lisp
```

Inside the REPL you can execute scripts using `(run-file "path/to/file.lisp")`.
