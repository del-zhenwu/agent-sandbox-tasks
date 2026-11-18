# sb-fs-download 核对

量的是大文件完整读回。

暴露问题：
- 有 `write_report` 无 `read_report` → agent 没跑读回
- 两个报告哈希不一致 → 读回截断或损坏
- 用时过长 → 大文件读路径慢

核对在 tests 里做，不要把合格标准写进给 agent 的题目。

先跑 tests（`bash scripts/check_files.sh tasks/sb-fs-download /含有output的目录`）。失败就记这题失败，不比速度。
通过后再看 `output/timing.json` 的 `elapsed_seconds`。和 Codex 或其他 agent 对比时，只用通过的那几次。相差不到 60 秒，不判断谁更快。
