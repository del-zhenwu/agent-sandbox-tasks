import hashlib
import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"
SIZE = 1024 * 1024 * 1024

def test_stdout_captured():
    receipt = json.loads((APP / "stdout_receipt.json").read_text())
    data = (APP / "captured_stdout.bin").read_bytes()
    assert len(data) == SIZE == receipt["bytes"]
    assert receipt["sha256"] == hashlib.sha256(data).hexdigest()

def test_timing_present():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
