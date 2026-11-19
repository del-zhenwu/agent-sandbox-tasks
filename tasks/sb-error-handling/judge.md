# sb-error-handling 核对

标记由 runner 每次随机注入，退出码与 stderr 由平台 trace 的原始返回包取证，不再信 agent 自报。

| 现象 | 归因 |
|---|---|
| `error_report.json` 里 exit_code 为 0 或缺失 | agent 把非零退出归一化成成功 |
| `stderr_marker` 不符 | agent 没拿到 stderr，或硬编码了旧标记 |
| `after.txt` 不存在 | 非零退出中断了 agent 的后续步骤 |
| `partial.bin` 不存在 | 失败前写入被回滚，或没同步出临时目录 |
| trace 里缺 `exec_result` / 退出码不是 3 | harness 证据通道问题，不是 agent 的锅 |

失败看 `scores.json` 的 `attribution`。这题测错误传播链，不测吞吐；耗时差异不作为对比依据。
