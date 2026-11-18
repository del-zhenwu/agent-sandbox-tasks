import json
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def test_upload_accepted():
    size = int(os.environ.get("BENCH_NET_UPLOAD_BYTES", str(1024 * 1024 * 1024)))
    report = json.loads((APP / "net_upload_report.json").read_text())
    assert report["status"] == 200
    assert report["upload_bytes"] == size
    assert isinstance(report["sha256"], str) and len(report["sha256"]) == 64
