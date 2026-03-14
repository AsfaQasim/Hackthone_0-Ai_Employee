#!/usr/bin/env python3
"""
Facebook MCP Integration Skill - Silver Tier

Provides MCP (Model Context Protocol) integration for Facebook posting.
This skill allows the AI agent to post to Facebook through the MCP server.
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FacebookMCPSkill")


class FacebookMCPSkill:
    """
    Facebook MCP Integration Skill.
    
    Enables AI agent to post to Facebook via MCP server.
    """
    
    def __init__(self, vault_path: str = "."):
        """
        Initialize Facebook MCP Skill.
        
        Args:
            vault_path: Path to vault for tracking
        """
        self.vault_path = Path(vault_path)
        self.tracking_dir = self.vault_path / "Social_Media_Tracking"
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        
        # Load credentials
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        
        # Validate credentials
        self.is_configured = bool(self.page_id and self.token)
        
        if not self.is_configured:
            logger.warning("Facebook credentials not configured. API posting will not work.")
        
        logger.info(f"Facebook MCP Skill initialized. Configured: {self.is_configured}")
    
    def post_to_facebook(self, message: str, link: Optional[str] = None) -> Dict[str, Any]:
        """
        Post a message to Facebook.
        
        Args:
            message: Message content to post
            link: Optional link to include
            
        Returns:
            dict: Result with success status, post_id, and message
        """
        logger.info(f"Posting to Facebook: {message[:50]}...")
        
        # Check if configured
        if not self.is_configured:
            result = {
                'success': False,
                'error': 'Facebook credentials not configured in .env',
                'requires_setup': True
            }
            self._track_post(message, result)
            return result
        
        # Import requests here to avoid dependency if not needed
        import requests
        
        url = f"https://graph.facebook.com/v18.0/{self.page_id}/feed"
        
        params = {
            'message': message,
            'access_token': self.token
        }
        
        if link:
            params['link'] = link
        
        try:
            response = requests.post(url, params=params, timeout=30)
            data = response.json()
            
            if 'id' in data:
                post_id = data['id']
                result = {
                    'success': True,
                    'post_id': post_id,
                    'url': f"https://facebook.com/{post_id}",
                    'message': 'Post published successfully!'
                }
                logger.info(f"Facebook post successful: {post_id}")
            else:
                error_msg = data.get('error', {}).get('message', 'Unknown error')
                result = {
                    'success': False,
                    'error': error_msg,
                    'error_code': data.get('error', {}).get('code')
                }
                logger.error(f"Facebook post failed: {error_msg}")
            
            self._track_post(message, result)
            return result
            
        except requests.exceptions.Timeout:
            result = {
                'success': False,
                'error': 'Request timed out'
            }
            self._track_post(message, result)
            return result
            
        except Exception as e:
            result = {
                'success': False,
                'error': str(e)
            }
            self._track_post(message, result)
            return result
    
    def post_daily_update(self) -> Dict[str, Any]:
        """
        Post a daily business update.
        
        Returns:
            dict: Result with success status
        """
        message = f"""🚀 Daily Update - {datetime.now().strftime('%B %d, %Y')}

Working on exciting AI automation projects today!

#Business #Productivity #AI #Automation"""
        
        return self.post_to_facebook(message)
    
    def post_achievement(self, achievement: str) -> Dict[str, Any]:
        """
        Post an achievement.
        
        Args:
            achievement: Achievement description
            
        Returns:
            dict: Result with success status
        """
        message = f"""🎉 Achievement Unlocked!

{achievement}

#Success #Milestone #Growth #AI"""
        
        return self.post_to_facebook(message)
    
    def post_business_update(self, update: str) -> Dict[str, Any]:
        """
        Post a business update.
        
        Args:
            update: Update description
            
        Returns:
            dict: Result with success status
        """
        message = f"""📢 Business Update

{update}

#Business #Update #News"""
        
        return self.post_to_facebook(message)
    
    def _track_post(self, message: str, result: Dict[str, Any]):
        """
        Track posted message in vault.
        
        Args:
            message: Posted message
            result: Post result
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"facebook_mcp_{timestamp}.md"
        filepath = self.tracking_dir / filename
        
        status = "✅ Published" if result['success'] else "❌ Failed"
        
        content = f"""---
type: facebook_mcp_post
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
post_id: "{result.get('post_id', 'N/A')}"
---

# Facebook MCP Post

**Status**: {status}
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Post ID**: {result.get('post_id', 'N/A')}
**URL**: {result.get('url', 'N/A')}

## Message
{message}

"""
        
        if not result['success']:
            content += f"\n## Error\n{result.get('error', 'Unknown error')}\n"
        
        if result.get('requires_setup'):
            content += """
## Setup Required

To enable Facebook posting:
1. Create Facebook App at https://developers.facebook.com
2. Get Page Access Token
3. Add to .env:
   - FACEBOOK_PAGE_ID=your_page_id
   - FACEBOOK_PAGE_ACCESS_TOKEN=your_token
"""
        
        content += "\n---\n\n*Posted via Facebook MCP Skill*\n"
        
        filepath.write_text(content, encoding='utf-8')
        logger.info(f"Tracked Facebook post: {filepath}")
    
    def get_setup_instructions(self) -> str:
        """
        Get Facebook setup instructions.
        
        Returns:
            str: Setup instructions
        """
        return """
# Facebook MCP Skill Setup

## Step 1: Create Facebook App
1. Go to https://developers.facebook.com
2. Click "Create App"
3. Choose "Business" app type
4. Fill in app details

## Step 2: Get Page Access Token
1. Go to Graph API Explorer: https://developers.facebook.com/tools/explorer/
2. Select your app
3. Click "Get Token" > "Get Page Access Token"
4. Select your page
5. Add permissions: pages_manage_posts, pages_read_engagement
6. Click "Generate Access Token"
7. Copy the token

## Step 3: Get Page ID
1. In Graph API Explorer
2. Change endpoint to: me/accounts
3. Click "Submit"
4. Copy your Page ID

## Step 4: Configure .env
Add these lines to your .env file:
```
FACEBOOK_PAGE_ID=your_page_id_here
FACEBOOK_PAGE_ACCESS_TOKEN=your_token_here
```

## Step 5: Test
Run: python facebook_silver_poster.py "Test post"
"""


# MCP Server integration
def register_mcp_tools(server) -> None:
    """
    Register Facebook tools with MCP server.
    
    Args:
        server: MCP server instance
    """
    from mcp.types import Tool
    
    # Post to Facebook tool
    server.add_tool(
        Tool(
            name="facebook_post",
            description="Post a message to Facebook Page",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message content to post"
                    },
                    "link": {
                        "type": "string",
                        "description": "Optional link to include"
                    }
                },
                "required": ["message"]
            }
        )
    )
    
    # Post daily update tool
    server.add_tool(
        Tool(
            name="facebook_post_daily_update",
            description="Post a daily business update to Facebook",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    )
    
    # Post achievement tool
    server.add_tool(
        Tool(
            name="facebook_post_achievement",
            description="Post an achievement to Facebook",
            inputSchema={
                "type": "object",
                "properties": {
                    "achievement": {
                        "type": "string",
                        "description": "Achievement description"
                    }
                },
                "required": ["achievement"]
            }
        )
    )
    
    # Get setup instructions tool
    server.add_tool(
        Tool(
            name="facebook_get_setup_instructions",
            description="Get Facebook integration setup instructions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    )


async def handle_facebook_tool_call(name: str, arguments: Dict[str, Any], skill: FacebookMCPSkill) -> str:
    """
    Handle Facebook tool calls.
    
    Args:
        name: Tool name
        arguments: Tool arguments
        skill: Facebook MCP Skill instance
        
    Returns:
        str: Tool result message
    """
    if name == "facebook_post":
        message = arguments.get("message", "")
        link = arguments.get("link")
        result = skill.post_to_facebook(message, link)
        
        if result['success']:
            return f"✅ Successfully posted to Facebook! Post ID: {result['post_id']}"
        else:
            return f"❌ Failed to post: {result['error']}"
    
    elif name == "facebook_post_daily_update":
        result = skill.post_daily_update()
        
        if result['success']:
            return f"✅ Daily update posted! Post ID: {result['post_id']}"
        else:
            return f"❌ Failed: {result['error']}"
    
    elif name == "facebook_post_achievement":
        achievement = arguments.get("achievement", "")
        result = skill.post_achievement(achievement)
        
        if result['success']:
            return f"✅ Achievement posted! Post ID: {result['post_id']}"
        else:
            return f"❌ Failed: {result['error']}"
    
    elif name == "facebook_get_setup_instructions":
        return skill.get_setup_instructions()
    
    else:
        return f"❌ Unknown tool: {name}"


# Example usage
if __name__ == "__main__":
    # Test the skill
    skill = FacebookMCPSkill()
    
    print("Facebook MCP Skill Test")
    print("=" * 50)
    
    # Test posting
    test_message = "Testing Facebook MCP Skill integration!"
    print(f"\nPosting: {test_message}")
    result = skill.post_to_facebook(test_message)
    
    if result['success']:
        print(f"✅ Success! Post ID: {result['post_id']}")
        print(f"URL: {result['url']}")
    else:
        print(f"❌ Failed: {result['error']}")
    
    print("\nTracking file created in Social_Media_Tracking/")
