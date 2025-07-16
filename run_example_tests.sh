#!/usr/bin/env bash
# Run example test suites with each interpreter.
# Expected results:
# - run_bootstrap.py passes bootstrap tests but fails the others
# - run_hosted.py runs bootstrap and hosted tests but fails toy tests
# - run_toy.py runs all tests

set -e
cd "$(dirname "$0")"

python ./run_bootstrap.py examples/bootstrap-tests.lisp
python ./run_bootstrap.py examples/hosted-tests.lisp || true
python ./run_bootstrap.py examples/toy-tests.lisp || true

python ./run_hosted.py examples/bootstrap-tests.lisp
python ./run_hosted.py examples/hosted-tests.lisp
python ./run_hosted.py examples/toy-tests.lisp || true

python ./run_toy.py examples/bootstrap-tests.lisp
python ./run_toy.py examples/hosted-tests.lisp
python ./run_toy.py examples/toy-tests.lisp
