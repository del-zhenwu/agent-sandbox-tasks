import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"

def test_call_files():
    for index in range(1000):
        assert (APP / "calls" / str(index)).read_text() == f"call-{index}\n"

def test_call_log_has_one_line_per_index():
    lines = [line for line in (APP / "call_log.txt").read_text().splitlines() if line != ""]
    assert sorted(lines) == [str(i) for i in range(1000)]

def test_timing_present():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
    assert report["started_at"] and report["ended_at"]
