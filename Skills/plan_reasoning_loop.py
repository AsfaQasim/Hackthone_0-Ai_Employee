"""
Plan Reasoning Loop

Creates execution plans before performing actions. Analyzes tasks, breaks them
into steps, identifies sensitive actions, and saves structured plans.
"""

import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import yaml


@dataclass
class PlanStep:
    """Represents a single step in an execution plan."""
    number: int
    description: str
    is_sensitive: bool
    requires_approval: bool
    estimated_time: Optional[str] = None
    dependencies: Optional[List[int]] = None


@dataclass
class ExecutionPlan:
    """Represents a complete execution plan."""
    task_id: str
    task_file: str
    goal: str
    steps: List[PlanStep]
    created_at: str
    status: str = "pending"
    current_step: int = 0


class PlanReasoningLoop:
    """
    Plan Reasoning Loop implementation.
    
    Analyzes tasks and creates structured execution plans with
    sensitive action detection.
    """
    
    # Sensitive action keywords that require approval
    SENSITIVE_KEYWORDS = [
        'send', 'email', 'post', 'publish', 'delete', 'remove',
        'pay', 'payment', 'invoice', 'transfer', 'purchase',
        'share', 'forward', 'reply', 'respond', 'commit',
        'deploy', 'release', 'approve', 'reject', 'cancel'
    ]
    
    # High-risk actions that always require approval
    HIGH_RISK_ACTIONS = [
        'delete', 'remove', 'cancel', 'reject',
        'pay', 'payment', 'transfer', 'purchase',
        'deploy', 'release', 'publish'
    ]
    
    def __init__(self, plans_dir: str = "Plans", needs_action_dir: str = "Needs_Action"):
        """
        Initialize the Plan Reasoning Loop.
        
        Args:
            plans_dir: Directory to save plans
            needs_action_dir: Directory containing tasks
        """
        self.plans_dir = Path(plans_dir)
        self.needs_action_dir = Path(needs_action_dir)
        self.logger = logging.getLogger("PlanReasoningLoop")
        
        # Ensure directories exist
        self.plans_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure logging if not already configured
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
    
    def read_task(self, task_filepath: str) -> Dict:
        """
        Read task file and extract metadata and content.
        
        Args:
            task_filepath: Path to task file
            
        Returns:
            Dictionary with metadata and content
        """
        try:
            with open(task_filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            metadata = {}
            body = content
            
            frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
            if frontmatter_match:
                try:
                    metadata = yaml.safe_load(frontmatter_match.group(1))
                    body = content[frontmatter_match.end():]
                except yaml.YAMLError as e:
                    self.logger.warning(f"Failed to parse frontmatter: {e}")
            
            return {
                'metadata': metadata,
                'body': body.strip(),
                'full_content': content
            }
        
        except Exception as e:
            self.logger.error(f"Failed to read task file {task_filepath}: {e}")
            raise
    
    def analyze_intent(self, task_data: Dict) -> str:
        """
        Analyze task intent and determine the goal.
        
        Args:
            task_data: Task data with metadata and body
            
        Returns:
            Goal statement
        """
        metadata = task_data['metadata']
        body = task_data['body']
        
        # Extract goal from various sources
        task_type = metadata.get('type', 'unknown')
        subject = metadata.get('subject', '')
        
        # Look for explicit goal in body
        goal_match = re.search(r'##\s*Goal[:\s]*(.*?)(?:\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
        if goal_match:
            return goal_match.group(1).strip()
        
        # Look for action items
        action_match = re.search(r'##\s*Action Items[:\s]*(.*?)(?:\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
        if action_match:
            actions = action_match.group(1).strip()
            first_action = actions.split('\n')[0].strip('- []')
            return first_action
        
        # Derive from task type and subject
        if task_type == 'email_task':
            return f"Respond to email: {subject}"
        elif 'project' in task_type.lower():
            return f"Complete project: {subject}"
        else:
            return f"Process task: {subject or 'Untitled'}"
    
    def break_into_steps(self, task_data: Dict, goal: str) -> List[PlanStep]:
        """
        Break task into numbered steps.
        
        Args:
            task_data: Task data
            goal: Goal statement
            
        Returns:
            List of plan steps
        """
        steps = []
        body = task_data['body']
        metadata = task_data['metadata']
        
        # Look for existing action items
        action_match = re.search(r'##\s*Action Items[:\s]*(.*?)(?:\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
        
        if action_match:
            # Parse existing action items
            actions_text = action_match.group(1).strip()
            action_lines = [line.strip() for line in actions_text.split('\n') if line.strip()]
            
            for i, line in enumerate(action_lines, 1):
                # Remove checkbox markers
                description = re.sub(r'^[-*]\s*\[[ x]\]\s*', '', line)
                description = description.strip()
                
                if description:
                    is_sensitive = self._is_sensitive_action(description)
                    steps.append(PlanStep(
                        number=i,
                        description=description,
                        is_sensitive=is_sensitive,
                        requires_approval=is_sensitive
                    ))
        else:
            # Generate steps based on task type
            task_type = metadata.get('type', 'unknown')
            
            if task_type == 'email_task':
                steps = self._generate_email_steps(task_data)
            elif 'project' in task_type.lower():
                steps = self._generate_project_steps(task_data)
            else:
                steps = self._generate_generic_steps(task_data, goal)
        
        return steps
    
    def _generate_email_steps(self, task_data: Dict) -> List[PlanStep]:
        """Generate steps for email tasks."""
        return [
            PlanStep(1, "Read and analyze email content", False, False),
            PlanStep(2, "Draft reply addressing all points", False, False),
            PlanStep(3, "Review draft for tone and accuracy", False, False),
            PlanStep(4, "Send email reply", True, True)
        ]
    
    def _generate_project_steps(self, task_data: Dict) -> List[PlanStep]:
        """Generate steps for project tasks."""
        return [
            PlanStep(1, "Review project requirements", False, False),
            PlanStep(2, "Break down into subtasks", False, False),
            PlanStep(3, "Execute each subtask", False, False),
            PlanStep(4, "Test and verify completion", False, False),
            PlanStep(5, "Document results", False, False)
        ]
    
    def _generate_generic_steps(self, task_data: Dict, goal: str) -> List[PlanStep]:
        """Generate generic steps for unknown task types."""
        return [
            PlanStep(1, "Analyze task requirements", False, False),
            PlanStep(2, f"Execute: {goal}", False, False),
            PlanStep(3, "Verify completion", False, False)
        ]
    
    def _is_sensitive_action(self, description: str) -> bool:
        """
        Check if a step description contains sensitive actions.
        
        Args:
            description: Step description
            
        Returns:
            True if sensitive, False otherwise
        """
        description_lower = description.lower()
        
        # Check for sensitive keywords
        for keyword in self.SENSITIVE_KEYWORDS:
            if keyword in description_lower:
                return True
        
        return False
    
    def _is_high_risk_action(self, description: str) -> bool:
        """
        Check if a step is high-risk.
        
        Args:
            description: Step description
            
        Returns:
            True if high-risk, False otherwise
        """
        description_lower = description.lower()
        
        for keyword in self.HIGH_RISK_ACTIONS:
            if keyword in description_lower:
                return True
        
        return False
    
    def mark_sensitive_steps(self, steps: List[PlanStep]) -> List[PlanStep]:
        """
        Mark sensitive steps that require approval.
        
        Args:
            steps: List of plan steps
            
        Returns:
            Updated list with sensitive flags
        """
        for step in steps:
            if not step.is_sensitive:
                step.is_sensitive = self._is_sensitive_action(step.description)
            
            # High-risk actions always require approval
            if self._is_high_risk_action(step.description):
                step.is_sensitive = True
                step.requires_approval = True
            
            # Sensitive actions require approval
            if step.is_sensitive:
                step.requires_approval = True
        
        return steps
    
    def save_plan(self, plan: ExecutionPlan) -> str:
        """
        Save execution plan to file.
        
        Args:
            plan: Execution plan to save
            
        Returns:
            Path to saved plan file
        """
        # Generate filename
        filename = f"{plan.task_id}_plan.md"
        filepath = self.plans_dir / filename
        
        # Format plan content
        content = self._format_plan(plan)
        
        # Write file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Saved plan: {filepath}")
            return str(filepath)
        
        except Exception as e:
            self.logger.error(f"Failed to save plan: {e}")
            raise
    
    def _format_plan(self, plan: ExecutionPlan) -> str:
        """
        Format plan as markdown.
        
        Args:
            plan: Execution plan
            
        Returns:
            Formatted markdown content
        """
        # Frontmatter
        frontmatter = f"""---
task_id: {plan.task_id}
task_file: {plan.task_file}
created: {plan.created_at}
status: {plan.status}
current_step: {plan.current_step}
total_steps: {len(plan.steps)}
---

"""
        
        # Goal
        goal_section = f"""# Execution Plan: {plan.goal}

## Goal
{plan.goal}

"""
        
        # Steps
        steps_section = "## Steps\n\n"
        
        for step in plan.steps:
            # Step number and description
            checkbox = "[ ]"
            steps_section += f"{step.number}. {checkbox} {step.description}"
            
            # Add flags
            flags = []
            if step.is_sensitive:
                flags.append("⚠️ SENSITIVE")
            if step.requires_approval:
                flags.append("🔒 REQUIRES APPROVAL")
            
            if flags:
                steps_section += f" - {' | '.join(flags)}"
            
            steps_section += "\n"
            
            # Add estimated time if available
            if step.estimated_time:
                steps_section += f"   - Estimated time: {step.estimated_time}\n"
            
            # Add dependencies if available
            if step.dependencies:
                deps = ", ".join(str(d) for d in step.dependencies)
                steps_section += f"   - Depends on: Step(s) {deps}\n"
            
            steps_section += "\n"
        
        # Sensitive actions summary
        sensitive_steps = [s for s in plan.steps if s.is_sensitive]
        if sensitive_steps:
            summary_section = f"""## Sensitive Actions Summary

This plan contains {len(sensitive_steps)} sensitive action(s) that require approval:

"""
            for step in sensitive_steps:
                summary_section += f"- Step {step.number}: {step.description}\n"
            
            summary_section += "\n**⚠️ These steps will require explicit approval before execution.**\n\n"
        else:
            summary_section = "## Sensitive Actions Summary\n\nNo sensitive actions detected. All steps can be executed automatically.\n\n"
        
        # Execution notes
        notes_section = """## Execution Notes

- Review each step before execution
- Sensitive steps will pause for approval
- Update this file as steps are completed
- Mark completed steps with [x]

---

*Generated by Plan Reasoning Loop*
"""
        
        return frontmatter + goal_section + steps_section + summary_section + notes_section
    
    def create_plan(self, task_filepath: str) -> str:
        """
        Create execution plan for a task.
        
        This is the main entry point that orchestrates the entire flow:
        1. Read task
        2. Analyze intent
        3. Break into steps
        4. Mark sensitive steps
        5. Save plan
        
        Args:
            task_filepath: Path to task file
            
        Returns:
            Path to created plan file
        """
        self.logger.info(f"Creating plan for task: {task_filepath}")
        
        # 1. Read task
        task_data = self.read_task(task_filepath)
        
        # 2. Analyze intent
        goal = self.analyze_intent(task_data)
        self.logger.info(f"Identified goal: {goal}")
        
        # 3. Break into steps
        steps = self.break_into_steps(task_data, goal)
        self.logger.info(f"Generated {len(steps)} steps")
        
        # 4. Mark sensitive steps
        steps = self.mark_sensitive_steps(steps)
        sensitive_count = sum(1 for s in steps if s.is_sensitive)
        self.logger.info(f"Marked {sensitive_count} sensitive steps")
        
        # Generate task ID from filename
        task_id = Path(task_filepath).stem
        
        # Create execution plan
        plan = ExecutionPlan(
            task_id=task_id,
            task_file=task_filepath,
            goal=goal,
            steps=steps,
            created_at=datetime.now().isoformat(),
            status="pending",
            current_step=0
        )
        
        # 5. Save plan
        plan_path = self.save_plan(plan)
        
        self.logger.info(f"Plan created successfully: {plan_path}")
        return plan_path


def create_execution_plan(task_filepath: str, plans_dir: str = "Plans") -> str:
    """
    Create an execution plan for a task.
    
    Convenience function for creating plans.
    
    Args:
        task_filepath: Path to task file in Needs_Action
        plans_dir: Directory to save plans
        
    Returns:
        Path to created plan file
        
    Example:
        >>> plan_path = create_execution_plan("Needs_Action/email_20260219_120000.md")
        >>> print(f"Plan created: {plan_path}")
        "Plan created: Plans/email_20260219_120000_plan.md"
    """
    loop = PlanReasoningLoop(plans_dir=plans_dir)
    return loop.create_plan(task_filepath)


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python plan_reasoning_loop.py <task_file>")
        sys.exit(1)
    
    task_file = sys.argv[1]
    
    try:
        plan_path = create_execution_plan(task_file)
        print(f"\n✓ Plan created: {plan_path}")
        
        # Display plan
        with open(plan_path, 'r') as f:
            print(f"\n{f.read()}")
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
