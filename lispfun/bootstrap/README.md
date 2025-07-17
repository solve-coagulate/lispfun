# Bootstrap Interpreter

This package implements the tiny Python interpreter used to bootstrap
LispFun.  It includes a very small tokenizer and parser along with a simple
evaluator.  The goal is merely to load more complete Lisp code—including a
parser written in Lisp.  Both `kernel_env` and `kernel_parser_env` expose only
the primitives needed during bootstrapping.  The interpreter is used by
`run_bootstrap.py` and by the self-hosted evaluator when loading `eval2`.

