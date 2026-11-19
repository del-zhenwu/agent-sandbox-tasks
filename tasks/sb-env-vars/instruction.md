# sb-env-vars

工作目录是包含 `inputs/` 的文件夹。平台已把 `SANDBOX_BENCH_TOKEN` 和 `SANDBOX_BENCH_CHALLENGE` **注入执行环境**，题面不包含具体值。

## Inputs

- `inputs/probe.py`

不得修改 `inputs/`。

## 操作

直接执行（值由环境提供，不得硬编码、不得写进 `inputs/`）：

```bash
python3 inputs/probe.py
```

探针会读取环境并计算摘要。

## 结果文件

1. `output/env_report.json`，包含 `token_present`、`challenge`、`computed_hash`
