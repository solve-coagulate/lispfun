(define import
  (lambda (path)
    (let ((code (read-file path)))
      (define exprs (py-parse-multiple code))
      (define loop
        (lambda (es result)
          (if (null? es)
              result
              (loop (cdr es) (eval2 (car es) env)))))
      (loop exprs 0)))
)
