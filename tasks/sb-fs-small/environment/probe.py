import os
import sys
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))
SIZE = 32 * 1024
BASE = bytes(i % 251 for i in range(SIZE))

def small_file(index):
    data = bytearray(BASE)
    data[0:4] = int(index).to_bytes(4, "little")
    return bytes(data)

def main():
    count = int(os.environ.get("BENCH_SMALL_FILES", "600"))
    out = APP / "small"
    out.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["write-all"]:
        for index in range(count):
            (out / str(index)).write_bytes(small_file(index))
        return
    raise SystemExit("local check uses: python3 probe.py write-all")

if __name__ == "__main__":
    main()
