"""
WhatsApp Watcher

Monitors WhatsApp Web for important messages and creates actionable markdown files.
Uses Playwright for browser automation.

IMPORTANT: This uses WhatsApp Web automation. Be aware of WhatsApp's terms of service.
"""

import logging
import time
from pathlib import Path
from datetime import datetime, UTC
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
import re

try:
    from playwright.sync_api import sync_playwright, Browser, Page
except ImportError:
    print("Playwright not installed. Install with: pip install playwright")
    print("Then run: playwright install chromium")
    exit(1)

from base_watcher import BaseWatcher, WatcherConfig


@dataclass
class WhatsAppWatcherConfig(WatcherConfig):
    """Configuration for WhatsApp Watcher"""
    session_path: str = ".whatsapp_session"
    keywords: List[str] = None
    polling_interval_ms: int = 30000  # 30 seconds
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = ['urgent', 'asap', 'invoice', 'payment', 'help', 'important']


class WhatsAppWatcher(BaseWatcher):
    """
    WhatsApp Watcher implementation using Playwright.
    
    Monitors WhatsApp Web for messages containing important keywords
    and creates markdown files in the vault.
    """
    
    def __init__(self, config: WhatsAppWatcherConfig):
        super().__init__(config, "WhatsAppWatcher")
        self.config: WhatsAppWatcherConfig = config
        self.session_path = Path(config.session_path)
        self.keywords = config.keywords
        self.processed_messages: set = set()
        
        # Ensure session directory exists
        self.session_path.mkdir(parents=True, exist_ok=True)
    
    def authenticate(self) -> bool:
        """
        Authenticate with WhatsApp Web.
        
        On first run, this will open a browser window for QR code scanning.
        Subsequent runs will use the saved session.
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            self.logger.info("Authenticating with WhatsApp Web...")
            
            with sync_playwright() as p:
                # Use system Chrome to avoid disk space issues
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Show browser for QR code on first run
                    channel="chrome"  # Use system Chrome instead of downloading Chromium
                )
                page = browser.pages[0]
                page.goto('https://web.whatsapp.com', timeout=60000)
                
                # Wait a bit for page to load
                time.sleep(2)
                
                # Check if already logged in by looking for common WhatsApp Web elements
                try:
                    # Try multiple selectors that indicate successful login
                    page.wait_for_selector('div[id="pane-side"]', timeout=5000)
                    self.logger.info("Already authenticated with WhatsApp Web")
                    browser.close()
                    return True
                except:
                    pass
                
                # Need to scan QR code
                self.logger.info("Please scan the QR code in the browser window...")
                self.logger.info("You have 5 minutes to scan the QR code...")
                
                # Wait for successful login - try multiple selectors
                start_time = time.time()
                timeout_seconds = 300  # 5 minutes
                
                while time.time() - start_time < timeout_seconds:
                    try:
                        # Check for main chat pane (most reliable indicator)
                        if page.query_selector('div[id="pane-side"]'):
                            self.logger.info("QR code scanned successfully!")
                            time.sleep(3)  # Give it time to fully load
                            browser.close()
                            return True
                        
                        # Also check for chat list
                        if page.query_selector('[data-testid="chat-list"]'):
                            self.logger.info("QR code scanned successfully!")
                            time.sleep(3)
                            browser.close()
                            return True
                        
                        # Check for search box (another indicator)
                        if page.query_selector('[data-testid="chat-list-search"]'):
                            self.logger.info("QR code scanned successfully!")
                            time.sleep(3)
                            browser.close()
                            return True
                        
                    except:
                        pass
                    
                    time.sleep(1)  # Check every second
                
                # Timeout
                self.logger.error("Timeout waiting for QR code scan")
                browser.close()
                return False
        
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return False
    
    def check_for_new_items(self) -> List[str]:
        """
        Check WhatsApp Web for new messages with important keywords.
        
        Returns:
            List of message IDs to process
        """
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    channel="chrome"  # Use system Chrome
                )
                page = browser.pages[0]
                page.goto('https://web.whatsapp.com', wait_until='networkidle')
                
                # Wait for chat list to load
                page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)
                
                # Find unread chats
                unread_chats = page.query_selector_all('[aria-label*="unread"]')
                
                message_ids = []
                for chat in unread_chats:
                    try:
                        # Get chat name and preview text
                        chat_name = self._get_chat_name(chat)
                        preview_text = self._get_preview_text(chat)
                        
                        # Check if message contains keywords
                        if self._contains_keywords(preview_text):
                            message_id = f"{chat_name}_{int(time.time())}"
                            if message_id not in self.processed_messages:
                                message_ids.append(message_id)
                                self.logger.info(f"Found important message from {chat_name}")
                    except Exception as e:
                        self.logger.warning(f"Error processing chat: {e}")
                        continue
                
                browser.close()
                return message_ids
        
        except Exception as e:
            self.logger.error(f"Failed to check for new messages: {e}")
            return []
    
    def get_item_content(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch full content for a specific WhatsApp message.
        
        Args:
            item_id: Message identifier (format: chatname_timestamp)
            
        Returns:
            Dictionary with message metadata and content
        """
        try:
            chat_name = item_id.split('_')[0]
            
            with sync_playwright() as p:
                browser = p.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=True,
                    channel="chrome"  # Use system Chrome
                )
                page = browser.pages[0]
                page.goto('https://web.whatsapp.com', wait_until='networkidle')
                page.wait_for_selector('[data-testid="chat-list"]', timeout=10000)
                
                # Search for the chat
                search_box = page.query_selector('[data-testid="chat-list-search"]')
                if search_box:
                    search_box.click()
                    search_box.fill(chat_name)
                    time.sleep(1)
                    
                    # Click first result
                    first_result = page.query_selector('[data-testid="cell-frame-container"]')
                    if first_result:
                        first_result.click()
                        time.sleep(1)
                        
                        # Get recent messages
                        messages = page.query_selector_all('[data-testid="msg-container"]')
                        recent_messages = []
                        
                        for msg in messages[-5:]:  # Last 5 messages
                            try:
                                text = msg.inner_text()
                                recent_messages.append(text)
                            except:
                                continue
                        
                        browser.close()
                        
                        return {
                            'id': item_id,
                            'chat_name': chat_name,
                            'messages': recent_messages,
                            'timestamp': datetime.now(UTC).isoformat() + 'Z',
                            'source': 'whatsapp'
                        }
                
                browser.close()
                return None
        
        except Exception as e:
            self.logger.error(f"Failed to get message content: {e}")
            return None
    
    def is_important(self, item: Dict[str, Any]) -> bool:
        """
        Check if message is important based on keywords.
        
        Args:
            item: Message metadata
            
        Returns:
            True if message contains important keywords
        """
        messages_text = ' '.join(item.get('messages', [])).lower()
        return self._contains_keywords(messages_text)
    
    def detect_priority(self, item: Dict[str, Any]) -> str:
        """
        Detect message priority based on keywords.
        
        Args:
            item: Message metadata
            
        Returns:
            Priority level: "high", "medium", or "low"
        """
        messages_text = ' '.join(item.get('messages', [])).lower()
        
        # High priority keywords
        high_keywords = ['urgent', 'asap', 'emergency', 'critical', 'help']
        if any(kw in messages_text for kw in high_keywords):
            return 'high'
        
        # Medium priority keywords
        medium_keywords = ['invoice', 'payment', 'important', 'deadline']
        if any(kw in messages_text for kw in medium_keywords):
            return 'medium'
        
        return 'low'
    
    def generate_markdown(self, item: Dict[str, Any]) -> str:
        """
        Generate markdown content for WhatsApp message.
        
        Args:
            item: Message metadata
            
        Returns:
            Markdown formatted string
        """
        priority = item.get('priority', 'low')
        priority_emoji = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        
        messages_formatted = '\n\n'.join([
            f"> {msg}" for msg in item.get('messages', [])
        ])
        
        content = f"""---
type: whatsapp_message
chat_name: "{item.get('chat_name', 'Unknown')}"
timestamp: "{item.get('timestamp', '')}"
priority: "{priority}"
status: "pending"
source: "whatsapp"
message_id: "{item.get('id', '')}"
---

# WhatsApp: {item.get('chat_name', 'Unknown')}

**Priority**: {priority_emoji.get(priority, '⚪')} {priority.capitalize()}  
**Received**: {item.get('timestamp', '')}  
**Source**: WhatsApp Web

## Recent Messages

{messages_formatted}

---

## Action Items

- [ ] Review and respond to this message
- [ ] Check if any follow-up is needed

## Links

- Open WhatsApp Web to respond

---

*Processed by WhatsApp Watcher v1.0.0*
"""
        return content
    
    def _get_chat_name(self, chat_element) -> str:
        """Extract chat name from chat element"""
        try:
            name_element = chat_element.query_selector('[data-testid="cell-frame-title"]')
            if name_element:
                return name_element.inner_text()
        except:
            pass
        return "Unknown"
    
    def _get_preview_text(self, chat_element) -> str:
        """Extract preview text from chat element"""
        try:
            preview_element = chat_element.query_selector('[data-testid="last-msg-text"]')
            if preview_element:
                return preview_element.inner_text()
        except:
            pass
        return ""
    
    def _contains_keywords(self, text: str) -> bool:
        """Check if text contains any important keywords"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in self.keywords)


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp Watcher for AI Employee")
    parser.add_argument(
        "command",
        choices=["auth", "poll", "start"],
        help="Command to execute"
    )
    parser.add_argument(
        "--session-path",
        default=".whatsapp_session",
        help="Path to WhatsApp session directory"
    )
    parser.add_argument(
        "--vault-path",
        default=".",
        help="Path to vault root directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (no modifications)"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create config
    config = WhatsAppWatcherConfig(
        vault_path=args.vault_path,
        session_path=args.session_path,
        dry_run=args.dry_run
    )
    
    # Create watcher
    watcher = WhatsAppWatcher(config)
    
    if args.command == "auth":
        if watcher.authenticate():
            print("✓ Authentication successful")
            print(f"Session saved to: {args.session_path}")
        else:
            print("✗ Authentication failed")
            exit(1)
    
    elif args.command == "poll":
        if not watcher.authenticate():
            print("✗ Authentication failed")
            exit(1)
        
        stats = watcher.poll_once()
        print(f"\nPoll Results:")
        print(f"  Retrieved: {stats['retrieved']}")
        print(f"  Processed: {stats['processed']}")
        print(f"  Filtered: {stats['filtered']}")
        print(f"  Created: {stats['created']}")
        print(f"  Errors: {stats['errors']}")
    
    elif args.command == "start":
        watcher.start()
