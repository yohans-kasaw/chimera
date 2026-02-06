"""Validate Chimera MCP configuration.

This is intentionally lightweight to keep CI and local validation fast.
It validates `mcp.json` against `mcp.schema.json` and performs a couple of
project-specific sanity checks.

Usage:
  python scripts/validate_mcp_config.py
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    schema_path = REPO_ROOT / "mcp.schema.json"
    config_path = REPO_ROOT / "mcp.json"
    schema = _load_json(schema_path)
    config = _load_json(config_path)

    try:
        import jsonschema  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "jsonschema is required to validate MCP config. Install it (e.g. `uv add jsonschema`)."
        ) from exc

    jsonschema.validate(instance=config, schema=schema)

    # Project-specific checks.
    servers = config.get("servers", {})
    if not isinstance(servers, dict) or not servers:
        raise SystemExit("mcp.json must define at least one server")

    for name, server in servers.items():
        if not isinstance(server, dict):
            raise SystemExit(f"Server '{name}' must be an object")
        tools = server.get("tools", [])
        if not tools:
            raise SystemExit(f"Server '{name}' must define at least one tool")
        seen = set()
        for tool in tools:
            tname = tool.get("name")
            if tname in seen:
                raise SystemExit(f"Duplicate tool name '{tname}' in server '{name}'")
            seen.add(tname)

    print("[mcp-validate] mcp.json is valid and self-consistent")


if __name__ == "__main__":
    main()
