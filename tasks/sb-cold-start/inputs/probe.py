import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    version = sys.version.split()[0]
    (OUT / "ready.txt").write_text(f"SANDBOX_READY {version}\n")

if __name__ == "__main__":
    main()
