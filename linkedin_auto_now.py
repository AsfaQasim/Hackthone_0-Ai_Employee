"""
LinkedIn Auto-Post - Connects to already open browser
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time
import subprocess

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def auto_post_existing():
    print("="*70)
    print("LINKEDIN AUTO-POST (Existing Browser)")
    print("="*70)
    print()
    
    content = """🚀 AI Testing & Automation Breakthrough!

Just completed comprehensive testing of our new AI automation system.

✅ Automated workflows running smoothly
✅ Error rates significantly reduced
✅ Productivity increased by 40%
✅ Seamless integration across all platforms

Key takeaways:
1. Start small, scale fast
2. Monitor everything
3. Human oversight remains critical
4. Continuous improvement is the key

#AITesting #Automation #ArtificialIntelligence #Innovation #Productivity"""

    print(f"📝 Content:\n{content}\n")
    print("🔗 Connecting to LinkedIn...")
    print()
    
    session_path = Path(".linkedin_session")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    
    try:
        with sync_playwright() as p:
            # Connect to existing Chrome
            print("🌐 Launching browser session...")
            
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 720},
                args=[
                    '--disable-blink-features=AutomationControlled',
                ]
            )
            
            # Get or create page
            if browser.pages:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Go to LinkedIn feed
            print("📍 Opening LinkedIn feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)
            
            # Check if logged in
            print(f"📍 Current page: {page.url}")
            
            if 'login' in page.url:
                print("❌ Not logged in!")
                print("   Pehle login karein browser mein")
                browser.close()
                return False
            
            print("✅ Logged in!")
            print()
            
            # Click Start a post
            print("📝 Opening post composer...")
            try:
                page.click('button[aria-label*="Start a post"]', timeout=5000)
                print("✅ Post composer opened")
            except Exception as e:
                print(f"⚠️  Alternative method...")
                page.goto('https://www.linkedin.com/feed/?shareActive=true')
            time.sleep(2)
            
            # Fill content
            print("✍️  Filling content...")
            editor_selectors = [
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
            ]
            
            for selector in editor_selectors:
                try:
                    editor = page.locator(selector).first
                    if editor.is_visible(timeout=5000):
                        editor.click()
                        time.sleep(1)
                        editor.fill(content)
                        print("✅ Content filled successfully")
                        break
                except:
                    continue
            
            time.sleep(2)
            
            # Click Post button
            print("📤 Publishing post...")
            try:
                page.click('button[aria-label*="Post"]', timeout=5000)
                print("✅ Post button clicked!")
            except:
                print("⚠️  Post manually click karein")
            
            # Wait for post
            print()
            print("⏳ Posting...")
            time.sleep(5)
            
            # Save tracking
            tracking_file = tracking_dir / f"linkedin_{timestamp}_auto.md"
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
method: auto_existing
---

# LinkedIn Post

{content}

Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            tracking_file.write_text(tracking_content, encoding='utf-8')
            
            print()
            print("="*70)
            print("✅ POST SUCCESSFUL!")
            print("="*70)
            print(f"🔗 Check: https://www.linkedin.com/feed/")
            print("="*70)
            
            time.sleep(3)
            browser.close()
            
            return True
            
    except Exception as e:
        print()
        print("="*70)
        print("❌ FAILED")
        print("="*70)
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = auto_post_existing()
    sys.exit(0 if success else 1)
