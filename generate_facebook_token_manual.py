#!/usr/bin/env python3
"""
Generate Facebook Token Manually

This creates a URL that will give you a token with correct permissions.
"""

import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('FACEBOOK_APP_ID', '1423095195415885')

print("\n" + "=" * 70)
print("  GENERATE FACEBOOK TOKEN MANUALLY")
print("=" * 70)

print(f"\n📱 Your App ID: {APP_ID}")

# Create OAuth URL with correct permissions
permissions = [
    'pages_manage_posts',
    'pages_read_engagement',
    'pages_show_list'
]

scope = ','.join(permissions)

oauth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={APP_ID}&redirect_uri=https://www.facebook.com/connect/login_success.html&scope={scope}&response_type=token"

print("\n📝 Step 1: Get User Token")
print("\n1. Copy this URL:")
print(f"\n{oauth_url}")
print("\n2. Paste it in your browser")
print("3. Click 'Continue' and allow permissions")
print("4. You'll be redirected to a page")
print("5. Look at the URL - it will have: access_token=EAA...")
print("6. Copy everything after 'access_token=' until '&'")

print("\n" + "=" * 70)

user_token = input("\n🔑 Paste the access_token here: ").strip()

if not user_token:
    print("\n❌ No token provided")
    exit(1)

# Now get page token
print("\n📝 Step 2: Getting Page Token...")

import requests

url = "https://graph.facebook.com/v18.0/me/accounts"
params = {'access_token': user_token}

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
            print()
        
        if len(pages) == 1:
            page = pages[0]
        else:
            choice = input(f"Select page (1-{len(pages)}): ").strip()
            try:
                page = pages[int(choice) - 1]
            except:
                print("❌ Invalid choice")
                exit(1)
        
        page_id = page['id']
        page_token = page['access_token']
        
        # Update .env
        print(f"\n📝 Updating .env...")
        
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            if line.startswith('FACEBOOK_PAGE_ID='):
                lines[i] = f'FACEBOOK_PAGE_ID={page_id}\n'
            elif line.startswith('FACEBOOK_PAGE_ACCESS_TOKEN='):
                lines[i] = f'FACEBOOK_PAGE_ACCESS_TOKEN={page_token}\n'
        
        with open('.env', 'w') as f:
            f.writelines(lines)
        
        print(f"\n✅ Updated!")
        print(f"   Page: {page['name']}")
        print(f"   ID: {page_id}")
        
        print(f"\n🎉 Now test:")
        print('   python facebook_auto_post.py "Test post!"')
        
    else:
        print(f"\n❌ Error: {data.get('error', {}).get('message', 'No pages found')}")

except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)
