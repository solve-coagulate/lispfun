(import "toy/toy-interpreter.lisp")

; Minimal REPL using the toy evaluator.  Type "exit" to quit.
(define toy-repl
  (lambda ()
    (define line (read-line "toy> "))
    (cond
      ((or (= line "exit") (= line "") (= line "'bye"))
       (begin
         (print "bye")
         (quote bye)))
      (else
       (begin
         (let ((expr (py-parse line)))
           (let ((result (eval2 expr env)))
             (if result (print result) 0)))
         (toy-repl))))))

(toy-repl)
