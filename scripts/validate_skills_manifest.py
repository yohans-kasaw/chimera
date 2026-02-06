"""Validate Chimera skills manifest.

Validates `skills.json` against `skills.schema.json` and performs a couple of
project-specific sanity checks.

Usage:
  python scripts/validate_skills_manifest.py
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    schema_path = REPO_ROOT / "skills.schema.json"
    manifest_path = REPO_ROOT / "skills.json"
    schema = _load_json(schema_path)
    manifest = _load_json(manifest_path)

    try:
        import jsonschema  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(
            "jsonschema is required to validate skills manifest. Install it (e.g. `uv add jsonschema`)."
        ) from exc

    jsonschema.validate(instance=manifest, schema=schema)

    skills = manifest.get("skills", [])
    if not isinstance(skills, list):
        raise SystemExit("skills.json must contain a skills array")

    seen = set()
    for entry in skills:
        name = entry.get("name")
        if name in seen:
            raise SystemExit(f"Duplicate skill name '{name}' in skills.json")
        seen.add(name)

    print("[skills-validate] skills.json is valid and self-consistent")


if __name__ == "__main__":
    main()
