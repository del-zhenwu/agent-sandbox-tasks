import hashlib
import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"
SIZE = 1024 * 1024 * 1024

def test_write_and_full_read():
    data = (APP / "large.bin").read_bytes()
    write_report = json.loads((APP / "write_report.json").read_text())
    read_report = json.loads((APP / "read_report.json").read_text())
    digest = hashlib.sha256(data).hexdigest()
    assert len(data) == SIZE
    assert write_report["bytes"] == SIZE
    assert write_report["sha256"] == digest
    assert read_report["bytes"] == SIZE
    assert read_report["sha256"] == digest

def test_timing_present():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
