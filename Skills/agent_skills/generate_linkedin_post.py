"""
Generate LinkedIn Post Skill

Creates LinkedIn post content based on a topic or task.
"""

from typing import Optional, List
from datetime import datetime
from .base_skill import BaseSkill


def generate_linkedin_post(
    topic: str,
    style: str = "professional",
    include_hashtags: bool = True,
    max_length: int = 3000,
    model_name: str = "gpt-4"
) -> str:
    """
    Generate a LinkedIn post.
    
    Args:
        topic: Topic or content for the post
        style: Style of post (professional, casual, thought-leadership, storytelling)
        include_hashtags: Whether to include relevant hashtags
        max_length: Maximum post length (LinkedIn limit is 3000 chars)
        model_name: AI model to use for generation
        
    Returns:
        LinkedIn post content
        
    Example:
        >>> post = generate_linkedin_post(
        ...     "AI automation in business",
        ...     style="thought-leadership",
        ...     include_hashtags=True
        ... )
        >>> print(post)
        "🚀 The Future of Work is Here...\n\n#AI #Automation #FutureOfWork"
    """
    skill = GenerateLinkedInPostSkill(model_name)
    return skill.execute(topic, style, include_hashtags, max_length)


class GenerateLinkedInPostSkill(BaseSkill):
    """Implementation of the LinkedIn post generation skill."""
    
    def execute(
        self,
        topic: str,
        style: str,
        include_hashtags: bool,
        max_length: int
    ) -> str:
        """
        Execute LinkedIn post generation.
        
        Args:
            topic: Post topic
            style: Post style
            include_hashtags: Include hashtags
            max_length: Maximum length
            
        Returns:
            Generated LinkedIn post
        """
        self.logger.info(f"Generating LinkedIn post: {topic} (style: {style})")
        
        # Build prompt for AI
        system_prompt = f"""You are a LinkedIn content strategist.
Your job is to create engaging, professional LinkedIn posts that drive engagement.

Style: {style}
Guidelines:
- Hook readers in the first line
- Use short paragraphs for readability
- Include relevant emojis (sparingly)
- End with a call-to-action or question
- Stay within {max_length} characters
- Be authentic and valuable"""
        
        hashtag_instruction = "\n- Include 3-5 relevant hashtags at the end" if include_hashtags else ""
        
        user_prompt = f"""Create a LinkedIn post about: {topic}

Requirements:
- Style: {style}
- Maximum length: {max_length} characters
- Engaging hook in first line
- Clear value proposition
- Professional yet personable tone{hashtag_instruction}

LinkedIn Post:"""
        
        # Call AI model
        post = self.ai_client.call(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.8,  # Higher temperature for more creative posts
            max_tokens=max_length // 2  # Rough token estimate
        )
        
        # Validate and format
        formatted_post = self._format_post(post, include_hashtags, max_length)
        
        self.logger.info(f"Generated LinkedIn post: {len(formatted_post)} characters")
        return formatted_post
    
    def _format_post(self, post: str, include_hashtags: bool, max_length: int) -> str:
        """
        Format and validate the LinkedIn post.
        
        Args:
            post: AI-generated post
            include_hashtags: Whether hashtags should be included
            max_length: Maximum allowed length
            
        Returns:
            Formatted post
        """
        post = post.strip()
        
        # Ensure it's within length limit
        if len(post) > max_length:
            self.logger.warning(f"Post exceeds {max_length} chars, truncating")
            # Truncate at last complete sentence before limit
            truncated = post[:max_length]
            last_period = truncated.rfind('.')
            if last_period > max_length * 0.8:  # If we can keep most of it
                post = truncated[:last_period + 1]
            else:
                post = truncated + "..."
        
        # Ensure hashtags are present if requested
        if include_hashtags and '#' not in post:
            post += "\n\n#professional #business #growth"
        
        return post
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from text.
        
        Args:
            text: Text containing hashtags
            
        Returns:
            List of hashtags
        """
        import re
        return re.findall(r'#\w+', text)


def generate_linkedin_post_from_task(
    task_filepath: str,
    style: str = "professional",
    model_name: str = "gpt-4"
) -> str:
    """
    Generate a LinkedIn post based on a task file.
    
    Args:
        task_filepath: Path to task markdown file
        style: Post style
        model_name: AI model to use
        
    Returns:
        LinkedIn post content
        
    Example:
        >>> post = generate_linkedin_post_from_task(
        ...     "Needs_Action/project_update.md",
        ...     style="storytelling"
        ... )
    """
    skill = GenerateLinkedInPostSkill(model_name)
    
    # Read task content
    content = skill.read_markdown(task_filepath)
    body = skill.extract_body(content)
    
    # Use task content as topic
    return skill.execute(body, style, include_hashtags=True, max_length=3000)


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python generate_linkedin_post.py <topic> [style]")
        print("Styles: professional, casual, thought-leadership, storytelling")
        sys.exit(1)
    
    topic = sys.argv[1]
    style = sys.argv[2] if len(sys.argv) > 2 else "professional"
    
    post = generate_linkedin_post(topic, style)
    print(f"\nLinkedIn Post:\n{post}")
    print(f"\nLength: {len(post)} characters")
