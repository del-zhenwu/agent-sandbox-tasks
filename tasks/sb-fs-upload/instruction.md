# sb-fs-upload

工作目录是包含 `inputs/` 的文件夹。

## Inputs

- `inputs/probe.py`
- `inputs/payload.bin`（平台本次 run 随机生成，内容不可预测）

不得修改 `inputs/`。

## 操作

```bash
python3 inputs/probe.py
```

探针会把 `payload.bin` 复制到 `output/large.bin`，并生成写入收据。

## 结果文件

1. `output/large.bin`
2. `output/write_report.json`
