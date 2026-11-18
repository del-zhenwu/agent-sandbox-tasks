# sb-tool-calls 核对

暴露问题：
- 文件不齐 → agent 没发够次数，或沙箱丢了写入
- 文件齐但用时接近「一条脚本写完」→ agent 可能合并调用；和 Codex 对比时看调用次数与用时
- 文件齐且用时明显更长 → 单次工具调用或沙箱往返慢

核对产物：
- `output/calls/0`–`999` 内容正确
- `output/call_log.txt` 正好覆盖 0–999

先跑 tests（`bash scripts/check_files.sh tasks/<名> /含有output的目录`）。失败就记这题失败，不比速度。
通过后再看 `output/timing.json` 的 `elapsed_seconds`。和 Codex 或其他 agent 对比时，只用通过的那几次。相差不到 60 秒，不判断谁更快。
