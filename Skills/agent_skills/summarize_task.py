"""
Summarize Task Skill

Reads a task markdown file and generates a concise summary.
"""

from typing import Optional
from .base_skill import BaseSkill


def summarize_task(task_filepath: str, max_length: int = 200, model_name: str = "gpt-4") -> str:
    """
    Summarize a task from its markdown file.
    
    Args:
        task_filepath: Path to the task markdown file
        max_length: Maximum length of summary in words
        model_name: AI model to use for summarization
        
    Returns:
        Concise summary of the task
        
    Example:
        >>> summary = summarize_task("Needs_Action/email_20260219_120000.md")
        >>> print(summary)
        "Client requests Q1 report review by Friday. High priority."
    """
    skill = SummarizeTaskSkill(model_name)
    return skill.execute(task_filepath, max_length)


class SummarizeTaskSkill(BaseSkill):
    """Implementation of the summarize task skill."""
    
    def execute(self, task_filepath: str, max_length: int) -> str:
        """
        Execute the summarization.
        
        Args:
            task_filepath: Path to task file
            max_length: Maximum summary length
            
        Returns:
            Task summary
        """
        self.logger.info(f"Summarizing task: {task_filepath}")
        
        # Read task content
        content = self.read_markdown(task_filepath)
        
        # Extract metadata and body
        metadata = self.extract_frontmatter(content)
        body = self.extract_body(content)
        
        # Build prompt for AI
        system_prompt = """You are a task summarization assistant. 
Your job is to read task descriptions and create concise, actionable summaries.
Focus on the key action items, deadlines, and priority."""
        
        user_prompt = f"""Summarize this task in {max_length} words or less:

Task Type: {metadata.get('type', 'unknown')}
Priority: {metadata.get('priority', 'normal')}
Subject: {metadata.get('subject', 'N/A')}

Content:
{body}

Provide a concise summary that captures:
1. What needs to be done
2. Who is involved
3. Any deadlines or urgency
4. Key context

Summary:"""
        
        # Call AI model
        summary = self.ai_client.call(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for more focused summaries
            max_tokens=max_length * 2  # Rough token estimate
        )
        
        self.logger.info(f"Generated summary: {len(summary)} characters")
        return summary.strip()


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python summarize_task.py <task_file>")
        sys.exit(1)
    
    task_file = sys.argv[1]
    summary = summarize_task(task_file)
    print(f"\nSummary:\n{summary}")
