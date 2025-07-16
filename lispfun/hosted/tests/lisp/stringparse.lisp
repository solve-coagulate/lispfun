(define pass 1)
(define assert-equal
  (lambda (result expected)
    (if (= result expected)
        1
        (begin (set! pass 0) 0))))

(define q (chr 34))
(define text (string-concat q "abc"))
(set! text (string-concat text q))
(set! text (string-concat text " rest"))
(define parsed (parse-string text 0))
(assert-equal (car parsed) "abc")
(assert-equal (car (cdr parsed)) 5)
pass
