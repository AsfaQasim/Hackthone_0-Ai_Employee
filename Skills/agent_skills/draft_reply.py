"""
Draft Reply Skill

Reads an email task and generates a draft reply.
"""

from typing import Optional
from datetime import datetime
from .base_skill import BaseSkill


def draft_reply(task_filepath: str, tone: str = "professional", model_name: str = "gpt-4") -> str:
    """
    Generate a draft reply for an email task.
    
    Args:
        task_filepath: Path to the email task markdown file
        tone: Tone of the reply (professional, friendly, formal, casual)
        model_name: AI model to use for draft generation
        
    Returns:
        Draft reply text
        
    Example:
        >>> reply = draft_reply("Needs_Action/email_20260219_120000.md", tone="friendly")
        >>> print(reply)
        "Hi John,\n\nThank you for reaching out..."
    """
    skill = DraftReplySkill(model_name)
    return skill.execute(task_filepath, tone)


class DraftReplySkill(BaseSkill):
    """Implementation of the draft reply skill."""
    
    def execute(self, task_filepath: str, tone: str) -> str:
        """
        Execute draft reply generation.
        
        Args:
            task_filepath: Path to task file
            tone: Desired tone for reply
            
        Returns:
            Draft reply text
        """
        self.logger.info(f"Drafting reply for: {task_filepath} (tone: {tone})")
        
        # Read task content
        content = self.read_markdown(task_filepath)
        
        # Extract metadata and body
        metadata = self.extract_frontmatter(content)
        body = self.extract_body(content)
        
        # Validate this is an email task
        if metadata.get('type') != 'email_task' and metadata.get('source') != 'gmail':
            self.logger.warning(f"Task may not be an email: {task_filepath}")
        
        # Extract email-specific metadata
        sender_name = metadata.get('sender_name', 'there')
        sender_email = metadata.get('sender_email', '')
        subject = metadata.get('subject', 'Your email')
        
        # Build prompt for AI
        system_prompt = f"""You are an email writing assistant.
Your job is to draft professional, clear, and helpful email replies.
Tone: {tone}
Guidelines:
- Be concise and clear
- Address all points raised in the original email
- Maintain appropriate tone
- Include proper greeting and closing
- Be helpful and actionable"""
        
        user_prompt = f"""Draft a reply to this email:

From: {sender_name} <{sender_email}>
Subject: {subject}

Original Email:
{body}

Write a {tone} reply that:
1. Acknowledges their message
2. Addresses their main points or questions
3. Provides clear next steps if applicable
4. Maintains appropriate tone

Draft Reply:"""
        
        # Call AI model
        draft = self.ai_client.call(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Format the draft
        formatted_draft = self._format_draft(draft, sender_name, subject)
        
        self.logger.info(f"Generated draft reply: {len(formatted_draft)} characters")
        return formatted_draft
    
    def _format_draft(self, draft: str, sender_name: str, subject: str) -> str:
        """
        Format the draft reply with proper structure.
        
        Args:
            draft: AI-generated draft
            sender_name: Name of original sender
            subject: Original subject
            
        Returns:
            Formatted draft
        """
        # Ensure proper greeting if not present
        if not draft.strip().startswith(('Hi', 'Hello', 'Dear')):
            draft = f"Hi {sender_name},\n\n{draft}"
        
        # Ensure proper closing if not present
        if not any(closing in draft.lower() for closing in ['best', 'regards', 'sincerely', 'thanks']):
            draft += "\n\nBest regards"
        
        return draft.strip()


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python draft_reply.py <email_task_file> [tone]")
        sys.exit(1)
    
    task_file = sys.argv[1]
    tone = sys.argv[2] if len(sys.argv) > 2 else "professional"
    
    reply = draft_reply(task_file, tone)
    print(f"\nDraft Reply:\n{reply}")
