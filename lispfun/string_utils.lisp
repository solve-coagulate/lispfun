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

(define string-for-each
  (lambda (f s)
    (begin
      (define len (string-length s))
      (define iter
        (lambda (i)
          (if (< i len)
              (begin
                (f (string-slice s i (+ i 1)))
                (iter (+ i 1)))
              0)))
      (iter 0))))

(define build-string
  (lambda (n f)
    (begin
      (define iter
        (lambda (i acc)
          (if (>= i n)
              (make-string acc)
              (iter (+ i 1)
                    (string-concat acc (f i))))) )
      (iter 0 ""))))
