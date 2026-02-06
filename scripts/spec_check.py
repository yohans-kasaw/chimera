"""Lightweight spec conformance checks for CI.

This script enforces high-level alignment between the implementation and
the executable specifications under ``specs/``. It is intentionally
lightweight so that AI agents can extend it over time.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]


def ensure_required_files() -> None:
    """Verify that core spec and governance files exist.

    Raises ``SystemExit`` with a non-zero code if any required file is
    missing. This keeps the check simple for use in CI.
    """

    required = [
        REPO_ROOT / "specs" / "_meta.md",
        REPO_ROOT / "specs" / "functional.md",
        REPO_ROOT / "specs" / "technical.md",
        REPO_ROOT / "specs" / "openclaw_integration.md",
        REPO_ROOT / ".coderabbit.yaml",
    ]

    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("[spec-check] Missing required spec/governance files:")
        for path in missing:
            print(f"  - {path}")
        raise SystemExit(1)


def _fail_if_missing(label: str, paths: Iterable[Path]) -> None:
    missing = [str(path) for path in paths if not path.exists()]
    if not missing:
        return
    print(f"[spec-check] Missing {label}:")
    for path in missing:
        print(f"  - {path}")
    raise SystemExit(1)


def ensure_contracts_are_tracked() -> None:
    """Ensure executable contracts referenced in ``technical.md`` exist."""

    contracts = [
        REPO_ROOT / "specs" / "001-agentic-commerce" / "contracts" / "openapi.yaml",
        REPO_ROOT / "specs" / "001-observable-mcp-swarm" / "contracts" / "openapi.yaml",
        REPO_ROOT / "specs" / "001-prod-stability-safety" / "contracts" / "review_api.yaml",
    ]

    _fail_if_missing("executable contract files", contracts)


def ensure_mcp_configuration() -> None:
    """Ensure MCP configuration is present and versioned.

    Rubric expectation:
    - versioned, self-documenting MCP configuration in-repo
    - explicitly defines connection details and tool schemas
    """

    required = [
        REPO_ROOT / "mcp.json",
        REPO_ROOT / "mcp.schema.json",
        REPO_ROOT / "specs" / "mcp_configuration.md",
    ]
    _fail_if_missing("MCP configuration", required)


def ensure_skill_structure() -> None:
    """Ensure skill contracts are formal and discoverable."""

    required = [
        REPO_ROOT / "skills.json",
        REPO_ROOT / "skills.schema.json",
        REPO_ROOT / "specs" / "skills_catalog.md",
    ]
    _fail_if_missing("Skills manifest", required)


def ensure_specs_are_covered_by_tests() -> None:
    """Ensure each feature spec has at least one corresponding test module.

    For every directory under ``specs/00*-*/`` that contains ``spec.md``, we
    require a pytest module named ``test_<feature>.py`` (with dashes replaced
    by underscores) to exist somewhere under ``tests``. This keeps a loose but
    explicit mapping between feature specs and the test suite.
    """

    spec_root = REPO_ROOT / "specs"
    feature_specs = sorted(spec_root.glob("00*-*/spec.md"))
    if not feature_specs:
        return

    test_root = REPO_ROOT / "tests"
    missing_features: list[str] = []
    for spec_path in feature_specs:
        feature_dir = spec_path.parent.name
        normalized = feature_dir.replace("-", "_")
        candidate_name = f"test_{normalized}.py"
        candidates = list(test_root.rglob(candidate_name))
        if not candidates:
            missing_features.append(feature_dir)

    if missing_features:
        print("[spec-check] Missing tests for feature specs:")
        for feature in missing_features:
            print(f"  - specs/{feature}/spec.md")
        raise SystemExit(1)


def ensure_security_specs() -> None:
    """Ensure all feature specs contain mandatory Security/Compliance sections.

    Per the "Security Pro" , every spec must explicitly address:
    1. AuthN/AuthZ (Authentication)
    2. Secrets/Vault
    3. Rate Limiting
    4. Content Safety/Moderation
    5. Containment/Boundaries
    """
    spec_root = REPO_ROOT / "specs"
    feature_specs = sorted(spec_root.glob("00*-*/spec.md"))

    required_keywords = {
        "Authentication": ["Authentication", "AuthN", "AuthZ", "OAuth", "JWT"],
        "Secrets": ["Secret", "Vault", "Environment Variable"],
        "Rate Limiting": ["Rate Limit", "Throttling", "Quota"],
        "Content Safety": ["Content Safety", "Moderation", "Guardrails"],
        "Containment": ["Containment", "Boundaries", "Forbidden Actions"],
    }

    failed_specs = []

    for spec_path in feature_specs:
        content = spec_path.read_text(encoding="utf-8")
        missing_in_file = []

        for category, keywords in required_keywords.items():
            if not any(k in content for k in keywords):
                missing_in_file.append(category)

        if missing_in_file:
            failed_specs.append((str(spec_path), missing_in_file))

    if failed_specs:
        print("[spec-check] Security Score Verification FAILED.")
        print("The following specs fail the 'Security Pro' requirements:")
        for path, missing in failed_specs:
            print(f"\nFILE: {path}")
            print(f"MISSING SECTIONS: {', '.join(missing)}")
            print(
                "REQUIRED: You must add a 'Security & Compliance' section addressing these topics."
            )
        raise SystemExit(1)


def ensure_acceptance_criteria() -> None:
    """Ensure all feature specs contain mandatory Acceptance Criteria (Gherkin).

    Per the "Acceptance Criteria Pro" rubric, every spec must include:
    1. A section named "Acceptance Criteria (Gherkin)"
    2. At least one "Given/When/Then" block
    3. Traceability tags (Ref/Trace)
    """
    spec_root = REPO_ROOT / "specs"
    feature_specs = sorted(spec_root.glob("00*-*/spec.md"))

    failed_specs = []

    for spec_path in feature_specs:
        content = spec_path.read_text(encoding="utf-8")

        has_header = "## Acceptance Criteria (Gherkin)" in content
        has_gherkin = "Given" in content and "When" in content and "Then" in content
        has_trace = "Trace" in content or "Ref" in content

        if not (has_header and has_gherkin and has_trace):
            failed_specs.append(str(spec_path))

    if failed_specs:
        print("[spec-check] Acceptance Criteria Verification FAILED.")
        print("The following specs fail the 'Acceptance Criteria Pro' rubric requirements:")
        for path in failed_specs:
            print(f"  - {path} (Missing 'Acceptance Criteria (Gherkin)' header or Gherkin syntax)")
        raise SystemExit(1)


def main() -> None:
    ensure_required_files()
    ensure_contracts_are_tracked()
    ensure_mcp_configuration()
    ensure_skill_structure()
    ensure_specs_are_covered_by_tests()
    ensure_security_specs()
    ensure_acceptance_criteria()
    print("[spec-check] All required spec, contract, and test mappings are present.")


if __name__ == "__main__":
    main()
