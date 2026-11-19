#!/usr/bin/env python3
"""最小 run runner：双平面取证 + 双分数归因。

用法：
  python3 scripts/run_task.py tasks/sb-env-vars --simulate
  python3 scripts/run_task.py tasks/sb-tool-calls --trace /path/from/cli.jsonl

职责：准备 workspace、生成私有随机证据、注入 secret、写 timing、收产物、
跑 check_files.sh，并按 test_harness_* / test_agent_* 的失败项给出归因。
"""

from __future__ import annotations

import argparse
import hashlib
import http.server
import json
import os
import secrets
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "runs"
BLOCK = bytes(i % 251 for i in range(64 * 1024))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def iso(dt: datetime) -> str:
    return dt.isoformat()


def make_payload(path: Path, size: int) -> None:
    block = os.urandom(min(1024 * 1024, size))
    with path.open("wb") as handle:
        left = size
        while left > 0:
            chunk = block[:left]
            handle.write(chunk)
            left -= len(chunk)


def start_net_server(private: Path, expected: dict) -> tuple[object, dict]:
    token = secrets.token_hex(12)
    nonce = secrets.token_hex(6)
    path = f"/{token}/{nonce}"
    body = os.urandom(2 * 1024 * 1024)
    expected["net_sha256"] = sha(body)
    expected["net_size"] = len(body)
    expected["net_path"] = path
    log_path = private / "net_access.jsonl"

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path == path:
                with log_path.open("a") as handle:
                    handle.write(json.dumps({"path": self.path, "ts": time.time()}) + "\n")
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_error(404)

        def log_message(self, *_args):
            pass

    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, {"SANDBOX_BENCH_NET_URL": f"http://127.0.0.1:{server.server_port}{path}"}


def setup(task: Path, workspace: Path, private: Path, payload_mb: int) -> tuple[dict, dict, object | None]:
    shutil.copytree(task / "inputs", workspace / "inputs")
    (workspace / "output").mkdir(parents=True, exist_ok=True)
    expected: dict = {}
    inject: dict = {}
    server = None
    name = task.name

    if name == "sb-tool-calls":
        nonces = [secrets.token_hex(5) for _ in range(50)]
        expected["nonces"] = nonces
        inject["SANDBOX_BENCH_NONCES"] = ",".join(nonces)
    elif name == "sb-concurrent-exec":
        nonces = [secrets.token_hex(5) for _ in range(20)]
        expected["nonces"] = nonces
        inject["SANDBOX_BENCH_NONCES"] = ",".join(nonces)
    elif name == "sb-env-vars":
        token = secrets.token_hex(8)
        challenge = secrets.token_hex(8)
        expected["env_hash"] = sha(f"{token}:{challenge}".encode())
        expected["token"] = token
        expected["challenge"] = challenge
        inject["SANDBOX_BENCH_TOKEN"] = token
        inject["SANDBOX_BENCH_CHALLENGE"] = challenge
    elif name == "sb-fs-upload":
        size = payload_mb * 1024 * 1024
        make_payload(workspace / "inputs" / "payload.bin", size)
        expected["payload_sha256"] = sha((workspace / "inputs" / "payload.bin").read_bytes())
        expected["payload_size"] = size
    elif name == "sb-stdout":
        total = 64 * 1024 * 1024
        full, rem = divmod(total, len(BLOCK))
        digest = hashlib.sha256()
        for _ in range(full):
            digest.update(BLOCK)
        if rem:
            digest.update(BLOCK[:rem])
        expected["stdout_sha256"] = digest.hexdigest()
        expected["stdout_size"] = total
    elif name == "sb-error-handling":
        marker = "SANDBOX_BENCH_ERROR_" + secrets.token_hex(6)
        expected["error_marker"] = marker
        expected["partial_bytes"] = 4 * 1024 * 1024
        inject["SANDBOX_BENCH_ERROR_MARKER"] = marker
    elif name == "sb-net-local":
        server, inject = start_net_server(private, expected)

    manifest = []
    for path in sorted(p for p in workspace.joinpath("inputs").rglob("*") if p.is_file()):
        rel = path.relative_to(workspace).as_posix()
        manifest.append(f"{sha(path.read_bytes())}  {rel}")
    (private / "inputs.sha256").write_text("\n".join(manifest) + "\n")
    (private / "expected.json").write_text(json.dumps(expected, indent=2) + "\n")
    (private / "env.json").write_text(json.dumps(inject, indent=2) + "\n")
    (private / "runner_health.json").write_text(
        json.dumps({"status": "ok", "run_id": private.parent.name, "trace_provided": False}, indent=2) + "\n"
    )
    return expected, inject, server


def make_trace(task_name: str, private: Path, expected: dict) -> None:
    """模拟 CLI harness 导出的 trace；真实 run 由 --trace 提供。"""
    events = []
    base = time.time()
    if task_name == "sb-tool-calls":
        for i, nonce in enumerate(expected["nonces"]):
            start = base + i * 0.6
            events.append({"type": "tool_call", "id": f"c{i}", "command": f"python3 inputs/probe.py {nonce}",
                           "start": start, "end": start + 0.4})
    elif task_name == "sb-concurrent-exec":
        for i, nonce in enumerate(expected["nonces"]):
            events.append({"type": "tool_call", "id": f"c{i}", "command": f"python3 inputs/probe.py {nonce}",
                           "start": base, "end": base + 5.2})
    elif task_name == "sb-error-handling":
        events.append({"type": "exec_result", "id": "e0", "command": "python3 inputs/probe_fail.py",
                       "exit_code": 3, "stdout": "SANDBOX_BENCH_PARTIAL\n",
                       "stderr": f"{expected['error_marker']}: upstream checksum mismatch\n"})
    else:
        commands = {
            "sb-env-vars": "python3 inputs/probe.py",
            "sb-fs-upload": "python3 inputs/probe.py",
            "sb-stdout": "python3 inputs/probe.py",
            "sb-net-local": "python3 inputs/probe.py",
        }
        events.append({"type": "exec_result", "id": "e0",
                       "command": commands.get(task_name, "agent action"), "exit_code": 0})
    (private / "trace.jsonl").write_text("\n".join(json.dumps(e) for e in events) + "\n")


def simulate(task: Path, workspace: Path, env: dict, expected: dict) -> None:
    """模拟 agent 按题面执行，用来验证正常路径。"""
    name = task.name
    base = dict(os.environ, **env)
    if name in ("sb-tool-calls", "sb-concurrent-exec"):
        args_list = [[sys.executable, "inputs/probe.py", n] for n in expected["nonces"]]
        if name == "sb-concurrent-exec":
            procs = [subprocess.Popen(a, cwd=workspace, env=base) for a in args_list]
            for proc in procs:
                proc.wait()
        else:
            for args in args_list:
                subprocess.run(args, cwd=workspace, env=base, check=True)
    elif name == "sb-env-vars":
        subprocess.run([sys.executable, "inputs/probe.py"], cwd=workspace, env=base, check=True)
    elif name == "sb-fs-upload":
        subprocess.run([sys.executable, "inputs/probe.py"], cwd=workspace, env=base, check=True)
    elif name == "sb-stdout":
        with (workspace / "output" / "captured_stdout.bin").open("wb") as handle:
            subprocess.run([sys.executable, "inputs/probe.py"], cwd=workspace, env=base, stdout=handle, check=True)
    elif name == "sb-error-handling":
        proc = subprocess.run([sys.executable, "inputs/probe_fail.py"], cwd=workspace, env=base, capture_output=True)
        marker = expected["error_marker"]
        (workspace / "output" / "error_report.json").write_text(json.dumps({
            "exit_code": proc.returncode,
            "stderr_marker": proc.stderr.decode().split(":")[0].strip(),
            "partial_bytes": expected["partial_bytes"],
        }))
        (workspace / "output" / "after.txt").write_text("continued\n")
    elif name == "sb-net-local":
        subprocess.run([sys.executable, "inputs/probe.py"], cwd=workspace, env=base, check=True)


def attribute(output_text: str) -> str:
    harness_failed = any("test_harness_" in line for line in output_text.splitlines()
                         if "FAIL" in line or "FAILED" in line)
    agent_failed = any("test_agent_" in line for line in output_text.splitlines()
                       if "FAIL" in line or "FAILED" in line)
    if harness_failed and agent_failed:
        return "both"
    if harness_failed:
        return "harness"
    if agent_failed:
        return "agent"
    return "ok"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    parser.add_argument("--trace")
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--payload-mb", type=int, default=256)
    parser.add_argument("--elapsed", type=float)
    parser.add_argument("--started-at", help="真实发题时间（ISO 8601），CLI 集成时传入")
    args = parser.parse_args()

    task = (ROOT / args.task).resolve()
    assert (task / "inputs").is_dir(), f"题目不存在：{task}"
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + secrets.token_hex(3)
    run_root = RUNS / task.name / run_id
    workspace = run_root / "workspace"
    private = run_root / "_private"
    workspace.mkdir(parents=True)
    private.mkdir(parents=True)

    expected, inject, server = setup(task, workspace, private, args.payload_mb)
    try:
        if args.trace:
            shutil.copy(args.trace, private / "trace.jsonl")
            health = json.loads((private / "runner_health.json").read_text())
            health["trace_provided"] = True
            (private / "runner_health.json").write_text(json.dumps(health, indent=2))
        elif args.simulate:
            make_trace(task.name, private, expected)
        else:
            (private / "trace.jsonl").write_text("")

        start_wall = time.time()
        if args.simulate:
            simulate(task, workspace, inject, expected)
        if args.elapsed is not None:
            elapsed = args.elapsed
        elif args.started_at:
            elapsed = max(0.0, (datetime.now(timezone.utc) - datetime.fromisoformat(
                args.started_at.replace("Z", "+00:00"))).total_seconds())
        else:
            elapsed = time.time() - start_wall
        end = datetime.now(timezone.utc)
        start = end - timedelta(seconds=elapsed)
        (workspace / "output" / "timing.json").write_text(json.dumps({
            "task": task.name,
            "started_at": iso(start),
            "ended_at": iso(end),
            "elapsed_seconds": elapsed,
        }, indent=2) + "\n")

        env = dict(os.environ, APP_ROOT=str(workspace), TASK_DIR=str(task), SB_PRIVATE_DIR=str(private))
        proc = subprocess.run(
            ["bash", str(ROOT / "scripts" / "check_files.sh"), str(task), str(workspace)],
            env=env, text=True, capture_output=True,
        )
        check_output = proc.stdout + proc.stderr
        print(check_output, end="")
        report = {
            "task": task.name,
            "run_id": run_id,
            "workspace": str(workspace),
            "private": str(private),
            "checker_exit": proc.returncode,
            "attribution": attribute(check_output) if proc.returncode != 0 else "ok",
        }
        (run_root / "scores.json").write_text(json.dumps(report, indent=2) + "\n")
        print("\nSCORES " + json.dumps(report, ensure_ascii=False))
        return proc.returncode
    finally:
        if server is not None:
            server.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
