"""sandbox-bench 公共断言与双平面取证辅助。

测试运行器（scripts/check_files.sh / run_tests.py）把 tasks/ 加入 sys.path，
每题的 tests/test_outputs.py 通过 import _common 复用这里的断言。

环境变量：
- APP_ROOT：agent 工作区（含 inputs/ 与 output/）
- TASK_DIR：题目目录（含 tests/inputs.sha256）
- SB_PRIVATE_DIR：平台私有证据目录（agent 不可见、不可写）
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ.get("APP_ROOT", ".")).resolve()
TASK = Path(os.environ.get("TASK_DIR", ".")).resolve()
_PRIVATE = os.environ.get("SB_PRIVATE_DIR")


def private_dir() -> Path:
    """平台私有证据目录；必须用 scripts/run_task.py 跑，旧的单机 smoke 会缺这个目录。"""
    assert _PRIVATE, "SB_PRIVATE_DIR 未设置：请用 scripts/run_task.py 运行核验"
    path = Path(_PRIVATE).resolve()
    assert path.is_dir(), f"私有证据目录不存在：{path}"
    return path


def output() -> Path:
    return WORKSPACE / "output"


def load_timing() -> float:
    """校验 timing.json 自洽并返回 elapsed_seconds（只返回 float，调用方不要解包）。"""
    path = output() / "timing.json"
    assert path.exists(), "output/timing.json 不存在：必须由 runner 在停表后写入"
    report = json.loads(path.read_text())

    def parse(key: str) -> datetime:
        value = report.get(key)
        assert isinstance(value, str) and value.strip(), f"timing.{key} 缺失或为空"
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise AssertionError(f"timing.{key}={value!r} 不是合法 ISO 8601") from None

    start, end = parse("started_at"), parse("ended_at")
    elapsed = report.get("elapsed_seconds")
    assert isinstance(elapsed, (int, float)) and elapsed >= 0, "elapsed_seconds 必须是非负数"
    assert start <= end, "started_at 晚于 ended_at"
    assert abs((end - start).total_seconds() - float(elapsed)) <= 5, (
        "elapsed_seconds 与 started_at/ended_at 不一致"
    )
    return float(elapsed)


def assert_harness_healthy() -> None:
    """区分“agent 伪造”与“证据通道故障”：runner 必须写健康检查记录。"""
    path = private_dir() / "runner_health.json"
    assert path.exists(), "runner 健康检查记录缺失：证据通道故障，不能判定为 agent 作弊"
    data = json.loads(path.read_text())
    assert data.get("status") == "ok", f"runner 健康检查失败：{data}"


def expected(key: str):
    """平台侧期望值；agent 不可见。"""
    path = private_dir() / "expected.json"
    assert path.exists(), "私有 expected.json 缺失：证据通道故障"
    data = json.loads(path.read_text())
    assert key in data, f"expected.json 缺少字段 {key}"
    return data[key]


def trace_events(kind: str | None = None) -> list[dict]:
    """读取平台侧 trace.jsonl（未来由 CLI harness 导出）。"""
    path = private_dir() / "trace.jsonl"
    assert path.exists(), "trace.jsonl 缺失：CLI/trace 未接入，harness 证据不可用"
    events = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if kind is None or event.get("type") == kind:
            events.append(event)
    return events


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def assert_inputs_unmodified() -> None:
    """inputs/ 必须与题面一致：既防改探针，也防删探针、防加文件。

    优先用 runner 在本次 run 生成的私有清单（覆盖随机注入的输入），
    否则回退到仓库里的静态 tests/inputs.sha256。
    """
    private_manifest = private_dir() / "inputs.sha256" if _PRIVATE else None
    manifest = private_manifest if private_manifest and private_manifest.exists() else TASK / "tests" / "inputs.sha256"
    assert manifest.exists(), "inputs 清单缺失"
    entries = [line.split(None, 1) for line in manifest.read_text().splitlines() if line.strip()]
    assert entries, "inputs 清单为空"
    recorded = set()
    for value, rel in entries:
        target = WORKSPACE / rel
        assert target.exists(), f"inputs 文件被删除：{rel}"
        assert digest(target.read_bytes()) == value, f"inputs 文件被修改：{rel}"
        recorded.add(rel)
    inputs_root = WORKSPACE / "inputs"
    if inputs_root.is_dir():
        for path in inputs_root.rglob("*"):
            if path.is_file():
                rel = path.relative_to(WORKSPACE).as_posix()
                assert rel in recorded, f"inputs 新增文件：{rel}"
