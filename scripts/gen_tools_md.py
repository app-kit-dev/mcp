#!/usr/bin/env python3
"""Generate docs/tools.md from the server's live `tools/list`.

    python3 scripts/gen_tools_md.py                                  # https://mcp.app-kit.dev/mcp
    python3 scripts/gen_tools_md.py --url http://127.0.0.1:8770/mcp  # any server
    python3 scripts/gen_tools_md.py --from-json tools.json           # saved tools/list result

Standard library only. Optional `--token mcpf_...` is sent as `Authorization: Bearer`.
Tools listed in scripts/planned_tools.json that the server does not expose yet are
appended in a separate "Planned" section; they drop out automatically once they ship.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_URL = "https://mcp.app-kit.dev/mcp"
PROTOCOL_VERSION = "2025-11-25"
PLANNED = ROOT / "scripts" / "planned_tools.json"


def _rpc(url: str, method: str, params: dict[str, Any], token: str | None) -> dict[str, Any]:
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": PROTOCOL_VERSION,
        "User-Agent": "app-kit-dev-mcp/gen_tools_md",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 - URL is chosen by the operator
        raw = resp.read().decode()
        ctype = resp.headers.get("Content-Type", "")
    if "text/event-stream" in ctype:
        for line in raw.splitlines():
            if line.startswith("data:"):
                msg = json.loads(line[5:].strip())
                if msg.get("id") == 1:
                    raw = json.dumps(msg)
                    break
    msg = json.loads(raw)
    if "error" in msg:
        raise SystemExit(f"{method} failed: {msg['error']}")
    return msg["result"]


def fetch_tools(url: str, token: str | None) -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        result = _rpc(url, "tools/list", {"cursor": cursor} if cursor else {}, token)
        tools.extend(result.get("tools", []))
        cursor = result.get("nextCursor")
        if not cursor:
            return tools


def _hints(ann: dict[str, Any]) -> str:
    keys = ("readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint")
    return ", ".join(f"`{k}={str(ann[k]).lower()}`" for k in keys if k in ann) or "-"


def _params(schema: dict[str, Any]) -> list[str]:
    props: dict[str, Any] = schema.get("properties", {})
    if not props:
        return ["No arguments."]
    required = set(schema.get("required", []))
    rows = ["| Argument | Type | Required | Description |", "|---|---|---|---|"]
    for name, spec in props.items():
        rows.append(
            f"| `{name}` | {_type(spec)} | {'yes' if name in required else 'no'} | "
            f"{_cell(spec.get('description', ''))} |"
        )
    return rows


def _type(spec: dict[str, Any]) -> str:
    if "enum" in spec:
        return " / ".join(f"`{v}`" for v in spec["enum"])
    if "anyOf" in spec:
        return " or ".join(_type(s) for s in spec["anyOf"] if s.get("type") != "null")
    if spec.get("type") == "array":
        return f"array of {_type(spec.get('items', {}))}"
    if "$ref" in spec:
        return f"`{spec['$ref'].rsplit('/', 1)[-1]}`"
    return f"`{spec.get('type', 'any')}`"


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def render_tool(tool: dict[str, Any]) -> list[str]:
    ann = tool.get("annotations", {})
    title = tool.get("title") or ann.get("title") or tool["name"]
    out = [f"## `{tool['name']}`", "", f"**Title:** {title}  ", f"**Annotations:** {_hints(ann)}", ""]
    out += ["```text", tool.get("description", "").strip(), "```", "", "### Input", ""]
    out += _params(tool.get("inputSchema", {}))
    out += ["", "<details><summary>Input JSON Schema</summary>", "", "```json"]
    out += [json.dumps(tool.get("inputSchema", {}), ensure_ascii=False, indent=2), "```", "", "</details>", ""]
    if tool.get("outputSchema"):
        out += ["### Output (`structuredContent`)", "", "<details><summary>Output JSON Schema</summary>", "", "```json"]
        out += [json.dumps(tool["outputSchema"], ensure_ascii=False, indent=2), "```", "", "</details>", ""]
    return out


def render_planned(planned: list[dict[str, Any]]) -> list[str]:
    out = [
        "## Planned tools (not in `tools/list` yet)",
        "",
        "Rolling out next. Arguments and output below are the design contract; the exact JSON Schemas",
        "will appear in this file once the tools are live (the file is regenerated from `tools/list`).",
        "",
    ]
    for tool in planned:
        out += [f"### `{tool['name']}`", "", tool["summary"], ""]
        out += [f"- **Input:** {tool['input']}", f"- **Output:** {tool['output']}", f"- **Free limits:** {tool['limits']}", ""]
    return out


def render(tools: list[dict[str, Any]], source: str) -> str:
    names = {t["name"] for t in tools}
    planned = [p for p in json.loads(PLANNED.read_text()) if p["name"] not in names] if PLANNED.exists() else []
    lines = [
        "# App-Kit MCP tools",
        "",
        "<!-- Generated by scripts/gen_tools_md.py. Do not edit by hand. -->",
        "",
        f"Source: `tools/list` of `{source}`. Tool descriptions are returned by the server as-is",
        "(currently in Russian; models handle them fine). Every tool also returns",
        "`structuredContent.quota = {remaining, reset_at, tier, upgrade_url}`.",
        "",
        "| Tool | Title | Read-only |",
        "|---|---|---|",
    ]
    for t in tools:
        ann = t.get("annotations", {})
        lines.append(f"| [`{t['name']}`](#{t['name']}) | {_cell(t.get('title') or ann.get('title', ''))} | "
                     f"{'yes' if ann.get('readOnlyHint') else 'no'} |")
    for p in planned:
        lines.append(f"| `{p['name']}` (planned) | {p['title']} | yes |")
    lines.append("")
    for t in tools:
        lines += render_tool(t)
    if planned:
        lines += render_planned(planned)
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--token", default=None, help="optional free token (mcpf_...)")
    ap.add_argument("--from-json", type=Path, default=None, help="file with a tools/list result or a list of tools")
    ap.add_argument("--source-label", default=None, help="source shown in the header (default: --url)")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "tools.md")
    a = ap.parse_args()
    if a.from_json:
        data = json.loads(a.from_json.read_text())
        tools = data["tools"] if isinstance(data, dict) else data
    else:
        tools = fetch_tools(a.url, a.token)
    a.out.write_text(render(tools, a.source_label or a.url))
    print(f"{a.out}: {len(tools)} tools", file=sys.stderr)


if __name__ == "__main__":
    main()
