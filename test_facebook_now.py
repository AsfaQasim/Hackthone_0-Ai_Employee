#!/usr/bin/env python3
"""
Quick Facebook Token Test
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("\n" + "=" * 70)
print("  FACEBOOK TOKEN TEST")
print("=" * 70)

page_id = os.getenv('FACEBOOK_PAGE_ID')
token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

print(f"\n📋 Configuration:")
print(f"   Page ID: {page_id}")
print(f"   Token: {token[:20] if token else 'NOT SET'}...")

if not page_id or not token:
    print("\n❌ Missing configuration in .env")
    exit(1)

print("\n🔍 Testing token...")

# Test 1: Get page info
url = f"https://graph.facebook.com/v18.0/{page_id}"
params = {
    'fields': 'id,name,access_token',
    'access_token': token
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'error' in data:
        print(f"\n❌ Token Error: {data['error'].get('message', 'Unknown')}")
        print("\n💡 Your token might be expired. To fix:")
        print("   1. Go to: https://developers.facebook.com/tools/explorer/")
        print("   2. Generate new token with pages_manage_posts permission")
        print("   3. Change endpoint to: me/accounts")
        print("   4. Copy the access_token from response")
        print("   5. Update FACEBOOK_PAGE_ACCESS_TOKEN in .env")
    else:
        print(f"\n✅ Token is valid!")
        print(f"\n📄 Page Info:")
        print(f"   Name: {data.get('name', 'N/A')}")
        print(f"   ID: {data.get('id', 'N/A')}")
        
        # Test 2: Check posting permission
        print("\n🔐 Testing posting permission...")
        test_url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
        test_params = {
            'message': 'Test post - please ignore',
            'access_token': token,
            'published': 'false'  # Don't actually publish
        }
        
        test_response = requests.post(test_url, params=test_params)
        
        if test_response.status_code == 200:
            print("   ✅ Posting permission: OK")
            print("\n🎉 Everything is working!")
            print("\n📝 You can now:")
            print("   - Post to Facebook using the MCP server")
            print("   - Use Claude Code to post automatically")
            print("   - Run: python test_facebook_autopost.py")
        else:
            error = test_response.json().get('error', {})
            print(f"   ❌ Posting permission: FAILED")
            print(f"   Error: {error.get('message', 'Unknown')}")
            print("\n💡 Make sure your token has 'pages_manage_posts' permission")

except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)
