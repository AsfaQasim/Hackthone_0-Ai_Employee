#!/usr/bin/env python3
"""
Quick Facebook Token Test

After updating your token in .env, run this to verify it works.
"""

import os
import requests
from dotenv import load_dotenv

# Reload .env to get latest values
load_dotenv(override=True)

print("\n" + "=" * 70)
print("  FACEBOOK TOKEN VERIFICATION")
print("=" * 70)

page_id = os.getenv('FACEBOOK_PAGE_ID')
token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

if not page_id or not token:
    print("\n❌ Missing credentials in .env")
    print("   Please update FACEBOOK_PAGE_ID and FACEBOOK_PAGE_ACCESS_TOKEN")
    exit(1)

print(f"\n📋 Testing credentials...")
print(f"   Page ID: {page_id}")
print(f"   Token: {token[:30]}...")

# Test token
url = f"https://graph.facebook.com/v18.0/{page_id}"
params = {'access_token': token}

try:
    response = requests.get(url, params=params, timeout=10)
    data = response.json()
    
    if 'id' in data:
        print("\n✅ TOKEN IS VALID!")
        print(f"\n   Page ID: {data['id']}")
        if 'name' in data:
            print(f"   Page Name: {data['name']}")
        
        print("\n" + "=" * 70)
        print("  ✅ READY TO POST!")
        print("=" * 70)
        print("\n📝 Test posting command:")
        print("   python facebook_silver_poster.py \"Hello from Silver Tier!\"")
        print("\n💡 Or use the MCP skill:")
        print("   from Skills.facebook_mcp_skill import FacebookMCPSkill")
        print("   skill = FacebookMCPSkill()")
        print("   skill.post_to_facebook(\"Test post\")")
        
    else:
        error = data.get('error', {})
        print("\n❌ TOKEN INVALID:")
        print(f"   Error: {error.get('message', 'Unknown')}")
        print("\n💡 To fix:")
        print("   1. Go to: https://developers.facebook.com/tools/explorer/")
        print("   2. Select your app")
        print("   3. Get Token > Get Page Access Token")
        print("   4. Select your page")
        print("   5. Copy the token")
        print("   6. Update .env: FACEBOOK_PAGE_ACCESS_TOKEN=<new_token>")
        print("   7. Run this test again")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70 + "\n")
