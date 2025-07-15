(define-macro when
  (lambda (test expr)
    (list (quote if) test expr 0)))

(begin
  (define result 0)
  (when (> 3 2) (set! result 42))
  (print result))
