# Python Bootstrap Interpreter

The bootstrap interpreter in `interpreter.py` is the initial Python implementation of LispFun. It provides a REPL and basic evaluation of arithmetic, variables and functions. The environment exposes list and string helpers, `import` for loading Lisp files and primitives needed by the Lisp evaluator.

Run the interpreter directly with:

```bash
./run_bootstrap.py [path/to/file.lisp] [args...]
```

Omit the path to start the REPL. Any additional arguments after the file name
are available inside the Lisp program via the `args` variable.
