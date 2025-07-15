(define pass 1)
(define assert-equal
  (lambda (result expected)
    (if (= result expected)
        1
        (begin (set! pass 0) 0))) )

(assert-equal (+ 1 2 3) 6)
(assert-equal (begin (define x 4) x) 4)
(assert-equal ((lambda (a b) (+ a b)) 3 4) 7)
(assert-equal (if (> 3 2) 1 0) 1)
(assert-equal (car (list 1 2 3)) 1)
(assert-equal (cond ((> 3 4) 0) ((< 3 4) 1) (else 2)) 1)
(begin
  (define-macro when (lambda (test expr) (list (quote if) test expr 0)))
  (assert-equal (when (> 3 2) 42) 42))
(assert-equal (length (list 1 2 3)) 3)
(assert-equal (map (lambda (x) (+ x 1)) (list 1 2 3)) (list 2 3 4))
(assert-equal (filter (lambda (x) (> x 2)) (list 1 2 3 4)) (list 3 4))
pass
