(import "lispfun/hosted/list_utils.lisp")
(import "toy/toy-parser.lisp")

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
        ((= (car x) 'define-macro)
         (begin
           (set! global-env
                 (extend-env global-env (list (cadr x))
                             (list (list 'macro (eval-expr (caddr x) env)))))
           (quote ok)))
        (else
         (let ((proc (eval-expr (car x) env)))
           (if (and (list? proc) (= (car proc) 'macro))
               (eval-expr (apply-closure (cadr proc) (cdr x)) env)
               (let ((args (map (lambda (e) (eval-expr e env)) (cdr x))))
                 (apply-closure proc args))))))
      (else
       (if (or (number? x) (string? x))
           x
           (lookup env x))))))
)

(define apply-closure
  (lambda (proc args)
    (if (list? proc)
        (if (= (car proc) 'closure)
            (eval-expr (caddr proc)
                       (extend-env (cadddr proc) (cadr proc) args))
            (apply proc args))
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
    (list "<=" (lambda (a b) (or (< a b) (= a b))))
    (list ">=" (lambda (a b) (or (> a b) (= a b))))
    (list "abs" (lambda (x) (if (< x 0) (- 0 x) x)))
    (list "max" (lambda (a b) (if (> a b) a b)))
    (list "min" (lambda (a b) (if (< a b) a b)))
    (list "apply" (lambda (f args) (apply-closure f args)))
    (list "list" list)
    (list "car" car)
    (list "cdr" cdr)
    (list "cons" cons)
    (list "number?" number?)
    (list "string?" string?)
    (list "print" print)
    (list "null?" null?)
    (list "length" length)
    (list "map" map)
    (list "filter" filter)
    (list "read-file" read-file)
    (list "read-line" read-line)))

; Basic boolean operators used by the tokenizer and parser
(define or
  (lambda (a b)
    (if a a b)))

(define and
  (lambda (a b)
    (if a b a)))


(define not
  (lambda (x)
    (if x 0 1)))

; Extra primitives implemented in Lisp now that the environment exists

; Check for the empty list without relying on Python
(define null?
  (lambda (x)
    (= x (quote ()))))

; Compute the length of a list recursively
(define length
  (lambda (lst)
    (if (null? lst)
        0
        (+ 1 (length (cdr lst))))) )

; Map a function over a list using apply-closure so closures work
(define map
  (lambda (f lst)
    (if (null? lst)
        (quote ())
        (cons (apply-closure f (list (car lst)))
              (map f (cdr lst))))))

; Filter a list according to predicate f
(define filter
  (lambda (pred lst)
    (if (null? lst)
        (quote ())
        (if (apply-closure pred (list (car lst)))
            (cons (car lst) (filter pred (cdr lst)))
            (filter pred (cdr lst))))))


; List access helpers used by the evaluator and parser
(define cadr (lambda (lst) (car (cdr lst))))
(define caddr (lambda (lst) (car (cdr (cdr lst)))))
(define cadddr (lambda (lst) (car (cdr (cdr (cdr lst))))))

; Reverse a list - helper for the parser
(define reverse
  (lambda (lst)
    (define iter
      (lambda (xs acc)
        (if (null? xs)
            acc
            (iter (cdr xs) (cons (car xs) acc)))))
    (iter lst (quote ()))))

; Convenience to evaluate a program string using the toy interpreter
(define eval-string
  (lambda (source)
    (eval-expr (parse source) global-env)))

; Evaluate an entire file using the toy interpreter
(define run-file
  (lambda (path)
    (import path)))

; Simple loop macros built entirely in Lisp
(define-macro while
  (lambda (test body)
    (list (quote if) test
          (list (quote begin)
                body
                (list (quote while) test body))
          0)))

(define-macro for
  (lambda (var start end body)
    (list (quote begin)
          (list (quote define) var start)
          (list (quote while) (list (quote <=) var end)
                (list (quote begin)
                      body
                      (list (quote set!) var (list (quote +) var 1)))))) )

; --- Simple module system -------------------------------------------------

; Track which files have been loaded so require only imports once
(define loaded-modules (quote ()))

(define member
  (lambda (item lst)
    (if (null? lst)
        0
        (if (= (car lst) item)
            1
            (member item (cdr lst))))))

(define require
  (lambda (path)
    (if (member path loaded-modules)
        0
        (begin
          (set! loaded-modules (cons path loaded-modules))
          (import path)))) )
