# sandbox-bench

同时量 **agent harness + 沙箱**（网络、工具调用、文件操作）和 **agent 是否按题面完成**。一道题出两个分数，失败时能归因到某一侧。

## 双平面

- **agent 工作区**：只放 `inputs/` 和 `output/`，agent 可见可写。这里的产物是 agent 维度证据。
- **平台私有平面**：`runs/<题目>/<run_id>/_private/`，agent 不可见不可写。里面是每次 run 随机生成的 secret/原件、trace、平台侧期望值、健康检查记录。这里是 harness 维度证据。

判据分三类，全在 `tests/test_outputs.py`：

- `test_agent_*`：产物正确（文件在不在、字节/哈希/退出码对不对）
- `test_harness_*`：平台证据（真实工具调用 trace、随机 secret 是否穿透、本地服务访问日志、原始 exec 返回包）
- 完整性：`inputs/` 未被改（私有清单哈希比对）、`timing.json` 自洽（runner 写入，ISO 起止时间）

## 目录

```
tasks/<名字>/
├── instruction.md     # 发给 agent 的题面
├── inputs/            # 探针，发题后不可改
├── output/            # 产物；runner 写入 timing.json
├── judge.md           # 失败归因参考
├── task.toml          # 元数据
└── tests/
    ├── test_outputs.py
    └── inputs.sha256  # 原始 inputs 摘要（runner 会生成本次 run 的私有清单）

tasks/_common.py       # 公共断言与私有证据辅助
scripts/run_task.py    # run runner：随机注入、计时、核验、出双分数
```

## 运行流程

```bash
python3 scripts/run_task.py tasks/sb-env-vars --simulate          # 本地冒烟：模拟 agent 按题面执行
python3 scripts/run_task.py tasks/sb-tool-calls --trace <CLI 导出的 trace.jsonl>
```

正式 run 由 CLI harness 导出 trace，`--trace` 传入；CLI 应在发题时记下时间并用 `--started-at` 传给 runner（否则 `--elapsed` 只覆盖核验阶段）。runner 做：准备 workspace → 生成随机 secret/原件 → 注入 → 计时 → 收产物 → 跑 `scripts/check_files.sh` → 写 `runs/<题目>/<run_id>/scores.json`。

`--simulate` 只用于验证判据本身，不算真实评测。没有 trace 时 `test_harness_*` 会明确失败并提示“CLI/trace 未接入”。

核验优先用 pytest，否则回退零依赖的 `scripts/run_tests.py`，结果一致。

## 正式套件

| 目录 | 测什么 | harness 证据 | 预算 |
|---|---|---|---|
| `sb-tool-calls` | 50 次独立工具调用 | trace 里 50 个唯一调用 ID + 注入 nonce | 240s |
| `sb-concurrent-exec` | 20 条并行执行 | trace 里最大并发 ≥ 10、总跨度 ≤ 30s | 40s |
| `sb-fs-upload` | 写随机 256 MiB 并出收据 | 平台侧随机原件哈希 | 60s |
| `sb-stdout` | 捕获 64 MiB 标准输出 | 平台独立计算的期望哈希 | 60s |
| `sb-env-vars` | env 经执行环境传入 | 每次 run 随机注入的 token/challenge | 30s |
| `sb-error-handling` | 非零退出码、stderr、失败后继续 | trace 原始返回包（退出码 + stderr 分信道） | 25s |
| `sb-net-local` | 本地 HTTP 往返 | 平台本地服务访问日志 + 随机响应体 | 30s |

单轮约 485s。默认跑 3 轮约 24 分钟，控制在半小时预算内。网络维度用本地 server，不依赖公网，避免 ISP 带宽/延迟主导结果。

## 归因

`scores.json` 的 `attribution`：

| 私有证据 | 产物 | 结论 |
|---|---|---|
| 完整 | 正确 | 通过 |
| 完整 | 错误 | agent 没做对，沙箱正常 |
| 缺失 | 正确 | 产物伪造，或证据通道坏了 |
| 缺失 | 错误 | harness 故障，或任务没启动 |

区分后两格靠 `runner_health.json`：有健康检查但无事件 = 伪造；连健康检查都没有 = 证据通道故障。

## 防作弊

- secret / payload / 网络响应每次 run 随机生成，题面不出现具体值，平台侧持有期望值。
- `inputs/` 私有清单全量哈希，改探针、删探针、加文件都判失败。
- `timing.json` 由 runner 在停表后写入并覆盖，agent 事先写的值不算数；仍做 ISO 与 ±5s 自洽校验。
- 不再用产物 mtime 判独立调用——快 harness 会被误伤，`sleep` 又能绕过。独立性和并发只看 trace。

## 和 Codex 对比

同一份 `instruction.md`、同一套 `tests/`；只对比检查通过的 run；用同一规则写 `timing.json`；相差不到 60 秒不判谁更快。分别看 agent 分和 harness 分，不要只看总分。

## Playwright（可选发题入口）

```bash
npm install
npx playwright install chromium
node gui/send-task.mjs tasks/sb-tool-calls
```

脚本把用时写到 `runs/<题目>/output/timing.json`，可再交给核验。正式评测仍以 CLI runner + trace 为准。

## 改题之后

改了任何 `inputs/`，都要重跑 `python3 scripts/sync_tests.py` 重建 `inputs.sha256`；runner 运行时会另建私有清单覆盖随机注入的输入。
