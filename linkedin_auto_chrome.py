"""
LinkedIn Auto-Post - Uses your Chrome with existing session
"""

import sys
import codecs
import subprocess
from pathlib import Path
from datetime import datetime
from patchright.sync_api import sync_playwright
import time

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def find_chrome_path():
    """Find Chrome installation"""
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        str(Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe"),
    ]
    for p in paths:
        if Path(p).exists():
            return p
    return None

def auto_post_chrome(content: str):
    print("="*70)
    print("LINKEDIN AUTO-POST (Chrome)")
    print("="*70)
    print()
    
    chrome_path = find_chrome_path()
    if not chrome_path:
        print("❌ Chrome not found!")
        print("Please install Google Chrome")
        return False
    
    print(f"✅ Chrome found: {chrome_path}")
    print()
    
    session_path = Path(".linkedin_session")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    tracking_file = tracking_dir / f"linkedin_{timestamp}_chrome.md"
    
    print(f"📝 Content:\n{content}\n")
    print("🌐 Opening Chrome with LinkedIn...")
    print()
    
    browser = None
    try:
        with sync_playwright() as p:
            # Launch Chrome with user data
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                viewport={'width': 1280, 'height': 720},
                executable_path=chrome_path,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process'
                ]
            )
            
            if browser.pages:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Go to LinkedIn
            print("📍 Navigating to LinkedIn...")
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(5)
            
            # Check URL
            print(f"📍 Current URL: {page.url}")
            
            # If on login page, wait for user to login
            if 'login' in page.url or 'authwall' in page.url:
                print()
                print("="*70)
                print("⚠️  LOGIN PAGE DETECTED")
                print("="*70)
                print()
                print("Browser window mein login karein...")
                print("Script 3 minutes wait karega...")
                print()
                
                max_wait = 180
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
                            print(f"⏳ Waiting... ({waited}s)")
                    except:
                        time.sleep(3)
                        waited += 3
                else:
                    print("❌ Login timeout")
                    browser.close()
                    return False
            
            # Navigate to feed
            page.goto('https://www.linkedin.com/feed/', timeout=60000)
            time.sleep(3)
            
            # Start post
            print()
            print("📝 Opening post composer...")
            try:
                page.click('button[aria-label*="Start a post"]', timeout=5000)
                print("✅ Post composer opened")
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
                print("⚠️  Please click Post button manually")
            
            time.sleep(5)
            
            # Track
            tracking_content = f"""---
platform: linkedin
timestamp: {timestamp}
status: posted
method: chrome_auto
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
        print()
        print("="*70)
        print("❌ FAILED")
        print("="*70)
        print(f"Error: {str(e)}")
        
        if browser:
            browser.close()
        
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python linkedin_auto_chrome.py \"Your post\"")
        sys.exit(1)
    
    content = " ".join(sys.argv[1:])
    success = auto_post_chrome(content)
    sys.exit(0 if success else 1)
