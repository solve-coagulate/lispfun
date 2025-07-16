; Run all Lisp tests using the built-in import facility.
; Define a helper that announces each file before importing it so
; Tests reside in interpreter-specific directories under lispfun/<interpreter>/tests/lisp.
; it's clear which tests execute.

(define run-test
  (lambda (file)
    (begin
      (print (string-concat "Running " file))
      (print (import file)))))

(run-test "lispfun/bootstrap/tests/lisp/bootstrap.lisp")
(run-test "lispfun/hosted/tests/lisp/basic.lisp")
(run-test "lispfun/bootstrap/tests/lisp/import_main.lisp")
(run-test "lispfun/hosted/tests/lisp/selftest.lisp")
(run-test "lispfun/hosted/tests/lisp/stringparse.lisp")
(run-test "lispfun/hosted/tests/lisp/stringutils.lisp")
