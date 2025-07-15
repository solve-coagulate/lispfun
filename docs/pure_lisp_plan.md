# Plan for a Pure Lisp Parser

The long term goal of **LispFun** is to load and interpret programs entirely in Lisp.  These steps outline how to replace the current Python tokenizer and reader with Lisp implementations.

1. **String Utilities**
   - Implement helpers in Lisp for iterating over characters in a string.
   - Provide operations for building and slicing strings so the tokenizer can read source text one character at a time.

2. **Expose Primitive Constructors**
   - Extend `standard_env` with functions to create `Symbol` objects from Lisp code.
   - Add utilities that convert sequences of digit characters into integers or floats.

3. **Tokenizer and Reader in Lisp**
   - Write a tokenizer in Lisp mirroring the behavior of Python's `tokenize` function in `interpreter.py`.
   - Implement a `read-from-tokens` procedure that produces lists and atoms just like Python's `read_from_tokens`.

4. **Integrate with the Runner**
   - Update `run.py` so the Lisp parser can be loaded optionally.
   - When available, parse input using the Lisp tokenizer and reader before evaluating with `eval2`.

Once these pieces are in place, Python will only start the REPL and load the Lisp parser and evaluator.

**Testing**
- Remember to extend the test suite to cover the Lisp parser once it's implemented. Tests should run both the Python and Lisp parsing paths.
