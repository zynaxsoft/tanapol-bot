#!/bin/bash
# Exit immediately when exit code is not 0
set -e

PACKAGE=tanapol

# Install linters
pip3 install flake8 > /dev/null
pip3 install pylint > /dev/null

cd app

flake8 ${PACKAGE} --ignore "I100, E123, W503"
python3 -m pylint ${PACKAGE} --errors-only --disable E0401
