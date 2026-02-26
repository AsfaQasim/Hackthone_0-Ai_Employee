---
type: system_spec
status: draft
category: execution
risk_level: high
created: 2026-02-15
requires_approval: true
version: 1.0.0
---

# Autonomous Loop Specification

## Overview

An autonomous execution loop that continuously works on tasks until completion, with configurable stop conditions, failure handling, and state persistence. Enables the AI Employee to work independently on complex tasks with minimal human intervention.

## Purpose

Enable the Personal AI Employee to:
- Execute tasks autonomously until completion
- Loop continuously with configurable stop conditions
- Handle failures gracefully with retry logic
- Persist state across interruptions
- Allow human intervention via stop hooks
- Reinject prompts for continued execution
- Track progress and iterations

## Loop Termination Conditions

### 1. Task Moved to Done
**Trigger**: Task file moved from any folder to `/Done/`  
**Behavior**: Loop completes successfully  
**Action**: Archive state, log completion

### 2. Max Iterations Reached
**Trigger**: Iteration count exceeds configured maximum  
**Behavior**: Loop stops with warning  
**Action**: Save state, create intervention request

### 3. Failure Threshold Exceeded
**Trigger**: Consecutive failures exceed threshold  
**Behavior**: Loop stops with error  
**Action**: Save state, escalate to human

### 4. Stop Hook Triggered
**Trigger**: Human creates stop file or hook  
**Behavior**: Loop stops gracefully  
**Action**: Save state, wait for resume

### 5. Manual Intervention
**Trigger**: Human moves task to `/Needs_Action/`  
**Behavior**: Loop pauses for human input  
**Action**: Save state, wait for guidance

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  AUTONOMOUS LOOP                             │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  INITIALIZATION                                         │ │
│  │  - Load state file                                      │ │
│  │  - Read task configuration                              │ │
│  │  - Set up stop hooks                                    │ │
│  │  - Initialize counters                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  LOOP ITERATION (Repeat)                               │ │
│  │                                                         │ │
│  │  1. Check stop conditions                              │ │
│  │  2. Execute task step                                   │ │
│  │  3. Update state file                                   │ │
│  │  4. Check completion                                    │ │
│  │  5. Handle failures                                     │ │
│  │  6. Increment iteration                                 │ │
│  │  7. Reinject prompt (if needed)                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ↓                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  TERMINATION                                            │ │
│  │  - Save final state                                     │ │
│  │  - Log completion/failure                               │ │
│  │  - Archive or escalate                                  │ │
│  │  - Clean up resources                                   │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## State File

### State File Format

**Location**: `.state/autonomous_loop_[task_id].json`

```json
{
  "task_id": "task_20260215_103000",
  "task_path": "/Specs/auth_feature/tasks.md",
  "status": "running",
  "started_at": "2026-02-15T10:30:00Z",
  "updated_at": "2026-02-15T10:35:00Z",
  "iteration": 5,
  "max_iterations": 100,
  "consecutive_failures": 0,
  "failure_threshold": 3,
  "total_failures": 1,
  "total_successes": 4,
  "current_step": {
    "step_id": "1.3",
    "description": "Implement authentication logic",
    "status": "in_progress",
    "started_at": "2026-02-15T10:34:00Z"
  },
  "completed_steps": [
    {
      "step_id": "1.1",
      "description": "Set up project structure",
      "completed_at": "2026-02-15T10:31:00Z",
      "duration_seconds": 45
    },
    {
      "step_id": "1.2",
      "description": "Install dependencies",
      "completed_at": "2026-02-15T10:33:00Z",
      "duration_seconds": 120
    }
  ],
  "failed_steps": [
    {
      "step_id": "1.3",
      "description": "Implement authentication logic",
      "failed_at": "2026-02-15T10:34:30Z",
      "error": "Type error in auth.ts",
      "retry_count": 1
    }
  ],
  "context": {
    "last_prompt": "Continue implementing authentication...",
    "last_response": "I encountered a type error...",
    "environment": {
      "node_version": "18.0.0",
      "typescript_version": "5.0.0"
    }
  },
  "stop_conditions": {
    "task_in_done": false,
    "max_iterations_reached": false,
    "failure_threshold_exceeded": false,
    "stop_hook_triggered": false,
    "manual_intervention": false
  },
  "metrics": {
    "total_duration_seconds": 300,
    "average_step_duration": 60,
    "success_rate": 0.80
  }
}
```

### State Persistence

```python
class StateManager:
    def __init__(self, task_id):
        self.task_id = task_id
        self.state_file = f".state/autonomous_loop_{task_id}.json"
        self.state = self.load_state()
    
    def load_state(self):
        """Load state from file or create new"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        else:
            return self.create_initial_state()
    
    def save_state(self):
        """Save current state to file"""
        self.state['updated_at'] = datetime.now().isoformat()
        
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def update_iteration(self):
        """Increment iteration counter"""
        self.state['iteration'] += 1
        self.save_state()
    
    def record_success(self, step):
        """Record successful step"""
        self.state['total_successes'] += 1
        self.state['consecutive_failures'] = 0
        self.state['completed_steps'].append({
            'step_id': step.id,
            'description': step.description,
            'completed_at': datetime.now().isoformat(),
            'duration_seconds': step.duration
        })
        self.save_state()
    
    def record_failure(self, step, error):
        """Record failed step"""
        self.state['total_failures'] += 1
        self.state['consecutive_failures'] += 1
        self.state['failed_steps'].append({
            'step_id': step.id,
            'description': step.description,
            'failed_at': datetime.now().isoformat(),
            'error': str(error),
            'retry_count': step.retry_count
        })
        self.save_state()
```

## Stop Hook

### Stop Hook File

**Location**: `.hooks/stop_autonomous_loop.md`

```markdown
---
type: stop_hook
task_id: task_20260215_103000
created: 2026-02-15T10:40:00Z
reason: manual
---

# Stop Autonomous Loop

## Reason for Stopping

[Human provides reason here]

## Current Status

**Iteration**: 5/100
**Current Step**: 1.3 - Implement authentication logic
**Success Rate**: 80%

## What to Do

- [ ] Review progress so far
- [ ] Provide guidance for next steps
- [ ] Resume loop
- [ ] Cancel task

## Resume Instructions

To resume the loop:
1. Delete this file
2. Or move task back to active folder
3. Loop will continue from saved state

---

**Loop is PAUSED until this file is deleted or task is moved.**
```

### Stop Hook Detection

```python
class StopHookDetector:
    def __init__(self, task_id):
        self.task_id = task_id
        self.hook_file = f".hooks/stop_autonomous_loop_{task_id}.md"
    
    def check_stop_hook(self):
        """Check if stop hook exists"""
        return os.path.exists(self.hook_file)
    
    def create_stop_hook(self, reason="manual"):
        """Create stop hook file"""
        content = f"""---
type: stop_hook
task_id: {self.task_id}
created: {datetime.now().isoformat()}
reason: {reason}
---

# Stop Autonomous Loop

Loop has been stopped. Delete this file to resume.
"""
        os.makedirs(os.path.dirname(self.hook_file), exist_ok=True)
        with open(self.hook_file, 'w') as f:
            f.write(content)
    
    def remove_stop_hook(self):
        """Remove stop hook to resume"""
        if os.path.exists(self.hook_file):
            os.remove(self.hook_file)
```

## Prompt Reinjection

### Reinjection Strategy

```python
class PromptReinjector:
    def __init__(self, state_manager):
        self.state = state_manager
    
    def should_reinject(self, iteration):
        """Determine if prompt reinjection needed"""
        
        # Reinject every 10 iterations
        if iteration % 10 == 0:
            return True
        
        # Reinject after failure
        if self.state.state['consecutive_failures'] > 0:
            return True
        
        # Reinject if context is stale
        last_update = datetime.fromisoformat(
            self.state.state['updated_at']
        )
        if (datetime.now() - last_update).seconds > 300:
            return True
        
        return False
    
    def generate_reinjection_prompt(self):
        """Generate prompt to reinject context"""
        
        state = self.state.state
        
        prompt = f"""
# Task Continuation Context

## Current Task
**Task**: {state['task_path']}
**Iteration**: {state['iteration']}/{state['max_iterations']}
**Status**: {state['status']}

## Progress
- **Completed Steps**: {len(state['completed_steps'])}
- **Failed Steps**: {len(state['failed_steps'])}
- **Success Rate**: {state['metrics']['success_rate']:.0%}

## Current Step
**Step**: {state['current_step']['step_id']}
**Description**: {state['current_step']['description']}
**Status**: {state['current_step']['status']}

## Recent Context
{state['context']['last_prompt']}

## Last Response
{state['context']['last_response']}

## Next Action
Continue working on the current step. If you encountered an error, 
try a different approach. Remember to update the state file after 
each step.

---

Please continue from where you left off.
"""
        return prompt
```


## Loop Implementation

```python
class AutonomousLoop:
    def __init__(self, task_id, config):
        self.task_id = task_id
        self.config = config
        self.state = StateManager(task_id)
        self.stop_hook = StopHookDetector(task_id)
        self.reinjector = PromptReinjector(self.state)
        self.running = False
    
    async def start(self):
        """Start the autonomous loop"""
        
        logger.info(f"Starting autonomous loop for task {self.task_id}")
        
        self.running = True
        self.state.state['status'] = 'running'
        self.state.save_state()
        
        try:
            while self.running:
                # Check stop conditions
                if self.should_stop():
                    break
                
                # Execute iteration
                await self.execute_iteration()
                
                # Update iteration counter
                self.state.update_iteration()
                
                # Brief pause between iterations
                await asyncio.sleep(1)
            
            # Loop completed
            await self.handle_completion()
            
        except Exception as e:
            logger.error(f"Loop error: {e}")
            await self.handle_error(e)
        
        finally:
            self.state.state['status'] = 'stopped'
            self.state.save_state()
    
    def should_stop(self):
        """Check if loop should stop"""
        
        # Check task moved to Done
        if self.check_task_in_done():
            logger.info("Task moved to Done - stopping loop")
            self.state.state['stop_conditions']['task_in_done'] = True
            return True
        
        # Check max iterations
        if self.state.state['iteration'] >= self.state.state['max_iterations']:
            logger.warning("Max iterations reached - stopping loop")
            self.state.state['stop_conditions']['max_iterations_reached'] = True
            return True
        
        # Check failure threshold
        if self.state.state['consecutive_failures'] >= self.state.state['failure_threshold']:
            logger.error("Failure threshold exceeded - stopping loop")
            self.state.state['stop_conditions']['failure_threshold_exceeded'] = True
            return True
        
        # Check stop hook
        if self.stop_hook.check_stop_hook():
            logger.info("Stop hook detected - stopping loop")
            self.state.state['stop_conditions']['stop_hook_triggered'] = True
            return True
        
        # Check manual intervention
        if self.check_manual_intervention():
            logger.info("Manual intervention requested - stopping loop")
            self.state.state['stop_conditions']['manual_intervention'] = True
            return True
        
        return False
    
    async def execute_iteration(self):
        """Execute one loop iteration"""
        
        iteration = self.state.state['iteration']
        logger.info(f"Executing iteration {iteration}")
        
        # Reinject prompt if needed
        if self.reinjector.should_reinject(iteration):
            prompt = self.reinjector.generate_reinjection_prompt()
            logger.info("Reinjecting context prompt")
            # Send prompt to AI agent
            await self.send_prompt(prompt)
        
        # Get current step
        current_step = self.get_current_step()
        
        if not current_step:
            logger.info("No more steps - task complete")
            await self.move_task_to_done()
            return
        
        # Execute step
        try:
            result = await self.execute_step(current_step)
            
            if result.success:
                self.state.record_success(current_step)
                logger.info(f"Step {current_step.id} completed successfully")
            else:
                self.state.record_failure(current_step, result.error)
                logger.warning(f"Step {current_step.id} failed: {result.error}")
                
        except Exception as e:
            self.state.record_failure(current_step, e)
            logger.error(f"Step {current_step.id} error: {e}")
    
    def check_task_in_done(self):
        """Check if task file is in Done folder"""
        task_path = self.state.state['task_path']
        return '/Done/' in task_path or not os.path.exists(task_path)
    
    def check_manual_intervention(self):
        """Check if task moved to Needs_Action"""
        task_path = self.state.state['task_path']
        return '/Needs_Action/' in task_path
    
    async def move_task_to_done(self):
        """Move task to Done folder"""
        task_path = self.state.state['task_path']
        done_path = task_path.replace('/Specs/', '/Done/')
        
        os.makedirs(os.path.dirname(done_path), exist_ok=True)
        shutil.move(task_path, done_path)
        
        self.state.state['task_path'] = done_path
        self.state.save_state()
        
        logger.info(f"Task moved to Done: {done_path}")
    
    async def handle_completion(self):
        """Handle loop completion"""
        
        stop_conditions = self.state.state['stop_conditions']
        
        if stop_conditions['task_in_done']:
            # Success - task completed
            logger.info("Loop completed successfully")
            await self.create_completion_report()
        
        elif stop_conditions['max_iterations_reached']:
            # Warning - max iterations
            logger.warning("Loop stopped: max iterations reached")
            await self.create_intervention_request(
                "Max iterations reached. Task may need human review."
            )
        
        elif stop_conditions['failure_threshold_exceeded']:
            # Error - too many failures
            logger.error("Loop stopped: failure threshold exceeded")
            await self.escalate_to_human(
                "Too many consecutive failures. Human intervention required."
            )
        
        elif stop_conditions['stop_hook_triggered']:
            # Manual stop
            logger.info("Loop stopped: stop hook triggered")
            # State already saved, just log
        
        elif stop_conditions['manual_intervention']:
            # Human requested intervention
            logger.info("Loop stopped: manual intervention requested")
            # Wait for human guidance
    
    async def create_completion_report(self):
        """Create completion report"""
        
        state = self.state.state
        
        report = f"""---
type: completion_report
task_id: {self.task_id}
completed_at: {datetime.now().isoformat()}
---

# Task Completion Report

## Summary
**Task**: {state['task_path']}
**Status**: ✅ COMPLETED
**Duration**: {state['metrics']['total_duration_seconds']} seconds
**Iterations**: {state['iteration']}

## Statistics
- **Total Steps**: {len(state['completed_steps']) + len(state['failed_steps'])}
- **Completed**: {len(state['completed_steps'])}
- **Failed**: {len(state['failed_steps'])}
- **Success Rate**: {state['metrics']['success_rate']:.0%}

## Completed Steps
{self.format_steps(state['completed_steps'])}

## Failed Steps (Recovered)
{self.format_steps(state['failed_steps'])}

## Metrics
- **Average Step Duration**: {state['metrics']['average_step_duration']}s
- **Total Successes**: {state['total_successes']}
- **Total Failures**: {state['total_failures']}

---

**Task successfully completed and moved to /Done/**
"""
        
        report_path = f"/Logs/completion_reports/{self.task_id}.md"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
    
    async def create_intervention_request(self, reason):
        """Create intervention request"""
        
        request = f"""---
type: intervention_request
task_id: {self.task_id}
created: {datetime.now().isoformat()}
reason: max_iterations
---

# Intervention Request

## Reason
{reason}

## Current Status
**Iteration**: {self.state.state['iteration']}/{self.state.state['max_iterations']}
**Success Rate**: {self.state.state['metrics']['success_rate']:.0%}
**Current Step**: {self.state.state['current_step']['description']}

## Options
- [ ] Increase max iterations and resume
- [ ] Review progress and provide guidance
- [ ] Mark task as complete
- [ ] Cancel task

## State File
State saved at: `.state/autonomous_loop_{self.task_id}.json`

---

**Please review and decide how to proceed.**
"""
        
        request_path = f"/Needs_Action/intervention_{self.task_id}.md"
        with open(request_path, 'w') as f:
            f.write(request)
    
    async def escalate_to_human(self, reason):
        """Escalate to human"""
        
        escalation = f"""---
type: escalation
task_id: {self.task_id}
created: {datetime.now().isoformat()}
priority: high
---

# 🚨 Task Escalation

## Reason
{reason}

## Failure Details
**Consecutive Failures**: {self.state.state['consecutive_failures']}
**Failure Threshold**: {self.state.state['failure_threshold']}

## Recent Failures
{self.format_recent_failures()}

## Current Step
**Step**: {self.state.state['current_step']['step_id']}
**Description**: {self.state.state['current_step']['description']}

## Recommended Actions
1. Review error logs
2. Identify root cause
3. Provide guidance or fix issue
4. Resume loop or cancel task

## State File
`.state/autonomous_loop_{self.task_id}.json`

---

**Human intervention required to proceed.**
"""
        
        escalation_path = f"/Needs_Action/escalation_{self.task_id}.md"
        with open(escalation_path, 'w') as f:
            f.write(escalation)
```

## Configuration

```yaml
# config/autonomous_loop.yaml

autonomous_loop:
  # Loop limits
  max_iterations: 100
  failure_threshold: 3
  timeout_seconds: 3600
  
  # Reinjection settings
  reinject_every_n_iterations: 10
  reinject_after_failure: true
  reinject_if_stale_seconds: 300
  
  # State management
  state_directory: ".state"
  save_state_every_iteration: true
  backup_state_every_n_iterations: 10
  
  # Stop conditions
  check_done_folder: true
  check_needs_action_folder: true
  check_stop_hook: true
  
  # Monitoring
  log_every_iteration: true
  create_progress_reports: true
  progress_report_every_n_iterations: 25
  
  # Error handling
  retry_failed_steps: true
  max_step_retries: 3
  exponential_backoff: true
  
  # Completion
  auto_move_to_done: true
  create_completion_report: true
  archive_state_file: true
```

## Usage

### Starting a Loop

```bash
# Start autonomous loop for a task
kiro loop start --task /Specs/auth_feature/tasks.md

# Start with custom config
kiro loop start --task /Specs/auth_feature/tasks.md --config custom.yaml

# Start with max iterations
kiro loop start --task /Specs/auth_feature/tasks.md --max-iterations 50

# Start with failure threshold
kiro loop start --task /Specs/auth_feature/tasks.md --failure-threshold 5
```

### Monitoring a Loop

```bash
# Check loop status
kiro loop status --task-id task_20260215_103000

# View state file
kiro loop state --task-id task_20260215_103000

# View progress
kiro loop progress --task-id task_20260215_103000

# Tail logs
kiro loop logs --task-id task_20260215_103000 --follow
```

### Stopping a Loop

```bash
# Create stop hook
kiro loop stop --task-id task_20260215_103000

# Force stop
kiro loop stop --task-id task_20260215_103000 --force

# Stop and save state
kiro loop stop --task-id task_20260215_103000 --save-state
```

### Resuming a Loop

```bash
# Resume from saved state
kiro loop resume --task-id task_20260215_103000

# Resume with new max iterations
kiro loop resume --task-id task_20260215_103000 --max-iterations 150

# Resume and reset failure count
kiro loop resume --task-id task_20260215_103000 --reset-failures
```

## Monitoring

### Progress Dashboard

```markdown
# Autonomous Loop Progress

## Active Loops (2)

### Task: auth_feature
**Status**: 🟢 RUNNING
**Iteration**: 15/100 (15%)
**Success Rate**: 93%
**Current Step**: 2.3 - Write unit tests
**Duration**: 8 minutes
**ETA**: 45 minutes

### Task: payment_integration
**Status**: 🟡 PAUSED (Stop Hook)
**Iteration**: 42/100 (42%)
**Success Rate**: 88%
**Last Step**: 3.1 - Integrate payment API
**Duration**: 22 minutes

## Completed Today (3)

### Task: email_templates
**Status**: ✅ COMPLETED
**Iterations**: 28/100
**Success Rate**: 96%
**Duration**: 15 minutes

## Failed (1)

### Task: database_migration
**Status**: ❌ FAILED (Threshold Exceeded)
**Iterations**: 67/100
**Consecutive Failures**: 3
**Reason**: Database connection errors
**Action**: Escalated to human
```

## Correctness Properties

### P-1: State Persistence
**Property**: State is saved after every iteration  
**Validation**: Check state file exists and is updated  
**Test**: Kill process mid-iteration, verify state recoverable

### P-2: Stop Condition Enforcement
**Property**: Loop stops when any stop condition is met  
**Validation**: Verify loop stops within 1 iteration of condition  
**Test**: Trigger each stop condition, verify immediate stop

### P-3: Failure Handling
**Property**: Failures don't crash the loop  
**Validation**: Inject failures, verify loop continues  
**Test**: Cause step failures, verify recovery

### P-4: Iteration Limit
**Property**: Loop never exceeds max iterations  
**Validation**: Check iteration count <= max  
**Test**: Run loop to max iterations, verify stops

### P-5: Progress Tracking
**Property**: All steps are tracked in state  
**Validation**: Compare executed steps to state file  
**Test**: Execute steps, verify all recorded

### P-6: Reinjection Effectiveness
**Property**: Context is maintained across iterations  
**Validation**: Check reinjected prompts contain current context  
**Test**: Verify prompt content after reinjection

## Security and Safety

### Safety Measures

1. **Iteration Limits**: Prevent infinite loops
2. **Failure Thresholds**: Stop on repeated failures
3. **Stop Hooks**: Human can stop anytime
4. **State Persistence**: No data loss on interruption
5. **Escalation**: Human intervention on critical failures

### Resource Limits

```yaml
resource_limits:
  max_memory_mb: 1024
  max_cpu_percent: 80
  max_disk_writes_per_minute: 100
  max_api_calls_per_minute: 60
```

## Future Enhancements

1. **Parallel Loops**: Run multiple tasks concurrently
2. **Smart Reinjection**: Context-aware prompt generation
3. **Adaptive Thresholds**: Adjust limits based on task complexity
4. **Checkpoint System**: Save checkpoints for rollback
5. **Loop Analytics**: Detailed performance analysis

---

**Status**: DRAFT  
**Next Steps**:
1. Review specification
2. Approve autonomous loop design
3. Implement core loop
4. Test stop conditions
5. Deploy with monitoring

