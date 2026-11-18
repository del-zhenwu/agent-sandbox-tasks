#!/bin/bash
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "用法: bash scripts/check_files.sh tasks/sb-tool-calls /含有output的目录"
  exit 1
fi
task=$(cd "$1" && pwd)
collected=$(cd "$2" && pwd)
env APP_ROOT="$collected" python3 -m pytest -q --tb=line "$task/tests/test_outputs.py"
