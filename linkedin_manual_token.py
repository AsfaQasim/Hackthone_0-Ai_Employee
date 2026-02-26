"""
LinkedIn Access Token - Manual Method

This script generates an authorization URL for you to paste in your browser.
Then you paste the authorization code back here to get your access token.
"""

import requests
import sys

# Your LinkedIn App credentials (from .env)
CLIENT_ID = "77u2ifxk5f5tg7"
CLIENT_SECRET = "WPL_AP1.F4cbJvmXbbiY9jo5.FA6DNQ=="
REDIRECT_URI = "http://localhost:8080"
SCOPES = "r_liteprofile r_emailaddress w_member_social"

def print_header():
    print("="*70)
    print("LINKEDIN ACCESS TOKEN - MANUAL METHOD")
    print("="*70)
    print()

def generate_auth_url():
    """Generate the authorization URL"""
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    )
    return auth_url

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    print("\nExchanging code for access token...")
    
    response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token"), token_data.get("expires_in")
    else:
        return None, response.text

def main():
    print_header()
    
    # Check if code is provided
    if len(sys.argv) > 1:
        # Exchange code for token
        code = sys.argv[1]
        access_token, expires_in = exchange_code_for_token(code)
        
        if access_token:
            print("\n" + "="*70)
            print("SUCCESS! Your LinkedIn Access Token:")
            print("="*70)
            print()
            print(access_token)
            print()
            print("="*70)
            print(f"\nToken expires in: {expires_in // 86400} days")
            print("\nNext Steps:")
            print("   1. Copy the token above")
            print("   2. Set environment variable:")
            print(f"      set LINKEDIN_ACCESS_TOKEN={access_token}")
            print("   3. Test authentication:")
            print("      python Skills/linkedin_watcher.py auth")
            print("="*70)
        else:
            print(f"\nError: {expires_in}")
            print("\nPossible issues:")
            print("   - Invalid authorization code")
            print("   - Code has expired")
            print("   - Redirect URI mismatch")
    else:
        # Generate authorization URL
        auth_url = generate_auth_url()
        
        print("STEP 1: Copy this URL and paste in your browser:")
        print("-"*70)
        print(auth_url)
        print("-"*70)
        print()
        print("STEP 2: In your browser:")
        print("   1. Paste the URL above")
        print("   2. Sign in to LinkedIn")
        print("   3. Click 'Allow' to authorize")
        print("   4. You'll be redirected to localhost:8080")
        print("   5. Copy the 'code' parameter from the URL")
        print()
        print("STEP 3: Run this command with your code:")
        print(f"   python linkedin_manual_token.py YOUR_CODE_HERE")
        print()
        print("Example:")
        print("   python linkedin_manual_token.py AQEDAThisIsACode123...")
        print()
        print("="*70)
        
        # Also open browser automatically
        import webbrowser
        print("\nOpening authorization URL in your browser...")
        webbrowser.open(auth_url)

if __name__ == "__main__":
    main()
