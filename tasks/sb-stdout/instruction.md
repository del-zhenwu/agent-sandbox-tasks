Use the Python already installed in this environment. Do not modify `/app/probe.py`.

Run `python3 /app/probe.py` once and keep its entire standard output. The output is exactly 1073741824 bytes: one 65536-byte block repeated, where byte `i` of the block is `i % 251`. The same command writes `/app/stdout_receipt.json`.

The saved output must be exactly 1073741824 bytes, and its SHA-256 must equal the `sha256` field in `/app/stdout_receipt.json`.

You have 1800 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
