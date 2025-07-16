# Self-hosted Evaluator

`evaluator.lisp` defines `eval2`, a Lisp implementation of the evaluator. The Python runner loads this file through `load_eval` in `run.py`. Once loaded, expressions are executed by wrapping them in `(eval2 ...)`.

Helper modules such as `list_utils.lisp`, `string_utils.lisp` and `eval_core.lisp` provide primitives required by `eval2`. The evaluator understands macros defined with `define-macro` and is the foundation used by higher level code.
