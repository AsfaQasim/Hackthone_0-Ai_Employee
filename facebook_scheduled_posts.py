#!/usr/bin/env python3
"""
Facebook Scheduled Posts

Automatically post predefined messages to Facebook at scheduled times.
"""

import os
import time
import schedule
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Sample posts - customize these!
SCHEDULED_POSTS = [
    {
        'time': '09:00',  # 9 AM
        'message': '🌅 Good morning! Starting the day with positive energy. #MorningMotivation'
    },
    {
        'time': '12:00',  # 12 PM
        'message': '☀️ Midday check-in! Hope everyone is having a productive day. #Productivity'
    },
    {
        'time': '18:00',  # 6 PM
        'message': '🌆 Evening vibes! Wrapping up the day. What did you accomplish today? #EveningThoughts'
    }
]

def post_to_facebook(message):
    """Post message to Facebook."""
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    
    if not page_id or not token:
        print("❌ Missing Facebook credentials in .env")
        return False
    
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    params = {
        'message': message,
        'access_token': token
    }
    
    try:
        response = requests.post(url, params=params)
        data = response.json()
        
        if 'id' in data:
            print(f"✅ Posted successfully! Post ID: {data['id']}")
            track_post(message, data['id'])
            return True
        else:
            error = data.get('error', {}).get('message', 'Unknown error')
            print(f"❌ Failed to post: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def track_post(message, post_id):
    """Track posted message."""
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"facebook_{timestamp}_scheduled.md"
    filepath = tracking_dir / filename
    
    content = f"""---
type: facebook_scheduled_post
timestamp: "{datetime.now().isoformat()}"
post_id: "{post_id}"
---

# Facebook Scheduled Post

**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Post ID**: {post_id}  
**URL**: https://facebook.com/{post_id}

## Message
{message}

---

*Posted via Facebook Scheduled Posts*
"""
    
    filepath.write_text(content, encoding='utf-8')

def schedule_posts():
    """Schedule all posts."""
    print("\n" + "=" * 70)
    print("  FACEBOOK SCHEDULED POSTS")
    print("=" * 70)
    print("\n📅 Scheduling posts...\n")
    
    for post in SCHEDULED_POSTS:
        schedule.every().day.at(post['time']).do(
            lambda msg=post['message']: post_scheduled(msg)
        )
        print(f"   ⏰ {post['time']} - {post['message'][:50]}...")
    
    print(f"\n✅ Scheduled {len(SCHEDULED_POSTS)} posts")
    print("\n💡 Press Ctrl+C to stop")
    print("\n" + "=" * 70)

def post_scheduled(message):
    """Post a scheduled message."""
    print(f"\n📤 [{datetime.now().strftime('%H:%M:%S')}] Posting scheduled message...")
    post_to_facebook(message)

def main():
    """Main function."""
    # Schedule posts
    schedule_posts()
    
    # Run scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped")

if __name__ == "__main__":
    main()
