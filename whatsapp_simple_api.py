"""
WhatsApp Simple API - Python Only
Lightweight solution without Go
Uses selenium for better reliability than Playwright
"""

import time
from pathlib import Path
from datetime import datetime
import json
from typing import List, Dict, Optional

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.service import Service as ChromeService
except ImportError:
    print("❌ Selenium not installed")
    print("Run: pip install selenium")
    exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False


class WhatsAppSimpleAPI:
    """Simple WhatsApp API using Selenium."""
    
    def __init__(self):
        self.session_path = Path(".whatsapp_session")
        self.inbox_path = Path("WhatsApp_Inbox")
        self.sent_path = Path("WhatsApp_Sent")
        self.inbox_path.mkdir(exist_ok=True)
        self.sent_path.mkdir(exist_ok=True)
        
        self.driver = None
    
    def start(self):
        """Start browser."""
        print("⏳ Starting WhatsApp (Selenium)...")
        
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={self.session_path.absolute()}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Start Chrome with auto-driver management
        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                from webdriver_manager.chrome import ChromeDriverManager
                service = ChromeService(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                # Try without webdriver-manager
                self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"❌ Error starting Chrome: {e}")
            print("\n💡 Try installing webdriver-manager:")
            print("   pip install webdriver-manager")
            return False
        
        self.driver.maximize_window()
        
        print("⏳ Loading WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")
        
        # Wait for WhatsApp to load
        print("⏳ Waiting for WhatsApp to load (60 seconds max)...")
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "pane-side"))
            )
            print("✅ WhatsApp loaded!")
            time.sleep(3)
            return True
        except:
            print("❌ WhatsApp didn't load")
            return False
    
    def get_unread_messages(self) -> List[Dict]:
        """Get unread messages."""
        print("\n📬 Checking for unread messages...")
        
        unread = []
        
        try:
            time.sleep(2)
            
            # Find unread chats
            chats = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
            
            for chat in chats[:15]:
                try:
                    # Check for unread badge
                    try:
                        chat.find_element(By.CSS_SELECTOR, 'span[data-testid="icon-unread-count"]')
                    except:
                        continue
                    
                    # Get name
                    try:
                        name_elem = chat.find_element(By.CSS_SELECTOR, 'span[title]')
                        name = name_elem.get_attribute('title')
                    except:
                        continue
                    
                    # Get preview
                    preview = ""
                    try:
                        preview_elem = chat.find_element(By.CSS_SELECTOR, 'span[dir="ltr"]')
                        preview = preview_elem.text
                    except:
                        pass
                    
                    print(f"   📩 {name}: {preview[:50]}...")
                    
                    unread.append({
                        'name': name,
                        'preview': preview,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                except:
                    continue
            
            print(f"\n✅ Found {len(unread)} unread messages")
            return unread
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def send_message(self, recipient: str, message: str) -> bool:
        """Send message."""
        print(f"\n📤 Sending to {recipient}...")
        print(f"💬 Message: {message[:80]}...")
        
        try:
            # Find search box
            print("   🔍 Finding search box...")
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
            )
            
            # Click and clear
            search_box.click()
            time.sleep(0.5)
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
            
            # Type recipient name slowly
            print(f"   ⌨️  Searching: {recipient}")
            for char in recipient:
                search_box.send_keys(char)
                time.sleep(0.05)
            
            time.sleep(3)
            
            # Find and click first result
            print("   📱 Opening chat...")
            try:
                first_result = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="listitem"]'))
                )
                first_result.click()
                time.sleep(2)
            except:
                print("   ❌ No results found")
                return False
            
            # Find message input
            print("   ⌨️  Finding message input...")
            message_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="10"]'))
            )
            
            # Type message
            print("   ⌨️  Typing message...")
            message_input.click()
            time.sleep(0.5)
            
            # Type slowly
            lines = message.split('\n')
            for i, line in enumerate(lines):
                for char in line:
                    message_input.send_keys(char)
                    time.sleep(0.02)
                
                if i < len(lines) - 1:
                    message_input.send_keys(Keys.SHIFT + Keys.ENTER)
                    time.sleep(0.2)
            
            time.sleep(1)
            
            # Send
            print("   📨 Sending...")
            message_input.send_keys(Keys.ENTER)
            time.sleep(2)
            
            print("   ✅ Message sent!")
            
            # Track
            self._save_to_sent(recipient, message)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def close(self):
        """Close browser."""
        if self.driver:
            self.driver.quit()
    
    def _save_to_sent(self, recipient: str, message: str):
        """Track sent message."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = recipient.replace(' ', '_').replace('/', '_')
        filename = f"sent_{timestamp}_{safe_name}.md"
        filepath = self.sent_path / filename
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "✅ Sent"
method: "selenium_api"
---

# WhatsApp Message to {recipient}

**Status**: ✅ Sent
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Method**: Selenium API

## Message
{message}

---

*Sent via WhatsApp Simple API*
"""
        
        filepath.write_text(content, encoding='utf-8')
        print(f"   📝 Tracked: {filepath}")


# CLI
def main():
    import sys
    
    if len(sys.argv) < 2:
        print("=" * 70)
        print("WhatsApp Simple API (Selenium)")
        print("=" * 70)
        print()
        print("Commands:")
        print("  python whatsapp_simple_api.py unread")
        print("  python whatsapp_simple_api.py send <contact> <message>")
        print()
        print("Examples:")
        print("  python whatsapp_simple_api.py unread")
        print('  python whatsapp_simple_api.py send Asyfa "Hello!"')
        print()
        return
    
    command = sys.argv[1].lower()
    
    wa = WhatsAppSimpleAPI()
    
    try:
        if not wa.start():
            print("❌ Failed to start")
            return
        
        if command == "unread":
            messages = wa.get_unread_messages()
            print(f"\n📊 Total: {len(messages)}")
        
        elif command == "send":
            if len(sys.argv) < 4:
                print("❌ Usage: python whatsapp_simple_api.py send <contact> <message>")
                return
            
            recipient = sys.argv[2]
            message = " ".join(sys.argv[3:])
            
            success = wa.send_message(recipient, message)
            
            if success:
                print("\n" + "=" * 70)
                print("✅ SUCCESS!")
                print("=" * 70)
                print(f"\nMessage sent to {recipient}")
            else:
                print("\n❌ Failed to send")
        
        else:
            print(f"❌ Unknown command: {command}")
        
        # Keep open
        print("\n⏳ Keeping browser open for 5 seconds...")
        time.sleep(5)
        
    finally:
        print("\n🧹 Closing...")
        wa.close()
        print("✅ Done!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
