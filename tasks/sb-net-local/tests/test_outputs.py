import json

import _common


def test_agent_response():
    output = _common.output()
    data = (output / "net_response.bin").read_bytes()
    receipt = json.loads((output / "net_receipt.json").read_text())
    assert len(data) == _common.expected("net_size"), f"响应 {len(data)} 字节，应为平台期望大小"
    assert _common.digest(data) == _common.expected("net_sha256"), "响应内容与平台原始响应不符"
    assert receipt["bytes"] == len(data), "net_receipt.bytes 不符"
    assert receipt["sha256"] == _common.digest(data), "net_receipt.sha256 不符"


def test_harness_local_request():
    expected = json.loads((_common.private_dir() / "expected.json").read_text())
    assert expected.get("net_path"), "平台没有生成本地服务地址"
    log = _common.private_dir() / "net_access.jsonl"
    assert log.exists(), "平台侧没有本地服务访问日志：请求没到服务"
    hits = [json.loads(line) for line in log.read_text().splitlines() if line.strip()]
    assert any(hit.get("path") == expected["net_path"] for hit in hits), "访问路径不符"
    events = _common.trace_events("exec_result")
    assert any("inputs/probe.py" in e.get("command", "") for e in events), "trace 里没有探针执行记录"


def test_harness_healthy():
    _common.assert_harness_healthy()


def test_timing_present():
    _common.load_timing()


def test_inputs_unmodified():
    _common.assert_inputs_unmodified()
