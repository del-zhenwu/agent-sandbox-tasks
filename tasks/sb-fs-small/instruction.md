Create `/app/small/0` through `/app/small/599`. Do not modify `/app/probe.py`.

Each file is exactly 32768 bytes. The byte at position `p` is `p % 251`. After that pattern is filled, replace the first 4 bytes with the file index as an unsigned little-endian integer.

You have 1800 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
