# Self-hosted Evaluator

`evaluator.lisp` defines `eval2`, a Lisp implementation of the evaluator.  The
Python runner invokes `load_eval` in `run_hosted.py` to read this file and bring
`eval2` into the environment.  Python is only needed for this initial
bootstrapping step, relying on the minimal kernel described in
[`bootstrap_interpreter.md`](bootstrap_interpreter.md).  Afterward the
interpreter can reload `evaluator.lisp` using `eval2` itself, so evaluation is
handled entirely in Lisp.

Helper modules such as `list_utils.lisp`, `string_utils.lisp` and
`eval_core.lisp` provide primitives required by `eval2`.  The evaluator
understands macros defined with `define-macro` and is the foundation used by
higher level code.
