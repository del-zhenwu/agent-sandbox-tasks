import json

import _common


def test_agent_error_captured():
    report = json.loads((_common.output() / "error_report.json").read_text())
    assert report["exit_code"] == 3, "exit_code 应为 3：非零退出被吞掉了"
    assert report["stderr_marker"] == _common.expected("error_marker"), "stderr 标记与平台注入值不符"
    assert report["partial_bytes"] == _common.expected("partial_bytes"), "partial_bytes 不符"


def test_agent_partial_effect_kept():
    path = _common.output() / "partial.bin"
    assert path.exists(), "output/partial.bin 不存在：失败前的写入没落盘"
    assert path.stat().st_size == _common.expected("partial_bytes"), "partial.bin 大小不对"


def test_agent_pipeline_continued():
    text = (_common.output() / "after.txt").read_text()
    assert text == "continued\n", f"after.txt={text!r}：非零退出后流程没有继续"


def test_harness_raw_result_in_trace():
    """退出码与 stderr 来自平台 trace 的原始返回包，不是 agent 自报。"""
    events = _common.trace_events("exec_result")
    candidates = [e for e in events if "probe_fail.py" in e.get("command", "")]
    assert candidates, "trace 里没有失败命令的执行记录"
    event = candidates[-1]
    assert event.get("exit_code") == 3, "trace 里的退出码不是 3"
    assert _common.expected("error_marker") in event.get("stderr", ""), "trace 里没有原始 stderr 标记"


def test_harness_healthy():
    _common.assert_harness_healthy()


def test_timing_present():
    _common.load_timing()


def test_inputs_unmodified():
    _common.assert_inputs_unmodified()
