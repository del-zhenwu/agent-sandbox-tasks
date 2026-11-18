import hashlib
import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"
SIZE = 1024 * 1024 * 1024

def test_large_write():
    report = json.loads((APP / "write_report.json").read_text())
    data = (APP / "large.bin").read_bytes()
    assert len(data) == SIZE == report["bytes"]
    assert report["sha256"] == hashlib.sha256(data).hexdigest()

def test_timing_present():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
