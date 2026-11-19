import _common

COUNT = 20


def test_agent_done_files():
    output = _common.output()
    nonces = _common.expected("nonces")
    assert len(nonces) == COUNT
    for nonce in nonces:
        path = output / "done" / nonce
        assert path.exists(), f"output/done/{nonce} 缺失"
        assert path.read_text() == f"{nonce}\n", f"output/done/{nonce} 内容不对"
    actual = {p.name for p in (output / "done").iterdir() if p.is_file()}
    assert actual == set(nonces), "output/done/ 出现多余产物"


def test_harness_trace_shows_overlap():
    """并发证据来自平台 trace 的单调起止时间，不再用 agent 可写的 mtime。"""
    nonces = _common.expected("nonces")
    events = _common.trace_events("tool_call")
    assert len(events) >= COUNT, f"trace 只有 {len(events)} 次工具调用"
    commands = [e.get("command", "") for e in events]
    for nonce in nonces:
        assert any(nonce in cmd for cmd in commands), f"trace 里没有针对 {nonce} 的调用"
    spans = [(e["start"], e["end"]) for e in events if "start" in e and "end" in e]
    assert len(spans) >= COUNT, "trace 缺少起止时间"
    points = []
    for start, end in spans:
        points.append((start, 1))
        points.append((end, -1))
    points.sort()
    current = peak = 0
    for _, delta in points:
        current += delta
        peak = max(peak, current)
    assert peak >= 10, f"trace 最大并发只有 {peak}：exec 被串行化了"
    assert max(end for _, end in spans) - min(start for start, _ in spans) <= 30, "trace 总跨度超过 30s"


def test_harness_healthy():
    _common.assert_harness_healthy()


def test_timing_present():
    _common.load_timing()


def test_inputs_unmodified():
    _common.assert_inputs_unmodified()
