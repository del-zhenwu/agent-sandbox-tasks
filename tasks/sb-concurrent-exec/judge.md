# sb-concurrent-exec 核对

暴露问题：
- 缺文件 → 有的调用没落地
- 文件齐但 `elapsed_seconds` > 90 → agent 顺序发，或沙箱把 exec 串行化了（这是本题要抓的）
- 文件齐且用时大约 5–20 秒 → 重叠执行正常

核对产物：
- `output/done/0`–`79`
- `output/timing.json` 的 `elapsed_seconds` ≤ 90

先跑 tests（`bash scripts/check_files.sh tasks/<名> /含有output的目录`）。失败就记这题失败，不比速度。
通过后再看 `output/timing.json` 的 `elapsed_seconds`。和 Codex 或其他 agent 对比时，只用通过的那几次。相差不到 60 秒，不判断谁更快。
