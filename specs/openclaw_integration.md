# OpenClaw Integration Strategy

## Overview
Project Chimera integrates with the OpenClaw "Agent Social Network" protocol to publish its availability, status, and capabilities to other agents in the ecosystem. This allows the Chimera swarm to participate in the broader economy of autonomous agents.

## Protocol Definition
The integration adheres to the OpenClaw Agent Protocol version 1.0.0.
*   **Protocol Spec**: [openclaw.yaml](./001-observable-mcp-swarm/contracts/openclaw.yaml)

## Interaction Patterns

### 1. Heartbeat & Availability
The Chimera Swarm Brain publishes a heartbeat message every 30 seconds to the `agent.heartbeat` channel.
*   **Payload**: `agent_id`, `status` (ONLINE, BUSY, OFFLINE), `capabilities` (list of supported skills), `load` (current CPU/Task load).
*   **Purpose**: Announces presence to the OpenClaw network registry.

### 2. Task Assignment
Chimera subscribes to the `agent.assign` channel to receive tasks from external orchestrators or other agents.
*   **Behavior**: Upon receiving a `TaskAssignment` message, the Swarm Brain:
    1.  Validates the task against the internal Judge Policy.
    2.  If accepted, spawns or assigns an internal agent.
    3.  Publishes a `TaskStarted` event.

### 3. Event Reporting
Throughout the lifecycle of an assigned task, Chimera publishes events to `agent.event`.
*   **Events**: `TaskStarted`, `TaskProgress`, `TaskCompleted`, `TaskFailed`.
*   **Traceability**: All events include the original `task_id` for correlation.

## Data Mapping
*   **Capabilities**: Mapped from the internal `Skills` registry.
*   **Agent ID**: Corresponds to the Tenant ID or specific Agent Node ID within Chimera.
