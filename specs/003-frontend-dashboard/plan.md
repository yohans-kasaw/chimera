# Implementation Plan: Chimera Command Console

## Phase 1: Foundation & Scaffolding
*   **Goal**: Initialize project and setup core libraries.
*   **Tasks**:
    1.  Initialize Vite project (React + TypeScript).
    2.  Install Tailwind CSS and configure `tailwind.config.js`.
    3.  Install Shadcn UI CLI and initialize.
    4.  Install `tanstack/react-query`, `axios`, `lucide-react`, `react-router-dom`.
    5.  Set up directory structure (`features/`, `components/`, `hooks/`).

## Phase 2: Core Components & Layout
*   **Goal**: Build the shell of the application.
*   **Tasks**:
    1.  Create `MainLayout` with Sidebar and Header.
    2.  Implement `StatusBar` component (mocked data).
    3.  Create reusable atoms: `StatusBadge`, `MetricCard`, `DataTable`.
    4.  Set up React Router with placeholders for all main pages.

## Phase 3: Swarm Dashboard (Read-Only)
*   **Goal**: Visualize agent state.
*   **Tasks**:
    1.  Create `useAgents` hook (mocked API).
    2.  Implement `AgentTable` with columns: ID, Name, Status, Role.
    3.  Implement `MetricGrid` for high-level stats.
    4.  Connect to real API `GET /api/v1/swarm/agents` (if available, else mock).

## Phase 4: Agent Detail & Live Logs
*   **Goal**: "Control Room" view.
*   **Tasks**:
    1.  Create `AgentDetail` page layout.
    2.  Implement `LogStream` component (auto-scrolling terminal view).
    3.  Implement `WebSocketProvider` to listen for log events.
    4.  Add `Pause/Resume` buttons with optimistic UI updates.

## Phase 5: Commerce & Settings
*   **Goal**: Manage secondary domains.
*   **Tasks**:
    1.  Build `CommerceLedger` table with transaction history.
    2.  Build `Settings` page with MoltBook connection form.
    3.  Implement form validation (Zod + React Hook Form).

## Phase 6: Polish & Accessibility
*   **Goal**: Ensure 5-star quality.
*   **Tasks**:
    1.  Audit color contrast and keyboard navigation.
    2.  Add empty states and loading skeletons.
    3.  Implement "Toast" notifications for success/error states.
    4.  Final build and lint check.
