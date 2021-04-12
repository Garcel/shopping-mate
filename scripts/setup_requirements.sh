#!/bin/bash

SCRIPT_PATH=$(dirname "$(realpath -s "$0")")
REQUIREMENTS_RELATIVE_PATH="$SCRIPT_PATH""/../requirements"

python -m piptools compile "$REQUIREMENTS_RELATIVE_PATH"/base.in
python -m piptools compile "$REQUIREMENTS_RELATIVE_PATH"/test.in

python -m piptools compile "$REQUIREMENTS_RELATIVE_PATH"/dev.in
python -m piptools compile "$REQUIREMENTS_RELATIVE_PATH"/prod.in
