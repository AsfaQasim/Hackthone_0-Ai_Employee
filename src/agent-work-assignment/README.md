# Agent Work Assignment and Tracking System

This module implements a file-based task orchestration system that manages work distribution across multiple AI agents operating within an Obsidian vault.

## Directory Structure

```
src/agent-work-assignment/
├── models/              # Core data models and type definitions
│   ├── TaskMetadata.ts      # Task metadata and priority types
│   ├── AgentMetadata.ts     # Agent metadata and status types
│   ├── ClaimResult.ts       # Task claim result types
│   ├── AssignmentStrategy.ts # Assignment strategy enum
│   └── index.ts             # Central export for all models
├── components/          # System components (to be implemented)
│   ├── AgentRegistry.ts
│   ├── TaskAssignmentEngine.ts
│   ├── TaskRouter.ts
│   ├── ClaimLockManager.ts
│   └── AbandonmentDetector.ts
└── README.md           # This file

tests/agent-work-assignment/
├── models.test.ts      # Unit tests for data models
└── ...                 # Additional test files (to be added)
```

## Core Data Models

### TaskMetadata
Represents metadata for a task in the system.

**Fields:**
- `taskId`: Unique identifier for the task
- `priority`: Task priority ('critical' | 'high' | 'medium' | 'low')
- `taskType`: Type of task (e.g., 'email_processing', 'invoice_generation')
- `requiredCapabilities`: Array of capabilities required to handle the task
- `createdAt`: Timestamp when task was created
- `claimedAt`: Optional timestamp when task was claimed
- `claimedBy`: Optional agent ID that claimed the task
- `completedAt`: Optional timestamp when task was completed
- `reclaimCount`: Number of times task has been reclaimed due to timeout
- `timeoutMinutes`: Timeout duration for this task

### AgentMetadata
Represents metadata for an agent in the system.

**Fields:**
- `agentId`: Unique identifier for the agent
- `capabilities`: Array of capabilities the agent possesses
- `maxConcurrentTasks`: Maximum number of tasks agent can handle concurrently
- `maxTasksByType`: Map of task type to maximum concurrent tasks of that type
- `status`: Agent status ('active' | 'inactive' | 'unresponsive')
- `lastHeartbeat`: Timestamp of last heartbeat from agent
- `registeredAt`: Timestamp when agent was registered

### ClaimResult
Represents the result of a task claim operation.

**Fields:**
- `success`: Whether the claim was successful
- `taskId`: ID of the task being claimed
- `agentId`: ID of the agent attempting to claim
- `error`: Optional error message if claim failed

### AssignmentStrategy
Enum for task assignment strategies:
- `'round-robin'`: Distribute tasks evenly across agents
- `'priority-first'`: Assign highest priority tasks first
- `'least-loaded'`: Assign to agent with fewest current tasks
- `'capability-match'`: Assign to most specialized agent

## Testing

The module uses both unit tests and property-based tests:

```bash
# Run all tests
npm test

# Run only unit tests
npm run test:unit

# Run only property-based tests
npm run test:property

# Run tests in watch mode
npm run test:watch
```

## Implementation Status

- [x] Core data models and types
- [x] Model validation functions
- [x] Basic unit tests for models
- [ ] Agent Registry component
- [ ] Task Assignment Engine component
- [ ] Task Router component
- [ ] Claim Lock Manager component
- [ ] Abandonment Detector component
- [ ] Property-based tests
- [ ] Integration tests

## References

- Requirements: `.kiro/specs/agent-work-assignment/requirements.md`
- Design: `.kiro/specs/agent-work-assignment/design.md`
- Tasks: `.kiro/specs/agent-work-assignment/tasks.md`
