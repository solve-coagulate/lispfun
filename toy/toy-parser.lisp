(import "toy/toy-tokenizer.lisp")

; Parse tokens into an expression
(define read-from-tokens
  (lambda (tokens)
    (if (null? tokens)
        (list (quote ()) (quote ()))
        (let ((token (car tokens)))
          (set! tokens (cdr tokens))
          (cond
            ((= token "(")
             (begin
               (define loop
                 (lambda (ts acc)
                   (if (= (car ts) ")")
                       (list (reverse acc) (cdr ts))
                       (let ((res (read-from-tokens ts)))
                         (loop (cadr res) (cons (car res) acc)))))
               (loop tokens (quote ()))))
            ((= token ")") (list (quote error) tokens))
            (else (list token tokens))))))
))

(define toy-parse
  (lambda (text)
    (car (read-from-tokens (tokenize text)))))

; Parse all expressions from a program string
(define toy-parse-multiple
  (lambda (text)
    (begin
      (define tokens (tokenize text))
      (define loop
        (lambda (ts acc)
          (if (null? ts)
              (reverse acc)
              (let ((res (read-from-tokens ts)))
                (loop (cadr res) (cons (car res) acc))))))
      (loop tokens (quote ())))))
