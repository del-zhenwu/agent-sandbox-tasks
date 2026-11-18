# sb-fs-small 核对

暴露问题：
- 缺小文件 → 写入工具调用失败或沙箱丢文件
- 字节不对 → 写入损坏
- 用时过长 → 小文件写入往返慢

核对产物（只在 tests 里做，不要把核对脚本交给 agent）：
- 600 个小文件字节正确

先跑 tests（`bash scripts/check_files.sh tasks/sb-fs-small /含有output的目录`）。失败就记这题失败，不比速度。
通过后再看 `output/timing.json` 的 `elapsed_seconds`。和 Codex 或其他 agent 对比时，只用通过的那几次。相差不到 60 秒，不判断谁更快。
