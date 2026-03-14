#!/usr/bin/env python3
"""
Facebook Token Generator - Silver Tier

This script helps you generate a new Facebook Page Access Token
with the correct permissions for posting.
"""

import os
import webbrowser
from dotenv import load_dotenv

load_dotenv()

print("\n" + "=" * 70)
print("  FACEBOOK TOKEN GENERATOR - SILVER TIER")
print("=" * 70)

print("\n📋 CURRENT STATUS:")
print(f"   FACEBOOK_APP_ID: {os.getenv('FACEBOOK_APP_ID', 'Not set')}")
print(f"   FACEBOOK_PAGE_ID: {os.getenv('FACEBOOK_PAGE_ID', 'Not set')}")

print("\n" + "=" * 70)
print("  STEP-BY-STEP GUIDE TO GET CORRECT TOKEN")
print("=" * 70)

print("""
🔧 You need a token with these permissions:
   ✅ pages_manage_posts
   ✅ pages_read_engagement
   ✅ pages_show_list

📝 FOLLOW THESE STEPS:

STEP 1: Open Facebook Graph API Explorer
   → https://developers.facebook.com/tools/explorer/

STEP 2: Select Your App
   → Choose your app from the dropdown at the top
   → App ID: {app_id}

STEP 3: Get User Token
   → Click "Get Token" button
   → Select "Get User Token"
   → In permissions, check:
      ☑️ pages_manage_posts
      ☑️ pages_read_engagement
      ☑️ pages_show_list
   → Click "Generate Access Token"
   → You may need to login and grant permissions

STEP 4: Get Page Token
   → After getting User Token, change "Get Token" to:
   → Click "Get Token" > "Get Page Access Token"
   → Select your page from the list
   → This generates a PAGE access token (this is what you need!)

STEP 5: Verify Permissions
   → Click "Debug" button next to the token
   → Check that these permissions are listed:
      - pages_manage_posts
      - pages_read_engagement
   → If not, go back to Step 3

STEP 6: Copy the Page Access Token
   → Copy the FULL token string (it's long, starts with EAA...)

STEP 7: Update .env File
   → Open .env file in this directory
   → Find line: FACEBOOK_PAGE_ACCESS_TOKEN=...
   → Replace with your new token
   → Save the file

STEP 8: Test
   → Run: python verify_facebook_token.py
   → Then: python facebook_silver_poster.py "Test post"

─────────────────────────────────────────────────────────────────────

🚀 QUICK LINK: Open Graph API Explorer Now?
   → https://developers.facebook.com/tools/explorer/?appid={app_id}

─────────────────────────────────────────────────────────────────────

⚠️  COMMON ISSUES:

Issue: "Pages you manage" list is empty
Fix: Make sure you're admin of at least one Facebook Page

Issue: Token expires quickly
Fix: You need a long-lived token. See Step 9 below.

Issue: Still getting permission error
Fix: Make sure you're using PAGE token, not USER token

─────────────────────────────────────────────────────────────────────

STEP 9 (Optional): Get Long-Lived Token (60 days)
   → Go to: https://developers.facebook.com/tools/debug/access_token/
   → Click "Debug" on your token
   → Click "Extend Access Token"
   → This gives you a 60-day token instead of 1-hour token
   → Copy the new token and update .env

─────────────────────────────────────────────────────────────────────
""")

# Offer to open browser
app_id = os.getenv('FACEBOOK_APP_ID', '1423095195415885')
explorer_url = f"https://developers.facebook.com/tools/explorer/?appid={app_id}"

print(f"\n🌐 Want to open Graph API Explorer in browser?")
print(f"   URL: {explorer_url}")

response = input("\nOpen browser now? (y/n): ").strip().lower()
if response == 'y':
    webbrowser.open(explorer_url)
    print("\n✅ Browser opened! Follow the steps above.")
else:
    print("\n💡 You can open it manually:")
    print(f"   {explorer_url}")

print("\n" + "=" * 70)
print("  AFTER YOU UPDATE THE TOKEN:")
print("=" * 70)
print("""
1. Run: python verify_facebook_token.py
   → Should show: ✅ TOKEN IS VALID!

2. Run: python facebook_silver_poster.py "Test post"
   → Should show: ✅ SUCCESS!

3. Check your Facebook page to see the post!

─────────────────────────────────────────────────────────────────────

📁 Files for reference:
   - verify_facebook_token.py - Test your token
   - facebook_silver_poster.py - Post to Facebook
   - test_facebook_silver_tier.py - Full test suite

─────────────────────────────────────────────────────────────────────
""")

print("\n" + "=" * 70)
print("  Need help? Check SILVER_TIER_FACEBOOK_QUICKSTART.md")
print("=" * 70 + "\n")
