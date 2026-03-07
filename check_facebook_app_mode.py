#!/usr/bin/env python3
"""
Check Facebook App Mode

Checks if your app is in Development or Live mode.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('FACEBOOK_APP_ID', '1423095195415885')
APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')

print("\n" + "=" * 70)
print("  FACEBOOK APP MODE CHECK")
print("=" * 70)

print(f"\n📱 App ID: {APP_ID}")

if not APP_SECRET:
    print("\n⚠️  App Secret not found in .env")
    print("   Add it to check app mode")
    print("\n💡 Get it from:")
    print("   https://developers.facebook.com/apps/")
    print("   → Your App → Settings → Basic → App Secret")
    exit(1)

# Get app access token
url = "https://graph.facebook.com/oauth/access_token"
params = {
    'client_id': APP_ID,
    'client_secret': APP_SECRET,
    'grant_type': 'client_credentials'
}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'access_token' in data:
        app_token = data['access_token']
        
        # Get app info
        url = f"https://graph.facebook.com/v18.0/{APP_ID}"
        params = {
            'fields': 'name,link,category,is_app_secret_set,development_mode',
            'access_token': app_token
        }
        
        response = requests.get(url, params=params)
        app_data = response.json()
        
        print(f"\n📊 App Information:")
        print(f"   Name: {app_data.get('name', 'Unknown')}")
        print(f"   Category: {app_data.get('category', 'Unknown')}")
        
        # Check development mode
        dev_mode = app_data.get('development_mode')
        
        if dev_mode is None:
            print(f"\n⚠️  Cannot determine app mode")
            print(f"   This usually means app is in Development mode")
        elif dev_mode:
            print(f"\n❌ App Mode: DEVELOPMENT")
            print(f"\n💡 This is why posting is not working!")
            print(f"\n🔧 To fix:")
            print(f"   1. Go to: https://developers.facebook.com/apps/{APP_ID}/settings/basic/")
            print(f"   2. Find 'App Mode' section")
            print(f"   3. Click 'Switch to Live Mode'")
            print(f"   4. Add Privacy Policy URL if asked")
            print(f"   5. Generate new token")
        else:
            print(f"\n✅ App Mode: LIVE")
            print(f"\n   App is in Live mode, posting should work!")
            print(f"\n   If still not working, check:")
            print(f"   1. Token has pages_manage_posts permission")
            print(f"   2. You're admin of the page")
            print(f"   3. Page is published (not draft)")
        
    else:
        print(f"\n❌ Error: {data.get('error', {}).get('message', 'Unknown error')}")

except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)
print("\n📝 Quick Links:")
print(f"   App Dashboard: https://developers.facebook.com/apps/{APP_ID}/")
print(f"   App Settings: https://developers.facebook.com/apps/{APP_ID}/settings/basic/")
print(f"   Graph Explorer: https://developers.facebook.com/tools/explorer/")
print("\n" + "=" * 70)
