import hashlib
import json
import os
import sys
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))
BLOCK = bytes(i % 251 for i in range(64 * 1024))

def main():
    size = int(os.environ.get("BENCH_STDOUT_BYTES", str(1024 * 1024 * 1024)))
    digest = hashlib.sha256()
    out = sys.stdout.buffer
    full, rem = divmod(size, len(BLOCK))
    for _ in range(full):
        out.write(BLOCK)
        digest.update(BLOCK)
    if rem:
        tail = BLOCK[:rem]
        out.write(tail)
        digest.update(tail)
    out.flush()
    (APP / "stdout_receipt.json").write_text(json.dumps({
        "bytes": size,
        "sha256": digest.hexdigest(),
    }))

if __name__ == "__main__":
    main()
