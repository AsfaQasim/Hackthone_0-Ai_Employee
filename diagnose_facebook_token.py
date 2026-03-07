#!/usr/bin/env python3
"""
Diagnose Facebook Token

Check what type of token you have and what permissions it has.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("\n" + "=" * 70)
print("  FACEBOOK TOKEN DIAGNOSIS")
print("=" * 70)

page_id = os.getenv('FACEBOOK_PAGE_ID')
token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

print(f"\n📋 Configuration:")
print(f"   Page ID: {page_id}")
print(f"   Token: {token[:30] if token else 'NOT SET'}...")

if not token:
    print("\n❌ No token found in .env")
    exit(1)

# Check token info
print("\n🔍 Checking token type and permissions...")

url = "https://graph.facebook.com/v18.0/debug_token"
params = {
    'input_token': token,
    'access_token': token
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' in data:
        token_data = data['data']
        
        print(f"\n📊 Token Information:")
        print(f"   Type: {token_data.get('type', 'Unknown')}")
        print(f"   App ID: {token_data.get('app_id', 'Unknown')}")
        print(f"   Valid: {token_data.get('is_valid', False)}")
        print(f"   Expires: {token_data.get('expires_at', 'Never')}")
        
        # Check permissions
        scopes = token_data.get('scopes', [])
        print(f"\n🔐 Permissions ({len(scopes)}):")
        
        required = ['pages_manage_posts', 'pages_read_engagement']
        for perm in required:
            has_it = perm in scopes
            status = "✅" if has_it else "❌"
            print(f"   {status} {perm}")
        
        # Show all permissions
        if scopes:
            print(f"\n📝 All permissions:")
            for scope in scopes:
                print(f"   - {scope}")
        
        # Check if it's a page token
        token_type = token_data.get('type', '').lower()
        
        if token_type == 'user':
            print("\n⚠️  WARNING: This is a USER token!")
            print("   You need a PAGE token to post to your page.")
            print("\n💡 How to get PAGE token:")
            print("   1. Go to Graph API Explorer")
            print("   2. Use your current token")
            print("   3. Change endpoint to: me/accounts")
            print("   4. Click Submit")
            print("   5. Copy the 'access_token' from the response")
            print("   6. That's your PAGE token!")
        elif token_type == 'page':
            print("\n✅ This is a PAGE token (correct!)")
            
            # Check if we have required permissions
            has_all = all(perm in scopes for perm in required)
            
            if has_all:
                print("✅ Has all required permissions")
                print("\n🤔 If posting still fails, check:")
                print("   1. Are you an ADMIN of the page?")
                print("   2. Is the page published (not in draft)?")
                print("   3. Try posting directly on Facebook to verify")
            else:
                print("❌ Missing required permissions")
                print("\n💡 Generate a new token with:")
                print("   - pages_manage_posts")
                print("   - pages_read_engagement")
    
    else:
        print(f"\n❌ Error: {data.get('error', {}).get('message', 'Unknown error')}")

except Exception as e:
    print(f"\n❌ Error: {e}")

# Try to get page info
print("\n" + "=" * 70)
print("  CHECKING PAGE ACCESS")
print("=" * 70)

url = f"https://graph.facebook.com/v18.0/{page_id}"
params = {
    'fields': 'id,name,access_token',
    'access_token': token
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'name' in data:
        print(f"\n✅ Can access page: {data['name']}")
        print(f"   Page ID: {data['id']}")
    else:
        print(f"\n❌ Cannot access page")
        print(f"   Error: {data.get('error', {}).get('message', 'Unknown')}")

except Exception as e:
    print(f"\n❌ Error: {e}")

# Try to get page roles
print("\n" + "=" * 70)
print("  CHECKING YOUR ROLE ON PAGE")
print("=" * 70)

url = f"https://graph.facebook.com/v18.0/me/accounts"
params = {
    'access_token': token
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' in data:
        pages = data['data']
        
        if pages:
            print(f"\n📄 Pages you manage ({len(pages)}):")
            for page in pages:
                is_target = page['id'] == page_id
                marker = "👉" if is_target else "  "
                print(f"{marker} {page['name']} (ID: {page['id']})")
                
                if is_target:
                    tasks = page.get('tasks', [])
                    print(f"   Your roles: {', '.join(tasks)}")
                    
                    if 'CREATE_CONTENT' in tasks or 'MANAGE' in tasks:
                        print("   ✅ You have permission to post")
                    else:
                        print("   ❌ You don't have permission to post")
                        print("   💡 You need to be an ADMIN or have CREATE_CONTENT role")
        else:
            print("\n❌ No pages found")
            print("   This means you're using a USER token, not a PAGE token")
    else:
        print(f"\n❌ Error: {data.get('error', {}).get('message', 'Unknown')}")

except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)
print("\n💡 RECOMMENDATION:")

print("\nIf you see 'USER token' above:")
print("   → You need to get the PAGE token from /me/accounts")
print("\nIf you see 'Missing permissions':")
print("   → Generate new token with both permissions")
print("\nIf you see 'No permission to post':")
print("   → Make sure you're an ADMIN of the Facebook page")

print("\n" + "=" * 70)
