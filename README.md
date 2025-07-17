# LispFun

LispFun is a tiny Lisp system.  The Python code provides only a minimal
bootstrap kernel able to load and run Lisp code.  Everything else, including the
main evaluator and a small toy interpreter, lives in Lisp.

The repository layout is simple:

- `lispfun/bootstrap` – Python bootstrap kernel
- `lispfun/hosted` – Lisp files for the self‑hosted evaluator
- `toy/` – toy interpreter written entirely in Lisp
- `examples/` – sample programs exercising the interpreters
- `docs/` – additional documentation

Helper scripts in the repository root run the different interpreters:


```bash
./run_bootstrap.py [--kernel] [file]
./run_hosted.py   [--kernel] [file]
./run_toy.py      [file]
```

Pass `--kernel` to start in the restricted bootstrap environment.  See the
individual documents under `docs/` and `lispfun/README.md` for full usage and
development notes.
