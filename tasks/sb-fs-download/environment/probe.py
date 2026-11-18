import hashlib
import json
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))
BLOCK = bytes(i % 251 for i in range(64 * 1024))

def write_pattern(path, size):
    digest = hashlib.sha256()
    with path.open("wb") as handle:
        full, rem = divmod(size, len(BLOCK))
        for _ in range(full):
            handle.write(BLOCK)
            digest.update(BLOCK)
        if rem:
            tail = BLOCK[:rem]
            handle.write(tail)
            digest.update(tail)
    return digest.hexdigest()

def main():
    size = int(os.environ.get("BENCH_FS_DOWNLOAD_BYTES", str(1024 * 1024 * 1024)))
    path = APP / "outgoing.bin"
    digest = write_pattern(path, size)
    receipt = {"bytes": size, "sha256": digest}
    (APP / "download_receipt.json").write_text(json.dumps(receipt))

if __name__ == "__main__":
    main()
