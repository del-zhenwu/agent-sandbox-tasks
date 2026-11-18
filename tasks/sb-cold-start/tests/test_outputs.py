import os
from pathlib import Path
APP = Path(os.environ.get("APP_ROOT", "/app"))

def test_ready_file():
    text = (APP / "ready.txt").read_text()
    assert text.startswith("SANDBOX_READY ")
    assert text.endswith("\n")
