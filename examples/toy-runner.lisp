(import "examples/toy-interpreter.lisp")

; Load and execute each example using eval2 so that macros work
(eval2 (list (quote import) "examples/factorial.lisp") env)
(eval2 (list (quote import) "examples/fibonacci.lisp") env)
(eval2 (list (quote import) "examples/list-demo.lisp") env)
; macro-example requires define-macro which isn't handled by the toy interpreter
; when imported directly via Python. It can be run manually if desired.
