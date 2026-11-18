# sandbox-bench-tasks

目的：通过同一个图形界面 coding agent 发题，牵引 **agent** 和 **内部沙箱** 迭代，并和 Codex 等对比。

正式套件只量工具调用和文件读写（含并发执行、标准输出），不量通用解题，也不拿公网带宽题做对比。

对错看 `output/`，用 `tests/` 做确定性检查。通过之后才比 `timing.json` 的秒数。相差不到 60 秒，不判断谁更快。聊天文字不算结果。计时范围内不要插手下载或改文件。

## 目录

```text
tasks/<名字>/
├── instruction.md     # 贴进输入框
├── inputs/            # 拖给 agent
├── output/            # 产物；发题人写入 timing.json
├── judge.md           # 这题失败时通常暴露什么
└── tests/test_outputs.py
```

## 怎么跑

1. 只把 `tasks/<名字>/inputs` 放进 agent 工作区。不要拖整个 `tasks/<名字>/`，里面的 `tests/`、`judge.md`、`instruction.md` 不能让 agent 看见。
2. 把 `instruction.md` 全文贴进输入框（不要把该文件放进工作区），点发送并开始计时。
3. 题目要求的文件都齐了就停表，写入 `output/timing.json`：`started_at`、`ended_at`、`elapsed_seconds`
4. `bash scripts/check_files.sh tasks/<名字> /含有output的目录`
5. 失败 → 按 `judge.md` 看更像 agent 问题还是沙箱问题；通过 → 才拿秒数和 Codex 对比


发题注意：工作区里只能有 `inputs/`。`tests/`、`judge.md`、仓库里的 `instruction.md` 文件本身都不要放进工作区；题目文字只粘贴进输入框。

`sb-tool-calls` / `sb-fs-small` 若被合成一条循环命令，产物仍可能通过 tests，但用时会偏短，对比时要结合调用记录看。`sb-concurrent-exec` 用 `elapsed_seconds ≤ 90` 抓没有重叠的情况。

## 正式套件

| 目录 | 量什么 | 失败时通常说明什么 |
|---|---|---|
| `sb-tool-calls` | 1000 次独立工具调用 | 调用次数不够，或单次调用往返太慢 |
| `sb-concurrent-exec` | 80 条重叠执行（各等 5 秒） | 没重叠：`elapsed_seconds` > 90（agent 顺序发，或沙箱串行化 exec） |
| `sb-fs-small` | 600 个小文件写入 | 丢文件、写坏 |
| `sb-fs-upload` | 工作区写入约 1 GiB | 大文件写失败、截断 |
| `sb-fs-download` | 大文件写完后再完整读回 | 没跑读回，或读回内容不一致 |
| `sb-stdout` | 一次命令保住约 1 GiB 标准输出 | 标准输出被截断 |

以下仍留在目录里，**不在正式套件**，不参与 Codex 用时对比：

- `sb-cold-start`（冷启动）
- `sb-net-rtt` / `sb-net-download` / `sb-net-upload`（公网 Cloudflare；用户 ISP 带宽会主导用时）

目录名 `sb-fs-upload` / `sb-fs-download` 沿用旧名：这里分别指大文件**写**与**读回**，不是浏览器下载。

## 和 Codex 对比时

- 同一份 `instruction.md`、同一套 `tests/`
- 只对比 tests 通过的 run
- 用同一规则写 `timing.json`（点发送 → 文件齐）
- 先看通过/失败和 `judge.md` 里的归因，再看秒数

## Playwright

```bash
npm install
npx playwright install chromium
node gui/send-task.mjs tasks/sb-tool-calls
```

脚本把用时写到 `runs/<题目>/output/timing.json`。再和产物一起跑 `check_files.sh`。

带 Docker/CLI 的一版在 `master`。
