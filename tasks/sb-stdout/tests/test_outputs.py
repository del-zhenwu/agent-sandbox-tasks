import json

import _common


def test_agent_stdout_captured():
    output = _common.output()
    data = (output / "captured_stdout.bin").read_bytes()
    receipt = json.loads((output / "stdout_receipt.json").read_text())
    assert len(data) == _common.expected("stdout_size"), f"捕获 {len(data)} 字节：stdout 被截断"
    assert _common.digest(data) == _common.expected("stdout_sha256"), "捕获内容与平台期望哈希不符"
    assert receipt["bytes"] == len(data), "stdout_receipt.bytes 不符"
    assert receipt["sha256"] == _common.digest(data), "stdout_receipt.sha256 不符"


def test_harness_stdout_channel():
    """期望值由平台独立计算；产物对上即证明 stdout 通道没被截断。"""
    expected = json.loads((_common.private_dir() / "expected.json").read_text())
    assert expected.get("stdout_size") and expected.get("stdout_sha256"), "平台未计算期望 stdout"
    events = _common.trace_events("exec_result")
    assert any("inputs/probe.py" in e.get("command", "") for e in events), "trace 里没有探针执行记录"


def test_harness_healthy():
    _common.assert_harness_healthy()


def test_timing_present():
    _common.load_timing()


def test_inputs_unmodified():
    _common.assert_inputs_unmodified()
