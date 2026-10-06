#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

# Stage 2 test: both command-line parameters.
python3 src/main.py --vfs "./data/vfs" --startup "./scripts/startup.txt"
