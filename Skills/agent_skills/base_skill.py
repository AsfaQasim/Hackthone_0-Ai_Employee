"""
Base Skill Module

Provides common functionality for all agent skills including AI model calling.
"""

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path


class AIModelClient:
    """
    Client for calling AI models.
    
    This is a placeholder that can be replaced with actual AI model integration
    (OpenAI, Anthropic, local models, etc.)
    """
    
    def __init__(self, model_name: str = "gpt-4", api_key: Optional[str] = None):
        """
        Initialize AI model client.
        
        Args:
            model_name: Name of the AI model to use
            api_key: API key for the model (reads from env if not provided)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.logger = logging.getLogger(f"AIModelClient.{model_name}")
    
    def call(self, prompt: str, system_prompt: Optional[str] = None, 
             temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Call the AI model with a prompt.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text from the model
        """
        # TODO: Implement actual AI model call
        # This is a placeholder that returns a mock response
        
        self.logger.info(f"Calling {self.model_name} with prompt length: {len(prompt)}")
        
        # For now, return a placeholder response
        # In production, this would call OpenAI, Anthropic, or other AI APIs
        return self._mock_response(prompt, system_prompt)
    
    def _mock_response(self, prompt: str, system_prompt: Optional[str]) -> str:
        """
        Generate a mock response for testing.
        
        In production, replace this with actual AI model calls.
        """
        if "summarize" in prompt.lower():
            return "This is a summary of the task content."
        elif "plan" in prompt.lower():
            return """# Plan

## Goal
Complete the task efficiently

## Steps
1. Analyze requirements
2. Execute task
3. Verify completion"""
        elif "reply" in prompt.lower():
            return """Subject: Re: Your Request

Thank you for your email. I will review this and get back to you shortly.

Best regards"""
        elif "linkedin" in prompt.lower():
            return """Excited to share some insights on productivity! 🚀

Here are 3 key takeaways:
1. Focus on high-impact tasks
2. Automate repetitive work
3. Continuous learning

#productivity #automation #growth"""
        else:
            return "AI-generated response based on the input."


class BaseSkill:
    """
    Base class for all agent skills.
    
    Provides common functionality like logging, AI model access, and file I/O.
    """
    
    def __init__(self, model_name: str = "gpt-4"):
        """
        Initialize the skill.
        
        Args:
            model_name: Name of the AI model to use
        """
        self.model_name = model_name
        self.ai_client = AIModelClient(model_name)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configure logging if not already configured
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
    
    def read_markdown(self, filepath: str) -> str:
        """
        Read markdown file content.
        
        Args:
            filepath: Path to markdown file
            
        Returns:
            File content as string
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to read file {filepath}: {e}")
            raise
    
    def write_markdown(self, filepath: str, content: str) -> bool:
        """
        Write content to markdown file.
        
        Args:
            filepath: Path to output file
            content: Content to write
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Wrote file: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to write file {filepath}: {e}")
            return False
    
    def extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Extract YAML frontmatter from markdown content.
        
        Args:
            content: Markdown content with frontmatter
            
        Returns:
            Dictionary of frontmatter fields
        """
        import re
        import yaml
        
        # Match frontmatter between --- delimiters
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError as e:
                self.logger.warning(f"Failed to parse frontmatter: {e}")
                return {}
        return {}
    
    def extract_body(self, content: str) -> str:
        """
        Extract body content (without frontmatter) from markdown.
        
        Args:
            content: Markdown content with frontmatter
            
        Returns:
            Body content without frontmatter
        """
        import re
        
        # Remove frontmatter
        content_without_frontmatter = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        return content_without_frontmatter.strip()
