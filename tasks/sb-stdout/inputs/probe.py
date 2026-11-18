import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
SIZE = 1024 * 1024 * 1024
BLOCK = bytes(i % 251 for i in range(64 * 1024))

def main():
    digest = hashlib.sha256()
    out = sys.stdout.buffer
    full, rem = divmod(SIZE, len(BLOCK))
    for _ in range(full):
        out.write(BLOCK)
        digest.update(BLOCK)
    if rem:
        tail = BLOCK[:rem]
        out.write(tail)
        digest.update(tail)
    out.flush()
    (OUT / "stdout_receipt.json").write_text(json.dumps({
        "bytes": SIZE,
        "sha256": digest.hexdigest(),
    }))

if __name__ == "__main__":
    main()
