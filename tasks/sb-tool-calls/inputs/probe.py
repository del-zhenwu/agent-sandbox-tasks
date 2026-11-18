import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        raise SystemExit(1)
    index = sys.argv[1]
    out = OUT / "calls"
    out.mkdir(parents=True, exist_ok=True)
    (out / index).write_text(f"call-{index}\n")
    log = OUT / "call_log.txt"
    with log.open("a", encoding="utf-8") as handle:
        handle.write(f"{index}\n")

if __name__ == "__main__":
    main()
