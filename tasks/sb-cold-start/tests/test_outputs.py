import json
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"

def test_ready_file():
    text = (APP / "ready.txt").read_text()
    assert text.startswith("SANDBOX_READY ")
    assert text.endswith("\n")

def test_timing():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
    assert report["started_at"]
    assert report["ended_at"]
