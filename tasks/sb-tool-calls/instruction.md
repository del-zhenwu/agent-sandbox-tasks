# sb-tool-calls

工作目录是包含 `inputs/` 的文件夹。

## Inputs

- `inputs/probe.py`

不得修改 `inputs/`。

## 操作

对每个整数 `i`（0 到 999）执行：

```bash
python3 inputs/probe.py $i
```

## 结果文件

1. `output/calls/0` … `output/calls/999`，内容为 `call-<编号>` 加换行
2. `output/call_log.txt`，正好 1000 行，每行一个编号，顺序不限
