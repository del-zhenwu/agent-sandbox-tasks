Place `/app/incoming.bin` in the environment before running any command. The file is exactly 1073741824 bytes, made by repeating one 65536-byte block. Byte `i` inside that block is `i % 251`. Do not create this file with a command inside the environment.

Then run `python3 /app/probe.py` once. Do not modify `/app/probe.py`.

`/app/upload_report.json` must report `"matched": true` and `"bytes": 1073741824`.

You have 1800 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
