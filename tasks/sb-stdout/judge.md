# sb-stdout 核对

暴露问题：
- 捕获文件偏短 → 工具或沙箱截断了标准输出
- 没有收据 → 命令没跑完

核对产物：
- `output/captured_stdout.bin` 正好 1073741824 字节
- 与 `stdout_receipt.json` 的 sha256 一致

先跑 tests（`bash scripts/check_files.sh tasks/<名> /含有output的目录`）。失败就记这题失败，不比速度。
通过后再看 `output/timing.json` 的 `elapsed_seconds`。和 Codex 或其他 agent 对比时，只用通过的那几次。相差不到 60 秒，不判断谁更快。
