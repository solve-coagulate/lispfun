(import "toy/toy-tokenizer.lisp")

; Parse tokens into an expression with simple error reporting
(define read-from-tokens
  (lambda (tokens)
    (if (null? tokens)
        (error "unexpected EOF while reading")
        (let ((token (car tokens)))
          (set! tokens (cdr tokens))
          (cond
            ((= token "(")
             (begin
               (define loop
                 (lambda (ts acc)
                   (if (null? ts)
                       (error "unexpected EOF while reading list")
                       (if (= (car ts) ")")
                           (list (reverse acc) (cdr ts))
                           (let ((res (read-from-tokens ts)))
                             (loop (cadr res) (cons (car res) acc)))))))
               (loop tokens (quote ())))
            )
            ((= token ")") (error "unexpected )"))
            (else (list token tokens))))))
)

(define parse
  (lambda (text)
    (let ((res (read-from-tokens (tokenize text))))
      (if (null? (cadr res))
          (car res)
          (error "extra tokens after expression")))))

(define parse-multiple
  (lambda (text)
    (begin
      (define tokens (tokenize text))
      (define loop
        (lambda (ts acc)
          (if (null? ts)
              (reverse acc)
              (let ((res (read-from-tokens ts)))
                (loop (cadr res) (cons (car res) acc)))))
      )
      (loop tokens (quote ()))
      ))
)
