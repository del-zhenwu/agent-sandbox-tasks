import json

import _common


def test_agent_large_write():
    output = _common.output()
    data = (output / "large.bin").read_bytes()
    report = json.loads((output / "write_report.json").read_text())
    assert len(data) == _common.expected("payload_size"), f"写入 {len(data)} 字节，不符预期"
    assert _common.digest(data) == _common.expected("payload_sha256"), "写入内容与平台随机原件不符"
    assert report["bytes"] == len(data), "write_report.bytes 不符"
    assert report["sha256"] == _common.digest(data), "write_report.sha256 不符"


def test_harness_private_original():
    """平台持有随机原件哈希；产物能对上就必然真的经过了沙箱写盘通道。"""
    expected = json.loads((_common.private_dir() / "expected.json").read_text())
    assert expected.get("payload_sha256") and expected.get("payload_size", 0) > 0, "平台没有生成随机原件"
    events = _common.trace_events("exec_result")
    assert any("inputs/probe.py" in e.get("command", "") for e in events), "trace 里没有探针执行记录"


def test_harness_healthy():
    _common.assert_harness_healthy()


def test_timing_present():
    _common.load_timing()


def test_inputs_unmodified():
    _common.assert_inputs_unmodified()
