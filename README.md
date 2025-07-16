# LispFun Development Plan

This repository aims to develop a minimal Lisp interpreter in Python and gradually transition its evaluation capabilities to Lisp itself.

## Tasks

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
  - Current progress: the Lisp evaluator now supports the `cond` form, `define-macro` for basic macros, Lisp implementations of `null?`, `length`, `map`, and `filter`, basic string literals, utilities like `parse-string`, `string-for-each`, and `build-string` for working with text, a `read-line` primitive for interactive input, and a Python-level `(import "file")` function for loading additional Lisp code.  The evaluator itself is split into multiple files that are loaded via `(import ...)` from `evaluator.lisp`.

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

## Running the Interpreter

Use Python's `-m` option from the repository root so that package imports resolve correctly:

```bash
python -m lispfun [path/to/script.lisp]
```

Running without a file starts an interactive REPL. Executing `run.py` directly
(`python lispfun/run.py`) will fail because it relies on relative imports.

The REPL supports command history if Python's `readline` module is available.
Use the up and down arrow keys to navigate through previous inputs, similar to
the bash shell.

The parser now understands semicolon comments, ignoring text from `;` to the end
of a line. This lets example files include explanatory comments without causing
parse errors.

## Example Programs

Several small example scripts live in the `examples` directory. Run them with

```bash
python -m lispfun examples/<script>.lisp
```

Available scripts:

- `factorial.lisp` – recursive factorial calculation
- `fibonacci.lisp` – compute Fibonacci numbers
- `list-demo.lisp` – demonstrate `length`, `map` and `filter`
- `macro-example.lisp` – use a simple `when` macro
- `toy-interpreter.lisp` – illustrative Lisp interpreter written in Lisp.
  The interpreter's code now lives in `toy-tokenizer.lisp`, `toy-parser.lisp`,
  and `toy-evaluator.lisp`, which `toy-interpreter.lisp` loads via `(import ...)`.
- `toy-runner.lisp` – load the toy interpreter and run all other examples
# <<<<<<< codex/get-toy-runner-example-running-on-eval2
  This script exercises the toy interpreter by running each example file.
  With comment parsing support you can now execute it directly:

```bash
python -m lispfun examples/toy-runner.lisp
```
=======
- `toy-repl.lisp` – simple REPL built on the toy interpreter
- `run-tests.lisp` – run all test scripts in `tests/lisp`
# >>>>>>> main

### Toy Interpreter Usage

Run the Lisp-based interpreter itself and then use `run-file` to execute other
examples:

```bash
python -m lispfun examples/toy-interpreter.lisp
; now inside the REPL
(run-file "examples/factorial.lisp")
```

The helper `read-file` function is available to slurp a file's contents as a
string, which `run-file` relies on.

`toy-repl.lisp` uses the new `read-line` primitive to provide a minimal REPL:

```bash
python -m lispfun examples/toy-repl.lisp
```

## Self-hosted Evaluator

The self-hosted interpreter now spans several Lisp files in the `lispfun/` directory.  The entry point `evaluator.lisp` loads helper modules using the Lisp `(import ...)` function.  `load_eval` in `lispfun/run.py` reads this entry file so that the Lisp evaluator can run within the Python environment.  Expressions are then executed by calling `eval_with_eval2`, which invokes the Lisp function `eval2` defined in `eval_core.lisp` rather than Python's `eval_lisp`.

List utilities live in `list_utils.lisp` and string helpers such as `parse-string`, `string-for-each`, and `build-string` reside in `string_utils.lisp`.  These modules are imported automatically when `evaluator.lisp` is loaded.

## Future Self-Hosting Goals

The long-term vision is for Python to serve purely as a thin loader and REPL interface.  All parsing and evaluation will ultimately happen in Lisp.
Currently, the interpreter in `lispfun/interpreter.py` still tokenizes and parses source code in Python.  Helpers now exist to create `Symbol` objects and convert digit sequences to numbers from Lisp code.  To finish moving the parser we must implement:

1. a tokenizer that splits program text into Lisp tokens,
2. a reader for building lists and atoms from those tokens.

Once these components exist in Lisp, Python's role can shrink to simply loading the evaluator and starting the REPL.

For a concrete checklist toward building a self-hosted parser, see
`docs/pure_lisp_plan.md`.
