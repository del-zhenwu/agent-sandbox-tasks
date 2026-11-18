import json
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def test_upload_report():
    size = int(os.environ.get("BENCH_FS_UPLOAD_BYTES", str(1024 * 1024 * 1024)))
    report = json.loads((APP / "upload_report.json").read_text())
    assert report["matched"] is True
    assert report["bytes"] == size
