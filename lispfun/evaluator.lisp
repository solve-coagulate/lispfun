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

(define eval2
  (lambda (x env)
    (if (symbol? x)
        (env-get env x)
        (if (list? x)
            ((lambda (op args)
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
                                               ((lambda (proc)
                                                  (if (list? proc)
                                                      (if (= (car proc) (quote macro))
                                                          (eval2 (apply (car (cdr proc)) args) env)
                                                          (apply proc (map (lambda (a) (eval2 a env)) args)))
                                                      (apply proc (map (lambda (a) (eval2 a env)) args))))
                                                (eval2 op env))))))))))
             )
             (car x)
            (cdr x))
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
