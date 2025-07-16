; Tokenizer helpers for the toy Lisp interpreter

; Basic string helpers
(define whitespace?
  (lambda (c)
    (or (= c " ") (= c "\n") (= c "\t"))))

(define digit?
  (lambda (c)
    (and (>= (char-code c) (char-code "0"))
         (<= (char-code c) (char-code "9")))) )

; Convert a string of digits to a number
(define string->number
  (lambda (s)
    (define len (string-length s))
    (define iter
      (lambda (i acc)
        (if (>= i len)
            acc
            (iter (+ i 1)
                  (+ (* acc 10)
                     (- (char-code (string-slice s i (+ i 1))) (char-code "0")))
))))
    (iter 0 0)))

; Read a number token starting at index idx
(define read-number
  (lambda (text idx len)
    (define j idx)
    (define loop
      (lambda (k)
        (if (and (< k len) (digit? (string-slice text k (+ k 1))))
            (loop (+ k 1))
            k)))
    (set! j (loop j))
    (list j (string->number (string-slice text idx j)))) )

; Read a symbol token
(define read-symbol
  (lambda (text idx len)
    (define j idx)
    (define loop
      (lambda (k)
        (if (and (< k len)
                 (not (whitespace? (string-slice text k (+ k 1))))
                 (not (= (string-slice text k (+ k 1)) "("))
                 (not (= (string-slice text k (+ k 1)) ")")))
            (loop (+ k 1))
            k)))
    (set! j (loop j))
    (list j (string-slice text idx j))))

; Tokenize a program string
(define tokenize
  (lambda (text)
    (define len (string-length text))
    (define iter
      (lambda (i acc)
        (if (>= i len)
            (reverse acc)
            (let ((c (string-slice text i (+ i 1))))
              (cond
                ((whitespace? c) (iter (+ i 1) acc))
                ((= c "(") (iter (+ i 1) (cons "(" acc)))
                ((= c ")") (iter (+ i 1) (cons ")" acc)))
                ((digit? c)
                 (let ((res (read-number text i len)))
                   (iter (car res) (cons (cadr res) acc))))
                (else
                 (let ((res (read-symbol text i len)))
                   (iter (car res) (cons (cadr res) acc))))))))
    (iter 0 (quote ()))) )
