; Run Lisp unit tests for the hosted evaluator.

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
    (let ((result (import file)))
      (if (equal? result expected)
          (print (string-concat file " ... PASS"))
          (begin
            (set! failures (+ failures 1))
            (print (string-concat file " ... FAIL"))
            (print "expected:")
            (print expected)
            (print "got:")
            (print result))))))

(run-test "lispfun/hosted/tests/lisp/basic.lisp"
          (quote (6 4 5 7 1 1 (2 3) (0 1 2 3) (1 2))))
(run-test "lispfun/hosted/tests/lisp/selftest.lisp" 1)
(run-test "lispfun/hosted/tests/lisp/stringparse.lisp" 1)
(run-test "lispfun/hosted/tests/lisp/stringutils.lisp" 1)

(if (= failures 0)
    (print "All hosted tests passed.")
    (begin
      (print "Some hosted tests failed.")
      (print failures)))
