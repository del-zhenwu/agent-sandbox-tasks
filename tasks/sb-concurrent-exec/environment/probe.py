import os
import sys
import time
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def main():
    index = sys.argv[1]
    if not index.isdigit():
        raise SystemExit("index must be an integer")
    time.sleep(float(os.environ.get("BENCH_SLEEP_SECONDS", "5")))
    out = APP / "done"
    out.mkdir(parents=True, exist_ok=True)
    (out / index).write_text(f"{index}\n")

if __name__ == "__main__":
    main()
