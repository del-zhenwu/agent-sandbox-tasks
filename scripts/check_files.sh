#!/bin/bash
# 用法: bash scripts/check_files.sh tasks/<名字> <含 inputs/ 与 output/ 的工作区>
# 判据：产物正确性 + 完整性（inputs 未改、timing 自洽）。
# 有 pytest 用它，没有就用零依赖的 scripts/run_tests.py。
set -euo pipefail
if [ "$#" -ne 2 ]; then
  echo "用法: bash scripts/check_files.sh tasks/<名字> <含 inputs/ 与 output/ 的工作区>"
  exit 1
fi
task=$(cd "$1" && pwd)
collected=$(cd "$2" && pwd)
export APP_ROOT="$collected"
export TASK_DIR="$task"
# 公共断言只在 tasks/_common.py 放一份，让测试模块能 import 到
export PYTHONPATH="$(cd "$task/.." && pwd)${PYTHONPATH:+:$PYTHONPATH}"

if python3 -c "import pytest" >/dev/null 2>&1; then
  exec python3 -m pytest -q --tb=line "$task/tests/test_outputs.py"
else
  exec python3 "$(dirname "$0")/run_tests.py" "$task" "$collected"
fi
