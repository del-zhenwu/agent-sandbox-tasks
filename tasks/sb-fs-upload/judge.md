# sb-fs-upload 核对

量的是大文件写入（目录名沿用 upload）。

暴露问题：
- 没有 `large.bin` 或大小不对 → 沙箱写大文件失败，或 agent 没跑完
- 收据哈希不一致 → 写入截断或损坏

核对产物：
- `output/large.bin` 正好 1073741824 字节
- `output/write_report.json` 的 `sha256` 与文件一致

先跑 tests（`bash scripts/check_files.sh tasks/<名> /含有output的目录`）。失败就记这题失败，不比速度。
通过后再看 `output/timing.json` 的 `elapsed_seconds`。和 Codex 或其他 agent 对比时，只用通过的那几次。相差不到 60 秒，不判断谁更快。
