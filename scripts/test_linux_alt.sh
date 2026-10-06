#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

# Second Linux OS script: both command-line parameters.
python3 src/main.py --vfs "$(pwd)/data/vfs" --startup "$(pwd)/scripts/startup_alt.txt"
