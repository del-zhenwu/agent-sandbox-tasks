# sb-stdout 核对

期望哈希由平台在私有平面独立计算，agent 看不到。

- `test_agent_stdout_captured` 失败 → stdout 被截断，或 agent 没按题面重定向
- `test_harness_stdout_channel` 失败 → 平台没算出期望值，或 trace 缺执行记录（证据通道问题）
- 捕获字节对上平台期望 → 沙箱 stdout 通道保住了完整输出

失败看 `scores.json` 的 `attribution`。通过后才比秒数，相差不到 60 秒不判谁更快。
