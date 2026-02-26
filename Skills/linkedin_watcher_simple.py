"""
Simple LinkedIn Watcher using Playwright
Similar to WhatsApp watcher - uses browser automation
"""

import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

class LinkedInWatcherSimple:
    def __init__(self, vault_path: str, session_path: str):
        self.vault_path = Path(vault_path)
        self.session_path = Path(session_path)
        self.inbox = self.vault_path / 'Inbox'
        self.logger = logging.getLogger('LinkedInWatcher')
        
    def authenticate(self):
        """Open LinkedIn for manual login"""
        print("🔐 LinkedIn Authentication")
        print("=" * 50)
        print("Browser will open. Please login to LinkedIn.")
        print("After login, press Enter to continue...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False
            )
            page = browser.pages[0]
            page.goto('https://www.linkedin.com/login')
            
            input("\nPress Enter when logged in...")
            
            # Test if logged in
            page.goto('https://www.linkedin.com/feed/')
            time.sleep(2)
            
            if 'feed' in page.url:
                print("✅ Authentication successful!")
            else:
                print("❌ Authentication failed. Please try again.")
            
            browser.close()
    
    def check_notifications(self):
        """Check LinkedIn notifications"""
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                str(self.session_path),
                headless=True
            )
            page = browser.pages[0]
            
            try:
                page.goto('https://www.linkedin.com/notifications/', timeout=30000)
                page.wait_for_selector('[role="main"]', timeout=10000)
                
                # Get notifications
                notifications = page.query_selector_all('.notification-card')
                
                items = []
                for notif in notifications[:5]:
                    text = notif.inner_text()
                    items.append({
                        'text': text,
                        'timestamp': datetime.now().isoformat()
                    })
                
                browser.close()
                return items
            
            except Exception as e:
                self.logger.error(f"Error checking notifications: {e}")
                browser.close()
                return []
    
    def create_notification_file(self, notification):
        """Create markdown file for notification"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"linkedin_{timestamp}.md"
        filepath = self.inbox / filename
        
        content = f"""---
type: linkedin_notification
timestamp: {notification['timestamp']}
source: linkedin
status: pending
---

# LinkedIn Notification

{notification['text']}

---

## Action Items
- [ ] Review this notification
- [ ] Take appropriate action

---

*Processed by LinkedIn Watcher*
"""
        
        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Created: {filename}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple LinkedIn Watcher")
    parser.add_argument("command", choices=["auth", "poll"], help="Command")
    parser.add_argument("--vault", default=".", help="Vault path")
    parser.add_argument("--session", default=".linkedin_session", help="Session path")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    watcher = LinkedInWatcherSimple(args.vault, args.session)
    
    if args.command == "auth":
        watcher.authenticate()
    elif args.command == "poll":
        notifications = watcher.check_notifications()
        print(f"Found {len(notifications)} notifications")
        for notif in notifications:
            watcher.create_notification_file(notif)
