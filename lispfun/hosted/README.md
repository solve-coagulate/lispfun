# Self-hosted Evaluator

This directory contains the Lisp source files for the `eval2` evaluator.  The
Python runner ``run_hosted.py`` reads ``evaluator.lisp`` and brings `eval2` into
the environment.  Python performs this bootstrap step, after which `eval2` can
evaluate the same file again or run other Lisp programs on its own.
