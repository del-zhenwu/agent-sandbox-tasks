import hashlib
import json
import time
import urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
SIZE = 1024 * 1024 * 1024
URL = f"https://speed.cloudflare.com/__down?bytes={SIZE}"

def main():
    dest = OUT / "download.bin"
    digest = hashlib.sha256()
    total = 0
    started = time.perf_counter()
    request = urllib.request.Request(URL, headers={"User-Agent": "sandbox-bench"})
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
    (OUT / "net_download_report.json").write_text(json.dumps(report))
    if status != 200 or total != SIZE:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
