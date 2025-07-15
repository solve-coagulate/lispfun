; Toy Lisp interpreter entirely in Lisp.
; This code does not rely on the existing interpreter implementation.
; It illustrates how a simple self-hosted evaluator could look.

(import "list_utils.lisp")

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
                     (- (char-code (string-slice s i (+ i 1))) (char-code "0")))))))
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

(define parse
  (lambda (text)
    (car (read-from-tokens (tokenize text)))) )

; Environment utilities as association list
(define lookup
  (lambda (env name)
    (if (null? env)
        0
        (if (= (car (car env)) name)
            (cadr (car env))
            (lookup (cdr env) name)))))

(define extend-env
  (lambda (env params args)
    (if (null? params)
        env
        (extend-env (cons (list (car params) (car args)) env)
                    (cdr params) (cdr args)))) )

; Evaluate an expression in a given environment
(define eval-expr
  (lambda (x env)
    (cond
      ((list? x)
       (cond
         ((null? x) x)
         ((= (car x) 'quote) (cadr x))
         ((= (car x) 'if)
          (if (eval-expr (cadr x) env)
              (eval-expr (caddr x) env)
              (eval-expr (cadddr x) env)))
         ((= (car x) 'lambda)
          (list 'closure (cadr x) (caddr x) env))
         (else
          (let ((proc (eval-expr (car x) env))
                (args (map (lambda (e) (eval-expr e env)) (cdr x))))
            (apply-closure proc args))))
      (else
       (if (number? x)
           x
           (lookup env x))))))

(define apply-closure
  (lambda (proc args)
    (if (and (list? proc) (= (car proc) 'closure))
        (eval-expr (caddr proc)
                   (extend-env (cadddr proc) (cadr proc) args))
        (apply proc args))))

; Simple global environment with arithmetic primitives
(define global-env
  (list
    (list "+" +)
    (list "-" -)
    (list "*" *)
    (list "/" /)
    (list "=" =)
    (list "<" <)
    (list ">" >)
    (list "list" list)
    (list "car" car)
    (list "cdr" cdr)
    (list "cons" cons)
    (list "print" print)
    (list "null?" null?)
    (list "length" length)
    (list "map" map)
    (list "filter" filter)
    (list "read-file" read-file)))

; Convenience to evaluate a program string using the toy interpreter
(define eval-string
  (lambda (source)
    (eval-expr (parse source) global-env)))

; Evaluate an entire file using the toy interpreter
(define run-file
  (lambda (path)
    (eval-string (read-file path))))
