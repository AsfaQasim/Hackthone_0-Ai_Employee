"""
LinkedIn API - Real Auto-Post

Actually posts to LinkedIn API using your credentials.
"""

import requests
import sys
import codecs
from pathlib import Path
from datetime import datetime

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Your LinkedIn credentials from .env
CLIENT_ID = "77u2ifxk5f5tg7"
CLIENT_SECRET = "WPL_AP1.F4cbJvmXbbiY9jo5.FA6DNQ=="

# You need to get an access token first
# This script helps you post using the LinkedIn API

def get_access_token_manual():
    """
    Get access token - requires OAuth flow.
    For now, you need to manually get this from LinkedIn Developer Portal.
    """
    print("="*70)
    print("LINKEDIN API ACCESS")
    print("="*70)
    print()
    print("To post directly to LinkedIn API, you need an access token.")
    print()
    print("Steps:")
    print("1. Go to: https://www.linkedin.com/developers/apps/")
    print("2. Select your app")
    print("3. Go to 'Auth' tab")
    print("4. Generate access token")
    print("5. Copy the token")
    print("6. Add to .env file: LINKEDIN_ACCESS_TOKEN=your_token")
    print()
    print("="*70)

def post_to_linkedin_api(access_token, content):
    """
    Post content directly to LinkedIn using API.
    
    Args:
        access_token: LinkedIn API access token
        content: Post content
    """
    print(f"\nPosting to LinkedIn API...")
    print(f"Content: {content[:100]}...")
    
    # LinkedIn API endpoint for posts
    # Note: This requires person URN which needs API approval
    api_url = "https://api.linkedin.com/v2/shares"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    # Post data
    data = {
        "text": content,
        "visibility": "PUBLIC",
        "distribute": True
    }
    
    try:
        response = requests.post(api_url, json=data, headers=headers)
        
        if response.status_code == 201:
            result = response.json()
            print("\n[OK] Successfully posted to LinkedIn!")
            print(f"Post ID: {result.get('id', 'N/A')}")
            return True
        else:
            print(f"\n[FAIL] Failed to post: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("="*70)
        print("LINKEDIN API AUTO-POST")
        print("="*70)
        print()
        print("Usage: python linkedin_real_post.py \"Your post content\"")
        print()
        print("Note: Requires LINKEDIN_ACCESS_TOKEN in .env file")
        print("="*70)
        sys.exit(1)
    
    # Check for access token
    access_token = None
    env_file = Path(".env")
    
    if env_file.exists():
        env_content = env_file.read_text()
        for line in env_content.split('\n'):
            if line.startswith('LINKEDIN_ACCESS_TOKEN='):
                access_token = line.split('=')[1].strip()
                break
    
    if not access_token:
        print("\n[ERROR] LINKEDIN_ACCESS_TOKEN not found in .env file!")
        print()
        get_access_token_manual()
        sys.exit(1)
    
    # Get content
    content = sys.argv[1]
    
    # Post to LinkedIn
    success = post_to_linkedin_api(access_token, content)
    
    if success:
        print("\n[OK] Posted to LinkedIn successfully!")
    else:
        print("\n[FAIL] Could not post to LinkedIn")
        print()
        print("Alternative: Use the copy-paste method:")
        print("   linkedin_post.bat \"Your topic\"")

if __name__ == "__main__":
    main()
