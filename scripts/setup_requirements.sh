#!/bin/bash

python -m piptools compile "$REQUIREMENTS_DIR"/base.in
python -m piptools compile "$REQUIREMENTS_DIR"/dev.in
python -m piptools compile "$REQUIREMENTS_DIR"/prod.in
python -m piptools compile "$REQUIREMENTS_DIR"/test.in

pip install -r "${REQUIREMENTS_DIR}"/"${ENVIRONMENT}".txt
