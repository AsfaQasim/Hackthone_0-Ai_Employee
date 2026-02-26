"""
Gmail Re-Authentication Script

Gets new Gmail API credentials when refresh token expires.
"""

import os
import sys
from pathlib import Path

# Add Skills to path
sys.path.insert(0, str(Path(__file__).parent / "Skills"))

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]

def main():
    print("="*70)
    print("GMAIL RE-AUTHENTICATION")
    print("="*70)
    print()
    
    # Check for credentials file
    creds_path = Path("config/gmail-credentials.json")
    token_path = Path("config/gmail-token.json")
    
    if not creds_path.exists():
        print("[ERROR] Credentials file not found: config/gmail-credentials.json")
        print()
        print("To get credentials:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create/select project")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Download credentials.json")
        print("6. Save as: config/gmail-credentials.json")
        print("="*70)
        sys.exit(1)
    
    print("Starting Gmail OAuth flow...")
    print()
    print("STEP 1: Browser will open")
    print("STEP 2: Sign in to Gmail")
    print("STEP 3: Allow access")
    print("STEP 4: Token will be saved automatically")
    print()
    print("Press Enter to continue...")
    input()
    
    try:
        # Start OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(
            str(creds_path),
            SCOPES
        )
        
        creds = flow.run_local_server(port=0)
        
        # Save token
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        
        print()
        print("="*70)
        print("[OK] Gmail authentication successful!")
        print("="*70)
        print()
        print("Token saved to: config/gmail-token.json")
        print()
        print("You can now run:")
        print("   python Skills/gmail_watcher.py poll")
        print("="*70)
        
        # Update .env if needed
        print("\nGmail Watcher is ready!")
        
    except Exception as e:
        print()
        print(f"[ERROR] Authentication failed: {e}")
        print()
        print("Make sure:")
        print("1. Credentials file exists")
        print("2. Gmail API is enabled")
        print("3. You have internet connection")
        sys.exit(1)

if __name__ == "__main__":
    main()
