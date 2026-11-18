import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
SIZE = 32 * 1024
COUNT = 600
BASE = bytes(i % 251 for i in range(SIZE))

def small_file(index):
    data = bytearray(BASE)
    data[0:4] = int(index).to_bytes(4, "little")
    return bytes(data)

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        raise SystemExit(1)
    index = int(sys.argv[1])
    if index >= COUNT:
        raise SystemExit(1)
    out = OUT / "small"
    out.mkdir(parents=True, exist_ok=True)
    (out / str(index)).write_bytes(small_file(index))

if __name__ == "__main__":
    main()
