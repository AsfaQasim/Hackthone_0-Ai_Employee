#!/usr/bin/env python3
"""
Simple Gmail Authentication Script
Helps you authenticate Gmail API step by step
"""

import os
import sys
from pathlib import Path

# Check if google packages are installed
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("❌ Required packages not installed!")
    print("\nInstall with:")
    print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify']

def main():
    print("🔐 Gmail Authentication Setup")
    print("=" * 50)
    
    # Check credentials file
    creds_path = Path("config/gmail-credentials.json")
    token_path = Path("config/gmail-token.json")
    
    if not creds_path.exists():
        print("\n❌ Credentials file not found!")
        print(f"Expected location: {creds_path}")
        print("\nTo get credentials:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create a new project (or select existing)")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Download as 'gmail-credentials.json'")
        print(f"6. Save to: {creds_path}")
        return
    
    print(f"✅ Found credentials file: {creds_path}")
    
    # Check if already authenticated
    if token_path.exists():
        print(f"✅ Found existing token: {token_path}")
        print("\nTesting existing authentication...")
        
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            
            if creds and creds.valid:
                print("✅ Existing token is valid!")
                
                # Test API call
                service = build('gmail', 'v1', credentials=creds)
                profile = service.users().getProfile(userId='me').execute()
                
                print(f"\n📧 Authenticated as: {profile.get('emailAddress')}")
                print(f"📊 Total messages: {profile.get('messagesTotal')}")
                print("\n✅ Gmail authentication working!")
                return
            
            elif creds and creds.expired and creds.refresh_token:
                print("⚠️ Token expired, refreshing...")
                creds.refresh(Request())
                
                # Save refreshed token
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
                
                print("✅ Token refreshed successfully!")
                return
        
        except Exception as e:
            print(f"❌ Existing token invalid: {e}")
            print("Will create new token...")
    
    # Start OAuth flow
    print("\n🔄 Starting OAuth authentication...")
    print("\nSteps:")
    print("1. Browser will open automatically")
    print("2. Select your Google account")
    print("3. Click 'Allow' to grant permissions")
    print("4. Browser will show 'authentication successful'")
    print("\nPress Enter to continue...")
    input()
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(creds_path), 
            SCOPES
        )
        
        # Run local server for OAuth callback
        creds = flow.run_local_server(
            port=0,  # Use random available port
            success_message='Authentication successful! You can close this window.',
            open_browser=True
        )
        
        # Save token
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        
        print(f"\n✅ Token saved to: {token_path}")
        
        # Test API call
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        
        print(f"\n📧 Authenticated as: {profile.get('emailAddress')}")
        print(f"📊 Total messages: {profile.get('messagesTotal')}")
        print("\n✅ Gmail authentication complete!")
        
    except Exception as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure credentials file is correct")
        print("2. Check if Gmail API is enabled in Google Cloud Console")
        print("3. Verify OAuth consent screen is configured")
        print("4. Try using a different browser")

if __name__ == "__main__":
    main()
