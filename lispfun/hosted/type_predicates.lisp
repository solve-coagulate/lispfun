(define number?
  (lambda (x)
    (trap-error
      (lambda ()
        (+ x 0)
        (< 0 1))
      (lambda (msg) (< 1 0)))))

(define string?
  (lambda (x)
    (trap-error
      (lambda ()
        (string-length x)
        (< 0 1))
      (lambda (msg) (< 1 0)))))

(define list?
  (lambda (x)
    (trap-error
      (lambda ()
        (cons 0 x)
        (< 0 1))
      (lambda (msg) (< 1 0))))
)

(define symbol?
  (lambda (x)
    (if (number? x)
        (< 1 0)
        (if (string? x)
            (< 1 0)
            (if (list? x)
                (< 1 0)
                (< 0 1))))) )
