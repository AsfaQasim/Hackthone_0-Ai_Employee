"""
LinkedIn Access Token Helper

Interactive script to obtain LinkedIn OAuth 2.0 access token.
Opens browser for authorization and displays the access token.

Requirements:
    pip install requests

Usage:
    python get_linkedin_token.py
"""

import requests
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import sys
import codecs

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Use ASCII-safe symbols
CHECK = "[OK]"
FAIL = "[FAIL]"
INFO = "[INFO]"

# ============================================================================
# CONFIGURATION - LinkedIn App credentials (from .env file)
# ============================================================================

CLIENT_ID = "77u2ifxk5f5tg7"
CLIENT_SECRET = "WPL_AP1.F4cbJvmXbbiY9jo5.FA6DNQ=="
REDIRECT_URI = "http://localhost:8080"

# Scopes for LinkedIn API access
# r_liteprofile: Basic profile (name, photo)
# r_emailaddress: Email address
# w_member_social: Post and manage content
SCOPES = "r_liteprofile r_emailaddress w_member_social"

# ============================================================================


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback"""
    
    access_token = None
    error = None
    
    def do_GET(self):
        """Handle OAuth callback"""
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get("code", [None])[0]
        error = query_components.get("error", [None])[0]
        
        if error:
            self.error = error
            print(f"\nAuthorization Error: {error}")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authorization Failed</h1>"
                b"<p>Error: " + error.encode() + b"</p>"
                b"<p>You can close this window.</p></body></html>"
            )
            return
        
        if code:
            print("\nExchanging authorization code for access token...")
            
            # Exchange code for access token
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
                self.access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 5184000)
                
                print("\n" + "="*70)
                print("SUCCESS! Your LinkedIn Access Token:")
                print("="*70)
                print(f"\n{self.access_token}\n")
                print("="*70)
                print(f"\nToken expires in: {expires_in // 86400} days")
                print("\nNext Steps:")
                print("   1. Copy the token above")
                print("   2. Set environment variable:")
                print(f"      set LINKEDIN_ACCESS_TOKEN={self.access_token}")
                print("   3. Test authentication:")
                print("      python Skills/linkedin_watcher.py auth")
                print("="*70)
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                success_html = f"""
                <html>
                <body style="font-family: Arial; padding: 40px; text-align: center;">
                    <h1 style="color: #0077b5;">✅ Authorization Complete!</h1>
                    <p>Your access token has been displayed in the terminal.</p>
                    <p>You can close this window.</p>
                </body>
                </html>
                """
                self.wfile.write(success_html.encode())
            else:
                error_msg = f"Token exchange failed: {response.text}"
                print(f"\n❌ {error_msg}")
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    f"<html><body><h1>Error</h1><p>{error_msg}</p></body></html>".encode()
                )
        else:
            print("\n❌ No authorization code received")
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Error</h1><p>No authorization code received.</p></body></html>"
            )
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def open_authorization_url():
    """Open LinkedIn authorization URL in browser"""
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    )
    
    print("\n" + "="*70)
    print("LinkedIn Access Token Helper")
    print("="*70)
    print("\nInstructions:")
    print("   1. A browser window will open with LinkedIn authorization page")
    print("   2. Sign in to LinkedIn (if not already)")
    print("   3. Click 'Allow' to authorize the application")
    print("   4. The access token will be displayed in this terminal")
    print("\nNOTE: Make sure you have configured CLIENT_ID and CLIENT_SECRET above!")
    print("="*70)
    
    input("\nPress Enter to open LinkedIn authorization page...")
    
    print("\nOpening authorization page...")
    webbrowser.open(auth_url)


def start_callback_server():
    """Start HTTP server to receive OAuth callback"""
    server = HTTPServer(("localhost", 8080), CallbackHandler)
    print(f"🔄 Waiting for authorization callback on {REDIRECT_URI}...")
    server.handle_request()
    return CallbackHandler.access_token is not None


def main():
    """Main function"""
    # Check if credentials are configured
    if CLIENT_ID == "YOUR_CLIENT_ID_HERE" or CLIENT_SECRET == "YOUR_CLIENT_SECRET_HERE":
        print("\n" + "="*70)
        print("ERROR: LinkedIn API credentials not configured!")
        print("="*70)
        print("\nYou need to:")
        print("   1. Create a LinkedIn App at: https://www.linkedin.com/developers/")
        print("   2. Get your Client ID and Client Secret")
        print("   3. Edit this file and replace:")
        print("      - CLIENT_ID = 'your_client_id'")
        print("      - CLIENT_SECRET = 'your_client_secret'")
        print("="*70)
        sys.exit(1)
    
    try:
        # Open authorization URL
        open_authorization_url()
        
        # Start callback server
        success = start_callback_server()
        
        if success:
            print("\nToken retrieval complete!")
        else:
            print("\nToken retrieval failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
