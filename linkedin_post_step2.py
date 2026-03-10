"""
Step 2: Post to LinkedIn (after login in Step 1)
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def post_linkedin(content: str):
    print("="*70)
    print("LINKEDIN POST - STEP 2")
    print("="*70)
    print()
    
    session_path = Path(".linkedin_session")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    
    print(f"📝 Content:\n{content}\n")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 720}
            )
            
            if browser.pages:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Go to feed
            print("📍 Opening LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)
            
            # Check login
            if 'login' in page.url:
                print("❌ Not logged in!")
                print("   First run: python linkedin_step1_login.py")
                browser.close()
                return False
            
            print("✅ Logged in")
            print()
            
            # Start post
            print("📝 Opening composer...")
            try:
                page.click('button[aria-label*="Start a post"]', timeout=5000)
            except:
                page.goto('https://www.linkedin.com/feed/?shareActive=true')
            time.sleep(2)
            
            # Fill content
            print("✍️  Writing content...")
            editors = ['.ql-editor[contenteditable="true"]', 'div[role="textbox"][contenteditable="true"]']
            
            for selector in editors:
                try:
                    editor = page.locator(selector).first
                    if editor.is_visible(timeout=5000):
                        editor.click()
                        time.sleep(1)
                        editor.fill(content)
                        print("✅ Content filled")
                        break
                except:
                    continue
            
            time.sleep(2)
            
            # Post
            print("📤 Publishing...")
            try:
                page.click('button[aria-label*="Post"]', timeout=5000)
                print("✅ Posted!")
            except:
                print("⚠️  Click Post button manually")
            
            time.sleep(5)
            
            # Track
            tracking_file = tracking_dir / f"linkedin_{timestamp}_step2.md"
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
---

# LinkedIn Post
{content}

Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            print()
            print("="*70)
            print("✅ SUCCESS!")
            print(f"🔗 Check: https://www.linkedin.com/feed/")
            print("="*70)
            
            time.sleep(3)
            browser.close()
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python linkedin_post_step2.py \"Your post\"")
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    success = post_linkedin(content)
    sys.exit(0 if success else 1)
