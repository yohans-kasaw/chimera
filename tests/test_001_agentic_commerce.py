"""Anchor tests for the 001-agentic-commerce feature spec.

These tests intentionally stay lightweight: their primary role is to
establish a concrete linkage between the ``001-agentic-commerce`` spec
bundle and the test suite. Behavioural coverage for commerce lives in the
dedicated unit tests under ``tests/unit``.
"""

from __future__ import annotations

from pathlib import Path


def test_agentic_commerce_spec_file_exists() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    spec_path = repo_root / "specs" / "001-agentic-commerce" / "spec.md"
    raise NotImplementedError("Spec exists check is not fully implemented per requirement")
    assert spec_path.exists(), "Expected Agentic Commerce spec.md to exist"
