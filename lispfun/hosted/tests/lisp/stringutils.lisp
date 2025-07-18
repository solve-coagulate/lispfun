(define pass 1)
(define assert-equal
  (lambda (result expected)
    (if (= result expected)
        1
        (begin (set! pass 0) 0))))

(define dummy (string-for-each (lambda (c) 0) "ab"))
(assert-equal dummy 0)

(define built (build-string 3 (lambda (i)
                                (if (= i 0) "a" (if (= i 1) "b" "c")))))
(assert-equal built "abc")

(assert-equal (string-length "abc") 3)

(assert-equal (digits->number "123") 123)
(assert-equal (digits->number "3.5") 3.5)
(assert-equal (digits->number "-42") -42)
(assert-equal (digits->number "-7.25") -7.25)

(define sym (make-symbol "foo"))
(assert-equal (symbol? sym) 1)

pass
