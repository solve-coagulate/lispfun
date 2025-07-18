# Interpreter Capabilities

This document summarizes what is available in the different LispFun interpreters.  The Python bootstrap interpreter exposes a very small core so that the rest of the system can be implemented in Lisp.  The self‑hosted evaluator, written in Lisp, reuses the same primitives but performs evaluation in Lisp code.

## Bootstrap Interpreter

The bootstrap interpreter lives in `lispfun/bootstrap`.  Its tokenizer handles parentheses, numbers, symbols and quoted strings.  Semicolons introduce comments that run until the end of the line.  The parser provides `parse` for a single expression and `parse_multiple` for a whole file.  `to_string` converts expressions back to a textual representation.

Evaluation is limited to a small set of special forms and primitives:

- Special forms: `quote`, `if`, `define`, `set!`, `lambda`, `begin`, `cond` and `let`.
- Arithmetic: `+`, `-`, `*`, `/`.
- Comparisons: `>`, `<`, `>=`, `<=`, `=`.
- List primitives: `list`, `car`, `cdr`, `cons`, and a host‑side `apply`.
- Environment helpers: `env-get`, `env-set!`, `make-procedure`.
- Predicates and utilities in the standard environment such as `null?`, `length`, `map`, `filter`, `number?`, `string?`, `read-file`, `read-line` and simple string helpers (`string-length`, `string-slice`, `string-concat`, `make-string`, `char-code`, `chr`).
- `(import "file.lisp")` loads additional Lisp source using the same parser and evaluator.
- Error handling via `(error "msg")` and `(trap-error thunk handler)`.

This kernel is intentionally small but complete enough to load Lisp source code that implements a more capable evaluator.

## Self-hosted Evaluator

`evaluator.lisp` defines `eval2`, a Lisp implementation of the evaluator.  It uses the same parser functions provided by the bootstrap interpreter.  Once `eval2` is loaded, evaluation occurs purely in Lisp.  The self-hosted interpreter supports all of the above forms and additionally understands `define-macro` so macros expand before execution.  Helper modules in `lispfun/hosted` implement list, string and numeric utilities—now including Lisp versions of `<=`, `>=`, `abs`, `max`, `min`, `string-length`, `digits->number`, `number?` and `string?`—that are themselves written in Lisp.

When run through `run_hosted.py`, the evaluator uses `eval2` for every expression but still relies on Python to tokenize and parse unless another parser is loaded.  The toy interpreter in `toy/` supplies its own tokenizer and parser so it can run entirely in Lisp once the evaluator is loaded.
