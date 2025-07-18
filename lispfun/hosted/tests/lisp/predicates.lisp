(define pass 1)
(define assert-equal
  (lambda (result expected)
    (if (= result expected)
        1
        (begin (set! pass 0) 0))))

(assert-equal (number? 42) (< 0 1))
(assert-equal (number? "foo") (< 1 0))
(assert-equal (string? "foo") (< 0 1))
(assert-equal (string? 42) (< 1 0))

pass
