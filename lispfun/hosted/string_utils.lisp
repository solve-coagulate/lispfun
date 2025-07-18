(define string-length
  (lambda (s)
    (begin
      (define iter
        (lambda (i)
          (if (= (string-slice s i (+ i 1)) "")
              i
              (iter (+ i 1)))))
      (iter 0))))

; Convert a string containing digits (and an optional decimal point)
; into a number.  Handles a leading '-' for negative values.
(define digits->number
  (lambda (s)
    (begin
      (define len (string-length s))
      (define start 0)
      (define sign 1)
      (if (> len 0)
          (if (= (string-slice s 0 1) "-")
              (begin
                (set! start 1)
                (set! sign -1))
              0)
          0)
      (define find-dot
        (lambda (i)
          (if (>= i len)
              -1
              (if (= (string-slice s i (+ i 1)) ".")
                  i
                  (find-dot (+ i 1))))) )
      (define dot (find-dot start))
      (define parse-int
        (lambda (i end acc)
          (if (>= i end)
              acc
              (parse-int (+ i 1) end
                         (+ (* acc 10)
                            (- (char-code (string-slice s i (+ i 1)))
                               (char-code "0")))))))
      (define result
        (if (= dot -1)
            (parse-int start len 0)
            (begin
              (define whole (parse-int start dot 0))
              (define frac-start (+ dot 1))
              (define frac (parse-int frac-start len 0))
              (define frac-len (- len frac-start))
              (define pow10
                (lambda (n acc)
                  (if (= n 0)
                      acc
                      (pow10 (- n 1) (* acc 10)))))
              (+ whole (/ frac (pow10 frac-len 1))))))
      (* sign result))))

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

; capture the double quote character before redefining chr
(define dq (chr 34))

(define char-code
  (lambda (c)
    (cond
      ((= c dq) 34)
      ((= c "0") 48)
      ((= c "1") 49)
      ((= c "2") 50)
      ((= c "3") 51)
      ((= c "4") 52)
      ((= c "5") 53)
      ((= c "6") 54)
      ((= c "7") 55)
      ((= c "8") 56)
      ((= c "9") 57)
      (else 0))) )

(define chr
  (lambda (code)
    (cond
      ((= code 34) dq)
      ((= code 48) "0")
      ((= code 49) "1")
      ((= code 50) "2")
      ((= code 51) "3")
      ((= code 52) "4")
      ((= code 53) "5")
      ((= code 54) "6")
      ((= code 55) "7")
      ((= code 56) "8")
      ((= code 57) "9")
      (else ""))))
