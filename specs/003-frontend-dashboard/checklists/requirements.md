# Requirements Checklist

## Functional Requirements
- [ ] **Dashboard**: Display list of all active agents with current status.
- [ ] **Dashboard**: Show aggregate metrics (Total Agents, Active Tasks, Error Count).
- [ ] **Agent Detail**: View real-time logs for a selected agent.
- [ ] **Agent Detail**: Pause and Resume agent execution.
- [ ] **Commerce**: View wallet balance and recent transactions.
- [ ] **Settings**: Connect and disconnect MoltBook integration.

## Non-Functional Requirements
- [ ] **Latency**: Dashboard updates should reflect state changes within < 2s.
- [ ] **Responsiveness**: Layout adapts to desktop sizes (min-width 1024px).
- [ ] **Accessibility**: All interactive elements are keyboard accessible (Tab index).
- [ ] **Visuals**: Dark mode default, consistent color coding for status (Green=Active, Red=Error).

## Technical Requirements
- [ ] Use React + TypeScript + Vite.
- [ ] Use Tailwind CSS for styling.
- [ ] Use Shadcn UI for component primitives.
- [ ] Use TanStack Query for data fetching.
- [ ] No hardcoded secrets; use environment variables or API calls.
