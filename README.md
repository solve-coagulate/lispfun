# LispFun Overview

LispFun is a small Lisp interpreter written in Python with an increasing amount of functionality implemented in Lisp itself.  The project began with a minimal evaluator in Python and now includes a self-hosted evaluator written in Lisp.

## Completed Features

# <<<<<<< codex/ensure-toy-repl-example-works
1. **Bootstrap Interpreter (Python)**
   - Implement a small Lisp interpreter in Python capable of parsing and evaluating simple expressions: arithmetic operations, variable bindings, and function calls.
   - Include a REPL for quick experimentation.

2. **Testing Basic Programs**
   - Provide unit tests demonstrating that simple Lisp programs evaluate correctly.
   - Example programs: arithmetic computations, defining and calling functions.
   - A Lisp test script (`selftest.lisp`) returns 1 when all tests pass, allowing Python to verify functionality by running it through the Lisp evaluator.

3. **Self-hosted Evaluator (Lisp)**
   - Write a Lisp evaluator in Lisp, running on the Python interpreter.
   - The Lisp evaluator should support the same basic features as the Python version.

4. **Expanding Features in Lisp**
   - Add more language features implemented in Lisp: conditionals, lists, higher-order functions, and macros.
   - Gradually reduce Python's role to just parsing and initial bootstrapping.
  - Current progress: the Lisp evaluator now supports the `cond` form, `define-macro` for basic macros, Lisp implementations of `null?`, `length`, `map`, and `filter`, a simple `let` macro for local bindings, basic string literals, utilities like `parse-string`, `string-for-each`, and `build-string` for working with text, a `read-line` primitive for interactive input, and a Python-level `(import "file")` function for loading additional Lisp code.  The evaluator itself is split into multiple files that are loaded via `(import ...)` from `evaluator.lisp`.

4.5 **Testing Expanded Lisp Features**
   - Extend the test suite to exercise new Lisp features as they are added.
   - The `tests/lisp/selftest.lisp` script performs assertions for `cond`, macros, and higher-order list utilities such as `length`, `map`, and `filter`, returning `1` when they succeed.
   - Python tests run this script via the Lisp evaluator to ensure feature parity.

5. **Documentation and Examples**
   - Document usage of the interpreter and provide example Lisp programs.

6. **Future Ideas**
   - Explore self-hosting (running the interpreter written in Lisp using itself).
   - Consider building a small standard library in Lisp for common utilities.
   - See `IDEAS.md` for additional ideas to explore.
=======
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
# >>>>>>> main

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
# <<<<<<< codex/ensure-toy-repl-example-works
- `toy-interpreter.lisp` – illustrative Lisp interpreter written in Lisp.
  The interpreter's code now lives in `toy-tokenizer.lisp`, `toy-parser.lisp`,
  and `toy-evaluator.lisp`, which `toy-interpreter.lisp` loads via `(import ...)`.
- `toy-runner.lisp` – load the toy interpreter and run all other examples
-  This script exercises the toy interpreter by running each example file.
-  With comment parsing support you can now execute it directly:

```bash
python -m lispfun examples/toy-runner.lisp
```
- `toy-repl.lisp` – simple REPL built on the toy interpreter
=======
- `toy-interpreter.lisp` – illustrative interpreter in Lisp that loads `toy-tokenizer.lisp`, `toy-parser.lisp` and `toy-evaluator.lisp`
- `toy-runner.lisp` – run every example using the toy interpreter
- `toy-repl.lisp` – a minimal REPL built on the toy interpreter
- `run-tests.lisp` – execute all test scripts in `tests/lisp`
# >>>>>>> main

### Toy Interpreter Usage

To experiment directly with the interpreter written in Lisp:

```bash
python -m lispfun examples/toy-interpreter.lisp
; once inside the REPL
(run-file "examples/factorial.lisp")
```

The helper `read-file` function reads a file into a string and is used by `run-file`.

## Self-hosted Evaluator Details

`evaluator.lisp` loads helper modules such as `list_utils.lisp`, `string_utils.lisp` and `eval_core.lisp`.  `load_eval` in `lispfun/run.py` reads this entry file so the evaluator can run in the Python environment.  Expressions are executed by calling `eval_with_eval2`, which invokes the Lisp function `eval2` defined in `eval_core.lisp`.

## Work Remaining

Python still handles tokenizing and parsing in `interpreter.py`.  The long term goal is to move these pieces to Lisp.  `docs/pure_lisp_plan.md` contains a checklist for building a tokenizer and reader in Lisp.  See `IDEAS.md` for additional future enhancements such as loop constructs, modules and full self-hosting.

