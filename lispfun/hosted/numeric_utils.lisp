(define <=
  (lambda (a b)
    (if (< a b)
        1
        (if (= a b) 1 0))))

(define >=
  (lambda (a b)
    (if (> a b)
        1
        (if (= a b) 1 0))))

(define abs
  (lambda (x)
    (if (< x 0) (- 0 x) x)))

(define max
  (lambda (a b)
    (if (> a b) a b)))

(define min
  (lambda (a b)
    (if (< a b) a b)))
