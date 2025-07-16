(define null?
  (lambda (x)
    (= x (quote ()))) )

(define length
  (lambda (lst)
    (if (null? lst)
        0
        (+ 1 (length (cdr lst))))))

(define map
  (lambda (f lst)
    (if (null? lst)
        (quote ())
        (cons (f (car lst)) (map f (cdr lst))))) )

(define filter
  (lambda (pred lst)
    (if (null? lst)
        (quote ())
        (if (pred (car lst))
            (cons (car lst) (filter pred (cdr lst)))
            (filter pred (cdr lst))))) )

(define append
  (lambda (a b)
    (if (null? a)
        b
        (cons (car a) (append (cdr a) b)))) )
