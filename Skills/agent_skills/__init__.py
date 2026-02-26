"""
Agent Skills System

Modular AI skills for task processing. Each skill is a separate function
that can be imported and used independently.

Silver Tier Skills:
- Core: summarize_task, create_plan, draft_reply, generate_linkedin_post
- Integration: process_whatsapp_messages, process_gmail_messages, auto_post_social_media
- Coordination: process_all_channels
"""

from .summarize_task import summarize_task
from .create_plan import create_plan
from .draft_reply import draft_reply
from .generate_linkedin_post import generate_linkedin_post
from .process_whatsapp_messages import process_whatsapp_messages
from .process_gmail_messages import process_gmail_messages
from .auto_post_social_media import auto_post_social_media, approve_and_post
from .process_all_channels import process_all_channels

__all__ = [
    # Core Skills
    'summarize_task',
    'create_plan',
    'draft_reply',
    'generate_linkedin_post',
    
    # Integration Skills
    'process_whatsapp_messages',
    'process_gmail_messages',
    'auto_post_social_media',
    'approve_and_post',
    
    # Coordination Skills
    'process_all_channels'
]

__version__ = '2.0.0-silver'
