# sb-fs-upload 核对

`inputs/payload.bin` 由 runner 每次随机生成，平台侧保存原始哈希；收据必须匹配**实际写出的字节**。

- `test_agent_large_write` 失败 → 写大文件失败、截断，或 agent 没跑探针
- `test_harness_private_original` 失败 → 平台随机原件缺失，或 trace 没有探针执行记录
- 哈希对上平台随机值 → 沙箱确实完成了这么多字节的真实写入

失败看 `scores.json` 的 `attribution`。通过后才比秒数，相差不到 60 秒不判谁更快。
