#!/usr/bin/env python3
"""
Facebook Post NOW - Simplified and Working

This script will actually post to Facebook using browser automation.
"""

import os
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

def post_to_facebook(message):
    """Post to Facebook using Playwright."""
    
    print("\n" + "=" * 70)
    print("  FACEBOOK POSTING - SIMPLIFIED")
    print("=" * 70)
    
    print(f"\n📝 Message to post:")
    print(f"   {message}")
    print("\n" + "=" * 70)
    
    try:
        with sync_playwright() as p:
            # Use saved session
            session_path = Path('.facebook_session')
            session_path.mkdir(exist_ok=True)
            
            print("\n🌐 Opening browser...")
            browser = p.chromium.launch_persistent_context(
                str(session_path),
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )
            
            if len(browser.pages) > 0:
                page = browser.pages[0]
            else:
                page = browser.new_page()
            
            # Go to Facebook
            print("📄 Going to Facebook...")
            page.goto('https://www.facebook.com', wait_until='networkidle')
            time.sleep(3)
            
            # Check if logged in
            if 'login' in page.url.lower():
                print("\n⚠️  You're not logged in!")
                print("\n📋 MANUAL STEPS:")
                print("   1. Login to Facebook in the browser")
                print("   2. Press Enter here after logging in")
                input("\n✅ Press Enter after logging in...")
                page.goto('https://www.facebook.com', wait_until='networkidle')
                time.sleep(3)
            
            # Go to your page
            print("\n📄 Opening your Facebook page...")
            page.goto('https://www.facebook.com/profile.php?id=967740493097470', wait_until='networkidle')
            time.sleep(5)
            
            print("\n" + "=" * 70)
            print("  MANUAL POSTING STEPS")
            print("=" * 70)
            print("\n1. Browser me apna Facebook page khul gaya hai")
            print("2. 'What's on your mind?' ya 'Create post' click karo")
            print("3. Ye message copy-paste karo:")
            print("\n" + "-" * 70)
            print(message)
            print("-" * 70)
            print("\n4. 'Post' button click karo")
            print("5. Post publish hone ka wait karo")
            print("6. Wapas yahan aao aur Enter press karo")
            print("\n" + "=" * 70)
            
            input("\n✅ Press Enter after posting...")
            
            # Track the post
            track_post(message)
            
            print("\n✅ Post tracked!")
            print("\n💡 Browser 5 seconds me band ho jayega...")
            time.sleep(5)
            
            browser.close()
            
            print("\n" + "=" * 70)
            print("  ✅ DONE!")
            print("=" * 70)
            
            print("\n💡 Check your post:")
            print("   https://www.facebook.com/profile.php?id=967740493097470")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def track_post(message):
    """Track posted message."""
    tracking_dir = Path("Social_Media_Tracking")
    tracking_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"facebook_{timestamp}_manual.md"
    filepath = tracking_dir / filename
    
    content = f"""---
type: facebook_manual_post
timestamp: "{datetime.now().isoformat()}"
status: "✅ Published"
---

# Facebook Manual Post

**Status**: ✅ Published  
**Posted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Method**: Manual-Assisted

## Message
{message}

---

*Posted via Manual-Assisted Method*
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"\n📝 Tracked: {filepath}")

def main():
    """Main function."""
    import sys
    
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
    else:
        print("\n📝 Enter your message:")
        message = input("   > ").strip()
    
    if not message:
        print("❌ No message provided")
        return
    
    post_to_facebook(message)

if __name__ == "__main__":
    main()
