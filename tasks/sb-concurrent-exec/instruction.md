# sb-concurrent-exec

工作目录是包含 `inputs/` 的文件夹。

## Inputs

- `inputs/probe.py`

不得修改 `inputs/`。

## 操作

对每个整数 `i`（0 到 79）执行：

```bash
python3 inputs/probe.py $i
```

这 80 条先全部发出，再等待它们结束。

## 结果文件

1. `output/done/0` … `output/done/79`，内容为编号加换行
