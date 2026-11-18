import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"

def test_rtt():
    report = json.loads((APP / "rtt_report.json").read_text())
    assert report["http_statuses"] == [200] * 1000

def test_timing_present():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
