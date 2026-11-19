# sb-tool-calls 核对

双判据：`test_agent_*` 看产物（agent 是否照题面完成），`test_harness_*` 看平台私有 trace（工具调用是否真的逐次经过 harness）。

- 产物不齐 → agent 少发了调用，或沙箱丢了写入
- 产物齐但 trace 次数不够 / 编号缺失 → 产物是批量伪造的
- 两者都齐但耗时偏长 → 单次工具调用或沙箱往返慢

先跑 `bash scripts/run_task.py tasks/sb-tool-calls --trace <CLI 导出的 trace>`；失败看 `scores.json` 的 `attribution` 归因。通过后才看 `timing.json` 的秒数；相差不到 60 秒不判谁更快。
