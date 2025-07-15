# LispFun Development Plan

This repository aims to develop a minimal Lisp interpreter in Python and gradually transition its evaluation capabilities to Lisp itself.

## Tasks

1. **Bootstrap Interpreter (Python)**
   - Implement a small Lisp interpreter in Python capable of parsing and evaluating simple expressions: arithmetic operations, variable bindings, and function calls.
   - Include a REPL for quick experimentation.

2. **Testing Basic Programs**
   - Provide unit tests demonstrating that simple Lisp programs evaluate correctly.
   - Example programs: arithmetic computations, defining and calling functions.

3. **Self-hosted Evaluator (Lisp)**
   - Write a Lisp evaluator in Lisp, running on the Python interpreter.
   - The Lisp evaluator should support the same basic features as the Python version.

4. **Expanding Features in Lisp**
   - Add more language features implemented in Lisp: conditionals, lists, higher-order functions, and macros.
   - Gradually reduce Python's role to just parsing and initial bootstrapping.

5. **Documentation and Examples**
   - Document usage of the interpreter and provide example Lisp programs.

6. **Future Ideas**
   - Explore self-hosting (running the interpreter written in Lisp using itself).
   - Consider building a small standard library in Lisp for common utilities.

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

