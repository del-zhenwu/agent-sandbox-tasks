# sandbox-bench-tasks

10 道题，测沙箱和外面的调用程序（harness）之间传命令、传文件、访问外网要花多久。每道只测一件事。目录格式与 [Terminal-Bench](https://github.com/harbor-framework/terminal-bench) 当前的 Harbor 任务相同。

墙钟相差不到 1 分钟，不拿来比高低。怎么计时写在下面的题目表里。`instruction.md` 只写沙箱里要留下什么，写法与 Harbor 的题目说明相同。`solution/solve.sh` 只核对结果。`environment/probe.py` 打进镜像。测试在另一个容器里跑，只读取 `task.toml` 的 `artifacts`。

```text
tasks/<名字>/
├── instruction.md
├── task.toml
├── environment/
│   ├── Dockerfile
│   └── probe.py
├── solution/
│   └── solve.sh
└── tests/
    ├── Dockerfile
    ├── test.sh
    └── test_outputs.py
```

本地把次数和字节缩小，只核对内容：

```bash
bash scripts/check_local.sh
```

## 题目

通过条件写在各题的 `instruction.md`。下表的规模比出处里的原题大，用来把墙钟差拉到 1 分钟以上。

| 目录 | 规模 | 出处 |
|---|---|---|
| `sb-tool-calls` | 1000 次单独调用，每次写一行 | [agent-sandbox-benchmark](https://github.com/FrigaZzz/agent-sandbox-benchmark) 的 `session_state`（原为 3 次） |
| `sb-concurrent-exec` | 80 次一起发出，每次等待 5 秒 | [sandbox-test](https://github.com/nickaggarwal/sandbox-test) 的 Concurrent Exec（原为 4 步，报告 2026-03-22） |
| `sb-cold-start` | 新建并销毁沙箱 60 次 | 同上 benchmark 的 `cold_start`；[ComputeSDK TTI](https://github.com/computesdk/benchmarks)（计时不含销毁）；[coldtally](https://coldtally.com/startup-times/)（2026-10-22，10 次：E2B 252 ms、Modal 484 ms、Daytona 1072 ms） |
| `sb-fs-small` | 600 个 32 KiB 文件，写入再逐个读回 | sandbox-test 的 Filesystem I/O（原为上传 5 个、下载 9 个） |
| `sb-fs-upload` | 经文件接口写入 1 GiB | 同上，API 上传原为 10MB（4.1–47.5 秒） |
| `sb-fs-download` | 经文件接口读回 1 GiB | 同上，API 下载原为 100MB（E2B 8.1 秒，Modal 51.6 秒） |
| `sb-stdout` | 一次命令输出 1 GiB，由 harness 收齐 | agent-sandbox-benchmark 的 `output_fidelity`（原为 131072 字节；AWS 少最后 1 字节，Blaxel 约停在 64 KiB） |
| `sb-net-rtt` | 沙箱内请求 `https://example.com` 1000 次 | sandbox-test 的 HTTP 延迟（原约 18–61 ms，只测几次） |
| `sb-net-download` | 沙箱从 Cloudflare `__down` 下载 1 GiB | sandbox-test 的沙箱内下载（100MB 约 54–135 MB/s）；[hpc-sandbox-benchmarks](https://github.com/starslingdev/hpc-sandbox-benchmarks) 的 iperf3 广域网下载 |
| `sb-net-upload` | 沙箱向 Cloudflare `__up` 发送 1 GiB | sandbox-test 的沙箱内上传（5MB 约 0.74–5.5 MB/s）；hpc 的 iperf3 广域网上传 |

按 sandbox-test 的测速，公网下载 1 GiB 往往只有十几秒；上传和文件接口的 1 GiB 才会到几分钟。hpc 的 iperf3 是沙箱内部网速（每秒几百 MB 到约 1 GB），不代替文件接口。

## 相关评测

- [computesdk/benchmarks](https://github.com/computesdk/benchmarks)（MIT）：最多 100 个沙箱一起创建，计时到第一条命令。另有 Dax（克隆、安装、类型检查）。
- [starslingdev/hpc-sandbox-benchmarks](https://github.com/starslingdev/hpc-sandbox-benchmarks)：固定 4 vCPU、8 GiB、40 GB，测沙箱内的磁盘、内存和 iperf3。该轮榜单完成 800/840。
- [nickaggarwal/sandbox-test](https://github.com/nickaggarwal/sandbox-test)：Daytona、E2B、Blaxel、Modal、Runloop、TensorLake 的文件、并发和出网。
- [FrigaZzz/agent-sandbox-benchmark](https://github.com/FrigaZzz/agent-sandbox-benchmark)：标准输出是否缺字节，以及同一次沙箱里文件还在不在。

暂停后恢复，以及一次创建很多个沙箱，上面的项目里有，这里还没有。
