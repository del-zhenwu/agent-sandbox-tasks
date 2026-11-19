import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = ROOT / "inputs" / "payload.bin"
    target = OUT / "large.bin"
    shutil.copyfile(source, target)
    data = target.read_bytes()
    (OUT / "write_report.json").write_text(json.dumps({
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "path": "output/large.bin",
    }))


if __name__ == "__main__":
    main()
