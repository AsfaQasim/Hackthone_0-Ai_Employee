# Implementation Plan: Agent Work Assignment and Tracking System

## Overview

This implementation plan breaks down the Agent Work Assignment and Tracking System into discrete coding tasks. The system will be built incrementally, starting with core data models and interfaces, then implementing each major component, and finally integrating everything together. Testing tasks are included as sub-tasks to validate functionality early and catch errors during development.

## Tasks

- [x] 1. Set up project structure and core data models
  - Create directory structure for components, models, and tests
  - Define TypeScript interfaces for TaskMetadata, AgentMetadata, ClaimResult
  - Define enums for AssignmentStrategy, AgentStatus, TaskPriority
  - Set up fast-check library for property-based testing
  - _Requirements: 1.1, 2.2, 3.1, 7.1, 8.3_

- [ ] 2. Implement Agent Registry component
  - [x] 2.1 Create AgentRegistry class with registration and deregistration methods
    - Implement registerAgent() to store agent metadata and create In_Progress folder
    - Implement deregisterAgent() to remove agent from registry
    - Implement agent metadata storage (in-memory Map and file-based persistence)
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ]* 2.2 Write property test for agent registration round-trip
    - **Property 1: Agent Registration Round-Trip**
    - **Validates: Requirements 1.1, 1.2, 9.2, 17.1**
  
  - [ ]* 2.3 Write property test for duplicate registration rejection
    - **Property 2: Duplicate Registration Rejection**
    - **Validates: Requirements 1.5**
  
  - [x] 2.4 Implement heartbeat tracking and agent status management
    - Implement recordHeartbeat() to update lastHeartbeat timestamp
    - Implement getAgentStatus() to query agent metadata
    - Implement listActiveAgents() to filter by status
    - _Requirements: 10.1, 10.4_
  
  - [ ]* 2.5 Write property test for heartbeat timestamp tracking
    - **Property 27: Heartbeat Timestamp Tracking**
    - **Validates: Requirements 10.4**
  
  - [x] 2.6 Implement capacity tracking methods
    - Implement hasCapacity() to check if agent can accept tasks
    - Implement hasCapacityForType() to check per-type limits
    - Implement getAgentWorkload() to count current tasks
    - _Requirements: 7.2, 7.5, 17.2, 17.5_
  
  - [ ]* 2.7 Write property tests for capacity tracking
    - **Property 21: Capacity Calculation Accuracy**
    - **Validates: Requirements 7.5, 17.5**
  
  - [x] 2.8 Implement capability-based agent queries
    - Implement getAgentsByCapability() to filter agents by capability
    - _Requirements: 9.1, 9.2_
  
  - [ ]* 2.9 Write unit tests for Agent Registry edge cases
    - Test empty registry, invalid agent IDs, missing folders
    - _Requirements: 1.1, 1.2, 1.5_

- [x] 3. Checkpoint - Ensure Agent Registry tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement Task Router component
  - [x] 4.1 Create TaskRouter class with capability matching
    - Implement getEligibleAgents() to match task capabilities to agent capabilities
    - Implement canAgentHandleTask() to check single agent-task match
    - _Requirements: 9.1, 9.4, 9.5_
  
  - [ ]* 4.2 Write property tests for capability-based routing
    - **Property 23: Capability-Based Task Routing**
    - **Property 24: Multiple Capabilities Support**
    - **Property 25: No-Capability Task Availability**
    - **Validates: Requirements 9.1, 9.4, 9.5**
  
  - [x] 4.3 Implement routing rules system
    - Implement addRoutingRule() and removeRoutingRule()
    - Implement evaluateRoutingRules() to apply rules to tasks
    - _Requirements: 9.1_
  
  - [ ]* 4.4 Write unit tests for routing rules
    - Test rule priority, rule conditions, rule conflicts
    - _Requirements: 9.1_

- [ ] 5. Implement Claim Lock Manager component
  - [x] 5.1 Create ClaimLockManager class with atomic file operations
    - Implement acquireLock() using file system locks or lock files
    - Implement releaseLock() to clean up locks
    - Implement releaseStaleLocksOlderThan() for timeout cleanup
    - _Requirements: 4.1, 4.3, 4.4_
  
  - [x] 5.2 Implement atomic claim operation
    - Implement attemptClaim() with atomic file rename
    - Update task frontmatter with claim metadata
    - Implement retry logic with exponential backoff
    - _Requirements: 3.1, 3.2, 4.1, 4.5_
  
  - [ ]* 5.3 Write property test for atomic task claim
    - **Property 10: Atomic Task Claim**
    - **Validates: Requirements 3.1, 3.2**
  
  - [ ]* 5.4 Write property test for mutual exclusion on claims
    - **Property 12: Mutual Exclusion on Claims**
    - **Validates: Requirements 4.1**
  
  - [ ]* 5.5 Write property test for failed claim atomicity
    - **Property 11: Failed Claim Atomicity**
    - **Validates: Requirements 3.4**
  
  - [x] 5.6 Implement releaseClaim() for task release
    - Move task back to Needs_Action
    - Clear claim metadata from frontmatter
    - _Requirements: 13.1, 13.2, 15.3_
  
  - [ ]* 5.7 Write unit tests for claim lock edge cases
    - Test concurrent claims, stale locks, lock timeouts
    - _Requirements: 4.1, 4.4, 4.5_

- [x] 6. Checkpoint - Ensure Claim Lock Manager tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement Task Assignment Engine component
  - [x] 7.1 Create TaskAssignmentEngine class with file watcher
    - Implement startWatching() to monitor Needs_Action folder
    - Implement stopWatching() to clean up file watcher
    - Implement task file parsing and metadata extraction
    - _Requirements: 2.1, 2.2, 2.4_
  
  - [x] 7.2 Implement task queue with priority ordering
    - Implement getAvailableTasks() to return sorted queue
    - Implement getTasksByPriority() to filter by priority
    - Maintain queue ordered by priority then timestamp
    - _Requirements: 2.3, 8.1, 8.4_
  
  - [ ]* 7.3 Write property test for task queue priority ordering
    - **Property 6: Task Queue Priority Ordering**
    - **Validates: Requirements 2.3, 8.1, 8.4**
  
  - [ ]* 7.4 Write property test for task queue synchronization
    - **Property 7: Task Queue Synchronization**
    - **Validates: Requirements 2.4**
  
  - [x] 7.5 Implement assignment strategies
    - Implement round-robin strategy
    - Implement priority-first strategy
    - Implement least-loaded strategy
    - Implement capability-match strategy
    - Implement setStrategy() to switch strategies at runtime
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_
  
  - [ ]* 7.6 Write property tests for assignment strategies
    - **Property 41: Round-Robin Distribution**
    - **Property 42: Priority-First Assignment**
    - **Property 43: Least-Loaded Assignment**
    - **Property 44: Runtime Strategy Change**
    - **Validates: Requirements 16.1, 16.2, 16.4, 16.5**
  
  - [x] 7.7 Implement assignNextTask() method
    - Coordinate with TaskRouter to get eligible agents
    - Apply assignment strategy to select agent
    - Coordinate with ClaimLockManager to claim task
    - _Requirements: 7.2, 9.1, 16.1_
  
  - [x] 7.8 Implement notifyAgentsOfTask() for critical priority tasks
    - Send notifications to all eligible agents for critical tasks
    - _Requirements: 8.5_
  
  - [ ]* 7.9 Write unit tests for Task Assignment Engine
    - Test empty queue, strategy switching, notification logic
    - _Requirements: 2.5, 8.5_

- [ ] 8. Implement task metadata validation
  - [x] 8.1 Create TaskValidator class
    - Implement validateTaskMetadata() to check required fields
    - Implement validatePriority() to check valid priority values
    - Implement validateTaskType() to check registered types
    - Implement validateYAML() to handle parse errors
    - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_
  
  - [ ]* 8.2 Write property tests for task validation
    - **Property 9: Priority Value Validation**
    - **Property 47: Task Metadata Validation**
    - **Property 48: Task Type Validation**
    - **Property 49: Invalid YAML Handling**
    - **Validates: Requirements 8.3, 18.1, 18.2, 18.3, 18.4, 18.5**
  
  - [x] 8.3 Integrate validation into Task Assignment Engine
    - Move malformed tasks to Malformed folder
    - Log validation errors
    - _Requirements: 18.2, 18.5_
  
  - [ ]* 8.4 Write property test for default priority assignment
    - **Property 8: Default Priority Assignment**
    - **Validates: Requirements 8.2**

- [ ] 9. Checkpoint - Ensure Task Assignment Engine tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement Abandonment Detector component
  - [ ] 10.1 Create AbandonmentDetector class with monitoring
    - Implement startMonitoring() to periodically check for timeouts
    - Implement stopMonitoring() to clean up monitoring
    - Implement detectTimedOutTasks() to find tasks exceeding timeout
    - Implement detectUnresponsiveAgents() to find agents missing heartbeats
    - _Requirements: 10.2, 11.2_
  
  - [ ] 10.2 Implement task reclaim logic
    - Implement reclaimTask() to move task back to Needs_Action
    - Increment reclaimCount in task frontmatter
    - Move tasks with reclaimCount > 3 to Failed folder
    - _Requirements: 11.2, 11.4, 11.5_
  
  - [ ]* 10.3 Write property tests for timeout detection and reclaim
    - **Property 28: Task Timeout Detection and Reclaim**
    - **Property 30: Failed Task Handling**
    - **Validates: Requirements 11.2, 11.4, 11.5**
  
  - [ ] 10.4 Implement reclaimAllTasksFromAgent() for unresponsive agents
    - Move all tasks from agent's In_Progress folder to Needs_Action
    - _Requirements: 10.3_
  
  - [ ]* 10.5 Write property test for unresponsive agent task reclaim
    - **Property 26: Unresponsive Agent Task Reclaim**
    - **Validates: Requirements 10.3**
  
  - [ ] 10.6 Implement configurable timeouts
    - Implement setTaskTimeout() to configure per-type timeouts
    - Implement setHeartbeatTimeout() to configure heartbeat threshold
    - Support default timeout and per-type overrides
    - _Requirements: 11.3_
  
  - [ ]* 10.7 Write property test for configurable timeout per task type
    - **Property 29: Configurable Timeout Per Task Type**
    - **Validates: Requirements 11.3**
  
  - [ ]* 10.8 Write unit tests for Abandonment Detector edge cases
    - Test empty folders, tasks at timeout boundary, repeated reclaims
    - _Requirements: 10.2, 11.2, 11.5_

- [ ] 11. Implement Agent interface and base implementation
  - [ ] 11.1 Create Agent base class
  