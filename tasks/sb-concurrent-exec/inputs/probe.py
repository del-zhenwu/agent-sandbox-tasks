import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        raise SystemExit(1)
    nonce = sys.argv[1]
    time.sleep(5)
    done = OUT / "done"
    done.mkdir(parents=True, exist_ok=True)
    (done / nonce).write_text(f"{nonce}\n")


if __name__ == "__main__":
    main()
