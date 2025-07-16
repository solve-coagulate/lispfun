# Future LispFun Enhancements

This file collects ideas for features we would like to implement. Development is
now focused on improving the Lisp toy interpreter found in
`docs/toy_interpreter.md`.

## Completed Work

- **Loop constructs**: `while` and `for` macros have been added so iterative
  examples can run without modifying the evaluator.
- **Macro support**: the toy evaluator understands `define-macro`, allowing
  basic macros in Lisp code.
- **String handling**: the tokenizer recognizes quoted strings and the parser
  supports semicolon comments.
- **Command line arguments** are exposed via the `args` list when running
  scripts through `run_toy.py`.
- **Interactive input**: `read-line` gracefully handles end-of-file so the
  toy REPL can be used with piped input. `run_toy.py` automatically executes
  code provided on standard input.
- **File reading**: a `read-file` primitive allows Lisp code to load other
  source files or data.


## Remaining Ideas

- **Quasiquote and unquote** to simplify macro writing.
- **Module system** for organizing code and supporting imports.
- **File I/O primitives** for writing to files, complementing `read-file`.
- **Exception handling** to manage runtime errors gracefully.
- **Full self-hosting**: move the tokenizer and parser to Lisp so the interpreter can boot itself.
- **Expanded standard library** providing utilities beyond the basic list functions.

## Task List
The following items are still planned for the toy interpreter:

- **Implement quasiquote/unquote** to simplify macro definitions.
- **Module system** for organizing code and supporting imports.
- **Add exception handling** so programs can recover from runtime errors.
- **Complete self-hosting** by migrating the tokenizer and parser to Lisp.
- **Expand the standard library** with additional list, string and numeric utilities.
