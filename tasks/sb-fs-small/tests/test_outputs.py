import json
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", ".")) / "output"
SIZE = 32 * 1024
BASE = bytes(i % 251 for i in range(SIZE))

def small_file(index):
    data = bytearray(BASE)
    data[0:4] = int(index).to_bytes(4, "little")
    return bytes(data)

def test_small_files():
    for index in range(600):
        assert (APP / "small" / str(index)).read_bytes() == small_file(index)

def test_timing_present():
    report = json.loads((APP / "timing.json").read_text())
    assert isinstance(report["elapsed_seconds"], (int, float))
    assert report["elapsed_seconds"] >= 0
