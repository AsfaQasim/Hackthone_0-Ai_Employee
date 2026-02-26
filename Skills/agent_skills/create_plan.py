"""
Create Plan Skill

Reads a task and generates a detailed execution plan with steps.
"""

from typing import Optional
from datetime import datetime
from .base_skill import BaseSkill


def create_plan(task_filepath: str, output_dir: str = "Plans", model_name: str = "gpt-4") -> str:
    """
    Create an execution plan for a task.
    
    Args:
        task_filepath: Path to the task markdown file
        output_dir: Directory to save the plan (default: Plans)
        model_name: AI model to use for plan generation
        
    Returns:
        Path to the generated Plan.md file
        
    Example:
        >>> plan_path = create_plan("Needs_Action/email_20260219_120000.md")
        >>> print(f"Plan created: {plan_path}")
        "Plan created: Plans/plan_20260219_120000.md"
    """
    skill = CreatePlanSkill(model_name)
    return skill.execute(task_filepath, output_dir)


class CreatePlanSkill(BaseSkill):
    """Implementation of the create plan skill."""
    
    def execute(self, task_filepath: str, output_dir: str) -> str:
        """
        Execute plan creation.
        
        Args:
            task_filepath: Path to task file
            output_dir: Output directory for plan
            
        Returns:
            Path to created plan file
        """
        self.logger.info(f"Creating plan for task: {task_filepath}")
        
        # Read task content
        content = self.read_markdown(task_filepath)
        
        # Extract metadata and body
        metadata = self.extract_frontmatter(content)
        body = self.extract_body(content)
        
        # Build prompt for AI
        system_prompt = """You are a strategic planning assistant.
Your job is to break down tasks into clear, actionable steps.
Create detailed plans with:
- Clear goal statement
- Step-by-step breakdown
- Dependencies between steps
- Estimated time for each step
- Success criteria"""
        
        user_prompt = f"""Create a detailed execution plan for this task:

Task Type: {metadata.get('type', 'unknown')}
Priority: {metadata.get('priority', 'normal')}
Subject: {metadata.get('subject', 'N/A')}

Content:
{body}

Generate a plan in markdown format with:
1. Goal statement
2. Numbered steps (be specific and actionable)
3. Dependencies (if any)
4. Estimated time
5. Success criteria

Plan:"""
        
        # Call AI model
        plan_content = self.ai_client.call(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=1500
        )
        
        # Generate plan file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plan_filename = f"plan_{timestamp}.md"
        plan_filepath = f"{output_dir}/{plan_filename}"
        
        # Create full plan with frontmatter
        full_plan = self._format_plan(plan_content, metadata, task_filepath)
        
        # Write plan file
        self.write_markdown(plan_filepath, full_plan)
        
        self.logger.info(f"Created plan: {plan_filepath}")
        return plan_filepath
    
    def _format_plan(self, plan_content: str, task_metadata: dict, task_filepath: str) -> str:
        """
        Format the plan with frontmatter and metadata.
        
        Args:
            plan_content: AI-generated plan content
            task_metadata: Metadata from original task
            task_filepath: Path to original task
            
        Returns:
            Formatted plan markdown
        """
        frontmatter = f"""---
plan_id: plan_{datetime.now().strftime('%Y%m%d%H%M%S')}
created: {datetime.now().isoformat()}
source_task: {task_filepath}
task_type: {task_metadata.get('type', 'unknown')}
priority: {task_metadata.get('priority', 'normal')}
status: pending
current_step: 0
---

"""
        return frontmatter + plan_content


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python create_plan.py <task_file>")
        sys.exit(1)
    
    task_file = sys.argv[1]
    plan_path = create_plan(task_file)
    print(f"\nPlan created: {plan_path}")
