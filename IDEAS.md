# Future LispFun Enhancements

This file collects ideas for features we would like to implement. Development is
now focused on improving the Lisp toy interpreter found in
`docs/toy_interpreter.md`.

- **Loop constructs** such as `while` or `for` to complement recursive iteration.
- **Quasiquote and unquote** to simplify macro writing.
- **Module system** for organizing code and supporting imports.
- **File I/O primitives** for reading from and writing to files within Lisp.
- **Exception handling** to manage runtime errors gracefully.
- **Full self-hosting**: run the Lisp evaluator written in Lisp using itself.
- **Expanded standard library** providing utilities beyond the basic list functions.

## Task List

- **Improve loop constructs**: Design `while`/`for` style macros for the toy interpreter so users can write iterative code without modifying the underlying evaluator.
- **Implement a module system**: Provide a way to organize Lisp files into modules and support importing them within toy programs.
- **Add exception handling**: Create primitives or macros to catch and handle runtime errors gracefully.
- **Complete self-hosting**: Finish moving the tokenizer and parser to Lisp so the interpreter can fully boot itself without Python.
- **Expand the standard library**: Grow the collection of built-in utilities for lists, strings and numbers to aid example programs.
