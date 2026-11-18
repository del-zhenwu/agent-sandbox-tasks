import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def test_every_call_finished():
    count = int(os.environ.get("BENCH_CONCURRENCY", "80"))
    for index in range(count):
        assert (APP / "done" / str(index)).read_text() == f"{index}\n"
