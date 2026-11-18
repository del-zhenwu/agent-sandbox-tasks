import json
import os
import time
import urllib.request
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def main():
    repeats = int(os.environ.get("BENCH_HTTP_REQUESTS", "1000"))
    page = os.environ.get("BENCH_HTTP_URL", "https://example.com")
    started = time.perf_counter()
    statuses = []
    for _ in range(repeats):
        request = urllib.request.Request(page, headers={"User-Agent": "sandbox-bench"})
        with urllib.request.urlopen(request, timeout=30) as response:
            statuses.append(response.status)
            response.read()
    (APP / "rtt_report.json").write_text(json.dumps({
        "http_statuses": statuses,
        "elapsed_seconds": time.perf_counter() - started,
    }))
    if any(code != 200 for code in statuses):
        raise SystemExit("http status was not 200")

if __name__ == "__main__":
    main()
