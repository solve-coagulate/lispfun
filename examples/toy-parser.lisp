(import "examples/toy-tokenizer.lisp")

; Parse tokens into an expression
(define read-from-tokens
  (lambda (tokens)
    (if (null? tokens)
        (list (quote ()) (quote ()))
        (let ((token (car tokens)))
          (set! tokens (cdr tokens))
          (cond
            ((= token "(")
             (define loop
               (lambda (ts acc)
                 (if (= (car ts) ")")
                     (list (reverse acc) (cdr ts))
                     (let ((res (read-from-tokens ts)))
                       (loop (cadr res) (cons (car res) acc)))))
             (loop tokens (quote ())))
            ((= token ")") (list (quote error) tokens))
            (else (list token tokens))))))
))

(define parse
  (lambda (text)
    (car (read-from-tokens (tokenize text)))) )
