import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"

def main():
    path = OUT / "large.bin"
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            total += len(chunk)
    (OUT / "read_report.json").write_text(json.dumps({
        "bytes": total,
        "sha256": digest.hexdigest(),
    }))

if __name__ == "__main__":
    main()
