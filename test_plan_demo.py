"""
Demo script to test Plan Reasoning Loop implementation
"""

import sys
from pathlib import Path

# Add Skills to path
sys.path.insert(0, 'Skills')

from plan_reasoning_loop import create_execution_plan

# Create a sample task file
sample_task = """---
email_id: "demo123"
subject: "Project Update Request"
type: "email_task"
priority: "high"
---

# Email: Project Update Request

Please send a project update to the team about Q1 progress.

## Action Items
- [ ] Review Q1 project status
- [ ] Draft comprehensive update email
- [ ] Send email to team
- [ ] Schedule follow-up meeting
"""

# Create Needs_Action directory if it doesn't exist
needs_action_dir = Path("Needs_Action")
needs_action_dir.mkdir(exist_ok=True)

# Create Plans directory if it doesn't exist
plans_dir = Path("Plans")
plans_dir.mkdir(exist_ok=True)

# Write sample task
task_file = needs_action_dir / "demo_task.md"
task_file.write_text(sample_task)

print("=" * 60)
print("PLAN REASONING LOOP DEMO")
print("=" * 60)
print(f"\nCreated sample task: {task_file}")
print("\nTask content:")
print("-" * 60)
print(sample_task)
print("-" * 60)

# Create plan
try:
    print("\n\nCreating execution plan...")
    plan_path = create_execution_plan(str(task_file))
    
    print(f"\n✓ Plan created successfully: {plan_path}")
    
    # Read and display plan
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan_content = f.read()
    
    print("\n" + "=" * 60)
    print("GENERATED PLAN")
    print("=" * 60)
    print(plan_content)
    
    # Verify key elements
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    
    checks = {
        "Has frontmatter": "---" in plan_content,
        "Has goal section": "## Goal" in plan_content,
        "Has steps section": "## Steps" in plan_content,
        "Has numbered steps": "1. [ ]" in plan_content,
        "Has sensitive actions summary": "## Sensitive Actions Summary" in plan_content,
        "Marks sensitive actions": "SENSITIVE" in plan_content or "REQUIRES APPROVAL" in plan_content,
        "Has execution notes": "## Execution Notes" in plan_content
    }
    
    all_passed = True
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"{status} {check}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✓ All verification checks passed!")
    else:
        print("\n✗ Some verification checks failed")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
