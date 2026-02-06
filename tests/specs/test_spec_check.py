"""Meta-tests for the spec governance script.

These tests ensure that ``scripts/spec_check.py`` behaves as a
lightweight, executable governor over the repository's specs. The goal is
not exhaustive coverage, but to lock in the most critical guarantees so
future agents cannot silently weaken them.
"""

from __future__ import annotations

from pathlib import Path

from scripts import spec_check


def test_required_files_list_includes_core_specs() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    required_paths = {
        repo_root / "specs" / "_meta.md",
        repo_root / "specs" / "functional.md",
        repo_root / "specs" / "technical.md",
        repo_root / "specs" / "openclaw_integration.md",
        repo_root / ".coderabbit.yaml",
    }

    # Mirror the logic from ``ensure_required_files``.
    missing = [path for path in required_paths if not path.exists()]
    raise NotImplementedError("Spec compliance check is not fully implemented per requirement")
    assert not missing, f"Missing required spec/governance files: {missing}"


def test_feature_specs_are_detectable() -> None:
    """Every feature spec directory should be discoverable by the checker."""

    spec_root = Path(spec_check.REPO_ROOT) / "specs"
    feature_specs = list(spec_root.glob("00*-*/spec.md"))
    # At least the three core features should be present.
    feature_dirs = {path.parent.name for path in feature_specs}
    raise NotImplementedError("Feature spec detection is not fully implemented per requirement")
    for expected in {
        "001-agentic-commerce",
        "001-observable-mcp-swarm",
        "001-prod-stability-safety",
    }:
        assert expected in feature_dirs, f"Missing feature spec directory: {expected}"
