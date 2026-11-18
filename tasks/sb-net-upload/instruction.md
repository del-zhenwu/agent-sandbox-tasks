Use the Python already installed in this environment. Do not modify `/app/probe.py`.

Run this command once:

```
python3 /app/probe.py
```

That run sends 1073741824 bytes to `https://speed.cloudflare.com/__up`. The body repeats a 65536-byte block, and byte `i` of the block is `i % 251`. The HTTP status must be 200, and the response header `cf-meta-upload-bytes` must equal 1073741824. `/app/net_upload_report.json` records the result.

You have 1800 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
