(import "toy/toy-interpreter.lisp")

; Minimal REPL using the toy evaluator.  Type "exit" to quit.
(define toy-repl
  (lambda ()
    (define line (read-line "toy> "))
    (if (or (= line "exit") (= line ""))
        'bye
        (begin
          (eval-string line)
          (toy-repl)))))

(toy-repl)
