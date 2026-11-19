import json

import _common


def test_agent_report():
    report = json.loads((_common.output() / "env_report.json").read_text())
    assert report["token_present"] is True, "token 没有传进执行环境"
    assert report["challenge"] == _common.expected("challenge"), "challenge 与平台注入值不符"
    assert report["computed_hash"] == _common.expected("env_hash"), "computed_hash 不符"


def test_harness_injected_secret():
    """secret 每次 run 随机生成且只存在平台侧；产物能对上即证明 env 真的穿过去了。"""
    injected = json.loads((_common.private_dir() / "env.json").read_text())
    assert injected.get("SANDBOX_BENCH_TOKEN"), "平台没有生成 token"
    assert injected.get("SANDBOX_BENCH_CHALLENGE"), "平台没有生成 challenge"
    events = _common.trace_events("exec_result")
    assert any("inputs/probe.py" in e.get("command", "") for e in events), "trace 里没有探针执行记录"


def test_harness_healthy():
    _common.assert_harness_healthy()


def test_timing_present():
    _common.load_timing()


def test_inputs_unmodified():
    _common.assert_inputs_unmodified()
