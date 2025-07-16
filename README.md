# LispFun Overview

LispFun is a small Lisp interpreter written in Python with an increasing amount of functionality implemented in Lisp itself. The project began with a minimal evaluator in Python and now includes a self-hosted evaluator written in Lisp.

The repository now separates the main components for clarity:

- `lispfun/bootstrap` contains the Python interpreter used for bootstrapping.
- `lispfun/hosted` holds the Lisp code implementing the `eval2` evaluator.
- `toy/` provides a pure Lisp toy interpreter.

## Completed Features

- **Python bootstrap interpreter** with a REPL, basic arithmetic, variables and functions. The environment now provides built-in list utilities `null?`, `length`, `map` and `filter`.
- **Self-hosted evaluator** written in Lisp loaded by `run.py` via `(import ...)`.
- Lisp features implemented in Lisp:
  - `cond` form and `define-macro` for simple macros.
  - List utilities: `null?`, `length`, `map` and `filter`.
  - String helpers: `parse-string`, `string-for-each`, `build-string`.
  - Predicates `number?` and `string?` for identifying literal types.
  - `read-line` primitive for interactive input.
  - `(import "file")` for loading additional Lisp code.
  - Toy interpreter supports `define-macro` so macros work when running example scripts.
  - Loop macros `while` and `for` allow simple iterative code in the toy interpreter.
  - Toy interpreter now parses string literals.
  - Semicolon comments are recognized by the parser.
  - Command line arguments after the script name are available as the `args` list.
  - `(require "file")` loads Lisp files once to support a basic module system.
- Example scripts demonstrate factorials, Fibonacci numbers, list processing, macros and loops.
- A comprehensive unit test suite with Lisp programs stored alongside each interpreter.

## Documentation

Separate documents describe each interpreter:

- [Python bootstrap interpreter](docs/bootstrap_interpreter.md)
- [Self-hosted evaluator](docs/self_hosted_evaluator.md)
- [Lisp toy interpreter](docs/toy_interpreter.md)

## Running the Interpreter

There are several helper scripts for running LispFun depending on how much Lisp code
you wish to bootstrap:

```bash
./run_bootstrap.py [file]   # pure Python interpreter
./run_hosted.py [file]      # load evaluator.lisp and use eval2
./run_toy.py [file]         # load evaluator and toy interpreter (toy REPL)
```
Each script is executable so you can invoke it directly from the shell.

You can also pipe a short snippet into the toy interpreter by passing
`/dev/stdin` as the file path:

```bash
echo '(print "hi")' | ./run_toy.py /dev/stdin
```

A here-document works as well:

```bash
cat <<'EOF' | ./run_toy.py /dev/stdin
(print "hi")
EOF
```

To send input to the toy REPL itself, run the REPL script and pipe a
string or here-document into standard input. The REPL now exits cleanly
when it reaches end-of-file:

```bash
./run_toy.py toy/toy-repl.lisp <<< '(print "hi")'
```

When running without a file, `run_toy.py` starts a minimal REPL that only
prints the result of side-effecting operations like `print`.

Running without a file starts a REPL. `run_bootstrap.py` and `run_hosted.py`
launch the Python REPL, while `run_toy.py` starts the toy REPL written in Lisp.
`python -m lispfun` behaves like `run_hosted.py` but only loads the toy
interpreter when executing a file. History support is enabled if the `readline`
module is available.

Any arguments provided after the script name are stored in the `args` variable
within the Lisp environment so scripts can access their command line parameters.

The interpreters are now organized as separate applications. The bootstrap
Python interpreter lives in `run_bootstrap.py`, the hosted evaluator is started
with `run_hosted.py`, and the toy interpreter sources reside in the `toy/`
directory and are launched via `run_toy.py`.

## Example Programs

Example scripts live in the `examples` directory and can be run with:

```bash
python -m lispfun examples/<script>.lisp
```

Available scripts include:

- `factorial.lisp` – recursive factorial calculation
- `fibonacci.lisp` – compute Fibonacci numbers
- `list-demo.lisp` – demonstrate list utilities
- `loop-demo.lisp` – illustrate `while` and `for` macros
- `macro-example.lisp` – use a simple `when` macro
- `toy-interpreter.lisp` – illustrative Lisp interpreter written in Lisp. See [docs/toy_interpreter.md](docs/toy_interpreter.md) for usage.
- `toy-runner.lisp` – load the toy interpreter and run all other examples.
  This script exercises the toy interpreter by running each example file.
  With comment parsing support you can execute it directly:

```bash
python -m lispfun toy/toy-runner.lisp
```
- `toy-repl.lisp` – simple REPL built on the toy interpreter. Run it with:

```bash
python -m lispfun toy/toy-repl.lisp
```
- `bootstrap-tests.lisp` – run Lisp unit tests for the bootstrap interpreter:

```bash
./run_bootstrap.py examples/bootstrap-tests.lisp
```
- `hosted-tests.lisp` – run tests using the self-hosted evaluator:

```bash
python -m lispfun examples/hosted-tests.lisp
```
- `toy-tests.lisp` – run tests for the toy interpreter:

```bash
./run_toy.py examples/toy-tests.lisp
```


## Work Remaining

Python still handles tokenizing and parsing in `interpreter.py`. The long term goal is to move these pieces to Lisp. See `toy/IDEAS.md` for additional future enhancements such as a module system and full self-hosting.

