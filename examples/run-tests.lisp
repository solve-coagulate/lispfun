; Run all Lisp tests using the built-in import facility.
; Output PASS/FAIL lines similar to a unit test runner.

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
(run-test "lispfun/hosted/tests/lisp/basic.lisp"
          (quote (6 4 5 7 1 1 (2 3) (0 1 2 3) (1 2))))
(run-test "lispfun/bootstrap/tests/lisp/import_main.lisp" 42)
(run-test "lispfun/hosted/tests/lisp/selftest.lisp" 1)
(run-test "lispfun/hosted/tests/lisp/stringparse.lisp" 1)
(run-test "lispfun/hosted/tests/lisp/stringutils.lisp" 1)
(import "toy/toy-interpreter.lisp")
(run-test "toy/tests/lisp/loops.lisp" (quote (120 15)))
(define expected-strings (list (string? "abc") (number? 42)))
(run-test "toy/tests/lisp/toy-strings.lisp" expected-strings)

(if (= failures 0)
    (print "All Lisp tests passed.")
    (begin
      (print "Some Lisp tests failed.")
      (print failures)))
