# LispFun Overview

LispFun is a small Lisp interpreter written in Python with an increasing amount of functionality implemented in Lisp itself. The project began with a minimal evaluator in Python and now includes a self-hosted evaluator written in Lisp.

The repository now separates the main components for clarity:

- `lispfun/bootstrap` contains the Python interpreter used for bootstrapping.
- `lispfun/hosted` holds the Lisp code implementing the `eval2` evaluator.
- `toy/` provides a pure Lisp toy interpreter.

## Completed Features

 - **Python bootstrap interpreter** with a REPL, a very small parser and the
   minimal operations required to get Lisp code running.  It offers separate
   `kernel_env` and `kernel_parser_env` functions exposing only the primitives
   and parser helpers needed for bootstrapping.  `run_bootstrap.py` accepts a
   `--kernel` flag to start in these restricted environments.  The full
   environment still provides list utilities `null?`, `length`, `map` and
   `filter`.
 - **Self-hosted evaluator** written in Lisp loaded by `run_hosted.py` via `(import ...)`.
 - `load_eval` now processes imports itself when `import` is undefined so the
   evaluator boots even in the minimal `kernel_env`.
 - The minimal `kernel_env` exposes `list?`, `symbol?`, `env-get`, `env-set!`
   and `make-procedure` primitives required by `eval2` so the hosted evaluator
   can run without enabling `import` or other convenience functions.
- Lisp features implemented in Lisp:
  - `cond` form and `define-macro` for simple macros.
  - List utilities: `null?`, `length`, `map` and `filter`.
  - String helpers: `parse-string`, `string-for-each`, `build-string`.
  - Predicates `number?` and `string?` for identifying literal types.
  - `read-line` primitive for interactive input.
  - Toy REPL prints evaluation results and accepts `'bye` as a shortcut to exit.
  - `(import "file")` for loading additional Lisp code.
  - Toy interpreter supports `define-macro` so macros work when running example scripts.
  - `lambda` forms now allow multiple expressions in the body.
  - Loop macros `while` and `for` allow simple iterative code in the toy interpreter.
  - Toy interpreter now parses string literals.
  - Semicolon comments are recognized by the parser.
  - Command line arguments after the script name are available as the `args` list.
  - `(require "file")` loads Lisp files once to support a basic module system.
  - `(error "msg")` raises an exception and `(trap-error thunk handler)`
    invokes `handler` with the message if evaluating `thunk` fails.
- Example scripts demonstrate factorials, Fibonacci numbers, list processing, macros and loops.
- A comprehensive unit test suite with Lisp programs stored alongside each interpreter.

## Bootstrapping vs Self-Hosting

`run_bootstrap.py` always launches the initial Python implementation.  It reads
`evaluator.lisp` and loads `eval2` into the environment.  Once `eval2` is
available the interpreter can evaluate its own source code purely in Lisp.  This
ability to execute itself is what we call *self&#8209;hosting*.  Python remains
responsible for parsing and starting the system, but after bootstrapping all
evaluation is handled by Lisp code.

## Documentation

Separate documents describe each interpreter:

- [Python bootstrap interpreter](docs/bootstrap_interpreter.md)
- [Self-hosted evaluator](docs/self_hosted_evaluator.md)
- [Lisp toy interpreter](docs/toy_interpreter.md)

## Running the Interpreter

There are several helper scripts for running LispFun depending on how much Lisp code
you wish to bootstrap:

```bash
./run_bootstrap.py [--kernel] [file]   # pure Python interpreter
./run_hosted.py [--kernel] [file]      # load evaluator.lisp and use eval2
./run_toy.py [file]         # load evaluator and toy interpreter (toy REPL)
```
Each script is executable so you can invoke it directly from the shell.
Pass the optional ``--kernel`` flag to start either interpreter in the
minimal ``kernel_env`` instead of the full ``standard_env``.

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

You can also feed a single expression to the toy interpreter by piping it
directly into `run_toy.py`. The program will execute the input and exit
when it reaches end-of-file:

```bash
./run_toy.py <<< '(print "hi")'
```

A small helper script `run_hi.sh` demonstrates the same idea (no `toy>` prompt
because it is not running the interactive REPL):

```bash
./run_hi.sh
# => hi
```

When launched without a file and an interactive terminal is attached,
`run_toy.py` starts the toy REPL implemented in Lisp. If standard input is redirected it
executes the provided code instead of starting the REPL.  A quick REPL
session looks like this:

```bash
$ ./run_toy.py
toy> (print "hi")
hi
toy>
```

Running without a file starts a REPL. `run_bootstrap.py` and `run_hosted.py`
launch the Python REPL, while `run_toy.py` starts a REPL executed by the toy
interpreter itself. The previous Python implementation of the REPL is still
available as the `python_toy_repl` function in `run_toy.py` for debugging or
experimentation.
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
./run_hosted.py examples/hosted-tests.lisp
```
- `toy-tests.lisp` – run tests for the toy interpreter:

```bash
./run_toy.py examples/toy-tests.lisp
```

The helper scripts load progressively more Lisp code. `run_bootstrap.py`
only supports programs that work with the Python evaluator so it fails on
the hosted and toy example tests. `run_hosted.py` adds the self-hosted
evaluator and runs both the bootstrap and hosted tests, while `run_toy.py`
runs them all. The new tests under `examples/tests` exercise this behaviour.
Run `./run_example_tests.sh` from the repository root to try each interpreter on the example test suites.


## Work Remaining

Python still handles tokenizing and parsing in `interpreter.py`. The long term goal is to move these pieces to Lisp. See `toy/IDEAS.md` for additional future enhancements like full self-hosting and improved debugging.

