# LispFun Overview

LispFun is a small Lisp interpreter written in Python with an increasing amount of functionality implemented in Lisp itself.  The project began with a minimal evaluator in Python and now includes a self-hosted evaluator written in Lisp.

## Completed Features

- **Python bootstrap interpreter** with a REPL and basic arithmetic, variables and functions.
- **Self-hosted evaluator** written in Lisp loaded by `run.py` via `(import ...)`.
- Lisp features implemented in Lisp:
  - `cond` form and `define-macro` for simple macros.
  - List utilities: `null?`, `length`, `map` and `filter`.
  - String helpers: `parse-string`, `string-for-each`, `build-string`.
  - `read-line` primitive for interactive input.
  - `(import "file")` for loading additional Lisp code.
- Semicolon comments are recognized by the parser.
- Example scripts demonstrate factorials, Fibonacci numbers, list processing and macros.
- A comprehensive unit test suite including a `selftest.lisp` script executed by the evaluator.

## Documentation

Separate documents describe each interpreter:

- [Python bootstrap interpreter](docs/bootstrap_interpreter.md)
- [Self-hosted evaluator](docs/self_hosted_evaluator.md)
- [Lisp toy interpreter](docs/toy_interpreter.md)

## Running the Interpreter

From the repository root use Python's `-m` switch so package imports resolve correctly:

```bash
python -m lispfun [path/to/script.lisp]
```

Running without a file starts the REPL.  When a script path is supplied the toy interpreter written in Lisp is loaded and its `run-file` function executes the program.

History support is enabled if the `readline` module is available.

## Example Programs

Example scripts live in the `examples` directory and can be run with:

```bash
python -m lispfun examples/<script>.lisp
```

Available scripts include:

- `factorial.lisp` – recursive factorial calculation
- `fibonacci.lisp` – compute Fibonacci numbers
- `list-demo.lisp` – demonstrate list utilities
- `macro-example.lisp` – use a simple `when` macro
- `toy-interpreter.lisp` – illustrative Lisp interpreter written in Lisp.
  See [docs/toy_interpreter.md](docs/toy_interpreter.md) for usage.
- `toy-runner.lisp` – load the toy interpreter and run all other examples.
  This script exercises the toy interpreter by running each example file.
  With comment parsing support you can execute it directly:

```bash
python -m lispfun examples/toy-runner.lisp
```
- `toy-repl.lisp` – simple REPL built on the toy interpreter. Run it with:

```bash
python -m lispfun examples/toy-repl.lisp
```
- `run-tests.lisp` – defines a `run-test` helper and runs each script in `tests/lisp`


## Work Remaining

Python still handles tokenizing and parsing in `interpreter.py`.  The long term goal is to move these pieces to Lisp.  `docs/pure_lisp_plan.md` contains a checklist for building a tokenizer and reader in Lisp.  See `IDEAS.md` for additional future enhancements such as loop constructs, modules and full self-hosting.

