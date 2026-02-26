"""
Get LinkedIn Access Token - Simple Method

This will open your browser, you authorize, and get the token.
"""

import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import sys
import codecs

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Your credentials
CLIENT_ID = "77u2ifxk5f5tg7"
CLIENT_SECRET = "WPL_AP1.F4cbJvmXbbiY9jo5.FA6DNQ=="
REDIRECT_URI = "http://localhost:8080"
SCOPES = "r_liteprofile r_emailaddress w_member_social"

class CallbackHandler(BaseHTTPRequestHandler):
    access_token = None
    
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get("code", [None])[0]
        
        if code:
            print("\n[INFO] Exchanging code for access token...")
            
            # Exchange code for token
            response = requests.post(
                "https://www.linkedin.com/oauth/v2/accessToken",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 5184000)
                
                print("\n" + "="*70)
                print("SUCCESS! Your LinkedIn Access Token:")
                print("="*70)
                print()
                print(self.access_token)
                print()
                print("="*70)
                print(f"\nToken expires in: {expires_in // 86400} days")
                print("\nNEXT STEP:")
                print("Add this to your .env file:")
                print(f"LINKEDIN_ACCESS_TOKEN={self.access_token}")
                print("="*70)
                
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = """
                <html><body style="font-family:Arial; text-align:center; padding:50px;">
                <h1 style="color:#0077b5;">Success!</h1>
                <p>Your access token is shown in the terminal.</p>
                <p>Copy it and add to .env file.</p>
                <p>You can close this window.</p>
                </body></html>
                """
                self.wfile.write(html.encode())
            else:
                print(f"\n[ERROR] Failed: {response.status_code}")
                print(f"Response: {response.text}")
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Error</h1><p>Failed to get token</p></body></html>")
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Error</h1><p>No code received</p></body></html>")
    
    def log_message(self, format, *args):
        pass

def main():
    print("="*70)
    print("GET LINKEDIN ACCESS TOKEN")
    print("="*70)
    print()
    print("STEP 1: Browser will open")
    print("STEP 2: Sign in to LinkedIn and click Allow")
    print("STEP 3: Token will be shown here")
    print()
    print("Press Enter to continue...")
    input()
    
    # Open authorization URL
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&scope={SCOPES}"
    )
    
    print("\nOpening LinkedIn authorization...")
    webbrowser.open(auth_url)
    
    # Start callback server
    print("Waiting for authorization...")
    server = HTTPServer(("localhost", 8080), CallbackHandler)
    server.handle_request()
    
    print("\nDone!")

if __name__ == "__main__":
    main()
