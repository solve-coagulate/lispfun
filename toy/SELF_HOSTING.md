# Self-Hosting Status

This document clarifies what "self‑hosting" means for the toy interpreter and
outlines the remaining work before the interpreter is truly self‑hosted.

## What is self‑hosting?

A language implementation is *self‑hosting* when it can bootstrap and run using
only code written in that language.  After an initial minimal loader, the system
is able to read, parse and evaluate its own source without relying on the host
(Python in this repository).

## Current state

The repository contains a Lisp implementation of the evaluator (`eval2`) and a
pure Lisp toy interpreter (`toy/…`) with its own tokenizer and parser.  These
components prove that the core of the interpreter can be expressed in Lisp.
However the startup process still depends on the Python implementation:

- Python reads the Lisp source files using the Python tokenizer and parser.
- The environment with primitives and file loading is created in Python.
- The toy interpreter is loaded after `eval2` is already running under the
  Python controlled environment.

Because of this, the interpreter cannot yet load and run its own source code
without help from the Python layer.  It is therefore **not fully self‑hosting**.

## What remains to be done

To claim true self‑hosting the following pieces must be implemented in Lisp and
used during startup:

1. **Bootstrapping in Lisp** – Load the Lisp tokenizer and parser using only a
   minimal set of Python primitives, then use those Lisp implementations to read
   the rest of the interpreter.
2. **Lisp environment setup** – Create the initial environment (list and string
   helpers, error handling, file I/O) from Lisp code so that Python provides only
   very small primitives such as reading a file or character input.
3. **Interpreter loading** – After the tokenizer, parser and environment are
   running in Lisp, load `eval2` and the toy interpreter using the Lisp parser so
   the system is executing its own code entirely.

Once these steps are complete the interpreter will be able to parse and evaluate
its own source without depending on Python parsing or environment setup.  At
that point it can be considered self‑hosting.
