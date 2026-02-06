# Frontend Architecture & Design System

## 1. Architectural Overview

The Chimera Frontend is a **Single Page Application (SPA)** built to provide real-time visibility and control over the Agent Swarm. It communicates with the FastAPI backend via REST and WebSockets.

### Core Stack
*   **Framework**: React 18+ (TypeScript) via Vite
*   **Styling**: Tailwind CSS + Shadcn UI (Radix Primitives)
*   **State Management**: TanStack Query (Server State) + Zustand (Client State)
*   **Routing**: React Router DOM v6
*   **Build/Tooling**: Vite, ESLint, Prettier

---

## 2. Design Patterns

### 2.1. Feature-First Directory Structure
We organize code by business domain (Features) rather than technical type.
```
src/
  features/
    swarm/          # Agent Swarm domain
    commerce/       # Commerce & Ledger domain
    settings/       # App configuration
  components/       # Shared UI atoms (Button, Card)
  hooks/            # Shared logic
  lib/              # Utilities (API client, formatters)
```

### 2.2. Data Fetching & Caching
*   **Queries**: Encapsulate API calls in custom hooks (e.g., `useSwarmAgents`).
*   **Optimistic Updates**: For high-frequency actions (e.g., "Pause Agent"), update UI immediately before server confirmation.
*   **WebSockets**: Use a global `SocketProvider` to listen for `agent.event` and invalidate relevant queries.

---

## 3. Integration Specifications

### 3.1. Backend-for-Frontend (BFF) Pattern
The frontend consumes the FastAPI endpoints directly.
*   **Base URL**: `/api/v1`
*   **Auth**: Bearer Token (JWT) stored in `localStorage` (or HTTP-only cookie).

### 3.2. WebSocket Protocol
*   **Endpoint**: `/ws/events`
*   **Message Format**:
    ```json
    {
      "type": "agent.log",
      "payload": { "agent_id": "123", "message": "Thinking..." }
    }
    ```

---

## 4. Design System (Chimera UI)

### 4.1. Theme
*   **Mode**: Dark Mode by default (Cyberpunk/Terminal aesthetic).
*   **Colors**:
    *   Primary: `cyan-500` (Active/Safe)
    *   Destructive: `rose-500` (Error/Stop)
    *   Background: `slate-950`
*   **Typography**: Inter (UI), JetBrains Mono (Logs/Code).

### 4.2. Core Components
*   `StatusBadge`: Visual indicator of agent state (Idle, Busy, Error).
*   `LogStream`: Virtualized list for real-time terminal output.
*   `MetricCard`: Sparkline + Value for dashboard stats.

---

## 5. Specification Registry

Detailed specifications for frontend modules:

| ID | Module | Status | Description |
| :--- | :--- | :--- | :--- |
| **003** | **[Frontend Dashboard](./003-frontend-dashboard/spec.md)** | **Draft** | Main console for Swarm and Commerce management. |

---

## 6. Governance & Compliance
All architectural decisions and code modifications are subject to the **Agent Governance Rules** defined in [`specs/_meta.md`](./_meta.md).
*   **Spec-First**: No architectural deviation without spec updates.
*   **Strict Typing**: All frontend code must pass TypeScript strict mode.
*   **Traceability**: All user actions must be logged via the `TelemeteryService`.
