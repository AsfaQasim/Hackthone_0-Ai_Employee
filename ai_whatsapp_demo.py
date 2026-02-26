"""
AI-Powered WhatsApp Demo
AI reads messages and sends responses automatically
"""

import asyncio
import logging
from pathlib import Path
from datetime import datetime
import json

try:
    from anthropic import Anthropic
except ImportError:
    print("Installing anthropic...")
    import subprocess
    subprocess.run(["pip", "install", "anthropic"])
    from anthropic import Anthropic

from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIWhatsAppAssistant:
    """AI Assistant that reads and responds to WhatsApp messages."""
    
    def __init__(self, api_key: str = None):
        """Initialize AI WhatsApp Assistant."""
        self.whatsapp = WhatsAppMCPServer()
        
        # Try to get API key from environment
        if not api_key:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if api_key:
            self.ai = Anthropic(api_key=api_key)
            self.ai_enabled = True
        else:
            self.ai = None
            self.ai_enabled = False
            logger.warning("No API key - AI responses disabled")
    
    async def check_unread_messages(self):
        """Check for unread WhatsApp messages."""
        print("\n📬 Checking for unread messages...")
        result = await self.whatsapp.execute_tool("get_unread_whatsapp_chats", {})
        print(f"Result: {result.text}")
        return result.text
    
    async def read_messages(self, contact: str, count: int = 5):
        """Read messages from a contact."""
        print(f"\n📖 Reading messages from {contact}...")
        result = await self.whatsapp.execute_tool("read_whatsapp_messages", {
            "contact": contact,
            "count": count
        })
        print(f"Result: {result.text}")
        return result.text
    
    async def generate_ai_response(self, contact: str, messages: str):
        """Generate AI response to messages."""
        if not self.ai_enabled:
            return f"Thanks for your message! (AI response disabled - no API key)"
        
        try:
            prompt = f"""You are a helpful AI assistant responding to WhatsApp messages.

Contact: {contact}
Their messages: {messages}

Generate a brief, friendly response (1-2 sentences). Be helpful and professional."""

            response = self.ai.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return "Thanks for your message! I'll get back to you soon."
    
    async def send_message(self, recipient: str, message: str):
        """Send WhatsApp message."""
        print(f"\n📤 Sending message to {recipient}...")
        print(f"Message: {message}")
        
        result = await self.whatsapp.execute_tool("send_whatsapp_message", {
            "recipient": recipient,
            "message": message
        })
        
        print(f"Result: {result.text}")
        return result.text
    
    async def demo_workflow(self):
        """Demo: AI reads and responds to messages."""
        print("=" * 70)
        print("AI WHATSAPP ASSISTANT - DEMO")
        print("=" * 70)
        print()
        print("This demo shows AI-powered WhatsApp automation:")
        print("  1. AI checks for unread messages")
        print("  2. AI reads messages from contacts")
        print("  3. AI generates intelligent responses")
        print("  4. AI sends responses back")
        print()
        print("=" * 70)
        
        # Step 1: Check unread
        await self.check_unread_messages()
        
        # Step 2: Demo with received messages
        inbox = Path("WhatsApp_Inbox")
        if inbox.exists():
            messages = list(inbox.glob("*.md"))
            if messages:
                print(f"\n✅ Found {len(messages)} received messages")
                
                # Read latest message
                latest = sorted(messages, reverse=True)[0]
                content = latest.read_text(encoding='utf-8')
                
                # Extract sender
                sender = "Unknown"
                for line in content.split('\n'):
                    if line.startswith('from:'):
                        sender = line.split('"')[1] if '"' in line else "Unknown"
                        break
                
                print(f"\n📨 Latest message from: {sender}")
                
                # Read their messages
                messages_text = await self.read_messages(sender, 3)
                
                # Generate AI response
                print(f"\n🤖 AI generating response...")
                ai_response = await self.generate_ai_response(sender, messages_text)
                print(f"AI Response: {ai_response}")
                
                # Ask user if they want to send
                print()
                print("=" * 70)
                print("READY TO SEND")
                print("=" * 70)
                print(f"To: {sender}")
                print(f"Message: {ai_response}")
                print()
                
                choice = input("Send this message? (yes/no): ").strip().lower()
                
                if choice in ['yes', 'y']:
                    await self.send_message(sender, ai_response)
                    print("\n✅ Message sent!")
                else:
                    print("\n⏭️  Skipped sending")
            else:
                print("\n⚠️  No messages in inbox yet")
        
        print()
        print("=" * 70)
        print("DEMO COMPLETE")
        print("=" * 70)
    
    async def cleanup(self):
        """Cleanup resources."""
        await self.whatsapp.cleanup()


async def main():
    """Run AI WhatsApp demo."""
    
    # Check for API key
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        print()
        print("⚠️  WARNING: No ANTHROPIC_API_KEY found in .env")
        print()
        print("AI responses will be generic. To enable AI:")
        print("1. Get API key from: https://console.anthropic.com/")
        print("2. Add to .env file: ANTHROPIC_API_KEY=your_key_here")
        print()
        input("Press Enter to continue with demo mode...")
    
    assistant = AIWhatsAppAssistant(api_key)
    
    try:
        await assistant.demo_workflow()
    finally:
        await assistant.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
