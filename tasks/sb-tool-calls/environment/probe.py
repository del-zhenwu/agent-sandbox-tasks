
import sys
from pathlib import Path
import os
APP = Path(os.environ.get("APP_ROOT", "/app"))

def main():
    index = sys.argv[1]
    if not index.isdigit():
        raise SystemExit("index must be an integer")
    out = APP / "calls"
    out.mkdir(parents=True, exist_ok=True)
    (out / index).write_text(f"call-{index}\n")

if __name__ == "__main__":
    main()
