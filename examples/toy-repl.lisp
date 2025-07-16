(import "examples/toy-interpreter.lisp")

; Minimal REPL using the toy evaluator.  Type "exit" to quit.
(define toy-repl
  (lambda ()
    (define line (read-line "toy> "))
    (if (= line "exit")
        'bye
        (begin
          (print (eval-string line))
          (toy-repl)))))

(toy-repl)
