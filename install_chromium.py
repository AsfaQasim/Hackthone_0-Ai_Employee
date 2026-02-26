#!/usr/bin/env python3
"""
Install Playwright Chromium browser
"""
import subprocess
import sys

print("=" * 60)
print("Installing Playwright Chromium Browser")
print("=" * 60)
print()
print("This will download ~150-200 MB")
print("Please wait, this may take 2-5 minutes...")
print()

try:
    # Run playwright install
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        print()
        print("=" * 60)
        print("✓ SUCCESS! Chromium installed successfully")
        print("=" * 60)
        print()
        print("Now you can run:")
        print("  python Skills/whatsapp_watcher.py auth")
    else:
        print()
        print("=" * 60)
        print("✗ Installation failed")
        print("=" * 60)
        print()
        print("Try running manually:")
        print("  python -m playwright install chromium")
        
except Exception as e:
    print(f"Error: {e}")
    print()
    print("Try running manually in a new terminal:")
    print("  python -m playwright install chromium")
