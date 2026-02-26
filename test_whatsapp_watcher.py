#!/usr/bin/env python3
"""
Test script for WhatsApp Watcher
Run this after authentication to verify functionality
"""

import sys
import logging
from pathlib import Path

# Add Skills to path
sys.path.insert(0, 'Skills')

from whatsapp_watcher import WhatsAppWatcher, WhatsAppWatcherConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_authentication():
    """Test if WhatsApp session is authenticated"""
    print("\n" + "="*60)
    print("TEST 1: Authentication Check")
    print("="*60)
    
    config = WhatsAppWatcherConfig(
        vault_path=".",
        session_path=".whatsapp_session",
        dry_run=True
    )
    
    watcher = WhatsAppWatcher(config)
    
    if watcher.authenticate():
        print("✓ Authentication successful!")
        print(f"  Session path: {config.session_path}")
        return True
    else:
        print("✗ Authentication failed!")
        print("  Run: python Skills/whatsapp_watcher.py auth")
        return False

def test_poll_dry_run():
    """Test polling in dry-run mode"""
    print("\n" + "="*60)
    print("TEST 2: Poll (Dry Run)")
    print("="*60)
    print("Checking for unread messages with keywords...")
    print("Keywords: urgent, asap, invoice, payment, help, important")
    print()
    
    config = WhatsAppWatcherConfig(
        vault_path=".",
        session_path=".whatsapp_session",
        dry_run=True  # Won't create files
    )
    
    watcher = WhatsAppWatcher(config)
    
    try:
        stats = watcher.poll_once()
        
        print("\nResults:")
        print(f"  Retrieved: {stats['retrieved']} messages")
        print(f"  Processed: {stats['processed']} messages")
        print(f"  Filtered: {stats['filtered']} (didn't match keywords)")
        print(f"  Would create: {stats['created']} files")
        print(f"  Errors: {stats['errors']}")
        
        if stats['created'] > 0:
            print("\n✓ Found important messages!")
            print("  Run without --dry-run to create markdown files")
        else:
            print("\n⚠ No important messages found")
            print("  Try sending a test message with keywords like 'urgent' or 'help'")
        
        return True
    except Exception as e:
        print(f"\n✗ Poll failed: {e}")
        return False

def test_poll_real():
    """Test polling and creating actual files"""
    print("\n" + "="*60)
    print("TEST 3: Poll (Real - Creates Files)")
    print("="*60)
    
    response = input("This will create markdown files. Continue? (y/n): ")
    if response.lower() != 'y':
        print("Skipped.")
        return True
    
    config = WhatsAppWatcherConfig(
        vault_path=".",
        session_path=".whatsapp_session",
        dry_run=False  # Will create files
    )
    
    watcher = WhatsAppWatcher(config)
    
    try:
        stats = watcher.poll_once()
        
        print("\nResults:")
        print(f"  Retrieved: {stats['retrieved']} messages")
        print(f"  Processed: {stats['processed']} messages")
        print(f"  Filtered: {stats['filtered']}")
        print(f"  Created: {stats['created']} files")
        print(f"  Errors: {stats['errors']}")
        
        if stats['created'] > 0:
            print("\n✓ Created markdown files!")
            print("  Check Inbox/ and Needs_Action/ folders")
        else:
            print("\n⚠ No files created")
        
        return True
    except Exception as e:
        print(f"\n✗ Poll failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("WhatsApp Watcher Test Suite")
    print("="*60)
    
    # Test 1: Authentication
    if not test_authentication():
        print("\n❌ Authentication failed. Please run auth first:")
        print("   python Skills/whatsapp_watcher.py auth")
        return
    
    # Test 2: Dry run poll
    if not test_poll_dry_run():
        print("\n❌ Dry run poll failed")
        return
    
    # Test 3: Real poll (optional)
    test_poll_real()
    
    print("\n" + "="*60)
    print("✓ Testing Complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Send test WhatsApp messages with keywords")
    print("  2. Run: python Skills/whatsapp_watcher.py poll")
    print("  3. Check Inbox/ and Needs_Action/ folders")
    print("  4. Start continuous monitoring:")
    print("     python Skills/whatsapp_watcher.py start")

if __name__ == "__main__":
    main()
