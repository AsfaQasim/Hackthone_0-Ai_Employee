"""
WhatsApp MCP Server

Implements WhatsApp messaging functionality using Playwright.
Provides tools for reading and sending WhatsApp messages.
Uses the same session as WhatsApp Watcher for authentication.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import json
import logging
import asyncio

from .base_mcp_server import BaseMCPServer, Tool, TextContent

try:
    from playwright.async_api import async_playwright, Browser, Page
except ImportError:
    print("Playwright not installed. Install with: pip install playwright")
    print("Then run: playwright install chromium")
    exit(1)


class WhatsAppMCPServer(BaseMCPServer):
    """
    WhatsApp MCP Server for reading and sending messages.
    
    Uses Playwright to interact with WhatsApp Web.
    Shares session with WhatsApp Watcher for seamless integration.
    """
    
    def __init__(
        self, 
        name: str = "whatsapp_mcp_server",
        session_path: str = ".whatsapp_session",
        vault_path: str = "."
    ):
        """
        Initialize the WhatsApp MCP Server.
        
        Args:
            name: Server name
            session_path: Path to WhatsApp session directory (shared with watcher)
            vault_path: Path to vault for tracking sent messages
        """
        self.session_path = Path(session_path)
        self.vault_path = Path(vault_path)
        self.tracking_dir = self.vault_path / "WhatsApp_Sent"
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        
        self.browser = None
        self.page = None
        self.playwright = None
        
        super().__init__(name)
    
    def register_tools(self) -> None:
        """Register WhatsApp messaging tools."""
        
        # Send message tool
        send_message_tool = Tool(
            name="send_whatsapp_message",
            description="Send a WhatsApp message to a contact or group",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipient": {
                        "type": "string",
                        "description": "Contact name or phone number (with country code)"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message text to send"
                    }
                },
                "required": ["recipient", "message"]
            }
        )
        self.add_tool(send_message_tool)
        
        # Read messages tool
        read_messages_tool = Tool(
            name="read_whatsapp_messages",
            description="Read recent messages from a WhatsApp contact or group",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact": {
                        "type": "string",
                        "description": "Contact name or phone number to read messages from"
                    },
                    "count": {
                        "type": "number",
                        "description": "Number of recent messages to read (default: 10)",
                        "default": 10
                    }
                },
                "required": ["contact"]
            }
        )
        self.add_tool(read_messages_tool)
        
        # Get unread chats tool
        unread_chats_tool = Tool(
            name="get_unread_whatsapp_chats",
            description="Get list of chats with unread messages",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        self.add_tool(unread_chats_tool)
        
        # Check connection status
        status_tool = Tool(
            name="check_whatsapp_status",
            description="Check if WhatsApp Web is connected and ready",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        self.add_tool(status_tool)
    
    async def _ensure_browser(self) -> bool:
        """
        Ensure browser is initialized and WhatsApp Web is loaded.
        Uses system Chrome instead of Playwright's Chromium.
        
        Returns:
            True if browser is ready, False otherwise
        """
        try:
            if self.browser is None or self.page is None:
                self.playwright = await async_playwright().start()
                
                # Use system Chrome instead of Playwright's Chromium
                # headless=False to avoid WhatsApp Web automation detection
                self.browser = await self.playwright.chromium.launch_persistent_context(
                    str(self.session_path),
                    headless=False,  # Keep browser visible to avoid detection
                    channel="chrome",  # Use system Chrome
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-dev-shm-usage'
                    ]
                )
                
                if len(self.browser.pages) > 0:
                    self.page = self.browser.pages[0]
                else:
                    self.page = await self.browser.new_page()
                
                await self.page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=60000)
                
                # Wait for WhatsApp to load - increased timeout
                try:
                    await self.page.wait_for_selector('[data-testid="chat-list"]', timeout=30000)
                    self.logger.info("WhatsApp Web loaded successfully")
                    return True
                except:
                    self.logger.error("WhatsApp Web not loaded - may need authentication")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize browser: {e}")
            return False
    
    async def _close_browser(self):
        """Close browser and cleanup resources."""
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self.browser = None
            self.page = None
            self.playwright = None
        except Exception as e:
            self.logger.error(f"Error closing browser: {e}")
    
    async def _search_and_open_chat(self, contact: str) -> bool:
        """
        Search for a contact and open their chat.
        
        Args:
            contact: Contact name or phone number
            
        Returns:
            True if chat opened successfully
        """
        try:
            # Click search box
            search_box = await self.page.wait_for_selector('[data-testid="chat-list-search"]', timeout=5000)
            await search_box.click()
            
            # Type contact name
            await self.page.keyboard.type(contact)
            await asyncio.sleep(1)
            
            # Click first result
            first_result = await self.page.wait_for_selector('[data-testid="cell-frame-container"]', timeout=5000)
            await first_result.click()
            await asyncio.sleep(1)
            
            self.logger.info(f"Opened chat with {contact}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to open chat with {contact}: {e}")
            return False
    
    async def _send_message_to_open_chat(self, message: str) -> bool:
        """
        Send message to currently open chat.
        
        Args:
            message: Message text
            
        Returns:
            True if message sent successfully
        """
        try:
            # Find message input box
            message_box = await self.page.wait_for_selector('[data-testid="conversation-compose-box-input"]', timeout=5000)
            
            # Type message
            await message_box.click()
            await self.page.keyboard.type(message)
            
            # Send message (press Enter)
            await self.page.keyboard.press('Enter')
            await asyncio.sleep(0.5)
            
            self.logger.info(f"Message sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False
    
    async def _read_messages_from_open_chat(self, count: int = 10) -> List[Dict[str, str]]:
        """
        Read messages from currently open chat.
        
        Args:
            count: Number of messages to read
            
        Returns:
            List of message dictionaries
        """
        try:
            # Wait for messages to load
            await self.page.wait_for_selector('[data-testid="msg-container"]', timeout=5000)
            
            # Get message elements
            message_elements = await self.page.query_selector_all('[data-testid="msg-container"]')
            
            messages = []
            for elem in message_elements[-count:]:
                try:
                    text = await elem.inner_text()
                    messages.append({
                        'text': text,
                        'timestamp': datetime.now().isoformat()
                    })
                except:
                    continue
            
            self.logger.info(f"Read {len(messages)} messages")
            return messages
            
        except Exception as e:
            self.logger.error(f"Failed to read messages: {e}")
            return []
    
    async def _get_unread_chats(self) -> List[Dict[str, str]]:
        """
        Get list of chats with unread messages.
        
        Returns:
            List of chat dictionaries with name and preview
        """
        try:
            # Find unread chat elements
            unread_elements = await self.page.query_selector_all('[aria-label*="unread"]')
            
            chats = []
            for elem in unread_elements:
                try:
                    # Get chat name
                    name_elem = await elem.query_selector('[data-testid="cell-frame-title"]')
                    name = await name_elem.inner_text() if name_elem else "Unknown"
                    
                    # Get preview text
                    preview_elem = await elem.query_selector('[data-testid="last-msg-text"]')
                    preview = await preview_elem.inner_text() if preview_elem else ""
                    
                    chats.append({
                        'name': name,
                        'preview': preview
                    })
                except:
                    continue
            
            self.logger.info(f"Found {len(chats)} unread chats")
            return chats
            
        except Exception as e:
            self.logger.error(f"Failed to get unread chats: {e}")
            return []
    
    def _track_sent_message(self, recipient: str, message: str, success: bool) -> Path:
        """
        Track a sent message in the vault.
        
        Args:
            recipient: Message recipient
            message: Message text
            success: Whether message was sent successfully
            
        Returns:
            Path to tracking file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whatsapp_{timestamp}_{recipient[:20]}.md"
        filepath = self.tracking_dir / filename
        
        status = "✅ Sent" if success else "❌ Failed"
        
        content = f"""---
type: whatsapp_sent
recipient: "{recipient}"
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
---

# WhatsApp Message to {recipient}

**Status**: {status}
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Message
{message}

---

*Sent via WhatsApp MCP Server*
"""
        
        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Tracked sent message: {filepath}")
        
        return filepath
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> TextContent:
        """
        Handle tool call requests.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            TextContent with result
        """
        try:
            if name == "send_whatsapp_message":
                return await self._handle_send_message(arguments)
            
            elif name == "read_whatsapp_messages":
                return await self._handle_read_messages(arguments)
            
            elif name == "get_unread_whatsapp_chats":
                return await self._handle_get_unread_chats(arguments)
            
            elif name == "check_whatsapp_status":
                return await self._handle_check_status(arguments)
            
            else:
                return TextContent(
                    type="text",
                    text=f"Error: Unknown tool '{name}'"
                )
        
        except Exception as e:
            error_msg = f"Error executing {name}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return TextContent(
                type="text",
                text=f"Error: {error_msg}"
            )
    
    async def _handle_send_message(self, arguments: Dict[str, Any]) -> TextContent:
        """Handle send_whatsapp_message tool call."""
        recipient = arguments['recipient']
        message = arguments['message']
        
        # Ensure browser is ready
        if not await self._ensure_browser():
            return TextContent(
                type="text",
                text="Error: WhatsApp Web not connected. Please authenticate first using: python Skills/whatsapp_watcher.py auth"
            )
        
        # Open chat
        if not await self._search_and_open_chat(recipient):
            return TextContent(
                type="text",
                text=f"Error: Could not find or open chat with {recipient}"
            )
        
        # Send message
        success = await self._send_message_to_open_chat(message)
        
        # Track the message
        self._track_sent_message(recipient, message, success)
        
        if success:
            return TextContent(
                type="text",
                text=f"✅ Message sent successfully to {recipient}"
            )
        else:
            return TextContent(
                type="text",
                text=f"❌ Failed to send message to {recipient}"
            )
    
    async def _handle_read_messages(self, arguments: Dict[str, Any]) -> TextContent:
        """Handle read_whatsapp_messages tool call."""
        contact = arguments['contact']
        count = arguments.get('count', 10)
        
        # Ensure browser is ready
        if not await self._ensure_browser():
            return TextContent(
                type="text",
                text="Error: WhatsApp Web not connected. Please authenticate first."
            )
        
        # Open chat
        if not await self._search_and_open_chat(contact):
            return TextContent(
                type="text",
                text=f"Error: Could not find or open chat with {contact}"
            )
        
        # Read messages
        messages = await self._read_messages_from_open_chat(count)
        
        if messages:
            messages_text = "\n\n".join([f"- {msg['text']}" for msg in messages])
            return TextContent(
                type="text",
                text=f"📱 Messages from {contact} ({len(messages)} messages):\n\n{messages_text}"
            )
        else:
            return TextContent(
                type="text",
                text=f"No messages found from {contact}"
            )
    
    async def _handle_get_unread_chats(self, arguments: Dict[str, Any]) -> TextContent:
        """Handle get_unread_whatsapp_chats tool call."""
        # Ensure browser is ready
        if not await self._ensure_browser():
            return TextContent(
                type="text",
                text="Error: WhatsApp Web not connected. Please authenticate first."
            )
        
        # Get unread chats
        chats = await self._get_unread_chats()
        
        if chats:
            chats_text = "\n".join([f"- {chat['name']}: {chat['preview']}" for chat in chats])
            return TextContent(
                type="text",
                text=f"📬 Unread chats ({len(chats)}):\n\n{chats_text}"
            )
        else:
            return TextContent(
                type="text",
                text="No unread chats"
            )
    
    async def _handle_check_status(self, arguments: Dict[str, Any]) -> TextContent:
        """Handle check_whatsapp_status tool call."""
        if await self._ensure_browser():
            return TextContent(
                type="text",
                text="✅ WhatsApp Web is connected and ready"
            )
        else:
            return TextContent(
                type="text",
                text="❌ WhatsApp Web is not connected. Please authenticate using: python Skills/whatsapp_watcher.py auth"
            )
    
    async def cleanup(self):
        """Cleanup resources when server stops."""
        await self._close_browser()


# Example usage
if __name__ == "__main__":
    import asyncio
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    async def test_whatsapp_server():
        """Test the WhatsApp MCP Server."""
        server = WhatsAppMCPServer()
        
        # List available tools
        print("Available tools:")
        for tool in server.list_tools():
            print(f"  - {tool['name']}: {tool['description']}")
        
        # Test status check
        result = await server.execute_tool("check_whatsapp_status", {})
        print(f"\nStatus: {result.text}")
    
    asyncio.run(test_whatsapp_server())
