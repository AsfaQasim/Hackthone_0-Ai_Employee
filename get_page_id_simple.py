#!/usr/bin/env python3
"""
Simple script to get Facebook Page ID
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

if not token:
    print("❌ No token found in .env")
    exit(1)

print("🔍 Getting your Facebook Page ID...\n")

# Try to get page info
url = "https://graph.facebook.com/v18.0/me"
params = {'access_token': token, 'fields': 'id,name'}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'id' in data:
        page_id = data['id']
        page_name = data.get('name', 'Unknown')
        
        print(f"✅ Found your page!")
        print(f"\n📄 Page Name: {page_name}")
        print(f"📄 Page ID: {page_id}")
        
        print(f"\n📝 Copy this line to your .env file:")
        print(f"\nFACEBOOK_PAGE_ID={page_id}")
        
        # Ask to update
        update = input("\n❓ Update .env automatically? (y/n): ").strip().lower()
        
        if update == 'y':
            # Read .env
            with open('.env', 'r') as f:
                content = f.read()
            
            # Replace or add
            if 'FACEBOOK_PAGE_ID=' in content:
                # Replace existing
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('FACEBOOK_PAGE_ID='):
                        lines[i] = f'FACEBOOK_PAGE_ID={page_id}'
                content = '\n'.join(lines)
            else:
                # Add new line after FACEBOOK_APP_SECRET
                content = content.replace(
                    'FACEBOOK_APP_SECRET=',
                    f'FACEBOOK_APP_SECRET='
                )
                # Find the line and add after it
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'FACEBOOK_APP_SECRET=' in line:
                        lines.insert(i + 1, f'FACEBOOK_PAGE_ID={page_id}')
                        break
                content = '\n'.join(lines)
            
            # Write back
            with open('.env', 'w') as f:
                f.write(content)
            
            print(f"\n✅ Updated .env with FACEBOOK_PAGE_ID={page_id}")
            print("\n🎉 Done! Now run:")
            print("   python facebook_token_helper.py")
            print("   Choose option 3 to test")
        else:
            print("\n📝 Please manually add this to .env:")
            print(f"   FACEBOOK_PAGE_ID={page_id}")
    
    elif 'error' in data:
        print(f"❌ Error: {data['error'].get('message', 'Unknown error')}")
        print("\n💡 Your token might be expired or invalid.")
        print("\nTo get a new token:")
        print("1. Go to: https://developers.facebook.com/tools/explorer/")
        print("2. Select your app")
        print("3. Click 'Generate Access Token'")
        print("4. Add permissions: pages_manage_posts, pages_show_list")
        print("5. Change endpoint to: me/accounts")
        print("6. Click Submit")
        print("7. Copy the 'access_token' from response")
        print("8. Update FACEBOOK_PAGE_ACCESS_TOKEN in .env")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
