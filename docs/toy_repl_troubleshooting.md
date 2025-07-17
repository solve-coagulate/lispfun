# Toy REPL Troubleshooting

This note describes the difficulties encountered when implementing the REPL in `toy/toy-repl.lisp` and how they were resolved.

## Symptoms

The test `test_lisp_toy_repl_reads_line` initially failed because the Lisp REPL did not echo input read via `read-line`. Typing `(print (read-line))` in the REPL produced no output.

## Cause

The REPL parsed user input using the toy interpreter's own tokenizer and parser. These components could not handle every feature supported by the hosted evaluator, such as quoting and multi-expression constructs. As a result the parsed form was incorrect and evaluation via `eval2` produced unexpected results or nothing at all.

## Solution

The REPL now calls the host parser exposed as `py-parse` to transform each line of input. The expression is evaluated with `(eval2 expr env)` so any constructs supported by `eval2` work in the interactive session. The evaluator and bootstrap interpreter were also updated to handle multi-expression `cond` clauses and `lambda` bodies which were needed by the REPL implementation.

After these changes the test passes and the REPL echoes lines read via `read-line`.
