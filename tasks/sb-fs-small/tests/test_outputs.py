import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))
SIZE = 32 * 1024
BASE = bytes(i % 251 for i in range(SIZE))

def small_file(index):
    data = bytearray(BASE)
    data[0:4] = int(index).to_bytes(4, "little")
    return bytes(data)

def test_small_files():
    count = int(os.environ.get("BENCH_SMALL_FILES", "600"))
    for index in range(count):
        assert (APP / "small" / str(index)).read_bytes() == small_file(index)
