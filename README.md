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
   - Current progress: the Lisp evaluator now supports the `cond` form, `define-macro` for basic macros, and Lisp implementations of `null?`, `length`, `map`, and `filter`.

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

