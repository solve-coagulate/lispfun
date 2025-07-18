(define pass 1)
(define assert-equal
  (lambda (result expected)
    (if (= result expected)
        1
        (begin (set! pass 0) 0))))

(assert-equal (<= 2 3) 1)
(assert-equal (<= 3 3) 1)
(assert-equal (<= 4 3) 0)
(assert-equal (>= 3 2) 1)
(assert-equal (>= 3 3) 1)
(assert-equal (>= 2 3) 0)
(assert-equal (abs -4) 4)
(assert-equal (abs 5) 5)
(assert-equal (max 2 3) 3)
(assert-equal (min 2 3) 2)

pass
