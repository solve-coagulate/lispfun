(define parse-string
  (lambda (text idx)
    (begin
      (define len (string-length text))
      (define loop
        (lambda (acc i)
          (if (>= i len)
              (list (make-string acc) i)
              (begin
                (define c (string-slice text i (+ i 1)))
                (if (= (char-code c) 34)
                    (list (make-string acc) (+ i 1))
                    (loop (string-concat acc c) (+ i 1)))))))
      (loop "" (+ idx 1)))) )
