#!/usr/bin/env python3
"""
Facebook Auto Poster

Automatically posts business updates to Facebook based on vault activity.
"""

import os
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FacebookAutoPoster:
    """
    Automatically posts to Facebook based on business activity.
    """
    
    def __init__(self, vault_path="."):
        """Initialize the auto poster."""
        self.vault_path = Path(vault_path)
        self.tracking_dir = self.vault_path / "Social_Media_Tracking"
        self.tracking_dir.mkdir(exist_ok=True)
        
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        
        if not self.page_id or not self.token:
            raise ValueError("Missing FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN in .env")
        
        logger.info(f"Facebook Auto Poster initialized for page: {self.page_id}")
    
    def post_to_facebook(self, message, link=None):
        """
        Post a message to Facebook.
        
        Args:
            message: Text to post
            link: Optional link to include
            
        Returns:
            dict: Result with success status and post ID
        """
        url = f"https://graph.facebook.com/v18.0/{self.page_id}/feed"
        
        params = {
            'message': message,
            'access_token': self.token
        }
        
        if link:
            params['link'] = link
        
        try:
            response = requests.post(url, params=params)
            data = response.json()
            
            if 'id' in data:
                post_id = data['id']
                logger.info(f"Posted successfully! Post ID: {post_id}")
                
                self._track_post(message, post_id, True)
                
                return {
                    'success': True,
                    'post_id': post_id,
                    'url': f"https://facebook.com/{post_id}"
                }
            else:
                error_msg = data.get('error', {}).get('message', 'Unknown error')
                logger.error(f"Failed to post: {error_msg}")
                
                self._track_post(message, None, False, error_msg)
                
                return {
                    'success': False,
                    'error': error_msg
                }
                
        except Exception as e:
            logger.error(f"Error posting: {e}")
            self._track_post(message, None, False, str(e))
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def _track_post(self, message, post_id, success, error=None):
        """Track posted message."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"facebook_{timestamp}_auto.md"
        filepath = self.tracking_dir / filename
        
        status = "✅ Published" if success else "❌ Failed"
        
        content = f"""---
type: facebook_auto_post
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
post_id: "{post_id if post_id else 'N/A'}"
---

# Facebook Auto Post

**Status**: {status}  
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Post ID**: {post_id if post_id else 'N/A'}  
**URL**: {f"https://facebook.com/{post_id}" if post_id else 'N/A'}

## Message
{message}

"""
        
        if error:
            content += f"\n## Error\n{error}\n"
        
        content += "\n---\n\n*Posted via Facebook Auto Poster*\n"
        
        filepath.write_text(content, encoding='utf-8')
        logger.info(f"Tracked post: {filepath}")
    
    def post_daily_update(self):
        """Post a daily business update."""
        message = f"""🚀 Daily Update - {datetime.now().strftime('%B %d, %Y')}

Working on exciting projects today! 

#Business #Productivity #AI #Automation"""
        
        return self.post_to_facebook(message)
    
    def post_achievement(self, achievement):
        """Post an achievement."""
        message = f"""🎉 Achievement Unlocked!

{achievement}

#Success #Milestone #Growth"""
        
        return self.post_to_facebook(message)
    
    def post_custom(self, message):
        """Post a custom message."""
        return self.post_to_facebook(message)

def main():
    """Main function for testing."""
    import sys
    
    print("\n" + "=" * 70)
    print("  FACEBOOK AUTO POSTER")
    print("=" * 70)
    
    try:
        poster = FacebookAutoPoster()
        
        if len(sys.argv) > 1:
            # Post message from command line
            message = ' '.join(sys.argv[1:])
            print(f"\n📤 Posting: {message[:50]}...")
            result = poster.post_custom(message)
        else:
            # Post daily update
            print("\n📤 Posting daily update...")
            result = poster.post_daily_update()
        
        if result['success']:
            print(f"\n✅ Success!")
            print(f"   Post ID: {result['post_id']}")
            print(f"   URL: {result['url']}")
        else:
            print(f"\n❌ Failed: {result['error']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
