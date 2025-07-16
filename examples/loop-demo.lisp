(define n 5)
(define fac 1)
(while (> n 1)
  (begin
    (set! fac (* fac n))
    (set! n (- n 1))))
(define sum 0)
(for i 1 5
  (set! sum (+ sum i)))
(print (list fac sum))
