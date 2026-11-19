import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        raise SystemExit(1)
    nonce = sys.argv[1]
    calls = OUT / "calls"
    calls.mkdir(parents=True, exist_ok=True)
    (calls / nonce).write_text(f"call-{nonce}\n")
    with (OUT / "call_log.txt").open("a", encoding="utf-8") as handle:
        handle.write(f"{nonce}\n")


if __name__ == "__main__":
    main()
