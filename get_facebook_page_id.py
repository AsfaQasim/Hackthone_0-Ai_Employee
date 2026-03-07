#!/usr/bin/env python3
"""
Get Facebook Page ID

This script uses your current token to find your Page ID.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_page_id_from_token():
    """
    Try to get page ID from the current token.
    """
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    
    if not token:
        print("❌ FACEBOOK_PAGE_ACCESS_TOKEN not found in .env")
        return None
    
    print("🔍 Checking your token...")
    print(f"   Token starts with: {token[:20]}...")
    
    # Method 1: Try to get page info directly from token
    print("\n📡 Method 1: Getting page info from token...")
    
    url = "https://graph.facebook.com/v18.0/me"
    params = {
        'access_token': token,
        'fields': 'id,name,category'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            page_id = data.get('id')
            page_name = data.get('name', 'Unknown')
            category = data.get('category', 'Unknown')
            
            print(f"\n✅ Found your Facebook Page!")
            print(f"\n📄 Page Details:")
            print(f"   Name: {page_name}")
            print(f"   ID: {page_id}")
            print(f"   Category: {category}")
            
            print(f"\n📝 Add this to your .env file:")
            print(f"   FACEBOOK_PAGE_ID={page_id}")
            
            # Update .env file automatically
            update_env = input("\n❓ Do you want me to update .env automatically? (y/n): ").strip().lower()
            
            if update_env == 'y':
                update_env_file(page_id)
            
            return page_id
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"\n❌ Error: {error_msg}")
            
            if 'expired' in error_msg.lower():
                print("\n💡 Your token has expired. You need to:")
                print("   1. Go to Graph API Explorer")
                print("   2. Generate a new token")
                print("   3. Get page token from /me/accounts")
                print("   4. Update FACEBOOK_PAGE_ACCESS_TOKEN in .env")
            
            return None
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

def update_env_file(page_id):
    """
    Update .env file with the page ID.
    """
    try:
        # Read current .env
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update or add FACEBOOK_PAGE_ID
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('FACEBOOK_PAGE_ID='):
                lines[i] = f'FACEBOOK_PAGE_ID={page_id}\n'
                updated = True
                break
        
        if not updated:
            # Add after FACEBOOK_APP_SECRET
            for i, line in enumerate(lines):
                if line.startswith('FACEBOOK_APP_SECRET='):
                    lines.insert(i + 1, f'FACEBOOK_PAGE_ID={page_id}\n')
                    break
        
        # Write back
        with open('.env', 'w') as f:
            f.writelines(lines)
        
        print(f"\n✅ Updated .env file with FACEBOOK_PAGE_ID={page_id}")
        print("\n🎉 You're all set! Run the test again:")
        print("   python facebook_token_helper.py")
        
    except Exception as e:
        print(f"\n❌ Error updating .env: {e}")
        print(f"\n📝 Please manually add this line to .env:")
        print(f"   FACEBOOK_PAGE_ID={page_id}")

def main():
    print("\n" + "=" * 70)
    print("  GET FACEBOOK PAGE ID")
    print("=" * 70)
    
    page_id = get_page_id_from_token()
    
    if not page_id:
        print("\n" + "=" * 70)
        print("  ALTERNATIVE METHOD")
        print("=" * 70)
        print("\nIf the automatic method didn't work, try this:")
        print("\n1. Go to: https://developers.facebook.com/tools/explorer/")
        print("2. Make sure your token is in the 'Access Token' field")
        print("3. Change the endpoint to: me/accounts")
        print("4. Click Submit")
        print("5. Copy the 'id' from the response")
        print("6. Add to .env: FACEBOOK_PAGE_ID=<that_id>")
        
        print("\nOr run:")
        print("   python facebook_token_helper.py")
        print("   Choose option 1")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
