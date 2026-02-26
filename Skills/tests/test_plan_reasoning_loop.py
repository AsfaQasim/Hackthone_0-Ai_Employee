"""
Unit tests for Plan Reasoning Loop

Tests plan creation, step generation, and sensitive action detection.
"""

import pytest
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from plan_reasoning_loop import PlanReasoningLoop, PlanStep, create_execution_plan


class TestPlanReasoningLoop:
    """Test suite for Plan Reasoning Loop."""
    
    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing."""
        temp_dir = tempfile.mkdtemp()
        plans_dir = Path(temp_dir) / "Plans"
        needs_action_dir = Path(temp_dir) / "Needs_Action"
        
        plans_dir.mkdir()
        needs_action_dir.mkdir()
        
        yield {
            'root': temp_dir,
            'plans': str(plans_dir),
            'needs_action': str(needs_action_dir)
        }
        
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def loop(self, temp_dirs):
        """Create a PlanReasoningLoop instance."""
        return PlanReasoningLoop(
            plans_dir=temp_dirs['plans'],
            needs_action_dir=temp_dirs['needs_action']
        )
    
    def test_initialization(self, loop, temp_dirs):
        """Test that loop initializes correctly."""
        assert loop.plans_dir == Path(temp_dirs['plans'])
        assert loop.plans_dir.exists()
    
    def test_read_task_with_frontmatter(self, loop, temp_dirs):
        """Test reading task with frontmatter."""
        task_content = """---
email_id: "test123"
subject: "Test Email"
type: "email_task"
priority: "high"
---

# Email: Test Email

This is the email body.

## Action Items
- [ ] Review email
- [ ] Send reply
"""
        
        task_file = Path(temp_dirs['needs_action']) / "test_task.md"
        task_file.write_text(task_content)
        
        task_data = loop.read_task(str(task_file))
        
        assert 'metadata' in task_data
        assert 'body' in task_data
        assert task_data['metadata']['email_id'] == "test123"
        assert task_data['metadata']['type'] == "email_task"
        assert "This is the email body" in task_data['body']
    
    def test_analyze_intent_from_subject(self, loop):
        """Test intent analysis from subject."""
        task_data = {
            'metadata': {
                'type': 'email_task',
                'subject': 'Q1 Report Review'
            },
            'body': 'Please review the Q1 report.'
        }
        
        goal = loop.analyze_intent(task_data)
        assert "Q1 Report Review" in goal
    
    def test_analyze_intent_from_action_items(self, loop):
        """Test intent analysis from action items."""
        task_data = {
            'metadata': {'type': 'task'},
            'body': """## Action Items
- [ ] Complete project documentation
- [ ] Submit for review"""
        }
        
        goal = loop.analyze_intent(task_data)
        assert "Complete project documentation" in goal
    
    def test_is_sensitive_action(self, loop):
        """Test sensitive action detection."""
        # Sensitive actions
        assert loop._is_sensitive_action("Send email to client") is True
        assert loop._is_sensitive_action("Post to LinkedIn") is True
        assert loop._is_sensitive_action("Delete old files") is True
        assert loop._is_sensitive_action("Make payment") is True
        
        # Non-sensitive actions
        assert loop._is_sensitive_action("Review document") is False
        assert loop._is_sensitive_action("Analyze data") is False
        assert loop._is_sensitive_action("Read email") is False
    
    def test_is_high_risk_action(self, loop):
        """Test high-risk action detection."""
        # High-risk actions
        assert loop._is_high_risk_action("Delete database") is True
        assert loop._is_high_risk_action("Make payment") is True
        assert loop._is_high_risk_action("Deploy to production") is True
        
        # Not high-risk
        assert loop._is_high_risk_action("Send email") is False
        assert loop._is_high_risk_action("Read file") is False
    
    def test_break_into_steps_from_action_items(self, loop):
        """Test step generation from existing action items."""
        task_data = {
            'metadata': {'type': 'task'},
            'body': """## Action Items
- [ ] Review requirements
- [ ] Send email to team
- [ ] Update documentation"""
        }
        
        steps = loop.break_into_steps(task_data, "Complete task")
        
        assert len(steps) == 3
        assert steps[0].number == 1
        assert "Review requirements" in steps[0].description
        assert steps[1].is_sensitive is True  # "Send email"
        assert steps[2].is_sensitive is False
    
    def test_generate_email_steps(self, loop):
        """Test email-specific step generation."""
        task_data = {
            'metadata': {'type': 'email_task'},
            'body': 'Email content'
        }
        
        steps = loop._generate_email_steps(task_data)
        
        assert len(steps) == 4
        assert any("Read" in s.description for s in steps)
        assert any("Draft" in s.description for s in steps)
        assert any("Send" in s.description for s in steps)
        
        # Last step (send) should be sensitive
        send_step = [s for s in steps if "Send" in s.description][0]
        assert send_step.is_sensitive is True
    
    def test_mark_sensitive_steps(self, loop):
        """Test marking sensitive steps."""
        steps = [
            PlanStep(1, "Review document", False, False),
            PlanStep(2, "Send email to client", False, False),
            PlanStep(3, "Delete old files", False, False),
            PlanStep(4, "Analyze results", False, False)
        ]
        
        marked_steps = loop.mark_sensitive_steps(steps)
        
        assert marked_steps[0].is_sensitive is False
        assert marked_steps[1].is_sensitive is True
        assert marked_steps[1].requires_approval is True
        assert marked_steps[2].is_sensitive is True
        assert marked_steps[2].requires_approval is True
        assert marked_steps[3].is_sensitive is False
    
    def test_save_plan(self, loop, temp_dirs):
        """Test saving plan to file."""
        from plan_reasoning_loop import ExecutionPlan
        
        steps = [
            PlanStep(1, "Review task", False, False),
            PlanStep(2, "Send email", True, True)
        ]
        
        plan = ExecutionPlan(
            task_id="test_task",
            task_file="Needs_Action/test_task.md",
            goal="Complete test task",
            steps=steps,
            created_at="2026-02-19T12:00:00",
            status="pending",
            current_step=0
        )
        
        plan_path = loop.save_plan(plan)
        
        assert Path(plan_path).exists()
        assert "test_task_plan.md" in plan_path
        
        # Check content
        content = Path(plan_path).read_text()
        assert "task_id: test_task" in content
        assert "## Steps" in content
        assert "Review task" in content
        assert "Send email" in content
        assert "SENSITIVE" in content
        assert "REQUIRES APPROVAL" in content
    
    def test_plan_format_structure(self, loop, temp_dirs):
        """Test that plan has correct structure."""
        from plan_reasoning_loop import ExecutionPlan
        
        steps = [
            PlanStep(1, "Step one", False, False),
            PlanStep(2, "Step two", True, True)
        ]
        
        plan = ExecutionPlan(
            task_id="test",
            task_file="test.md",
            goal="Test goal",
            steps=steps,
            created_at="2026-02-19T12:00:00"
        )
        
        content = loop._format_plan(plan)
        
        # Check required sections
        assert "---" in content  # Frontmatter
        assert "# Execution Plan:" in content
        assert "## Goal" in content
        assert "## Steps" in content
        assert "## Sensitive Actions Summary" in content
        assert "## Execution Notes" in content
        
        # Check step numbering
        assert "1. [ ]" in content
        assert "2. [ ]" in content
    
    def test_create_plan_end_to_end(self, loop, temp_dirs):
        """Test complete plan creation flow."""
        # Create sample task
        task_content = """---
email_id: "test123"
subject: "Project Update Request"
type: "email_task"
priority: "high"
---

# Email: Project Update Request

Please send a project update to the team.

## Action Items
- [ ] Review project status
- [ ] Draft update email
- [ ] Send to team
"""
        
        task_file = Path(temp_dirs['needs_action']) / "test_email.md"
        task_file.write_text(task_content)
        
        # Create plan
        plan_path = loop.create_plan(str(task_file))
        
        # Verify plan exists
        assert Path(plan_path).exists()
        assert plan_path.endswith("_plan.md")
        
        # Verify plan content
        content = Path(plan_path).read_text()
        assert "Project Update Request" in content or "project update" in content.lower()
        assert "## Steps" in content
        assert "1. [ ]" in content
        
        # Verify sensitive actions are marked
        assert "Send" in content
        assert "SENSITIVE" in content or "REQUIRES APPROVAL" in content
    
    def test_convenience_function(self, temp_dirs):
        """Test the convenience function."""
        # Create sample task
        task_content = """---
subject: "Test Task"
type: "task"
---

# Test Task

Complete this task.
"""
        
        task_file = Path(temp_dirs['needs_action']) / "test.md"
        task_file.write_text(task_content)
        
        # Use convenience function
        plan_path = create_execution_plan(str(task_file), plans_dir=temp_dirs['plans'])
        
        assert Path(plan_path).exists()
        assert "test_plan.md" in plan_path
    
    def test_plan_with_no_sensitive_actions(self, loop, temp_dirs):
        """Test plan creation with no sensitive actions."""
        task_content = """---
subject: "Analysis Task"
type: "task"
---

# Analysis Task

## Action Items
- [ ] Review data
- [ ] Analyze trends
- [ ] Document findings
"""
        
        task_file = Path(temp_dirs['needs_action']) / "analysis.md"
        task_file.write_text(task_content)
        
        plan_path = loop.create_plan(str(task_file))
        content = Path(plan_path).read_text()
        
        assert "No sensitive actions detected" in content
        assert "SENSITIVE" not in content
    
    def test_plan_with_multiple_sensitive_actions(self, loop, temp_dirs):
        """Test plan with multiple sensitive actions."""
        task_content = """---
subject: "Multi-Action Task"
type: "task"
---

# Multi-Action Task

## Action Items
- [ ] Review requirements
- [ ] Send email to client
- [ ] Post update to LinkedIn
- [ ] Delete old files
- [ ] Analyze results
"""
        
        task_file = Path(temp_dirs['needs_action']) / "multi.md"
        task_file.write_text(task_content)
        
        plan_path = loop.create_plan(str(task_file))
        content = Path(plan_path).read_text()
        
        # Should have multiple sensitive actions
        assert content.count("SENSITIVE") >= 3
        assert "Sensitive Actions Summary" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
