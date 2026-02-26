"""
WhatsApp Business API Integration
Direct message sending to WhatsApp - Official Method

This uses WhatsApp Business API (Cloud API) which is:
- Official and supported by Meta/WhatsApp
- No automation detection
- Reliable and scalable
- Requires business verification
"""

import os
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class WhatsAppBusinessAPI:
    """
    WhatsApp Business API client for sending messages directly.
    
    Setup Required:
    1. Create Meta Business Account
    2. Get WhatsApp Business API access
    3. Get Phone Number ID and Access Token
    4. Add to .env file
    """
    
    def __init__(self):
        self.phone_id = os.getenv('WHATSAPP_PHONE_ID')
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.api_version = 'v18.0'
        self.base_url = f'https://graph.facebook.com/{self.api_version}'
        
        self.tracking_dir = Path("WhatsApp_Sent")
        self.tracking_dir.mkdir(exist_ok=True)
    
    def send_message(self, to_phone, message):
        """
        Send a WhatsApp message directly.
        
        Args:
            to_phone: Recipient phone number (with country code, no +)
                     Example: "923001234567" for Pakistan
            message: Message text to send
            
        Returns:
            dict: API response with message ID if successful
        """
        if not self.phone_id or not self.access_token:
            return {
                'success': False,
                'error': 'WhatsApp Business API not configured. See setup instructions.'
            }
        
        url = f"{self.base_url}/{self.phone_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if response.status_code == 200:
                message_id = result.get('messages', [{}])[0].get('id')
                print(f"✅ Message sent successfully!")
                print(f"   Message ID: {message_id}")
                
                # Track the message
                self._track_message(to_phone, message, True, message_id)
                
                return {
                    'success': True,
                    'message_id': message_id,
                    'response': result
                }
            else:
                error = result.get('error', {})
                print(f"❌ Failed to send message")
                print(f"   Error: {error.get('message', 'Unknown error')}")
                
                self._track_message(to_phone, message, False, None)
                
                return {
                    'success': False,
                    'error': error.get('message', 'Unknown error'),
                    'response': result
                }
        
        except Exception as e:
            print(f"❌ Exception: {e}")
            self._track_message(to_phone, message, False, None)
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_template_message(self, to_phone, template_name, language_code="en"):
        """
        Send a pre-approved template message.
        
        Args:
            to_phone: Recipient phone number
            template_name: Name of approved template
            language_code: Template language (default: en)
            
        Returns:
            dict: API response
        """
        if not self.phone_id or not self.access_token:
            return {
                'success': False,
                'error': 'WhatsApp Business API not configured'
            }
        
        url = f"{self.base_url}/{self.phone_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if response.status_code == 200:
                return {'success': True, 'response': result}
            else:
                return {'success': False, 'error': result}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _track_message(self, to_phone, message, success, message_id=None):
        """Track sent message."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whatsapp_api_{timestamp}_{to_phone}.md"
        filepath = self.tracking_dir / filename
        
        status = "✅ Sent" if success else "❌ Failed"
        
        content = f"""---
type: whatsapp_sent_api
to: "{to_phone}"
timestamp: "{datetime.now().isoformat()}"
status: "{status}"
message_id: "{message_id or 'N/A'}"
method: "business_api"
---

# WhatsApp Message via Business API

**To**: {to_phone}
**Status**: {status}
**Sent**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Message ID**: {message_id or 'N/A'}

## Message
{message}

---

*Sent via WhatsApp Business API*
"""
        
        filepath.write_text(content, encoding='utf-8')
    
    def check_configuration(self):
        """Check if API is properly configured."""
        print("=" * 60)
        print("WhatsApp Business API Configuration Check")
        print("=" * 60)
        
        if self.phone_id:
            print(f"✅ Phone ID: {self.phone_id[:10]}...")
        else:
            print("❌ Phone ID: Not configured")
        
        if self.access_token:
            print(f"✅ Access Token: {self.access_token[:20]}...")
        else:
            print("❌ Access Token: Not configured")
        
        if self.phone_id and self.access_token:
            print("\n✅ API is configured!")
            print("\nYou can now send messages directly to WhatsApp")
            return True
        else:
            print("\n❌ API not configured")
            print("\nSetup Instructions:")
            print("1. Go to: https://developers.facebook.com/")
            print("2. Create a Meta Business Account")
            print("3. Set up WhatsApp Business API")
            print("4. Get Phone Number ID and Access Token")
            print("5. Add to .env file:")
            print("   WHATSAPP_PHONE_ID=your_phone_id")
            print("   WHATSAPP_ACCESS_TOKEN=your_access_token")
            return False


def setup_guide():
    """Print detailed setup guide."""
    print("""
╔══════════════════════════════════════════════════════════╗
║     WhatsApp Business API Setup Guide                    ║
╚══════════════════════════════════════════════════════════╝

📋 STEP-BY-STEP SETUP:

1️⃣ Create Meta Business Account
   • Go to: https://business.facebook.com/
   • Create a business account
   • Verify your business

2️⃣ Set Up WhatsApp Business API
   • Go to: https://developers.facebook.com/
   • Create a new app
   • Select "Business" type
   • Add WhatsApp product

3️⃣ Get Test Phone Number (Free)
   • Meta provides a test number
   • Can send to 5 numbers
   • Good for development

4️⃣ Get Credentials
   • Phone Number ID: In WhatsApp > API Setup
   • Access Token: In WhatsApp > API Setup
   • Copy both values

5️⃣ Configure .env File
   Create/edit .env file:
   
   WHATSAPP_PHONE_ID=123456789012345
   WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxx

6️⃣ Add Test Recipients
   • In WhatsApp > API Setup
   • Add phone numbers you want to message
   • Verify them

7️⃣ Test
   python whatsapp_business_api.py test

═══════════════════════════════════════════════════════════

💰 PRICING:

Free Tier:
• 1,000 conversations/month (free)
• Good for testing and small projects

Paid:
• ~$0.005 - $0.09 per conversation
• Varies by country
• Conversation = 24-hour window

═══════════════════════════════════════════════════════════

✅ BENEFITS:

• ✅ Official WhatsApp support
• ✅ No automation detection
• ✅ Reliable and scalable
• ✅ Can send to any WhatsApp number
• ✅ Rich media support (images, videos, etc.)
• ✅ Template messages
• ✅ Read receipts
• ✅ Webhook for incoming messages

═══════════════════════════════════════════════════════════

📚 DOCUMENTATION:

Official Docs:
https://developers.facebook.com/docs/whatsapp/cloud-api/

Quick Start:
https://developers.facebook.com/docs/whatsapp/cloud-api/get-started

═══════════════════════════════════════════════════════════
""")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("WhatsApp Business API - Direct Messaging")
        print("=" * 60)
        print("\nCommands:")
        print("  python whatsapp_business_api.py setup")
        print("  python whatsapp_business_api.py check")
        print("  python whatsapp_business_api.py test")
        print("  python whatsapp_business_api.py send <phone> <message>")
        print("\nExamples:")
        print("  python whatsapp_business_api.py setup")
        print("  python whatsapp_business_api.py check")
        print('  python whatsapp_business_api.py send 923001234567 "Hello!"')
        print("=" * 60)
        exit(0)
    
    command = sys.argv[1].lower()
    api = WhatsAppBusinessAPI()
    
    if command == "setup":
        setup_guide()
    
    elif command == "check":
        api.check_configuration()
    
    elif command == "test":
        if api.check_configuration():
            print("\n" + "=" * 60)
            print("Test Message")
            print("=" * 60)
            phone = input("Enter phone number (with country code, no +): ")
            message = input("Enter message: ")
            
            print(f"\nSending to {phone}...")
            result = api.send_message(phone, message)
            
            if result['success']:
                print("\n✅ SUCCESS! Message sent to WhatsApp!")
            else:
                print(f"\n❌ FAILED: {result.get('error')}")
    
    elif command == "send":
        if len(sys.argv) < 4:
            print("Usage: python whatsapp_business_api.py send <phone> <message>")
            exit(1)
        
        phone = sys.argv[2]
        message = " ".join(sys.argv[3:])
        
        result = api.send_message(phone, message)
        
        if not result['success']:
            print(f"\nError: {result.get('error')}")
            print("\nRun 'python whatsapp_business_api.py setup' for instructions")
    
    else:
        print(f"Unknown command: {command}")
        print("Available: setup, check, test, send")
