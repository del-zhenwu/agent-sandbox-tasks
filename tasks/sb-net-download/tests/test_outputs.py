import hashlib
import json
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def test_download_file():
    size = int(os.environ.get("BENCH_NET_DOWNLOAD_BYTES", str(1024 * 1024 * 1024)))
    report = json.loads((APP / "net_download_report.json").read_text())
    data = (APP / "download.bin").read_bytes()
    assert report["status"] == 200
    assert report["bytes"] == size == len(data)
    assert report["sha256"] == hashlib.sha256(data).hexdigest()
