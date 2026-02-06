# Frontend Specification: Chimera Command Console
**Spec ID**: 003-frontend-dashboard
**Status**: Draft
**Version**: 1.0.0

## 1. Overview
The **Chimera Command Console** is the primary user interface for the Chimera modular monolith. It enables human operators to monitor the Agent Swarm, manage Commerce flows, and configure Integrations (MoltBook, OpenClaw). It provides a "Control Room" experience with real-time data streaming and direct intervention capabilities.

## 2. User Experience (UX) Goals
1.  **Observability**: Instant visibility into "Who is doing what?" (Agent States).
2.  **Intervention**: One-click ability to Pause, Stop, or Redirect an agent.
3.  **Transparency**: Clear audit trails for financial transactions (Commerce) and social actions (MoltBook).
4.  **Aesthetic**: "Cyber-Physical" — Dark mode, monospaced fonts, high-contrast status indicators.

---

## 3. Screen Inventory & Routing

| Route | Screen Name | Description | Key Interactions |
| :--- | :--- | :--- | :--- |
| `/` | **Swarm Dashboard** | High-level overview of system health and active agents. | Filter agents, View aggregate metrics. |
| `/agents/:id` | **Agent Detail** | Deep dive into a single agent's "Brain" (logs, memory, state). | View live logs, Pause/Resume, Inspect Memory. |
| `/commerce` | **Commerce Ledger** | Financial overview of the swarm. | View wallet balances, Review transaction history. |
| `/settings` | **System Settings** | Configuration for API keys and Integrations. | Connect MoltBook, Rotate API Keys. |

---

## 4. Component Hierarchy & Wireframes

### 4.1. Global Layout (`MainLayout`)
Persistent navigation and status bar.
```
+---------------------------------------------------------------+
| [Logo] Chimera    [Dashboard] [Commerce] [Settings]   (User)  |  <-- Header
+---------------------------------------------------------------+
|                                                               |
|  (Page Content Area)                                          |
|                                                               |
+---------------------------------------------------------------+
| [Status: Connected]  [Active Agents: 12]  [Errors: 0]         |  <-- StatusBar
+---------------------------------------------------------------+
```

### 4.2. Swarm Dashboard (`/`)
**Goal**: Monitor fleet health.

**Wireframe**:
```
+---------------------------------------------------------------+
|  h1. Swarm Overview                                           |
|                                                               |
|  [ MetricCard: Active Agents (12) ] [ MetricCard: Tasks (45) ]|
|  [ MetricCard: Revenue ($1,204)   ] [ MetricCard: Errors (0) ]|
|                                                               |
|  h2. Active Agents                               [Filter v]   |
|  +---------------------------------------------------------+  |
|  | Agent ID | Name      | Status      | Last Action        |  |
|  |----------|-----------|-------------|--------------------|  |
|  | ag_001   | Scout-1   | (O) Working | Scraping page...   |  | -> Click rows
|  | ag_002   | Buyer-9   | (X) Error   | Timeout waiting... |  |    to nav to
|  | ag_003   | Writer-X  | (-) Idle    | Waiting for task   |  |    /agents/:id
|  +---------------------------------------------------------+  |
+---------------------------------------------------------------+
```
*   **Data Source**: `GET /api/v1/swarm/agents` (List)
*   **Components**: `MetricGrid`, `AgentTable`, `StatusBadge`.

### 4.3. Agent Detail (`/agents/:id`)
**Goal**: Debug and control a specific agent.

**Wireframe**:
```
+---------------------------------------------------------------+
|  < Back  |  h1. Scout-1 (ag_001)           [Pause] [Restart]  |
+---------------------------------------------------------------+
|  [ Col 1: State & Config ]  |  [ Col 2: Live Terminal ]       |
|                             |                                 |
|  Status: Working            |  > [10:01] Observing task...    |
|  Role: Research             |  > [10:02] Thinking...          |
|  Model: gpt-4-turbo         |  > [10:02] Tool Call: fetch()   |
|                             |  > [10:03] Result: 200 OK       |
|  Current Task:              |  > _                            |
|  "Analyze market trends..." |                                 |
|                             |                                 |
|  Memory Usage: 45%          |                                 |
+---------------------------------------------------------------+
```
*   **Data Source**:
    *   Init: `GET /api/v1/swarm/agents/{id}`
    *   Stream: `WS /ws/events` (Filter by `agent_id`)
*   **Actions**:
    *   `[Pause]`: `POST /api/v1/swarm/agents/{id}/pause`
    *   `[Restart]`: `POST /api/v1/swarm/agents/{id}/restart`

### 4.4. Commerce Ledger (`/commerce`)
**Goal**: Audit financial flows.

**Wireframe**:
```
+---------------------------------------------------------------+
|  h1. Commerce & Wallet                                        |
|                                                               |
|  [ Wallet Balance: $540.22 USD ]  [ Pending: $50.00 ]         |
|                                                               |
|  h2. Transactions                                             |
|  +---------------------------------------------------------+  |
|  | Date       | Agent    | Amount  | Type     | Status     |  |
|  |------------|----------|---------|----------|------------|  |
|  | 2023-10-01 | Buyer-9  | -$20.00 | Purchase | Completed  |  |
|  | 2023-10-01 | Scout-1  | +$0.05  | Reward   | Pending    |  |
|  +---------------------------------------------------------+  |
+---------------------------------------------------------------+
```
*   **Data Source**: `GET /api/v1/commerce/ledger`
*   **Schema**: `Transaction` object (amount, currency, timestamp, agent_id).

### 4.5. Settings (`/settings`)
**Goal**: Manage integrations.

**Wireframe**:
```
+---------------------------------------------------------------+
|  h1. Settings                                                 |
|                                                               |
|  h3. Integrations                                             |
|                                                               |
|  [ MoltBook ]                                                 |
|  Status: (x) Disconnected                                     |
|  [ Connect Account ] button                                   |
|                                                               |
|  [ OpenClaw ]                                                 |
|  Status: (v) Connected (Endpoint: wss://api.openclaw.net)     |
|                                                               |
+---------------------------------------------------------------+
```
*   **Data Source**: `GET /api/v1/integrations/moltbook/status`
*   **Action**: `POST /api/v1/integrations/moltbook/connect` (Payload: `{ api_key, handle }`)

---

## 5. Interaction Flows

### 5.1. Critical Flow: Human Intervention (Stop Agent)
1.  **Trigger**: User spots an agent in "Looping" or "Error" state on the **Swarm Dashboard**.
2.  **Action**: User clicks the agent row.
3.  **View**: User is navigated to **Agent Detail**.
4.  **Verification**: User reviews the "Live Terminal" log to confirm bad behavior.
5.  **Intervention**: User clicks the **[Pause]** button.
6.  **System Response**:
    *   Frontend sends `POST .../pause`.
    *   Frontend optimistically updates UI status to "Pausing...".
    *   Backend confirms pause.
    *   UI status updates to "Paused (Human Intervention)".

### 5.2. Critical Flow: Connect MoltBook
1.  **Trigger**: User wants to enable social capabilities.
2.  **Action**: Navigate to **Settings** -> Click **[Connect Account]** on MoltBook card.
3.  **Interaction**: Modal appears requesting `Handle` and `API Key`.
4.  **Submission**: User enters data and clicks **Save**.
5.  **System Response**:
    *   Frontend sends `POST .../connect`.
    *   Backend validates credentials.
    *   On success, Modal closes, and Card updates to "Connected (Last sync: Just now)".

---

## 6. Data & Accessibility

### 6.1. Accessibility Standards (WCAG 2.1 AA)
*   **Keyboard Nav**: All tables and actions must be focusable via `Tab`.
*   **ARIA Labels**:
    *   Status Badges: `aria-label="Status: Working"`
    *   Terminal: `aria-live="polite"` for new log entries.
*   **Color Contrast**: Ensure text on status badges passes 4.5:1 ratio.

### 6.2. Error Handling
*   **Network**: Global `ToastProvider` for API failures ("Failed to fetch agents").
*   **Validation**: Form inputs (e.g., API Key) must show inline errors.
*   **Empty States**: Tables must show "No agents found" or "No transactions" placeholders.

## 7. API Contract Mapping

| Frontend Component | Field/Action | Backend Schema / Endpoint |
| :--- | :--- | :--- |
| **AgentTable** | `id`, `name`, `status` | `AgentSchema` from `GET /swarm/agents` |
| **AgentDetail** | `logs` (stream) | `LogMessage` from `WS /events` |
| **AgentDetail** | `[Pause]` button | `POST /swarm/agents/{id}/pause` |
| **CommerceLedger** | `amount`, `currency` | `TransactionSchema` from `GET /commerce/ledger` |
| **Settings** | `connect` | `POST /integrations/moltbook/connect` |

## Security & Compliance *(mandatory)*
This feature adheres to the [Master Security Architecture](../technical.md#7-security-architecture--compliance-rubric-pro).

*   **Authentication**: Uses standard OAuth2/JWT flow via the CommerceManager.
*   **Secrets Management**: All credentials managed via Vault/Env.
*   **Rate Limiting**: Enforces standard 60 req/min limit.
*   **Content Safety**: Subject to standard Moderation/Judge pipeline.
*   **Containment**: Strict Resource Limits apply (Execution Time, Token Budget).
