import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"
SIZE = 1024 * 1024 * 1024

def test_net_upload():
    report = json.loads((APP / "net_upload_report.json").read_text())
    assert report["status"] == 200
    assert report["upload_bytes"] == SIZE

def test_timing_present():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
