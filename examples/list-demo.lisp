(define square (lambda (x) (* x x)))
(define nums (list 1 2 3 4 5))
(print (list
  (length nums)
  (map square nums)
  (filter (lambda (x) (> x 2)) nums)))
