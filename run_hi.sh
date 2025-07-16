#!/bin/bash
# Simple script to demonstrate piping a single expression into run_toy.py
# Prints "hi" if everything works correctly.

SCRIPT_DIR="$(dirname "$0")"

"$SCRIPT_DIR"/run_toy.py <<< '(print "hi")'
