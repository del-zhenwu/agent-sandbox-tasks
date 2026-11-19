#!/usr/bin/env python3
"""重建各题的 inputs.sha256。

inputs.sha256 必须在发题前生成——它记录 agent 尚未碰过的原始 inputs。
改过任何 inputs/ 之后要重跑本脚本，否则正常 run 会被误判为“改过探针”。

用法：python3 scripts/sync_tests.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    tasks = sorted(p for p in (ROOT / "tasks").iterdir() if p.is_dir() and p.name.startswith("sb-"))
    for task in tasks:
        inputs = task / "inputs"
        tests = task / "tests"
        if not inputs.is_dir() or not tests.is_dir():
            continue
        lines = []
        for path in sorted(p for p in inputs.rglob("*") if p.is_file()):
            rel = path.relative_to(task).as_posix()
            lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}")
        (tests / "inputs.sha256").write_text("\n".join(lines) + "\n")
        print(f"{task.name}: {len(lines)} 个 inputs 文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
