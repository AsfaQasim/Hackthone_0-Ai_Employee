"""
Step 1: Open LinkedIn and Login
Just opens browser, you login, keep it open
"""

import sys
import codecs
from pathlib import Path
from patchright.sync_api import sync_playwright
import time

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def login_linkedin():
    print("="*70)
    print("LINKEDIN LOGIN - STEP 1")
    print("="*70)
    print()
    print("📌 INSTRUCTIONS:")
    print("   1. Browser will open")
    print("   2. Login to LinkedIn")
    print("   3. DON'T close the browser")
    print("   4. Run Step 2 to post")
    print()
    
    session_path = Path(".linkedin_session")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 720}
            )
            
            if not browser.pages:
                browser.new_page()
            
            page = browser.pages[0]
            page.goto('https://www.linkedin.com/login', timeout=60000)
            
            print("✅ Browser opened: https://www.linkedin.com/login")
            print()
            print("👉 Login now in the browser window...")
            print()
            print("⏹️  KEEP BROWSER OPEN")
            print("   When ready to post, run:")
            print("   python linkedin_post_step2.py \"Your post content\"")
            print()
            print("="*70)
            
            # Keep running - don't close browser
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nBrowser closed.")
                browser.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    login_linkedin()
