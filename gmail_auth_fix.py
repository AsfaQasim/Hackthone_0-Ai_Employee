#!/usr/bin/env python3
"""
Gmail Authentication Fix
Solves the "browser opens but nothing happens" issue
"""

import os
import sys
from pathlib import Path
import webbrowser

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("❌ Missing packages!")
    print("Run: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

def main():
    print("🔐 Gmail Authentication Fix")
    print("=" * 60)
    
    creds_path = Path("config/gmail-credentials.json")
    token_path = Path("config/gmail-token.json")
    
    # Check credentials
    if not creds_path.exists():
        print(f"\n❌ Credentials not found: {creds_path}")
        print("\nGet credentials from:")
        print("https://console.cloud.google.com/apis/credentials")
        return
    
    print(f"✅ Found credentials: {creds_path}")
    
    # Delete old token if exists
    if token_path.exists():
        print(f"⚠️  Deleting old token: {token_path}")
        token_path.unlink()
    
    print("\n" + "=" * 60)
    print("AUTHENTICATION STEPS:")
    print("=" * 60)
    print("1. Browser will open automatically")
    print("2. Select your Google account")
    print("3. Click 'Continue' (ignore 'unverified app' warning)")
    print("4. Click 'Allow' to grant permissions")
    print("5. Wait for 'Authentication successful' message")
    print("=" * 60)
    print("\nPress Enter to start...")
    input()
    
    try:
        # Create flow
        flow = InstalledAppFlow.from_client_secrets_file(
            str(creds_path),
            SCOPES
        )
        
        print("\n🌐 Opening browser for authentication...")
        print("(If browser doesn't open, copy the URL shown below)")
        
        # Run OAuth flow with better settings
        creds = flow.run_local_server(
            port=8080,  # Fixed port
            success_message='✅ Authentication successful! You can close this window now.',
            open_browser=True,
            authorization_prompt_message='Opening browser for authentication...\n'
        )
        
        # Save token
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
        
        print(f"\n✅ Token saved: {token_path}")
        
        # Test API
        print("\n🧪 Testing Gmail API...")
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        
        print("\n" + "=" * 60)
        print("✅ AUTHENTICATION SUCCESSFUL!")
        print("=" * 60)
        print(f"📧 Email: {profile.get('emailAddress')}")
        print(f"📊 Total messages: {profile.get('messagesTotal')}")
        
        # Check unread
        unread = service.users().messages().list(
            userId='me',
            q='is:unread in:inbox',
            maxResults=10
        ).execute()
        
        unread_count = len(unread.get('messages', []))
        print(f"📬 Unread messages: {unread_count}")
        
        print("\n✅ Gmail Watcher is ready to use!")
        print("\nNext step:")
        print("  python Skills/gmail_watcher.py poll")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Authentication cancelled by user")
        
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if Gmail API is enabled in Google Cloud Console")
        print("2. Verify OAuth consent screen is configured")
        print("3. Make sure you're using the correct Google account")
        print("4. Try a different browser")
        print("\nFor detailed guide, see: GMAIL_AUTH_GUIDE.md")

if __name__ == "__main__":
    main()
