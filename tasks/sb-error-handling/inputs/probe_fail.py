import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
SIZE = 4 * 1024 * 1024
MARKER = os.environ.get("SANDBOX_BENCH_ERROR_MARKER", "SANDBOX_BENCH_ERROR")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "partial.bin").write_bytes(b"x" * SIZE)
    sys.stdout.write("SANDBOX_BENCH_PARTIAL\n")
    sys.stdout.flush()
    print(f"{MARKER}: upstream checksum mismatch", file=sys.stderr)
    raise SystemExit(3)


if __name__ == "__main__":
    main()
