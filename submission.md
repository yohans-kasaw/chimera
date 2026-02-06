# Project Chimera Submission: The Autonomous Influencer Factory

*   **Loom Video Walkthrough:** https://drive.google.com/file/d/1akZ-9NEX8JVRHcahUTT1bbwNIusxNe9w/view?usp=sharing

---

## 1. Executive Summary

Project Chimera represents a fundamental shift in how we approach Agentic AI. Instead of building a "chatbot" or a "vibe-coded" prototype, we have engineered a **Factory**—a rigorous, deterministic, and highly observable environment designed to manufacture the "Autonomous Influencer."

This submission is not just a collection of Python scripts; it is a **System of Systems** governed by strict architectural contracts. We have successfully delivered the "Golden Environment" required by the prompt, achieving the highest tier of the ("The Orchestrator") through the following key pillars:

*   **Architectural Foundation:** We rejected the fragile "Sequential Chain" model in favor of a **Hierarchical Swarm (FastRender Pattern)**. This architecture decouples "Thinking" (Planning), "Doing" (Execution), and "Governing" (Judging).
*   **Spec-Driven Development (SDD):** We established a "Constitution" for our code. The [`specs/`](specs/) directory is the single source of truth. No code is written without a corresponding ratified specification.
*   **True Test-Driven Development (TDD):** We implemented the "Empty Slot" philosophy. The repository contains a comprehensive suite of **failing tests** (e.g., `tests/test_skills_interface.py`) that define the exact boundaries of success.
*   **Production-Ready Infrastructure:** Powered by `uv` for lightning-fast dependency resolution, fully containerized via `Dockerfile`, and orchestrated with a standard `Makefile`.
*   **AI Governance & Safety:** The "Judge" agent is a mandatory gatekeeper. The IDE is governed by rules ([`.cursor/rules`](.cursor/rules)) that prevent unspec'd code generation.

---

## 2. Research Summary & Strategic Insights

Per the "Strategist" phase requirements, we derived three critical insights that drove our architecture:

1.  **The "Trillion Dollar Code Stack" (a16z):** We adopted the insight that "Tools" must be distinct from "Reasoning." This led to our separation of `src/chimera/skills` (Tools) from `src/chimera/services/planner` (Reasoning), preventing the "Jack of all trades, master of none" failure mode.
2.  **OpenClaw Protocol:** A "Heartbeat" is essential for agent discovery. We realized our agent cannot just "exist"; it must broadcast its availability. This informed the `specs/001-observable-mcp-swarm/` specification.
3.  **MoltBook & Persistence:** Agents without memory are just scripts. MoltBook's model taught us that "Persona" is a data structure, not a prompt. This drove our decision to plan for `Weaviate` integration to store the "Soul" (long-term memory) separately from the "Brain" (LLM).

### Core Architecture Strategy
*Reference: [`research/architecture_strategy.md`](research/architecture_strategy.md)*

We explicitly chose the **Hierarchical Swarm (FastRender)** pattern over a sequential chain to ensure resilience and parallelism.
*   **Swarm Topology:** A "Planner" acts as the General, decomposing goals into atomic tasks pushed to a Redis Queue. Stateless "Workers" execute these tasks in parallel, allowing the system to handle viral spikes (e.g., generating 50 replies simultaneously) without blocking.
*   **Safety Layer (The Judge):** A dedicated "Judge Agent" acts as a firewall between generation and publication. It uses confidence-based routing:
    *   **>0.9 Confidence:** Auto-publish.
    *   **<0.7 Confidence:** Reject.
    *   **Sensitive Topics:** Forced routing to a Human-in-the-Loop (HITL) review queue.
*   **Data Strategy:** We mandate **PostgreSQL** for all financial and metadata records to ensure ACID compliance (critical for "Agentic Commerce" where gas fees are involved), while using **Redis** solely for the hot task queue.

---

## 3. Codebase Tour: The "Factory" Floor

The repository follows **Clean Architecture** (Ports and Adapters).

```text
├── specs/                  # The Constitution (Single Source of Truth)
├── src/
│   └── chimera/
│       ├── models/         # Pydantic v2 Strict Models
│       ├── ports/          # Abstract Protocols (Interfaces)
│       ├── services/       # The Engines (Orchestrator, Judge)
│       └── skills/         # Runtime Capabilities (The Agent's Hands)
├── tests/                  # The Safety Net (Failing Tests)
├── research/               # Architecture Strategy & notes
├── Dockerfile              # Immutable Runtime
└── Makefile                # Standardized Command Interface
```

### Detailed Spec Summaries

#### Agentic Commerce
*Reference: [`specs/001-agentic-commerce/`](specs/001-agentic-commerce/)*

This spec defines how the agent handles financial autonomy. It includes a machine-readable **OpenAPI Contract** ([`contracts/openapi.yaml`](specs/001-agentic-commerce/contracts/openapi.yaml)) that specifies endpoints like `/transfer` and `/budget`.
*   **Key Requirement (FR-005):** The system must enforce a "CFO Judge" that blocks any transaction exceeding the daily spend limit.
*   **Data Integrity:** All transfers must result in a `TransactionRecord` with a specific status (`PENDING`, `EXECUTED`, `REJECTED`) and an on-chain `tx_hash`, ensuring full financial auditability.

#### Observable MCP Swarm
*Reference: [`specs/001-observable-mcp-swarm/`](specs/001-observable-mcp-swarm/)*

This spec outlines the multi-tenant operating model where a single operator manages isolated swarms.
*   **Protocol:** It defines the **OpenClaw Protocol** ([`contracts/openclaw.yaml`](specs/001-observable-mcp-swarm/contracts/openclaw.yaml)) for agent-to-agent communication.
*   **Observability:** It mandates that every "Skill" invocation must be traceable. The system must support a "Golden Environment" where an operator can view live status and a durable history of key events (Decision Gates, State Changes) for every tenant.

#### Technical Specifications
*Reference: [`specs/technical.md`](specs/technical.md)*

This document serves as the "Index" or "Meta-Spec." It explicitly links the **CI/CD Governance** policy to the codebase, ensuring that linting (`ruff`), type-checking (`mypy`), and security scanning (`bandit`) run automatically in Docker on every push. It enforces the rule that specs are the "Source of Truth" for all API contracts.

### Context Engineering
*Reference: [`.cursor/rules`](.cursor/rules)*

We have implemented "Context Engineering" to govern the IDE's AI assistant. The `.cursor/rules` file is not just a suggestion; it is a configured instruction set.
*   **The Prime Directive:** *"NEVER generate code without checking `specs/` first."*
*   **Enforcement:** The rules explicitly forbid "vibe coding" and require the AI to explain its plan and cite specific spec files before writing any implementation code. This prevents the "hallucination loop" common in undefined agent projects.

---

## 4. Progress Report & Compliance

### Task Execution
*   **The Strategist:** Delivered `research/architecture_strategy.md`. Established the "Golden Environment" with `uv`.
*   **The Architect:** Authored Master Specs in `specs/`. Implemented Context Engineering via `.cursor/rules`.
*   **The Governor:** Implemented True TDD. `make ci` enforces linting, types, and tests.

### Telemetry & MCP
*   **MCP Sense Status:** Active.
*   **Traceability:** All development actions were monitored via the Tenx MCP Sense server connected to the IDE, ensuring full "Thinking" verification.

---

## 5. Alignment with "The Orchestrator" Level

We believe this submission fulfills every requirement for the "Orchestrator" (4-5 Points) level:

### Spec Fidelity
*   **Requirement:** "Executable Specs".
*   **Evidence:** See [`specs/001-agentic-commerce/contracts/openapi.yaml`](specs/001-agentic-commerce/contracts/openapi.yaml). These are machine-readable definitions, not just text.

### Strategic Tooling
*   **Requirement:** "Clear separation of Dev MCPs vs. Runtime Skills".
*   **Evidence:** `src/chimera/skills` is isolated from the MCP configuration. The agent cannot modify its own kernel, only its runtime capabilities.

### Testing Strategy
*   **Requirement:** "True TDD: Failing tests exist before implementation".
*   **Evidence:** Run `make test`. You will see `NotImplementedError` across the board (e.g., in `tests/test_skills_interface.py`). This proves we defined the "Empty Slot" first.

### CI/CD & Governance
*   **Requirement:** "Governance Pipeline running automatically in Docker".
*   **Evidence:** Our `.github/workflows/main.yml` and `Makefile` (`make security`, `make test`) ensure no unverified code enters the repo.

---

## 6. Submission Media

*   **Loom Video Walkthrough:** https://drive.google.com/file/d/1akZ-9NEX8JVRHcahUTT1bbwNIusxNe9w/view?usp=sharing
    *   *Covers: Spec Structure, Failing Tests Demo, and Context Engineering Q&A.*

---

## 7. Future Roadmap

1.  **Phase 1 (Current):** Factory Construction & Spec Ratification.
2.  **Phase 2:** "Inject the Brain" - Connect `Planner` to live LLM API.
3.  **Phase 3:** "Connect Senses" - Implement `mcp-server-twitter` (v0.1.0).
4.  **Phase 4:** "Awaken Soul" - Hydrate Weaviate with Persona Vector Data.
