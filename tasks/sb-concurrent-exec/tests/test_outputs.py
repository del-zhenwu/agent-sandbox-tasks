import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"

def test_done_files():
    for index in range(80):
        assert (APP / "done" / str(index)).read_text() == f"{index}\n"

def test_timing_shows_overlap():
    """串行约 400 秒；能重叠应远小于该值。超过 90 秒视为没有真正并行。"""
    report = json.loads((APP / "timing.json").read_text())
    assert report["elapsed_seconds"] <= 90, (
        f"elapsed_seconds={report['elapsed_seconds']} > 90；"
        "命令像是一条条跑完的，agent 或沙箱没有重叠执行"
    )
