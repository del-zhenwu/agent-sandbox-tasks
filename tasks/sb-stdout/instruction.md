# sb-stdout

工作目录是包含 `inputs/`、`output/` 的文件夹。

## Inputs

- `inputs/probe.py`

不得修改 `inputs/`。

## 操作

```bash
python3 inputs/probe.py > output/captured_stdout.bin
```

探针会同时写 `output/stdout_receipt.json`。

## 结果文件

1. `output/captured_stdout.bin`
2. `output/stdout_receipt.json`
