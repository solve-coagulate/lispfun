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
   - Current progress: the Lisp evaluator now supports the `cond` form, `define-macro` for basic macros, Lisp implementations of `null?`, `length`, `map`, and `filter`, and basic string literals.

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

## Self-hosted Evaluator

The self-hosted interpreter lives in `lispfun/evaluator.lisp`. It is loaded by `load_eval` in `lispfun/run.py` (lines 10-15) so that the Lisp version of the evaluator can run within the Python environment. Expressions are then executed by calling `eval_with_eval2` (lines 18-20) which invokes the Lisp function `eval2` rather than Python's `eval_lisp`.

The `eval2` procedure is defined in `lispfun/evaluator.lisp` on lines 21-56 and provides the Lisp-level implementation of evaluation. This function is separate from Python's `eval_lisp` located in `lispfun/interpreter.py` (lines 123-151).

To handle the `begin` special form without colliding with Python's implementation, `eval-begin` is defined on lines 1-7 of `lispfun/evaluator.lisp` and is used internally by `eval2`.
