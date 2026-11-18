Use the Python already installed in this environment. Do not modify `/app/probe.py`.

Run this command once:

```
python3 /app/probe.py
```

That run downloads `https://speed.cloudflare.com/__down?bytes=1073741824` and writes `/app/download.bin`. The file must be exactly 1073741824 bytes. `/app/net_download_report.json` must record status 200, that byte count, and the SHA-256 of `/app/download.bin`.

You have 1800 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
