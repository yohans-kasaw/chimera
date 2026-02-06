"""Anchor tests for the 001-prod-stability-safety feature spec.

These tests provide an explicit, machine-checkable link between the
production stability & safety specs and the automated test suite.
"""

from __future__ import annotations

from pathlib import Path


def test_prod_stability_safety_spec_file_exists() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    spec_path = repo_root / "specs" / "001-prod-stability-safety" / "spec.md"
    assert spec_path.exists(), "Expected Prod Stability & Safety spec.md to exist"
