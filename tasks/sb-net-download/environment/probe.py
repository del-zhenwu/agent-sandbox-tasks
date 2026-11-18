import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def main():
    size = int(os.environ.get("BENCH_NET_DOWNLOAD_BYTES", str(1024 * 1024 * 1024)))
    base = os.environ.get("BENCH_DOWNLOAD_URL", "https://speed.cloudflare.com/__down")
    url = base if "?" in base else f"{base}?bytes={size}"
    dest = APP / "download.bin"
    digest = hashlib.sha256()
    total = 0
    started = time.perf_counter()
    request = urllib.request.Request(url, headers={"User-Agent": "sandbox-bench"})
    with urllib.request.urlopen(request, timeout=900) as response:
        status = response.status
        with dest.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
                digest.update(chunk)
                total += len(chunk)
    report = {
        "status": status,
        "bytes": total,
        "sha256": digest.hexdigest(),
        "elapsed_seconds": time.perf_counter() - started,
    }
    (APP / "net_download_report.json").write_text(json.dumps(report))
    if status != 200 or total != size:
        raise SystemExit("download size mismatch")

if __name__ == "__main__":
    main()
