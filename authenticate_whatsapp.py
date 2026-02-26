"""
Simple WhatsApp Authentication Script
Run this to scan QR code and authenticate WhatsApp Web
"""

import logging
from Skills.whatsapp_watcher import WhatsAppWatcher, WhatsAppWatcherConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("=" * 60)
print("WhatsApp Authentication")
print("=" * 60)
print("\nThis will open Chrome browser with WhatsApp Web.")
print("Please scan the QR code with your phone.")
print("You have 5 minutes to complete the scan.")
print("\n" + "=" * 60 + "\n")

# Create config
config = WhatsAppWatcherConfig(
    vault_path=".",
    session_path=".whatsapp_session"
)

# Create watcher
watcher = WhatsAppWatcher(config)

# Authenticate
if watcher.authenticate():
    print("\n" + "=" * 60)
    print("✅ Authentication successful!")
    print("=" * 60)
    print("\nSession saved to: .whatsapp_session")
    print("\nYou can now:")
    print("  1. Run: python test_whatsapp_mcp.py")
    print("  2. Use commands: status, unread, read, send")
    print("\n" + "=" * 60)
else:
    print("\n" + "=" * 60)
    print("❌ Authentication failed")
    print("=" * 60)
    print("\nPlease try again:")
    print("  python authenticate_whatsapp.py")
    exit(1)
