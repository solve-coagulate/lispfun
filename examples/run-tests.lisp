; Run all Lisp tests using the built-in import facility.
; Each imported file prints its result so you can verify success.

(print (import "tests/lisp/bootstrap.lisp"))
(print (import "tests/lisp/basic.lisp"))
(print (import "tests/lisp/import_main.lisp"))
(print (import "tests/lisp/selftest.lisp"))
(print (import "tests/lisp/stringparse.lisp"))
(print (import "tests/lisp/stringutils.lisp"))
