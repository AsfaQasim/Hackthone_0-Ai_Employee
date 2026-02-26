#!/usr/bin/env python3
"""Quick test to check WhatsApp watcher dependencies"""

print("Checking WhatsApp Watcher dependencies...")
print()

# Check Playwright
try:
    from playwright.sync_api import sync_playwright
    print("✓ Playwright is installed")
    playwright_installed = True
except ImportError:
    print("✗ Playwright is NOT installed")
    print("  Install with: pip install playwright")
    print("  Then run: playwright install chromium")
    playwright_installed = False

print()

# Check base_watcher
try:
    import sys
    sys.path.insert(0, 'Skills')
    from base_watcher import BaseWatcher
    print("✓ base_watcher module found")
    base_watcher_found = True
except ImportError as e:
    print(f"✗ base_watcher module NOT found: {e}")
    base_watcher_found = False

print()
print("=" * 50)

if playwright_installed and base_watcher_found:
    print("✓ All dependencies are ready!")
    print()
    print("To test WhatsApp watcher:")
    print("  1. python Skills/whatsapp_watcher.py auth")
    print("  2. python Skills/whatsapp_watcher.py poll --dry-run")
elif playwright_installed:
    print("⚠ Playwright is ready but base_watcher is missing")
    print("  Check if Skills/base_watcher.py exists")
else:
    print("✗ Missing dependencies")
    print()
    print("Install Playwright:")
    print("  pip install playwright")
    print("  playwright install chromium")
