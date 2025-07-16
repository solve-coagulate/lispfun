; Toy Lisp interpreter entirely in Lisp.
; This code does not rely on the existing interpreter implementation.
; It illustrates how a simple self-hosted evaluator could look.

(import "toy/toy-tokenizer.lisp")
(import "toy/toy-parser.lisp")
(import "toy/toy-evaluator.lisp")
