#!/usr/bin/env python3
"""
Verify Facebook Posts

Check if posts are actually visible on your Facebook page.
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

print("\n" + "=" * 70)
print("  FACEBOOK POSTS VERIFICATION")
print("=" * 70)

print(f"\n📄 Page ID: {PAGE_ID}")
print(f"🔑 Token: {TOKEN[:30] if TOKEN else 'NOT SET'}...")

if not PAGE_ID or not TOKEN:
    print("\n❌ Missing configuration in .env")
    exit(1)

# Get page posts
print("\n🔍 Fetching posts from your page...")

url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
params = {
    'fields': 'id,message,created_time,permalink_url',
    'limit': 10,
    'access_token': TOKEN
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' in data:
        posts = data['data']
        
        if posts:
            print(f"\n✅ Found {len(posts)} post(s) on your page:")
            print("\n" + "-" * 70)
            
            for i, post in enumerate(posts, 1):
                message = post.get('message', '(No message)')
                created = post.get('created_time', 'Unknown')
                post_id = post.get('id', 'Unknown')
                permalink = post.get('permalink_url', 'No URL')
                
                # Parse date
                try:
                    dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    created_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    created_str = created
                
                print(f"\n📝 Post #{i}")
                print(f"   Posted: {created_str}")
                print(f"   Message: {message[:100]}...")
                print(f"   URL: {permalink}")
                print(f"   ID: {post_id}")
            
            print("\n" + "-" * 70)
            print(f"\n✅ Your posts ARE visible on Facebook!")
            print(f"\n🌐 View your page:")
            print(f"   https://www.facebook.com/profile.php?id={PAGE_ID}")
            
        else:
            print("\n❌ No posts found on your page")
            print("\n🤔 Possible reasons:")
            print("   1. App is in Development mode (most likely)")
            print("   2. Token doesn't have pages_manage_posts permission")
            print("   3. Posts were created but not published")
            print("   4. You're not admin of the page")
            
            print("\n💡 Check app mode:")
            print("   python check_facebook_app_mode.py")
            
            print("\n💡 Check token permissions:")
            print("   python diagnose_facebook_token.py")
    
    elif 'error' in data:
        error = data['error']
        print(f"\n❌ Error: {error.get('message', 'Unknown error')}")
        print(f"   Code: {error.get('code', 'Unknown')}")
        print(f"   Type: {error.get('type', 'Unknown')}")
        
        if error.get('code') == 190:
            print("\n💡 Token is invalid or expired")
            print("   Generate a new token:")
            print("   python facebook_token_helper.py")
        
        elif error.get('code') == 200:
            print("\n💡 Permission issue")
            print("   Make sure token has:")
            print("   - pages_read_engagement")
            print("   - pages_manage_posts")
    
    else:
        print(f"\n⚠️  Unexpected response: {data}")

except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)
print("\n📋 SUMMARY:")
print("\n   If you see 'No posts found':")
print("   → Your app is likely in Development mode")
print("   → Posts are being tracked but not actually published")
print("   → You need to switch app to Live mode")
print("\n   If you see posts listed:")
print("   → Everything is working! ✅")
print("   → Posts are visible on Facebook")
print("\n" + "=" * 70)

