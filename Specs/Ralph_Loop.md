---
type: system_spec
status: draft
category: architecture
risk_level: critical
created: 2026-02-15
requires_approval: true
version: 2.0.0
---

# Ralph Loop Architecture Specification

## Overview

The Ralph Loop is the core cognitive architecture of the Personal AI Employee, implementing a continuous cycle of Perception → Reasoning → Action with human oversight. Named after the observe-orient-decide-act (OODA) loop, it enables autonomous yet controlled operation.

## Purpose

Enable the Personal AI Employee to:
- Continuously perceive changes in the environment
- Reason about observations and make decisions
- Execute actions through MCP tools
- Maintain human control through approval gates
- Learn and improve from outcomes
- Operate safely and transparently

## Architecture

### The Ralph Loop Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                      RALPH LOOP                              │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐      ┌───────────┐ │
│  │  PERCEPTION  │ ───> │  REASONING   │ ───> │  ACTION   │ │
│  └──────────────┘      └──────────────┘      └───────────┘ │
│         │                     │                     │        │
│         │                     │                     │        │
│    [Observe]            [Decide]              [Execute]     │
│    [Context]            [Plan]                [Log]         │
│         │                     │                     │        │
│         │                     ↓                     │        │
│         │            ┌─────────────────┐            │        │
│         │            │ APPROVAL GATE   │            │        │
│         │            │ (Human Review)  │            │        │
│         │            └─────────────────┘            │        │
│         │                     │                     │        │
│         └─────────────────────┴─────────────────────┘        │
│                              │                               │
│                       [Feedback Loop]                        │
│                              │                               │
│                    ┌──────────────────┐                      │
│                    │  LEARNING ENGINE │                      │
│                    └──────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

## Three Layers

### 1. Perception Layer

**Purpose**: Observe and understand the environment

**Components**:
- File system watchers (vault changes)
- Email monitors (Gmail watcher)
- Dashboard scanners (metrics, KPIs)
- Event queue (prioritized observations)

**Inputs**:
- File system events (create, modify, delete, move)
- Email notifications (new messages)
- Scheduled triggers (time-based)
- User commands (manual invocations)

**Outputs**:
- Structured observations
- Context snapshots
- Event metadata
- Trigger signals

**Example Observations**:
```json
{
  "observation_id": "obs_20260215_103000",
  "type": "FILE_MODIFIED",
  "path": "/Specs/auth_feature.md",
  "timestamp": "2026-02-15T10:30:00Z",
  "context": {
    "file_type": "feature_spec",
    "status": "draft",
    "last_modified": "2026-02-14T15:20:00Z",
    "related_files": ["/Specs/user_model.md"]
  },
  "priority": "medium"
}
```

**Perception Skills**:
- `file_watcher` - Monitor vault for changes
- `email_watcher` - Monitor Gmail for new emails
- `dashboard_scanner` - Scan metrics and KPIs
- `context_builder` - Aggregate related information

### 2. Reasoning Layer

**Purpose**: Analyze observations and decide actions

**Components**:
- Context analyzer (build complete picture)
- Decision engine (evaluate options)
- Plan generator (create execution plans)
- Risk assessor (determine approval needs)

**Inputs**:
- Observations from Perception
- Historical data and patterns
- Business rules and policies
- User preferences

**Outputs**:
- Decisions with rationale
- Execution plans
- Approval requests (if high-risk)
- Confidence scores

**Example Decision**:
```json
{
  "decision_id": "dec_20260215_103001",
  "observation_id": "obs_20260215_103000",
  "decision": "generate_tasks",
  "rationale": "Spec updated with new requirements, ready for task generation",
  "confidence": 0.85,
  "risk_level": "low",
  "requires_approval": false,
  "plan_id": "plan_20260215_103002"
}
```

**Reasoning Skills**:
- `spec_analyzer` - Analyze specification completeness
- `task_planner` - Generate task lists
- `priority_ranker` - Prioritize tasks by business impact
- `risk_evaluator` - Assess action risks

### 3. Action Layer

**Purpose**: Execute decisions through MCP tools

**Components**:
- MCP client (invoke external tools)
- Vault writer (create/update files)
- Task executor (run planned tasks)
- Status tracker (update progress)

**Inputs**:
- Execution plans from Reasoning
- Approved requests from humans
- MCP tool configurations
- Execution context

**Outputs**:
- Modified vault files
- MCP tool results
- Execution logs
- Status updates

**Example Action**:
```json
{
  "action_id": "act_20260215_103003",
  "plan_id": "plan_20260215_103002",
  "action_type": "create_file",
  "mcp_tool": "vault.write",
  "params": {
    "path": "/Specs/auth_feature/tasks.md",
    "content": "..."
  },
  "result": {
    "success": true,
    "file_created": true,
    "timestamp": "2026-02-15T10:30:05Z"
  }
}
```

**Action Skills**:
- `vault_writer` - Create/update vault files
- `email_sender` - Send emails via Gmail
- `payment_processor` - Process payments
- `social_poster` - Post to social media

## Complete Loop Execution

### Example: New Spec Created

```
CYCLE START: 2026-02-15 10:30:00

┌─────────────────────────────────────────────────────────────┐
│ PERCEPTION (2 seconds)                                       │
├─────────────────────────────────────────────────────────────┤
│ 1. File watcher detects: /Specs/auth_feature.md modified   │
│ 2. Read file content and frontmatter                        │
│ 3. Identify related files via wikilinks                     │
│ 4. Build context with historical data                       │
│ 5. Create observation object                                │
│ 6. Queue for reasoning                                      │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ REASONING (3 seconds)                                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Analyze context: Spec has new requirements              │
│ 2. Evaluate options:                                        │
│    - Generate tasks (score: 0.85)                          │
│    - Request clarification (score: 0.65)                   │
│ 3. Select: Generate tasks                                   │
│ 4. Create execution plan:                                   │
│    - Read spec file                                         │
│    - Generate tasks.md                                      │
│    - Write to vault                                         │
│ 5. Assess risk: LOW (file write only)                      │
│ 6. Decision: Proceed without approval                       │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ ACTION (2 seconds)                                           │
├─────────────────────────────────────────────────────────────┤
│ 1. Execute plan step 1: Read spec                          │
│ 2. Execute plan step 2: Generate tasks                      │
│ 3. Execute plan step 3: Write tasks.md                      │
│ 4. Log success                                              │
│ 5. Update dashboard                                         │
│ 6. Archive to /Done/                                        │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ LEARNING (1 second)                                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Record outcome: Success                                  │
│ 2. Update decision patterns                                 │
│ 3. Improve confidence scores                                │
│ 4. Store for future reference                              │
└─────────────────────────────────────────────────────────────┘

CYCLE END: 2026-02-15 10:30:08 (8 seconds total)

NEXT CYCLE: Wait for next observation...
```

### Example: High-Risk Action (Payment)

```
CYCLE START: 2026-02-15 11:00:00

┌─────────────────────────────────────────────────────────────┐
│ PERCEPTION (2 seconds)                                       │
├─────────────────────────────────────────────────────────────┤
│ 1. Detect: New invoice in /Accounting/                     │
│ 2. Parse invoice: $1,250 payment due                       │
│ 3. Build context: Budget, vendor history                    │
│ 4. Create observation                                       │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ REASONING (3 seconds)                                        │
├─────────────────────────────────────────────────────────────┤
│ 1. Analyze: Payment > $50 threshold                        │
│ 2. Evaluate impact: Budget OK, vendor verified             │
│ 3. Create payment plan                                      │
│ 4. Assess risk: HIGH (financial transaction)               │
│ 5. Decision: REQUIRE APPROVAL                              │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ APPROVAL GATE (WAITING FOR HUMAN)                           │
├─────────────────────────────────────────────────────────────┤
│ 1. Create approval request                                  │
│ 2. Save to /Pending_Approval/payments/                     │
│ 3. Notify human                                             │
│ 4. PAUSE - Wait for decision                               │
│                                                             │
│ [45 minutes later...]                                       │
│                                                             │
│ 5. Human moves file to /Approved/                          │
│ 6. Detect approval                                          │
│ 7. Resume execution                                         │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ ACTION (5 seconds)                                           │
├─────────────────────────────────────────────────────────────┤
│ 1. Process payment via MCP                                  │
│ 2. Update accounting records                                │
│ 3. Send confirmation                                        │
│ 4. Log transaction                                          │
│ 5. Archive to /Approved/2026-02/payments/                  │
└─────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────┐
│ LEARNING (1 second)                                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Record: Approval granted in 45 min                      │
│ 2. Update: Similar payments likely approved                │
│ 3. Note: Human response time acceptable                    │
└─────────────────────────────────────────────────────────────┘

CYCLE END: 2026-02-15 11:45:11 (45 min 11 sec total)
```

## Approval Gate Integration

### When Approval Required

**Automatic Triggers**:
1. **Financial**: Payments > $50
2. **Communication**: Emails to new contacts
3. **Public**: Social media posts/replies
4. **Strategic**: Major business decisions
5. **Destructive**: File deletions
6. **External**: API calls to new services

**Risk-Based**:
- Risk score > 0.7 → Always require approval
- Risk score 0.4-0.7 → Require if novel situation
- Risk score < 0.4 → Auto-approve with logging

### Approval Workflow

```
High-Risk Decision
    ↓
Generate Approval Request
    ↓
Save to /Pending_Approval/[type]/
    ↓
Notify Human (desktop, email, dashboard)
    ↓
PAUSE Ralph Loop for this action
    ↓
Continue with other observations
    ↓
[Human Reviews]
    ↓
    ├─ Approve → Move to /Approved/
    │              ↓
    │         Detect approval
    │              ↓
    │         Resume action execution
    │              ↓
    │         Complete cycle
    │
    ├─ Reject → Move to /Rejected/
    │              ↓
    │         Detect rejection
    │              ↓
    │         Cancel action
    │              ↓
    │         Learn from rejection
    │
    └─ Modify → Edit in /Pending_Approval/
                   ↓
              Re-validate
                   ↓
              Wait for decision
```


## Loop Orchestration

### Main Loop Controller

```python
class RalphLoop:
    def __init__(self):
        self.perception = PerceptionLayer()
        self.reasoning = ReasoningLayer()
        self.action = ActionLayer()
        self.approval_gate = ApprovalGate()
        self.learning = LearningEngine()
        self.running = False
    
    async def start(self):
        """Start the Ralph Loop"""
        self.running = True
        
        # Start perception watchers
        await self.perception.start_watchers()
        
        # Start approval watcher
        await self.approval_gate.start_watcher()
        
        # Main loop
        while self.running:
            try:
                # Get next observation
                observation = await self.perception.get_next_observation()
                
                if observation:
                    # Process through loop
                    await self.process_observation(observation)
                else:
                    # No observations, wait briefly
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"Loop error: {e}")
                await self.handle_error(e)
    
    async def process_observation(self, observation):
        """Process single observation through Ralph Loop"""
        
        cycle_id = generate_cycle_id()
        start_time = time.time()
        
        logger.info(f"Cycle {cycle_id} started", {
            "observation_id": observation.id,
            "type": observation.type
        })
        
        try:
            # REASONING: Analyze and decide
            decision = await self.reasoning.analyze(observation)
            
            logger.info(f"Decision made", {
                "cycle_id": cycle_id,
                "decision": decision.action,
                "confidence": decision.confidence,
                "risk_level": decision.risk_level
            })
            
            # Check if approval required
            if decision.requires_approval:
                # Create approval request
                approval_id = await self.approval_gate.create_request(
                    decision, observation
                )
                
                logger.info(f"Approval required", {
                    "cycle_id": cycle_id,
                    "approval_id": approval_id
                })
                
                # Don't execute now, will resume when approved
                return
            
            # ACTION: Execute decision
            result = await self.action.execute(decision)
            
            logger.info(f"Action executed", {
                "cycle_id": cycle_id,
                "success": result.success
            })
            
            # LEARNING: Record outcome
            await self.learning.record_outcome(
                observation, decision, result
            )
            
            elapsed = time.time() - start_time
            logger.info(f"Cycle {cycle_id} completed in {elapsed:.2f}s")
            
        except Exception as e:
            logger.error(f"Cycle {cycle_id} failed: {e}")
            await self.handle_cycle_error(cycle_id, e)
    
    async def handle_approved_action(self, approval):
        """Resume execution after approval"""
        
        logger.info(f"Approval granted", {
            "approval_id": approval.id,
            "decision_id": approval.decision_id
        })
        
        # Retrieve original decision
        decision = await self.reasoning.get_decision(approval.decision_id)
        
        # Execute approved action
        result = await self.action.execute(decision)
        
        # Learn from approval
        await self.learning.record_approval(approval, result)
        
        logger.info(f"Approved action completed", {
            "approval_id": approval.id,
            "success": result.success
        })
    
    def stop(self):
        """Stop the Ralph Loop"""
        self.running = False
        logger.info("Ralph Loop stopped")
```

### Perception Layer Implementation

```python
class PerceptionLayer:
    def __init__(self):
        self.watchers = []
        self.observation_queue = asyncio.Queue()
    
    async def start_watchers(self):
        """Start all perception watchers"""
        
        # File system watcher
        file_watcher = FileSystemWatcher([
            "/Specs",
            "/Needs_Action",
            "/Approved",
            "/Dashboard",
            "/Accounting"
        ])
        file_watcher.on_event(self.handle_file_event)
        await file_watcher.start()
        self.watchers.append(file_watcher)
        
        # Email watcher
        email_watcher = EmailWatcher()
        email_watcher.on_email(self.handle_email_event)
        await email_watcher.start()
        self.watchers.append(email_watcher)
        
        # Scheduled tasks
        scheduler = TaskScheduler()
        scheduler.add_task("daily_review", "0 8 * * *", self.daily_review)
        scheduler.add_task("weekly_planning", "0 9 * * 1", self.weekly_planning)
        await scheduler.start()
        self.watchers.append(scheduler)
    
    async def handle_file_event(self, event):
        """Handle file system event"""
        
        # Build context
        context = await self.build_context(event)
        
        # Create observation
        observation = Observation(
            type=event.type,
            path=event.path,
            context=context,
            timestamp=datetime.now(),
            priority=self.calculate_priority(event, context)
        )
        
        # Queue for processing
        await self.observation_queue.put(observation)
    
    async def build_context(self, event):
        """Build rich context for observation"""
        
        context = {}
        
        # Read file if exists
        if event.type != "FILE_DELETED":
            content = await read_file(event.path)
            context["content"] = content
            context["frontmatter"] = parse_frontmatter(content)
        
        # Find related files
        context["related_files"] = await find_related_files(event.path)
        
        # Get historical data
        context["history"] = await get_file_history(event.path)
        
        return context
    
    async def get_next_observation(self):
        """Get next observation from queue"""
        try:
            return await asyncio.wait_for(
                self.observation_queue.get(),
                timeout=5.0
            )
        except asyncio.TimeoutError:
            return None
```

### Reasoning Layer Implementation

```python
class ReasoningLayer:
    def __init__(self):
        self.context_analyzer = ContextAnalyzer()
        self.decision_engine = DecisionEngine()
        self.plan_generator = PlanGenerator()
        self.risk_assessor = RiskAssessor()
    
    async def analyze(self, observation):
        """Analyze observation and make decision"""
        
        # Analyze context
        analysis = await self.context_analyzer.analyze(observation)
        
        # Make decision
        decision = await self.decision_engine.decide(analysis)
        
        # Generate execution plan
        plan = await self.plan_generator.generate(decision)
        
        # Assess risk
        risk = await self.risk_assessor.assess(plan)
        
        # Combine into decision object
        return Decision(
            action=decision.action,
            rationale=decision.rationale,
            confidence=decision.confidence,
            plan=plan,
            risk_level=risk.level,
            requires_approval=risk.requires_approval
        )
```

### Action Layer Implementation

```python
class ActionLayer:
    def __init__(self):
        self.mcp_client = MCPClient()
        self.vault_writer = VaultWriter()
        self.executor = ActionExecutor()
    
    async def execute(self, decision):
        """Execute decision plan"""
        
        results = []
        
        for step in decision.plan.steps:
            try:
                # Execute step
                if step.tool.startswith("vault."):
                    result = await self.vault_writer.execute(step)
                else:
                    result = await self.mcp_client.call(
                        step.tool,
                        step.params
                    )
                
                results.append(result)
                
                # Check if step failed
                if not result.success:
                    # Execute rollback
                    await self.rollback(decision.plan, results)
                    return ExecutionResult(
                        success=False,
                        error=result.error
                    )
                    
            except Exception as e:
                # Execute rollback
                await self.rollback(decision.plan, results)
                return ExecutionResult(
                    success=False,
                    error=str(e)
                )
        
        return ExecutionResult(
            success=True,
            results=results
        )
```

## Loop States

### State Machine

```
┌─────────────┐
│   IDLE      │ ← Start state
└─────────────┘
       ↓
┌─────────────┐
│  OBSERVING  │ ← Waiting for observations
└─────────────┘
       ↓
┌─────────────┐
│  REASONING  │ ← Analyzing and deciding
└─────────────┘
       ↓
       ├─────────────────┐
       │                 │
┌─────────────┐   ┌─────────────┐
│  EXECUTING  │   │  AWAITING   │ ← Waiting for approval
└─────────────┘   │  APPROVAL   │
       │           └─────────────┘
       │                 │
       ↓                 ↓
┌─────────────┐   ┌─────────────┐
│  LEARNING   │   │  APPROVED   │
└─────────────┘   └─────────────┘
       │                 │
       │                 ↓
       │           ┌─────────────┐
       │           │  EXECUTING  │
       │           └─────────────┘
       │                 │
       └─────────────────┘
              ↓
       ┌─────────────┐
       │  OBSERVING  │ ← Loop continues
       └─────────────┘
```

### State Transitions

```python
class LoopState(Enum):
    IDLE = "idle"
    OBSERVING = "observing"
    REASONING = "reasoning"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    LEARNING = "learning"
    ERROR = "error"

class RalphLoopStateMachine:
    def __init__(self):
        self.state = LoopState.IDLE
        self.state_history = []
    
    def transition(self, new_state, context=None):
        """Transition to new state"""
        
        old_state = self.state
        self.state = new_state
        
        self.state_history.append({
            "from": old_state,
            "to": new_state,
            "timestamp": datetime.now(),
            "context": context
        })
        
        logger.info(f"State transition: {old_state} → {new_state}")
        
        # Emit state change event
        self.emit_state_change(old_state, new_state)
```

## Performance Metrics

### Target Performance

- **Perception**: < 2 seconds per observation
- **Reasoning**: < 3 seconds per decision
- **Action**: < 5 seconds per execution
- **Complete Cycle**: < 10 seconds (without approval)
- **Approval Wait**: Variable (human-dependent)

### Throughput

- **Observations**: 100+ per hour
- **Decisions**: 80+ per hour
- **Actions**: 60+ per hour
- **Approvals**: 10-20 per day

### Latency

- **Observation to Decision**: < 5 seconds
- **Decision to Action**: < 1 second
- **Action to Completion**: < 5 seconds
- **End-to-End**: < 11 seconds

## Monitoring and Observability

### Loop Metrics

```markdown
# Ralph Loop Metrics - 2026-02-15

## Cycle Statistics
- **Total Cycles**: 127
- **Successful**: 121 (95%)
- **Failed**: 6 (5%)
- **Average Duration**: 8.3 seconds
- **Fastest Cycle**: 3.2 seconds
- **Slowest Cycle**: 45 minutes (approval wait)

## Layer Performance
- **Perception**: 1.8s avg
- **Reasoning**: 2.4s avg
- **Action**: 3.1s avg
- **Learning**: 0.9s avg

## Approval Statistics
- **Approval Requests**: 29
- **Approved**: 25 (86%)
- **Rejected**: 4 (14%)
- **Average Wait Time**: 2.3 hours
- **Fastest Approval**: 5 minutes
- **Slowest Approval**: 8 hours

## Error Analysis
- **Perception Errors**: 1 (network timeout)
- **Reasoning Errors**: 2 (low confidence)
- **Action Errors**: 3 (MCP failures)
- **Recovery Success**: 100%
```

### Health Dashboard

```markdown
# Ralph Loop Health - Real-Time

## System Status
🟢 **RUNNING** - All systems operational

## Current State
**State**: OBSERVING
**Last Cycle**: 2 minutes ago
**Next Cycle**: Waiting for observation

## Queue Status
- **Observation Queue**: 0 pending
- **Approval Queue**: 3 pending
- **Action Queue**: 0 pending

## Recent Activity (Last Hour)
- Cycles: 12
- Observations: 15
- Decisions: 12
- Actions: 9
- Approvals: 2

## Alerts
⚠️ **Warning**: 3 approvals pending > 4 hours
✅ **OK**: All systems responding
✅ **OK**: No errors in last hour
```

## Error Handling

### Error Categories

1. **Perception Errors**
   - File read failures
   - Network timeouts
   - Parse errors

2. **Reasoning Errors**
   - Low confidence decisions
   - Conflicting data
   - Missing context

3. **Action Errors**
   - MCP tool failures
   - File write errors
   - API errors

4. **Approval Errors**
   - Timeout (no response)
   - Invalid approval format
   - Approval file corruption

### Recovery Strategies

```python
async def handle_error(self, error, context):
    """Handle loop error"""
    
    if isinstance(error, PerceptionError):
        # Retry observation
        await asyncio.sleep(5)
        return "retry"
    
    elif isinstance(error, ReasoningError):
        # Escalate to human
        await self.create_escalation(error, context)
        return "escalate"
    
    elif isinstance(error, ActionError):
        # Rollback and retry
        await self.rollback_action(context)
        await asyncio.sleep(10)
        return "retry"
    
    elif isinstance(error, ApprovalError):
        # Move to Needs_Action
        await self.move_to_needs_action(context)
        return "manual"
    
    else:
        # Unknown error, log and continue
        logger.error(f"Unknown error: {error}")
        return "continue"
```

## Correctness Properties

### P-1: Loop Continuity
**Property**: Loop never deadlocks or hangs  
**Validation**: Monitor cycle completion rate  
**Test**: Stress test with high observation rate

### P-2: Observation Completeness
**Property**: All observations are processed  
**Validation**: Compare observations detected vs processed  
**Test**: Generate known observations, verify all processed

### P-3: Decision Determinism
**Property**: Same observation produces same decision  
**Validation**: Process same observation twice, compare decisions  
**Test**: Property-based test with generated observations

### P-4: Action Safety
**Property**: High-risk actions always require approval  
**Validation**: Check all high-risk actions have approval records  
**Test**: Generate high-risk actions, verify approval required

### P-5: State Consistency
**Property**: Loop state is always valid  
**Validation**: Check state transitions follow state machine  
**Test**: Monitor state transitions, verify validity

### P-6: Error Recovery
**Property**: Errors don't crash the loop  
**Validation**: Inject errors, verify loop continues  
**Test**: Fault injection testing

### P-7: Learning Effectiveness
**Property**: Decision quality improves over time  
**Validation**: Track success rate over time  
**Test**: Measure early vs late decision success rates

### P-8: Approval Enforcement
**Property**: No high-risk action executes without approval  
**Validation**: Audit all actions, verify approval for high-risk  
**Test**: Generate high-risk actions, verify none execute without approval


## Integration with Existing Components

### Gmail Watcher Integration

```python
# Perception Layer
class EmailWatcher:
    async def poll_gmail(self):
        """Poll Gmail for new emails"""
        
        # Use Gmail Watcher skill
        emails = await gmail_watcher.fetch_unread_emails()
        
        for email in emails:
            # Create observation
            observation = Observation(
                type="EMAIL_RECEIVED",
                data=email,
                context={
                    "sender": email.sender,
                    "subject": email.subject,
                    "priority": email.priority
                }
            )
            
            # Queue for reasoning
            await self.observation_queue.put(observation)

# Reasoning Layer
class EmailProcessor:
    async def process_email(self, observation):
        """Process email observation"""
        
        email = observation.data
        
        # Determine action
        if email.priority == "high":
            decision = Decision(
                action="create_task",
                params={"email": email}
            )
        else:
            decision = Decision(
                action="archive",
                params={"email": email}
            )
        
        return decision

# Action Layer
class EmailActionExecutor:
    async def create_task(self, email):
        """Create task from email"""
        
        # Generate markdown
        markdown = generate_email_task_markdown(email)
        
        # Write to vault
        await vault.write(
            f"/Needs_Action/email_{email.id}.md",
            markdown
        )
```

### Business Reasoning Integration

```python
# Perception Layer
class BusinessDataScanner:
    async def scan_business_data(self):
        """Scan business folders"""
        
        # Scan Needs_Action
        needs_action = await scan_folder("/Needs_Action")
        
        # Scan Accounting
        accounting = await scan_folder("/Accounting")
        
        # Scan Dashboard
        dashboard = await scan_folder("/Dashboard")
        
        # Create observation
        observation = Observation(
            type="BUSINESS_DATA_UPDATE",
            data={
                "needs_action": needs_action,
                "accounting": accounting,
                "dashboard": dashboard
            }
        )
        
        return observation

# Reasoning Layer
class BusinessReasoningEngine:
    async def analyze_business_data(self, observation):
        """Apply CEO-level reasoning"""
        
        data = observation.data
        
        # Aggregate data
        aggregated = aggregate_business_data(data)
        
        # Detect patterns
        patterns = detect_patterns(aggregated)
        
        # Prioritize tasks
        prioritized = prioritize_tasks(
            data["needs_action"],
            business_impact=True
        )
        
        # Generate plan
        plan = generate_business_plan(prioritized, patterns)
        
        # Assess risk
        if plan.budget > 50:
            requires_approval = True
        else:
            requires_approval = False
        
        return Decision(
            action="execute_business_plan",
            plan=plan,
            requires_approval=requires_approval
        )
```

### MCP Email Action Integration

```python
# Action Layer
class EmailActionExecutor:
    async def send_email(self, params):
        """Send email via MCP"""
        
        # Call MCP email.send tool
        result = await mcp_client.call(
            "gmail-action-server",
            "email.send",
            {
                "to": params["to"],
                "subject": params["subject"],
                "body": params["body"],
                "dry_run": params.get("dry_run", False)
            }
        )
        
        # Check if approval required
        if result.get("approval_required"):
            # Approval request already created by MCP server
            return ExecutionResult(
                success=False,
                approval_required=True,
                approval_id=result["approval_request_id"]
            )
        
        # Email sent successfully
        return ExecutionResult(
            success=True,
            message_id=result["message_id"]
        )
```

## Deployment

### System Requirements

- **OS**: Linux, macOS, or Windows
- **Runtime**: Node.js 18+ or Python 3.10+
- **Memory**: 512 MB minimum, 2 GB recommended
- **Storage**: 10 GB for logs and vault
- **Network**: Internet for MCP servers (Gmail, etc.)

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/ralph-loop.git
cd ralph-loop

# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure
cp config/example.yaml config/config.yaml
# Edit config/config.yaml with your settings

# Set up vault structure
./scripts/setup-vault.sh

# Initialize
./scripts/init-ralph-loop.sh
```

### Configuration

```yaml
# config/config.yaml

ralph_loop:
  # Loop settings
  observation_queue_size: 100
  max_concurrent_cycles: 5
  cycle_timeout_seconds: 300
  
  # Perception settings
  perception:
    file_watchers:
      - path: "/Specs"
        events: ["create", "modify", "delete", "move"]
      - path: "/Needs_Action"
        events: ["create", "modify", "move"]
      - path: "/Approved"
        events: ["move"]
    
    email_watcher:
      enabled: true
      poll_interval_seconds: 300
    
    scheduled_tasks:
      - name: "daily_review"
        cron: "0 8 * * *"
      - name: "weekly_planning"
        cron: "0 9 * * 1"
  
  # Reasoning settings
  reasoning:
    confidence_threshold: 0.7
    risk_threshold: 0.3
    max_decision_time_seconds: 10
  
  # Action settings
  action:
    max_retries: 3
    retry_delay_seconds: 5
    rollback_on_failure: true
  
  # Approval settings
  approval:
    enabled: true
    timeout_hours: 72
    reminder_hours: 24
  
  # Learning settings
  learning:
    enabled: true
    min_samples: 10
    update_frequency: "daily"
  
  # Logging
  logging:
    level: "INFO"
    format: "json"
    audit_trail: true
    retention_days: 365
```

### Running

```bash
# Start Ralph Loop
npm start
# or
python -m ralph_loop

# Start with specific config
npm start -- --config config/production.yaml

# Start in dry-run mode
DRY_RUN=true npm start

# Run as daemon
npm run daemon

# Stop daemon
npm run stop
```

### Monitoring

```bash
# Check status
npm run status

# View logs
npm run logs

# View metrics
npm run metrics

# Health check
npm run health
```

## Testing

### Unit Tests

```bash
# Run all tests
npm test

# Run specific layer
npm test perception
npm test reasoning
npm test action

# Run with coverage
npm test -- --coverage
```

### Integration Tests

```bash
# End-to-end tests
npm run test:e2e

# Approval workflow tests
npm run test:approval

# MCP integration tests
npm run test:mcp
```

### Property-Based Tests

```bash
# Run property tests
npm run test:properties

# Specific properties
npm run test:properties -- --grep "Loop Continuity"
```

### Load Tests

```bash
# Stress test
npm run test:load

# High observation rate
npm run test:load -- --observations 1000

# Concurrent cycles
npm run test:load -- --concurrent 10
```

## Security

### Threat Model

**Threats**:
- Malicious file modifications
- Unauthorized MCP access
- Approval bypass attempts
- Data exfiltration
- Denial of service

**Mitigations**:
- File integrity monitoring
- MCP authentication
- Approval enforcement
- Audit logging
- Rate limiting

### Security Measures

1. **Authentication**
   - OAuth for external services
   - API keys for MCP servers
   - Local file permissions

2. **Authorization**
   - Approval gates for high-risk
   - Role-based access (future)
   - Audit trail

3. **Data Protection**
   - Local-first architecture
   - Encrypted logs (optional)
   - No external transmission

4. **Monitoring**
   - Anomaly detection
   - Failed approval attempts
   - Unusual activity patterns

## Future Enhancements

### Planned Features

1. **Parallel Execution**
   - Process multiple observations concurrently
   - Parallel action execution
   - Dependency management

2. **Advanced Learning**
   - Reinforcement learning
   - Transfer learning
   - Meta-learning

3. **Multi-Agent Collaboration**
   - Specialized sub-agents
   - Agent communication
   - Coordinated execution

4. **Predictive Reasoning**
   - Anticipate future observations
   - Proactive actions
   - Scenario planning

5. **Natural Language Interface**
   - Chat with Ralph Loop
   - Natural language commands
   - Conversational feedback

### Research Areas

- Optimal cycle timing
- Approval threshold tuning
- Learning rate optimization
- Error recovery strategies
- State machine optimization

## Success Metrics

### Effectiveness

- **Decision Quality**: 95%+ success rate
- **Approval Accuracy**: 90%+ approval rate
- **Error Recovery**: 100% recovery rate
- **Learning Progress**: Improving over time

### Efficiency

- **Cycle Time**: < 10 seconds average
- **Throughput**: 100+ cycles per hour
- **Resource Usage**: < 500 MB memory
- **Approval Wait**: < 4 hours average

### Reliability

- **Uptime**: 99.9%+
- **Error Rate**: < 1%
- **Data Loss**: 0%
- **Deadlocks**: 0

## Approval Required

This specification requires approval for:
- Ralph Loop architecture
- Layer implementations
- Approval gate integration
- State machine design
- Error handling strategies

**Risk Assessment**: CRITICAL
- Core system architecture
- Affects all operations
- Requires careful implementation
- Must be thoroughly tested

**Mitigation**:
- Comprehensive testing
- Gradual rollout
- Monitoring and alerting
- Emergency stop capability
- Human oversight maintained

---

**Status**: DRAFT  
**Version**: 2.0.0  
**Next Steps**:
1. Review architecture with team
2. Approve Ralph Loop design
3. Implement core loop
4. Test each layer independently
5. Integration testing
6. Deploy with monitoring
7. Iterate based on performance

