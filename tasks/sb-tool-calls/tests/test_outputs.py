import _common

COUNT = 50


def test_agent_call_files():
    output = _common.output()
    nonces = _common.expected("nonces")
    assert len(nonces) == COUNT
    for nonce in nonces:
        path = output / "calls" / nonce
        assert path.exists(), f"output/calls/{nonce} 缺失：少发了一次工具调用"
        assert path.read_text() == f"call-{nonce}\n", f"output/calls/{nonce} 内容不对"
    actual = {p.name for p in (output / "calls").iterdir() if p.is_file()}
    assert actual == set(nonces), "output/calls/ 出现多余产物"


def test_agent_call_log():
    nonces = _common.expected("nonces")
    lines = [line for line in (_common.output() / "call_log.txt").read_text().splitlines() if line]
    assert sorted(lines) == sorted(nonces), "call_log.txt 不是每个注入编号一行"


def test_harness_trace_has_independent_calls():
    nonces = _common.expected("nonces")
    events = _common.trace_events("tool_call")
    assert len(events) >= COUNT, f"trace 只有 {len(events)} 次工具调用，应为 {COUNT}"
    ids = {e.get("id") for e in events}
    assert len(ids) >= COUNT, "trace 里调用 ID 不唯一"
    commands = [e.get("command", "") for e in events]
    for nonce in nonces:
        assert any(nonce in cmd for cmd in commands), f"trace 里没有针对 {nonce} 的工具调用"
    ordered = sorted(e["start"] for e in events if "start" in e)
    assert len(ordered) >= COUNT, "trace 缺少开始时间"
    assert all(b >= a for a, b in zip(ordered, ordered[1:])), "trace 时间戳不自洽"


def test_harness_healthy():
    _common.assert_harness_healthy()


def test_timing_present():
    _common.load_timing()


def test_inputs_unmodified():
    _common.assert_inputs_unmodified()
