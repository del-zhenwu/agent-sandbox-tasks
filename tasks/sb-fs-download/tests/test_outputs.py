import hashlib
import json
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def test_outgoing_matches_receipt():
    size = int(os.environ.get("BENCH_FS_DOWNLOAD_BYTES", str(1024 * 1024 * 1024)))
    receipt = json.loads((APP / "download_receipt.json").read_text())
    data = (APP / "outgoing.bin").read_bytes()
    assert receipt["bytes"] == size == len(data)
    assert receipt["sha256"] == hashlib.sha256(data).hexdigest()
