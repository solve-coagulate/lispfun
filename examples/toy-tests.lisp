; Run Lisp unit tests for the toy interpreter.

(define failures 0)

(define equal?
  (lambda (a b)
    (if (list? a)
        (if (list? b)
            (if (= (length a) (length b))
                (if (null? a)
                    1
                    (if (equal? (car a) (car b))
                        (equal? (cdr a) (cdr b))
                        0))
                0)
            0)
        (= a b))))

(define run-test
  (lambda (file expected)
    (let ((result (run-file file))) ; run-file defined by toy interpreter
      (if (equal? result expected)
          (print (string-concat file " ... PASS"))
          (begin
            (set! failures (+ failures 1))
            (print (string-concat file " ... FAIL"))
            (print "expected:")
            (print expected)
            (print "got:")
            (print result))))))

(run-test "toy/tests/lisp/loops.lisp" (quote (120 15)))
(define expected-strings (list (string? "abc") (number? 42)))
(run-test "toy/tests/lisp/toy-strings.lisp" expected-strings)

(if (= failures 0)
    (print "All toy tests passed.")
    (begin
      (print "Some toy tests failed.")
      (print failures)))
