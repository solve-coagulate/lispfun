(define eval-begin
  (lambda (es env)
    (if (= (cdr es) (quote ()))
        (eval2 (car es) env)
        (begin
          (eval2 (car es) env)
          (eval-begin (cdr es) env)))) )

(define eval-cond
  (lambda (clauses env)
    (if (= clauses (quote ()))
        None
        ((lambda (clause)
           (if (= (car clause) (quote else))
               (eval2 (car (cdr clause)) env)
               (if (eval2 (car clause) env)
                   (eval2 (car (cdr clause)) env)
                   (eval-cond (cdr clauses) env))))
         (car clauses)))) )

(define apply-proc
  (lambda (op args env)
    ((lambda (proc)
       (if (list? proc)
           (if (= (car proc) (quote macro))
               (eval2 (apply (car (cdr proc)) args) env)
               (apply proc (map (lambda (a) (eval2 a env)) args)))
           (apply proc (map (lambda (a) (eval2 a env)) args))))
     (eval2 op env)))
)

(define eval-list
  (lambda (op args env)
    (if (= op (quote quote))
        (car args)
        (if (= op (quote if))
            (eval2 (if (eval2 (car args) env)
                       (car (cdr args))
                       (car (cdr (cdr args))))
                   env)
            (if (= op (quote define))
                (env-set! env (car args) (eval2 (car (cdr args)) env))
                (if (= op (quote set!))
                    (env-set! env (car args) (eval2 (car (cdr args)) env))
                    (if (= op (quote lambda))
                        (make-procedure (car args) (car (cdr args)) env)
                        (if (= op (quote begin))
                            (eval-begin args env)
                            (if (= op (quote cond))
                                (eval-cond args env)
                                (if (= op (quote define-macro))
                                    (env-set! env (car args) (list (quote macro) (eval2 (car (cdr args)) env)))
                                    (apply-proc op args env)))))))))))

(define eval2
  (lambda (x env)
    (if (symbol? x)
        (env-get env x)
        (if (list? x)
            (eval-list (car x) (cdr x) env)
            x))))

(define null?
  (lambda (x)
    (= x (quote ()))) )

(define length
  (lambda (lst)
    (if (null? lst)
        0
        (+ 1 (length (cdr lst))))))

(define map
  (lambda (f lst)
    (if (null? lst)
        (quote ())
        (cons (f (car lst)) (map f (cdr lst))))) )

(define filter
  (lambda (pred lst)
    (if (null? lst)
        (quote ())
        (if (pred (car lst))
            (cons (car lst) (filter pred (cdr lst)))
            (filter pred (cdr lst))))) )


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
      (loop "" (+ idx 1)))))
