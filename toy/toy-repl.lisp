(import "toy/toy-interpreter.lisp")

; Minimal REPL using the toy evaluator.  Type "exit" to quit.
(define toy-repl
  (lambda ()
    (define line (read-line "toy> "))
    (cond
      ((or (= line "exit") (= line "") (= line "'bye"))
       (print "bye")
       'bye)
      (else
       (let ((result (eval-string line)))
         (if result (print result)))
       (toy-repl)))))

(toy-repl)
