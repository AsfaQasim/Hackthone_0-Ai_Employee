#!/usr/bin/env python3
"""
Facebook Silver Tier - Simple Auto Poster

Unified Facebook posting script for Silver Tier.
Supports both API and browser automation methods.
"""

import os
import sys
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FacebookSilverPoster:
    """
    Silver Tier Facebook Poster.
    
    Provides simple, reliable Facebook posting with automatic tracking.
    """
    
    def __init__(self):
        """Initialize the Facebook poster."""
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
        
        # Setup tracking directory
        self.tracking_dir = Path("Social_Media_Tracking")
        self.tracking_dir.mkdir(exist_ok=True)
        
        # Validate credentials
        if not self.page_id or not self.token:
            print("⚠️  Warning: FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN not set in .env")
            print("   Facebook API posting will not work.")
            print("   Use browser automation method instead.\n")
    
    def post_via_api(self, message, link=None):
        """
        Post to Facebook using Graph API.
        
        Args:
            message: Message to post
            link: Optional link to include
            
        Returns:
            dict: Result with success status and post ID
        """
        if not self.page_id or not self.token:
            return {
                'success': False,
                'error': 'Missing Facebook credentials in .env'
            }
        
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
                return {
                    'success': True,
                    'post_id': post_id,
                    'url': f"https://facebook.com/{post_id}",
                    'method': 'API'
                }
            else:
                error_msg = data.get('error', {}).get('message', 'Unknown error')
                return {
                    'success': False,
                    'error': error_msg,
                    'method': 'API'
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timed out',
                'method': 'API'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'API'
            }
    
    def track_post(self, message, result):
        """
        Track posted message in Social_Media_Tracking folder.
        
        Args:
            message: Posted message
            result: Post result
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"facebook_{timestamp}_silver.md"
        filepath = self.tracking_dir / filename
        
        status = "✅ Published" if result['success'] else "❌ Failed"
        
        content = f"""---
type: facebook_silver_post
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
post_id: "{result.get('post_id', 'N/A')}"
method: "{result.get('method', 'Unknown')}"
---

# Facebook Silver Tier Post

**Status**: {status}
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Post ID**: {result.get('post_id', 'N/A')}
**URL**: {result.get('url', 'N/A')}
**Method**: {result.get('method', 'Unknown')}

## Message
{message}

"""
        
        if not result['success']:
            content += f"\n## Error\n{result.get('error', 'Unknown error')}\n"
        
        content += "\n---\n\n*Posted via Facebook Silver Tier*\n"
        
        filepath.write_text(content, encoding='utf-8')
        return filepath
    
    def post_daily_update(self):
        """Post a daily business update."""
        message = f"""🚀 Daily Update - {datetime.now().strftime('%B %d, %Y')}

Working on exciting AI automation projects today!

#Business #Productivity #AI #Automation"""
        return self.post(message)
    
    def post_achievement(self, achievement):
        """Post an achievement."""
        message = f"""🎉 Achievement Unlocked!

{achievement}

#Success #Milestone #Growth #AI"""
        return self.post(message)
    
    def post(self, message, link=None):
        """
        Post a message to Facebook.
        
        Tries API method first, falls back to manual instructions.
        
        Args:
            message: Message to post
            link: Optional link to include
            
        Returns:
            dict: Result with success status
        """
        print("\n" + "=" * 70)
        print("  FACEBOOK SILVER TIER POSTER")
        print("=" * 70)
        
        print(f"\n📝 Message:")
        print(f"   {message[:100]}{'...' if len(message) > 100 else ''}")
        
        # Try API method first
        print(f"\n📤 Posting via API...")
        result = self.post_via_api(message, link)
        
        # Track the post
        filepath = self.track_post(message, result)
        
        # Show result
        print("\n" + "=" * 70)
        if result['success']:
            print("  ✅ SUCCESS!")
            print("=" * 70)
            print(f"\n📄 Post ID: {result['post_id']}")
            print(f"🔗 URL: {result['url']}")
            print(f"📁 Tracked: {filepath}")
            print(f"\n💡 View your post: {result['url']}")
        else:
            print("  ❌ FAILED")
            print("=" * 70)
            print(f"\n❌ Error: {result['error']}")
            print(f"📁 Tracked: {filepath}")
            
            if 'expired' in result['error'].lower() or 'invalid' in result['error'].lower():
                print("\n💡 Token issue detected. To fix:")
                print("   1. Go to: https://developers.facebook.com/tools/explorer/")
                print("   2. Generate new token with pages_manage_posts permission")
                print("   3. Change endpoint to: me/accounts")
                print("   4. Copy the access_token from response")
                print("   5. Update FACEBOOK_PAGE_ACCESS_TOKEN in .env")
                print("\n   Or use browser automation:")
                print("   python facebook_post_now.py \"Your message\"")
            
            elif 'permission' in result['error'].lower():
                print("\n💡 Permission issue. Check:")
                print("   1. You're admin of the Facebook Page")
                print("   2. Token has pages_manage_posts permission")
                print("   3. App is in Live mode (not Development)")
        
        print("\n" + "=" * 70)
        
        return result


def main():
    """Main function."""
    print("\n" + "=" * 70)
    print("  FACEBOOK SILVER TIER - AUTO POSTER")
    print("=" * 70)
    
    # Check if message provided as argument
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        print("\n📝 Enter your message (or 'quit' to exit):")
        message = input("> ").strip()
        
        if message.lower() == 'quit':
            print("👋 Goodbye!")
            return
    
    if not message:
        print("❌ No message provided")
        return
    
    # Create poster and post
    poster = FacebookSilverPoster()
    result = poster.post(message)
    
    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()
