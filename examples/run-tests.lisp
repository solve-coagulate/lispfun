; Run all Lisp tests using the built-in import facility.
; Define a helper that announces each file before importing it so
; it's clear which tests execute.

(define run-test
  (lambda (file)
    (begin
      (print (string-concat "Running " file))
      (print (import file)))))

(run-test "tests/lisp/bootstrap.lisp")
(run-test "tests/lisp/basic.lisp")
(run-test "tests/lisp/import_main.lisp")
(run-test "tests/lisp/selftest.lisp")
(run-test "tests/lisp/stringparse.lisp")
(run-test "tests/lisp/stringutils.lisp")
