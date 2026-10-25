#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the seven current official MCP reference servers locally.

This is a local structural matrix, not a scanner:

    initialize -> tools/list -> full digest -> repeat N times

No public network, no user files, no credentials.  Dependencies are installed
outside the repository (see the command paths in --help).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from drivers.mcp_client import MCPStdioClient, MCPError  # noqa: E402


def canonical(v) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def digest(v) -> str:
    return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()[:16]


def init_git_repo(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": "mcp-test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
        "GIT_COMMITTER_NAME": "mcp-test",
        "GIT_COMMITTER_EMAIL": "test@example.invalid",
    })
    subprocess.run(["git", "init", "-q"], cwd=path, check=True, env=env)
    (path / "README.md").write_text("official mcp git fixture\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True, env=env)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=path, check=True, env=env)


def build_commands(args, work: Path):
    node = str(Path(args.node).resolve())
    modules = Path(args.modules).resolve()
    py = Path(args.python_bin).resolve()
    sandbox = work / "filesystem"
    sandbox.mkdir(parents=True, exist_ok=True)
    git_repo = work / "git-repo"
    init_git_repo(git_repo)

    def ts(pkg: str, *extra: str):
        return [node, str(modules / ("@modelcontextprotocol/" + pkg) /
                           "dist" / "index.js"), *extra]

    return [
        ("everything", ts("server-everything"), work),
        ("filesystem", ts("server-filesystem", str(sandbox)), work),
        ("memory", ts("server-memory"), work / "memory"),
        ("sequentialthinking", ts("server-sequential-thinking"), work),
        ("fetch", [str(py / "mcp-server-fetch"), "--allow-private-ips"], work),
        ("git", [str(py / "mcp-server-git"), "--repository", str(git_repo)], work),
        ("time", [str(py / "mcp-server-time")], work),
    ]


class _HelloHandler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        body = b"hello from the local MCP fetch fixture\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _local_http():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), _HelloHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}/hello"


def _smoke(name, c, cwd: Path, fetch_url: str):
    """One safe, local call per reference server. No public network."""
    if name == "everything":
        return c.call_tool("echo", {"message": "hello"})
    if name == "filesystem":
        return c.call_tool("list_allowed_directories", {})
    if name == "memory":
        return c.call_tool("read_graph", {})
    if name == "sequentialthinking":
        return c.call_tool("sequentialthinking", {
            "thought": "local smoke test",
            "nextThoughtNeeded": False,
            "thoughtNumber": 1,
            "totalThoughts": 1,
        })
    if name == "fetch":
        return c.call_tool("fetch", {"url": fetch_url, "max_length": 200})
    if name == "git":
        return c.call_tool("git_status", {"repo_path": str(cwd / "git-repo")})
    if name == "time":
        return c.call_tool("get_current_time", {"timezone": "UTC"})
    return None


def run_one(name: str, command: list[str], cwd: Path, timeout: float,
            fetch_url: str = ""):
    start = time.monotonic()
    c = MCPStdioClient(command, cwd=str(cwd), timeout=timeout,
                       inherit_env=True)
    try:
        info = c.start()
        tools = list(c.tools)
        snap = {
            "serverInfo": info.get("serverInfo"),
            "instructions": info.get("instructions", ""),
            "tools": tools,
        }
        smoke = {"ok": True, "result": None}
        try:
            smoke["result"] = _smoke(name, c, cwd, fetch_url)
        except Exception as e:
            smoke = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        return {
            "ok": True,
            "elapsed_ms": int((time.monotonic() - start) * 1000),
            "protocolVersion": info.get("protocolVersion"),
            "serverInfo": info.get("serverInfo"),
            "instructions_len": len(info.get("instructions") or ""),
            "tools_count": len(tools),
            "tools": [t.get("name") for t in tools],
            "digest": digest(snap),
            "smoke": smoke,
        }
    except Exception as e:
        return {
            "ok": False,
            "elapsed_ms": int((time.monotonic() - start) * 1000),
            "error": f"{type(e).__name__}: {e}",
            "stderr_tail": list(getattr(c, "stderr_tail", []) or [])[-6:],
        }
    finally:
        c.close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--node", default="/tmp/node22/bin/node")
    ap.add_argument("--modules", default="/tmp/mcp-official/node_modules")
    ap.add_argument("--python-bin", default="/tmp/mcp-official/.venv/bin")
    ap.add_argument("--repeat", type=int, default=5)
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--out", default="/tmp/mcp-official/matrix.json")
    ap.add_argument("--md", default="/tmp/mcp-official/matrix.md")
    a = ap.parse_args(argv)

    work_root = Path(tempfile.mkdtemp(prefix="mcp-official-matrix-"))
    commands = build_commands(a, work_root)
    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "repeat": a.repeat,
        "node": a.node,
        "modules": a.modules,
        "python_bin": a.python_bin,
        "servers": [],
    }
    httpd, fetch_url = _local_http()
    try:
        for name, cmd, cwd in commands:
            cwd.mkdir(parents=True, exist_ok=True)
            runs = [run_one(name, cmd, cwd, a.timeout, fetch_url)
                    for _ in range(a.repeat)]
            ok_runs = [r for r in runs if r["ok"]]
            digests = sorted({r["digest"] for r in ok_runs})
            report["servers"].append({
                "name": name,
                "command": cmd,
                "runs": runs,
                "ok": len(ok_runs) == len(runs),
                "stable_digest": len(digests) == 1 and len(ok_runs) == len(runs),
                "digest": digests[0] if len(digests) == 1 else None,
                "digests": digests,
            })
            status = "OK" if len(ok_runs) == len(runs) and len(digests) == 1 else "FAIL"
            print(f"{status:4} {name:20} {len(ok_runs)}/{len(runs)} "
                  f"digests={digests}", flush=True)
    finally:
        httpd.shutdown()
        httpd.server_close()
        shutil.rmtree(work_root, ignore_errors=True)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    lines = [
        "# MCP Official Reference Matrix",
        "",
        f"- generated: `{report['generated_at']}`",
        f"- repeat: `{a.repeat}`",
        f"- node: `{a.node}`",
        "",
        "| server | runs | digest stable | tools | instructions | smoke | elapsed p50 | digest |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for s in report["servers"]:
        ok_runs = [r for r in s["runs"] if r["ok"]]
        p50 = sorted(r["elapsed_ms"] for r in ok_runs)[len(ok_runs)//2] if ok_runs else "-"
        first = ok_runs[0] if ok_runs else {}
        lines.append(
            f"| {s['name']} | {len(ok_runs)}/{len(s['runs'])} | "
            f"{'yes' if s['stable_digest'] else 'no'} | "
            f"{first.get('tools_count','-')} | {first.get('instructions_len','-')} | "
            f"{'yes' if first.get('smoke',{}).get('ok') else 'no'} | "
            f"{p50} ms | `{s.get('digest') or '-'}` |")
    lines += ["", "Failures:", ""]
    for s in report["servers"]:
        for i, r in enumerate(s["runs"], 1):
            if not r["ok"]:
                lines.append(f"- `{s['name']}` run {i}: `{r.get('error')}`")
                for tail in r.get("stderr_tail") or []:
                    lines.append(f"  - `{tail[:300]}`")
            if r.get("smoke") and not r["smoke"].get("ok"):
                lines.append(f"- `{s['name']}` run {i} smoke: `{r['smoke'].get('error')}`")
    Path(a.md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {a.out} and {a.md}")
    smoke_ok = all(
        all(r.get("smoke", {}).get("ok") for r in s["runs"])
        for s in report["servers"]
    )
    return 0 if all(s["ok"] and s["stable_digest"] for s in report["servers"]) and smoke_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
