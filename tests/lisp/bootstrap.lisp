(define x 4)
(define add2 (lambda (a b) (+ a b)))
(list (+ 1 2 3)
      x
      (add2 3 4)
      (if (> 3 2) 1 0)
      (quote (1 2)))
