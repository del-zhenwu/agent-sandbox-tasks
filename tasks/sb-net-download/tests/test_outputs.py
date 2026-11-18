import hashlib
import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"
SIZE = 1024 * 1024 * 1024

def test_net_download():
    report = json.loads((APP / "net_download_report.json").read_text())
    data = (APP / "download.bin").read_bytes()
    assert report["status"] == 200
    assert len(data) == SIZE == report["bytes"]
    assert report["sha256"] == hashlib.sha256(data).hexdigest()

def test_timing_present():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
