import hashlib
import json
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))
BLOCK = bytes(i % 251 for i in range(64 * 1024))

def expected_sha(size):
    digest = hashlib.sha256()
    full, rem = divmod(size, len(BLOCK))
    for _ in range(full):
        digest.update(BLOCK)
    if rem:
        digest.update(BLOCK[:rem])
    return digest.hexdigest()

def main():
    size = int(os.environ.get("BENCH_FS_UPLOAD_BYTES", str(1024 * 1024 * 1024)))
    path = APP / "incoming.bin"
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    matched = len(data) == size and digest == expected_sha(size)
    (APP / "upload_report.json").write_text(json.dumps({
        "bytes": len(data),
        "sha256": digest,
        "matched": matched,
    }))
    if not matched:
        raise SystemExit("uploaded file does not match")

if __name__ == "__main__":
    main()
