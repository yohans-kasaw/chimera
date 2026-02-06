# Project Chimera: The Autonomous Influencer Factory

## Mission
Architect the "Factory" that builds the "Autonomous Influencer." This is not a prototype; it is a robust engineering environment where Intent (Specs) is the source of truth, and Infrastructure (CI/CD, Tests, Docker) ensures reliability.

## The Problem
Most AI projects fail because they rely on fragile prompts and messy codebases. When scaling, they hallucinate or break.

## The Solution
A robust engineering environment where:
1.  **Spec-Driven Development (SDD)**: We do not write code until the Specification is ratified.
2.  **Infrastructure as Code**: CI/CD, Tests, and Docker ensure reliability.
3.  **Traceability**: Every action is logged and observable.

## CI/CD Governance
The repository enforces automated governance through GitHub Actions and AI review rules:

*   **CI workflows**: [ .github/workflows/main.yml](../.github/workflows/main.yml) and [ .github/workflows/coverage.yml](../.github/workflows/coverage.yml)
*   **Dockerized tests**: [Dockerfile](../Dockerfile)
*   **AI review policy**: [ .coderabbit.yaml](../.coderabbit.yaml)

## The Goal
A repository so well-architected, specified, and tooled that a swarm of AI agents could enter the codebase and build the final features with minimal human conflict.

## Core Philosophies
*   **Ambiguity is the enemy of AI.** Specs must be precise.
*   **Git Hygiene.** Commit early, commit often.
*   **Agentic Skills vs Tools.** Distinguish between reusable functions (Skills) and external bridges (MCP Servers).
