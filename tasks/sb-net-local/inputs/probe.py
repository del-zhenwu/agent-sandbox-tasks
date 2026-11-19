import hashlib
import json
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    url = os.environ.get("SANDBOX_BENCH_NET_URL", "")
    if not url:
        raise SystemExit(1)
    with urllib.request.urlopen(url, timeout=20) as response:
        data = response.read()
    target = OUT / "net_response.bin"
    target.write_bytes(data)
    (OUT / "net_receipt.json").write_text(json.dumps({
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }))


if __name__ == "__main__":
    main()
