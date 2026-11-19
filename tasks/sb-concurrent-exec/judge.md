# sb-concurrent-exec 核对

双判据：`test_agent_*` 看产物齐不齐；`test_harness_*` 看平台 trace 里 20 次工具调用是否重叠（最大并发 ≥ 10、总跨度 ≤ 30s）——不再用 agent 可写的 mtime。

- 产物缺 → 有的调用没落地
- 产物齐但 trace 并发度低 → agent 顺序发，或沙箱把 exec 串行化（本题要抓的）
- 产物齐且 trace 并发正常但总时长偏长 → 单次 exec 启动开销大

先跑 `bash scripts/run_task.py tasks/sb-concurrent-exec --trace <CLI trace>`；失败看 `scores.json` 的 `attribution`。通过后才比秒数，相差不到 60 秒不判谁更快。
