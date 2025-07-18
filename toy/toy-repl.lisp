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
         (trap-error
           (lambda ()
             (let ((expr (parse line)))
               (let ((result (eval2 expr env)))
                 (if result (print result) 0))))
           (lambda (msg)
             (print (string-concat "Error: " msg))))
         (toy-repl))))))

(toy-repl)
