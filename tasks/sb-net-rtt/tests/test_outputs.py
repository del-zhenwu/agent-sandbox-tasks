import json
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def test_all_statuses_ok():
    repeats = int(os.environ.get("BENCH_HTTP_REQUESTS", "1000"))
    report = json.loads((APP / "rtt_report.json").read_text())
    assert report["http_statuses"] == [200] * repeats
    assert report["elapsed_seconds"] >= 0
