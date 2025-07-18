# LispFun

LispFun is a tiny Lisp system.  The Python code supplies only a very small
bootstrap kernel able to load and run Lisp code.  This kernel is purposely kept
minimal—yet still Turing complete—so a Lisp bootstrap interpreter can build the
rest of the system.  A bootstrap interpreter written in Lisp uses this kernel to
construct the full evaluator so it can eventually run itself.  Everything else,
including the main evaluator and a small toy interpreter, lives in Lisp.

The repository layout is simple:

- `lispfun/bootstrap` – Python bootstrap kernel
- `lispfun/hosted` – Lisp files for the self‑hosted evaluator
- `toy/` – toy interpreter written entirely in Lisp
- `examples/` – sample programs exercising the interpreters
- `docs/` – additional documentation

Helper scripts in the repository root run the different interpreters:


```bash
./run_bootstrap.py [--kernel] [file]
./run_hosted.py   [--kernel] [file]
./run_toy.py      [file]
```

Pass `--kernel` to start in the restricted bootstrap environment.  See the
individual documents under `docs/` and `lispfun/README.md` for full usage and
development notes.

The toy interpreter is now completely self-hosted.  It ships with a tokenizer
and parser written in Lisp so programs run without using the Python parser once
bootstrapped.  In addition to `<=`, `>=`, `abs`, `max`, `min` and a Lisp version
of `apply`, several primitives from the Python environment are now
reimplemented purely in Lisp:

- `null?` – check for the empty list
- `length` – compute list length
- `map` – apply a function to each element
- `filter` – select elements matching a predicate
# <<<<<<< codex/document-unimplemented-environment-functions-in-toy-interpre
- `string-length` – compute the length of a string
- `digits->number` – convert a string of digits to a number
- `number?` – check if a value is numeric
- `string?` – check if a value is a string
- Numeric helpers `<=`, `>=`, `abs`, `max` and `min`

The remaining host-provided primitives are:
- low level string helpers `string-slice`, `string-concat`, `make-string`,
  `char-code` and `chr`
- type predicates `symbol?` and `list?`
- symbol utility `make-symbol`
- environment helpers `env-get`, `env-set!` and `make-procedure`
- file I/O primitives `read-file` and `read-line`
# =======

String operations and type predicates (`number?`, `string?`, `symbol?`,
`list?`), along with file I/O, still rely on the Python runtime.  The
`string?` predicate now only matches actual string literals so symbols
are evaluated correctly by the toy interpreter.

The Lisp parser includes basic error reporting so malformed input is handled
gracefully inside the toy REPL without relying on Python exceptions.
The tokenizer also now returns proper symbol objects so the REPL evaluates
identifiers correctly when using the toy parser.
# >>>>>>> main
