# sb-tool-calls

工作目录是包含 `inputs/` 的文件夹，平台已注入环境变量 `SANDBOX_BENCH_NONCES`（50 个一次性逗号分隔编号）。

## Inputs

- `inputs/probe.py`

不得修改 `inputs/`。

## 操作

对每个注入的编号 `n`，以**独立的工具调用**执行：

```bash
python3 inputs/probe.py $n
```

不得把多次执行合并为循环、脚本或批处理。每次执行必须是单独的一次工具调用。

## 结果文件

1. `output/calls/<n>`，内容为 `call-<n>` 加换行
2. `output/call_log.txt`，每个编号一行，顺序不限
