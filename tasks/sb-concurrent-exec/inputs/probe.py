import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        raise SystemExit(1)
    index = sys.argv[1]
    time.sleep(5)
    out = OUT / "done"
    out.mkdir(parents=True, exist_ok=True)
    (out / index).write_text(f"{index}\n")

if __name__ == "__main__":
    main()
