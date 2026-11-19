# sb-net-local

工作目录是包含 `inputs/` 的文件夹。平台已注入 `SANDBOX_BENCH_NET_URL`（本次 run 随机生成本地 HTTP 地址，题面不出现）。

## Inputs

- `inputs/probe.py`

不得修改 `inputs/`。

## 操作

```bash
python3 inputs/probe.py
```

探针会访问注入的本地地址，把响应写到 `output/net_response.bin`，并生成收据。

## 结果文件

1. `output/net_response.bin`
2. `output/net_receipt.json`
