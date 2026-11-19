# sb-concurrent-exec

工作目录是包含 `inputs/` 的文件夹，平台已注入环境变量 `SANDBOX_BENCH_NONCES`（20 个一次性逗号分隔编号）。

## Inputs

- `inputs/probe.py`

不得修改 `inputs/`。

## 操作

对每个注入的编号 `n`，以**独立的工具调用**执行：

```bash
python3 inputs/probe.py $n
```

这 20 次调用必须并行发出（每次仍是单独一次工具调用），再等待全部结束。不得合并为循环、脚本或批处理。

## 结果文件

1. `output/done/<n>`，内容为编号加换行
