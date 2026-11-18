#!/bin/bash
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
fail=0
# 正式题的次数和字节会跑好几分钟。这里只核对内容。
export BENCH_TOOL_CALLS=12
export BENCH_CONCURRENCY=4
export BENCH_SLEEP_SECONDS=0.1
export BENCH_SMALL_FILES=4
export BENCH_FS_DOWNLOAD_BYTES=65536
export BENCH_FS_UPLOAD_BYTES=65536
export BENCH_STDOUT_BYTES=65536
export BENCH_HTTP_REQUESTS=2
export BENCH_NET_DOWNLOAD_BYTES=65536
export BENCH_NET_UPLOAD_BYTES=65536
for task in "$ROOT"/tasks/sb-*; do
  name=$(basename "$task")
  app=$(mktemp -d)
  cp "$task/environment/probe.py" "$app/probe.py"
  if ! env APP_ROOT="$app" bash "$task/solution/solve.sh"; then
    echo "FAIL solution $name"
    fail=1
    rm -rf "$app"
    continue
  fi
  if ! env APP_ROOT="$app" python3 -m pytest -q --tb=line "$task/tests/test_outputs.py"; then
    echo "FAIL pytest $name"
    fail=1
    rm -rf "$app"
    continue
  fi
  echo "PASS $name"
  rm -rf "$app"
done
exit "$fail"
