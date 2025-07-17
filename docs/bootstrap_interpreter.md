# Python Bootstrap Interpreter

The bootstrap interpreter in `interpreter.py` is the initial Python implementation of LispFun. It provides a REPL and basic evaluation of arithmetic, variables and functions. A new `kernel_env` function returns only the primitives required for bootstrapping. The standard environment builds on top of this, exposing list and string helpers, `import` for loading Lisp files and other conveniences. It still includes simple list utilities like `null?`, `length`, `map` and `filter` so example programs run without additional modules.

Run the interpreter directly with:

```bash
./run_bootstrap.py [path/to/file.lisp] [args...]
```

Omit the path to start the REPL. Any additional arguments after the file name
are available inside the Lisp program via the `args` variable.
