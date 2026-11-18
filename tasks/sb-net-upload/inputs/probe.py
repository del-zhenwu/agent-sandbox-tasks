import hashlib
import http.client
import json
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
SIZE = 1024 * 1024 * 1024
BLOCK = bytes(i % 251 for i in range(64 * 1024))

def payload(size):
    full, rem = divmod(size, len(BLOCK))
    return BLOCK * full + BLOCK[:rem]

def main():
    body = payload(SIZE)
    digest = hashlib.sha256(body).hexdigest()
    started = time.perf_counter()
    connection = http.client.HTTPSConnection("speed.cloudflare.com", timeout=900)
    connection.request(
        "POST",
        "/__up",
        body=body,
        headers={
            "Content-Type": "application/octet-stream",
            "User-Agent": "sandbox-bench",
        },
    )
    response = connection.getresponse()
    response.read()
    received = response.getheader("cf-meta-upload-bytes")
    report = {
        "status": response.status,
        "upload_bytes": None if received is None else int(received),
        "sha256": digest,
        "elapsed_seconds": time.perf_counter() - started,
    }
    (OUT / "net_upload_report.json").write_text(json.dumps(report))
    connection.close()
    if response.status != 200 or report["upload_bytes"] != SIZE:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
