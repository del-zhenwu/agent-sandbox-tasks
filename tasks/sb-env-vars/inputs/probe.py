import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    token = os.environ.get("SANDBOX_BENCH_TOKEN", "")
    challenge = os.environ.get("SANDBOX_BENCH_CHALLENGE", "")
    if not token or not challenge:
        raise SystemExit(1)
    computed = hashlib.sha256(f"{token}:{challenge}".encode()).hexdigest()
    (OUT / "env_report.json").write_text(json.dumps({
        "token_present": bool(token),
        "challenge": challenge,
        "computed_hash": computed,
    }))


if __name__ == "__main__":
    main()
