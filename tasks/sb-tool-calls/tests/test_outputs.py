
import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def test_each_call_file():
    count = int(os.environ.get("BENCH_TOOL_CALLS", "1000"))
    for index in range(count):
        assert (APP / "calls" / str(index)).read_text() == f"call-{index}\n"
