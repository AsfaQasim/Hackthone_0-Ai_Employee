#!/usr/bin/env python3
"""
Get Page Token from User Token

This script will use your current USER token to get the PAGE token.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("\n" + "=" * 70)
print("  GET PAGE TOKEN")
print("=" * 70)

print("\n⚠️  IMPORTANT: First, make sure you have BOTH permissions:")
print("   1. pages_manage_posts")
print("   2. pages_read_engagement")
print("\nThen generate a NEW token in Graph API Explorer.")

user_token = input("\n🔑 Paste your NEW USER token (with both permissions): ").strip()

if not user_token:
    print("\n❌ No token provided")
    exit(1)

print(f"\n📝 Token preview: {user_token[:30]}...")

# Get pages
print("\n🔍 Getting your pages...")

url = "https://graph.facebook.com/v18.0/me/accounts"
params = {
    'access_token': user_token
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' in data and len(data['data']) > 0:
        pages = data['data']
        
        print(f"\n✅ Found {len(pages)} page(s):\n")
        
        for i, page in enumerate(pages, 1):
            print(f"{i}. {page['name']}")
            print(f"   ID: {page['id']}")
            print(f"   Token: {page['access_token'][:30]}...")
            print(f"   Roles: {', '.join(page.get('tasks', []))}")
            print()
        
        # If only one page, use it automatically
        if len(pages) == 1:
            page = pages[0]
            page_id = page['id']
            page_token = page['access_token']
            
            print(f"✅ Using page: {page['name']}")
        else:
            # Let user choose
            choice = input(f"Which page? (1-{len(pages)}): ").strip()
            try:
                idx = int(choice) - 1
                page = pages[idx]
                page_id = page['id']
                page_token = page['access_token']
            except:
                print("\n❌ Invalid choice")
                exit(1)
        
        # Update .env
        print(f"\n📝 Updating .env file...")
        
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update both ID and token
        for i, line in enumerate(lines):
            if line.startswith('FACEBOOK_PAGE_ID='):
                lines[i] = f'FACEBOOK_PAGE_ID={page_id}\n'
            elif line.startswith('FACEBOOK_PAGE_ACCESS_TOKEN='):
                lines[i] = f'FACEBOOK_PAGE_ACCESS_TOKEN={page_token}\n'
        
        with open('.env', 'w') as f:
            f.writelines(lines)
        
        print(f"\n✅ Updated .env with:")
        print(f"   FACEBOOK_PAGE_ID={page_id}")
        print(f"   FACEBOOK_PAGE_ACCESS_TOKEN={page_token[:30]}...")
        
        print(f"\n🎉 Done! Now test it:")
        print('   python facebook_auto_post.py "Test with correct PAGE token"')
        
    else:
        error = data.get('error', {})
        print(f"\n❌ Error: {error.get('message', 'No pages found')}")
        print("\n💡 Make sure:")
        print("   1. You have pages_manage_posts permission")
        print("   2. You have pages_read_engagement permission")
        print("   3. You're an admin of at least one Facebook page")

except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)
