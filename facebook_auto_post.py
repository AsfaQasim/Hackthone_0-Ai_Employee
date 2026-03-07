#!/usr/bin/env python3
"""
Facebook Auto Post

Simple script to post to Facebook automatically.
"""

import os
import sys
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def post_to_facebook(message, image_url=None):
    """
    Post a message to Facebook page.
    
    Args:
        message: Text to post
        image_url: Optional image URL
        
    Returns:
        dict: Response with success status and post ID
    """
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    
    if not page_id or not token:
        return {
            'success': False,
            'error': 'Missing FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN in .env'
        }
    
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    
    params = {
        'message': message,
        'access_token': token
    }
    
    # Add image if provided
    if image_url:
        params['link'] = image_url
    
    try:
        response = requests.post(url, params=params)
        data = response.json()
        
        if 'id' in data:
            post_id = data['id']
            return {
                'success': True,
                'post_id': post_id,
                'message': 'Post published successfully!',
                'url': f"https://facebook.com/{post_id}"
            }
        else:
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            return {
                'success': False,
                'error': error_msg
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def track_post(message, result):
    """
    Track posted message in Social_Media_Tracking folder.
    
    Args:
        message: Posted message
        result: Post result
    """
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"facebook_{timestamp}_post.md"
    filepath = tracking_dir / filename
    
    status = "✅ Published" if result['success'] else "❌ Failed"
    
    content = f"""---
type: facebook_post
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
post_id: "{result.get('post_id', 'N/A')}"
---

# Facebook Post

**Status**: {status}  
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Post ID**: {result.get('post_id', 'N/A')}  
**URL**: {result.get('url', 'N/A')}

## Message
{message}

"""
    
    if not result['success']:
        content += f"\n## Error\n{result.get('error', 'Unknown error')}\n"
    
    content += "\n---\n\n*Posted via Facebook Auto Post*\n"
    
    filepath.write_text(content, encoding='utf-8')
    print(f"📝 Tracked post: {filepath}")

def main():
    """Main function."""
    print("\n" + "=" * 70)
    print("  FACEBOOK AUTO POST")
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
    
    print(f"\n📤 Posting to Facebook...")
    print(f"   Message: {message[:50]}{'...' if len(message) > 50 else ''}")
    
    # Post to Facebook
    result = post_to_facebook(message)
    
    # Show result
    print("\n" + "=" * 70)
    if result['success']:
        print("  ✅ SUCCESS!")
        print("=" * 70)
        print(f"\n📄 Post ID: {result['post_id']}")
        print(f"🔗 URL: {result['url']}")
        print(f"\n💡 View your post at: {result['url']}")
    else:
        print("  ❌ FAILED")
        print("=" * 70)
        print(f"\n❌ Error: {result['error']}")
        
        if 'expired' in result['error'].lower():
            print("\n💡 Your token has expired. To fix:")
            print("   1. Go to: https://developers.facebook.com/tools/explorer/")
            print("   2. Generate new token with pages_manage_posts permission")
            print("   3. Change endpoint to: me/accounts")
            print("   4. Copy the access_token from response")
            print("   5. Update FACEBOOK_PAGE_ACCESS_TOKEN in .env")
    
    # Track the post
    track_post(message, result)
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
