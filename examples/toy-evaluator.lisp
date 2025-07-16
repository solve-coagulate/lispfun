(import "lispfun/list_utils.lisp")
(import "examples/toy-parser.lisp")

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
        ((= (car x) 'define)
         (begin
           (set! global-env
                 (extend-env global-env (list (cadr x))
                             (list (eval-expr (caddr x) env))))
           (quote ok)))
        (else
          (let ((proc (eval-expr (car x) env))
                (args (map (lambda (e) (eval-expr e env)) (cdr x))))
            (apply-closure proc args))))
      (else
       (if (number? x)
           x
           (lookup env x))))))
)

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
    (list "read-file" read-file)
    (list "read-line" read-line)))

; Convenience to evaluate a program string using the toy interpreter
(define eval-string
  (lambda (source)
    (eval-expr (parse source) global-env)))

; Evaluate an entire file using the toy interpreter
(define run-file
  (lambda (path)
    (eval-string (read-file path))))
