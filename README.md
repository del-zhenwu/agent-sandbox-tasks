# sandbox-bench-tasks

这一支默认用图形界面。不建镜像，也不在命令行里启动 agent。

打开 agent 的窗口，把题目说明贴进去，把 `probe.py` 放进它的工作区，点发送。从点发送记到它做完。两家差不到 1 分钟，不比谁快。

也可以让 Playwright 替你打开同一个窗口、贴上题目并点发送。它不会自己判断做完没有。你看着界面，做完后回到终端按回车，它把用时写到 `runs/<题目>/timing.json`。

```text
tasks/<名字>/
├── instruction.md    # 贴进输入框的说明
├── probe.py          # 放进 agent 工作区的 /app/probe.py
├── task.toml         # 做完后要拿回来的文件
└── tests/test_outputs.py
```

## 人来做

1. 打开 agent 的图形界面。
2. 把 `tasks/<名字>/probe.py` 放到它能读到的 `/app/probe.py`。
3. 把 `instruction.md` 全文贴进输入框，点发送，同时开始记时间。
4. 它做完后停止记时。`sb-cold-start` 要新建 60 次，每次都是新的工作区，做完就关掉，60 次时间相加。
5. 按 `task.toml` 里的 `artifacts` 把文件拷出来。
6. 核对内容：`bash scripts/check_files.sh tasks/<名字> /拷出来的目录`。这一步只看文件，不会去打开 agent。

## 用 Playwright 发题

复制 `gui/config.example.json` 为 `gui/config.json`，填上界面地址、输入框、发送按钮。能传文件的话，再填文件选择框，脚本会带上 `probe.py`。

```bash
npm install
npx playwright install chromium
node gui/send-task.mjs tasks/sb-tool-calls
```

`doneSelector` 留空。脚本发出去之后会等你按回车，再记下结束时间。

## 题目

| 目录 | 规模 | 出处 |
|---|---|---|
| `sb-tool-calls` | 1000 次单独调用，每次写一行 | [agent-sandbox-benchmark](https://github.com/FrigaZzz/agent-sandbox-benchmark) 的 `session_state`（原为 3 次） |
| `sb-concurrent-exec` | 80 次一起发出，每次等待 5 秒 | [sandbox-test](https://github.com/nickaggarwal/sandbox-test) 的 Concurrent Exec（原为 4 步，报告 2026-03-22） |
| `sb-cold-start` | 新建并销毁沙箱 60 次 | 同上 benchmark 的 `cold_start`；[ComputeSDK TTI](https://github.com/computesdk/benchmarks)；[coldtally](https://coldtally.com/startup-times/)（2026-10-22：E2B 252 ms、Modal 484 ms、Daytona 1072 ms） |
| `sb-fs-small` | 600 个 32 KiB 文件，写入再逐个读回 | sandbox-test 的 Filesystem I/O（原为上传 5 个、下载 9 个） |
| `sb-fs-upload` | 经文件接口写入 1 GiB | 同上，API 上传原为 10MB（4.1–47.5 秒） |
| `sb-fs-download` | 经文件接口读回 1 GiB | 同上，API 下载原为 100MB（E2B 8.1 秒，Modal 51.6 秒） |
| `sb-stdout` | 一次命令输出 1 GiB，由界面收齐 | agent-sandbox-benchmark 的 `output_fidelity`（原为 131072 字节） |
| `sb-net-rtt` | 沙箱内请求 `https://example.com` 1000 次 | sandbox-test 的 HTTP 延迟（原约 18–61 ms） |
| `sb-net-download` | 从 Cloudflare `__down` 下载 1 GiB | sandbox-test 的沙箱内下载；[hpc-sandbox-benchmarks](https://github.com/starslingdev/hpc-sandbox-benchmarks) 的 iperf3 下载 |
| `sb-net-upload` | 向 Cloudflare `__up` 发送 1 GiB | sandbox-test 的沙箱内上传；hpc 的 iperf3 上传 |

带镜像、用命令行跑的那一版在 `master`。
