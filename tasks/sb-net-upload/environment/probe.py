import hashlib
import http.client
import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse
APP = Path(os.environ.get("APP_ROOT", "/app"))
BLOCK = bytes(i % 251 for i in range(64 * 1024))

def payload(size):
    full, rem = divmod(size, len(BLOCK))
    return BLOCK * full + BLOCK[:rem]

def main():
    size = int(os.environ.get("BENCH_NET_UPLOAD_BYTES", str(1024 * 1024 * 1024)))
    url = os.environ.get("BENCH_UPLOAD_URL", "https://speed.cloudflare.com/__up")
    body = payload(size)
    digest = hashlib.sha256(body).hexdigest()
    parsed = urlparse(url)
    started = time.perf_counter()
    connection = http.client.HTTPSConnection(parsed.hostname, timeout=900)
    path = parsed.path or "/"
    connection.request(
        "POST",
        path,
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
    (APP / "net_upload_report.json").write_text(json.dumps(report))
    connection.close()
    if response.status != 200 or report["upload_bytes"] != size:
        raise SystemExit("upload was not accepted")

if __name__ == "__main__":
    main()
