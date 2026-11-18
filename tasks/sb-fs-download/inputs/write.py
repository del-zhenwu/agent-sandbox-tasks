import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
SIZE = 1024 * 1024 * 1024
BLOCK = bytes(i % 251 for i in range(64 * 1024))

def main():
    path = OUT / "large.bin"
    digest = hashlib.sha256()
    with path.open("wb") as handle:
        full, rem = divmod(SIZE, len(BLOCK))
        for _ in range(full):
            handle.write(BLOCK)
            digest.update(BLOCK)
        if rem:
            tail = BLOCK[:rem]
            handle.write(tail)
            digest.update(tail)
    (OUT / "write_report.json").write_text(json.dumps({
        "bytes": SIZE,
        "sha256": digest.hexdigest(),
    }))

if __name__ == "__main__":
    main()
