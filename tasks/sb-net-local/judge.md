# sb-net-local 核对

平台在每次 run 起一个本地 HTTP server：随机路径 token + 随机响应体；地址只通过 env 注入，公网不参与，避免 ISP 带宽/延迟主导结果。

- `test_agent_response` 失败 → agent 没访问成功，或沙箱截断了响应
- `test_harness_local_request` 失败 → 请求没到平台侧服务，或 trace 缺执行记录
- 响应哈希对上平台原始响应 → 沙箱的 loopback / HTTP 栈确实工作

失败看 `scores.json` 的 `attribution`。通过后才比秒数，相差不到 60 秒不判谁更快。
