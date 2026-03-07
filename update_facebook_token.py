#!/usr/bin/env python3
"""
Update Facebook Token

Simple script to update your Facebook token in .env file.
"""

import os
from pathlib import Path

print("\n" + "=" * 70)
print("  UPDATE FACEBOOK TOKEN")
print("=" * 70)

print("\n📝 Instructions:")
print("1. Go to Graph API Explorer")
print("2. Make sure you have these permissions:")
print("   - pages_manage_posts ✅")
print("   - pages_read_engagement ✅")
print("3. Click 'Generate Access Token'")
print("4. Change endpoint to: me/accounts")
print("5. Click Submit")
print("6. Copy the 'access_token' from the response")
print("\n" + "=" * 70)

new_token = input("\n🔑 Paste your NEW page token here: ").strip()

if not new_token:
    print("\n❌ No token provided")
    exit(1)

if not new_token.startswith('EAA'):
    print("\n⚠️  Warning: Token should start with 'EAA'")
    confirm = input("Continue anyway? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        exit(1)

print(f"\n📝 Token preview: {new_token[:30]}...")

# Read .env file
env_path = Path('.env')

if not env_path.exists():
    print("\n❌ .env file not found")
    exit(1)

with open(env_path, 'r') as f:
    lines = f.readlines()

# Update token
updated = False
for i, line in enumerate(lines):
    if line.startswith('FACEBOOK_PAGE_ACCESS_TOKEN='):
        lines[i] = f'FACEBOOK_PAGE_ACCESS_TOKEN={new_token}\n'
        updated = True
        break

if not updated:
    print("\n❌ FACEBOOK_PAGE_ACCESS_TOKEN not found in .env")
    print("   Adding it now...")
    # Add after FACEBOOK_PAGE_ID
    for i, line in enumerate(lines):
        if line.startswith('FACEBOOK_PAGE_ID='):
            lines.insert(i + 1, f'FACEBOOK_PAGE_ACCESS_TOKEN={new_token}\n')
            updated = True
            break

if updated:
    # Write back
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print("\n✅ Token updated successfully!")
    print("\n🎉 Now test it:")
    print('   python facebook_auto_post.py "Test post with new token"')
else:
    print("\n❌ Failed to update token")

print("\n" + "=" * 70)
