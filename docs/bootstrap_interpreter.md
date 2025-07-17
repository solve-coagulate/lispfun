# Python Bootstrap Interpreter

The bootstrap interpreter in `interpreter.py` is the initial Python
implementation of LispFun.  It intentionally keeps the parser and evaluator as
small as possible—just enough to load and execute a parser written in Lisp.  The
resulting kernel is fully Turing complete but deliberately limited so that a
bootstrap interpreter written in Lisp can build the rest of the system.  The
goal is to rely only on this kernel; everything beyond it is written in Lisp so
the Python layer stays minimal.
Separate `kernel_env` and `kernel_parser_env` functions return only the
evaluation and parser primitives required for bootstrapping.  The standard
environment builds on top of this, exposing list and string helpers, `import`
for loading Lisp files and other conveniences.  It still includes simple list
utilities like `null?`, `length`, `map` and `filter` so example programs run
without additional modules.

Run the interpreter directly with:

```bash
./run_bootstrap.py [--kernel] [path/to/file.lisp] [args...]
```

Omit the path to start the REPL. Passing `--kernel` starts the interpreter with
the minimal `kernel_env`. Any additional arguments after the file name are
available inside the Lisp program via the `args` variable.

