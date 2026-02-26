"""
LinkedIn Access Token - Exchange Code for Token

Usage:
    1. Get authorization code from browser URL
    2. Run: python linkedin_exchange_code.py YOUR_CODE_HERE
"""

import requests
import sys

# Your LinkedIn App credentials
CLIENT_ID = "77u2ifxk5f5tg7"
CLIENT_SECRET = "WPL_AP1.F4cbJvmXbbiY9jo5.FA6DNQ=="
REDIRECT_URI = "http://localhost:8080"

if len(sys.argv) < 2:
    print("="*70)
    print("LinkedIn Access Token - Exchange Code for Token")
    print("="*70)
    print("\nUsage:")
    print("   python linkedin_exchange_code.py YOUR_AUTHORIZATION_CODE")
    print("\nWhere to get the code:")
    print("   1. Open LinkedIn authorization page (should already be open)")
    print("   2. Sign in and authorize the app")
    print("   3. Copy the 'code' parameter from the redirect URL")
    print("   4. Run this script with the code")
    print("\nExample:")
    print("   python linkedin_exchange_code.py ABC123456789...")
    print("="*70)
    sys.exit(1)

authorization_code = sys.argv[1]

print("\nExchanging authorization code for access token...")
print(f"Code: {authorization_code[:20]}...")

response = requests.post(
    "https://www.linkedin.com/oauth/v2/accessToken",
    data={
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get("access_token")
    expires_in = token_data.get("expires_in", 5184000)
    
    print("\n" + "="*70)
    print("SUCCESS! Your LinkedIn Access Token:")
    print("="*70)
    print(f"\n{access_token}\n")
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
    print(f"\nError: {response.status_code}")
    print(f"Response: {response.text}")
