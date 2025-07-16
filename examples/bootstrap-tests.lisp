; Run Lisp unit tests for the bootstrap interpreter.

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

(run-test "lispfun/bootstrap/tests/lisp/bootstrap.lisp"
          (quote (6 4 7 1 (1 2))))
(run-test "lispfun/bootstrap/tests/lisp/import_main.lisp" 42)

(if (= failures 0)
    (print "All bootstrap tests passed.")
    (begin
      (print "Some bootstrap tests failed.")
      (print failures)))
