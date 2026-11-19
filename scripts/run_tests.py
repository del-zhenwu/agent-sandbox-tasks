#!/usr/bin/env python3
"""零依赖测试运行器：跑测试模块里所有 test_* 函数。

用法：python3 scripts/run_tests.py tasks/sb-tool-calls /工作区
有 pytest 时 check_files.sh 会优先用它，这里是不依赖 pytest 的兜底。
"""

from __future__ import annotations

import importlib.util
import inspect
import sys
import traceback
from pathlib import Path


def load(path: Path):
    spec = importlib.util.spec_from_file_location(f"_task_{path.parent.parent.name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python3 scripts/run_tests.py tasks/<名字> <含 inputs/ 和 output/ 的工作区>", file=sys.stderr)
        return 2
    task_dir, workspace = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    import os

    os.environ["APP_ROOT"] = str(workspace)
    os.environ["TASK_DIR"] = str(task_dir)
    # 公共断言只有 tasks/_common.py 一份；测试模块通过 import _common 引用
    sys.path.insert(0, str(task_dir.parent))
    sys.path.insert(0, str(task_dir / "tests"))

    module = load(task_dir / "tests" / "test_outputs.py")
    tests = [(name, fn) for name, fn in vars(module).items()
             if name.startswith("test_") and callable(fn)]
    if not tests:
        print("没有找到 test_* 函数", file=sys.stderr)
        return 2

    failed = []
    for name, fn in sorted(tests):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - 测试失败都要报出来
            failed.append(name)
            print(f"FAIL {name}")
            detail = str(exc).strip() or exc.__class__.__name__
            for line in detail.splitlines():
                print(f"     {line}")
            if os.environ.get("SB_DEBUG"):
                traceback.print_exc()
        else:
            print(f"PASS {name}")

    print(f"\n{len(tests) - len(failed)}/{len(tests)} passed")
    if failed:
        print("失败项: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
