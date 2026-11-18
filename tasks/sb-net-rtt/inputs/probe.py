import json
import time
import urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
REPEATS = 1000
PAGE = "https://example.com"

def main():
    started = time.perf_counter()
    statuses = []
    for _ in range(REPEATS):
        request = urllib.request.Request(PAGE, headers={"User-Agent": "sandbox-bench"})
        with urllib.request.urlopen(request, timeout=30) as response:
            statuses.append(response.status)
            response.read()
    (OUT / "rtt_report.json").write_text(json.dumps({
        "http_statuses": statuses,
        "elapsed_seconds": time.perf_counter() - started,
    }))
    if any(code != 200 for code in statuses):
        raise SystemExit(1)

if __name__ == "__main__":
    main()
