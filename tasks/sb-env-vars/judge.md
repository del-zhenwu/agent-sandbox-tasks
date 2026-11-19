# sb-env-vars 核对

双判据：token/challenge 由 runner 每次随机生成，题面不出现具体值，平台侧保存 `env.json` 与期望哈希。

- `test_agent_report` 失败 → agent 没跑探针、或把值硬编码/写错
- `test_harness_injected_secret` 失败 → secret 没生成，或 trace 没有探针执行记录（证据通道问题）
- 产物能对上平台随机值 → env 确实穿透到沙箱进程；这是本题要抓的核心

失败看 `scores.json` 的 `attribution`；通过后才比秒数，相差不到 60 秒不判谁更快。
