(import "examples/toy-interpreter.lisp")

; Load and execute each example using the toy interpreter's run-file
(run-file "examples/factorial.lisp")
(run-file "examples/fibonacci.lisp")
(run-file "examples/list-demo.lisp")
(run-file "examples/loop-demo.lisp")
; macro-example requires define-macro which isn't handled by the toy interpreter
; when imported directly via Python. It can be run manually if desired.
