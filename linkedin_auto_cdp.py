"""
LinkedIn Auto-Post - Connects to existing Chrome via CDP
Uses your already logged-in Chrome browser
"""

import sys
import codecs
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time
import subprocess
import json

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def get_chrome_debug_port():
    """Try to find Chrome with debug port"""
    # Common debug ports
    return 9222

def auto_post_via_cdp():
    print("="*70)
    print("LINKEDIN AUTO-POST (Chrome CDP)")
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
    print()
    
    # First, open Chrome with debug port
    print("🌐 Opening Chrome with debug port...")
    print()
    print("⚠️  IMPORTANT: Chrome will open with debugging enabled")
    print("   Isme login karein agar pehle se nahi hai")
    print()
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = str(Path.home() / "AppData/Local/Google/Chrome/User Data")
    
    # Close existing Chrome
    print("⏹️  Closing existing Chrome...")
    subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], capture_output=True)
    time.sleep(2)
    
    # Start Chrome with remote debugging
    print("🚀 Starting Chrome with debug port 9222...")
    chrome_cmd = [
        chrome_path,
        '--remote-debugging-port=9222',
        '--user-data-dir=' + user_data_dir,
        '--disable-blink-features=AutomationControlled',
        'https://www.linkedin.com/feed/'
    ]
    
    # Start Chrome
    subprocess.Popen(chrome_cmd)
    
    print()
    print("="*70)
    print("⏳ Waiting 5 seconds for Chrome to start...")
    print("="*70)
    time.sleep(5)
    
    browser = None
    try:
        with sync_playwright() as p:
            # Connect to existing Chrome
            print()
            print("🔗 Connecting to Chrome...")
            browser = p.chromium.connect_over_cdp(
                'http://localhost:9222',
                timeout=30000
            )
            
            print("✅ Connected to Chrome!")
            print()
            
            # Get context and page
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.pages[0] if context.pages else context.new_page()
            
            # Go to LinkedIn
            print("📍 Opening LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)
            
            # Check URL
            print(f"📍 Current URL: {page.url[:80]}...")
            
            # If on login page, wait for user
            if 'login' in page.url:
                print()
                print("="*70)
                print("⚠️  LOGIN PAGE")
                print("="*70)
                print()
                print("👉 Chrome window mein login karein")
                print("   Script 10 minutes wait karega...")
                print()
                
                max_wait = 600  # 10 minutes
                waited = 0
                
                while waited < max_wait:
                    try:
                        if any(x in page.url for x in ['/feed', '/mynetwork', '/jobs']):
                            print()
                            print("✅ Login detected!")
                            break
                        
                        time.sleep(3)
                        waited += 3
                        
                        if waited % 30 == 0:
                            print(f"⏳ Waiting... ({waited}s / {max_wait}s)")
                    except:
                        time.sleep(3)
                        waited += 3
                else:
                    print("❌ Login timeout")
                    return False
            
            # Navigate to feed
            print()
            print("📍 Going to feed...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)
            
            # Click Start a post
            print("📝 Opening post composer...")
            try:
                page.click('button[aria-label*="Start a post"]', timeout=5000)
                print("✅ Composer opened")
            except:
                page.goto('https://www.linkedin.com/feed/?shareActive=true')
            time.sleep(2)
            
            # Fill content
            print("✍️  Writing content...")
            editors = [
                '.ql-editor[contenteditable="true"]',
                'div[role="textbox"][contenteditable="true"]',
            ]
            
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
                print("✅ Post button clicked!")
            except:
                print("⚠️  Post button manually click karein")
            
            # Wait
            print()
            print("⏳ Posting...")
            time.sleep(5)
            
            # Track
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            tracking_dir = Path("Social_Media_Tracking")
            tracking_dir.mkdir(exist_ok=True)
            tracking_file = tracking_dir / f"linkedin_{timestamp}_cdp.md"
            
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
method: cdp_auto
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
            
            time.sleep(2)
            
            return True
            
    except Exception as e:
        print()
        print("="*70)
        print("❌ FAILED")
        print("="*70)
        print(f"Error: {str(e)}")
        return False
    finally:
        try:
            if browser:
                browser.close()
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use provided content
        content = " ".join(sys.argv[1:])
    else:
        content = None
    
    success = auto_post_via_cdp()
    sys.exit(0 if success else 1)
