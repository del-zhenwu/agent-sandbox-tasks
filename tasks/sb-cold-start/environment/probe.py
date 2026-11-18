import os
import sys
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def main():
    version = sys.version.split()[0]
    (APP / "ready.txt").write_text(f"SANDBOX_READY {version}\n")

if __name__ == "__main__":
    main()
