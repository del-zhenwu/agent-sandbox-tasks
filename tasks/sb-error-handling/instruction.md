# sb-error-handling

工作目录是包含 `inputs/` 的文件夹。平台已注入 `SANDBOX_BENCH_ERROR_MARKER`（每次 run 随机，题面不出现）。

## Inputs

- `inputs/probe_fail.py`

不得修改 `inputs/`。

## 操作

执行下面这条命令，它**预期会失败**：

```bash
python3 inputs/probe_fail.py
```

要求：

1. 记录真实退出码与 stderr 标记，不得当作成功。
2. 命令非零退出后**流程必须继续**，不许中断后续步骤。

## 结果文件

1. `output/error_report.json`：`exit_code`、`stderr_marker`（只写标记本身）、`partial_bytes`
2. `output/after.txt`，内容为 `continued` 加换行
