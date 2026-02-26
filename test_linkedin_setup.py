"""
LinkedIn Watcher Quick Test

Tests LinkedIn Watcher setup and functionality.
"""

import sys
import os
from pathlib import Path
import codecs

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Use ASCII-safe symbols
CHECK = "[OK]"
FAIL = "[FAIL]"
SKIP = "[SKIP]"
INFO = "[INFO]"

# Add Skills directory to path
sys.path.insert(0, str(Path(__file__).parent / "Skills"))

print("="*70)
print("LINKEDIN WATCHER - QUICK TEST")
print("="*70)

# Test 1: Check environment variable
print("\n[TEST 1] Checking LINKEDIN_ACCESS_TOKEN...")
token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")

if not token:
    print(f"  {FAIL} LINKEDIN_ACCESS_TOKEN not set")
    print("\n  {INFO} Set the token:")
    print("     set LINKEDIN_ACCESS_TOKEN=your_token_here")
    print("\n  Or run: python get_linkedin_token.py")
    test1_pass = False
else:
    print(f"  {CHECK} Token found: {token[:20]}...{token[-10:]}")
    test1_pass = True

# Test 2: Import LinkedIn Watcher
print("\n[TEST 2] Importing LinkedIn Watcher...")
try:
    from Skills.linkedin_watcher import LinkedInWatcher, LinkedInWatcherConfig
    print(f"  {CHECK} Import successful")
    test2_pass = True
except Exception as e:
    print(f"  {FAIL} Import failed: {e}")
    test2_pass = False

# Test 3: Create configuration
print("\n[TEST 3] Creating configuration...")
if test1_pass and test2_pass:
    try:
        config = LinkedInWatcherConfig(
            access_token=token,
            vault_path=".",
            dry_run=True
        )
        print(f"  {CHECK} Configuration created")
        print(f"     - Vault: {config.vault_path}")
        print(f"     - Polling: {config.polling_interval_ms}ms")
        print(f"     - Monitor messages: {config.monitor_messages}")
        test3_pass = True
    except Exception as e:
        print(f"  {FAIL} Configuration failed: {e}")
        test3_pass = False
else:
    print(f"  {SKIP} Skipped (previous tests failed)")
    test3_pass = False

# Test 4: Create watcher instance
print("\n[TEST 4] Creating watcher instance...")
if test3_pass:
    try:
        watcher = LinkedInWatcher(config)
        print(f"  {CHECK} Watcher created")
        test4_pass = True
    except Exception as e:
        print(f"  {FAIL} Watcher creation failed: {e}")
        test4_pass = False
else:
    print(f"  {SKIP} Skipped (previous tests failed)")
    test4_pass = False

# Test 5: Check methods
print("\n[TEST 5] Checking watcher methods...")
if test4_pass:
    methods = [
        'authenticate',
        'check_for_new_items',
        'get_item_content',
        'is_important',
        'detect_priority',
        'generate_markdown',
        'poll_once',
        'start'
    ]
    
    all_present = True
    for method in methods:
        if hasattr(watcher, method) and callable(getattr(watcher, method)):
            print(f"  {CHECK} {method}()")
        else:
            print(f"  {FAIL} {method}() - MISSING")
            all_present = False
    
    test5_pass = all_present
else:
    print(f"  {SKIP} Skipped (previous tests failed)")
    test5_pass = False

# Test 6: Authentication test (optional)
print("\n[TEST 6] Testing authentication...")
if test4_pass:
    print("\n  [INFO] This will attempt to authenticate with LinkedIn API")
    print("     Press Ctrl+C to skip")
    
    try:
        import time
        start = time.time()
        auth_result = watcher.authenticate()
        elapsed = time.time() - start
        
        if auth_result:
            print(f"  {CHECK} Authentication successful ({elapsed:.2f}s)")
            test6_pass = True
        else:
            print(f"  {FAIL} Authentication failed ({elapsed:.2f}s)")
            print("\n  [INFO] Possible issues:")
            print("     - Invalid access token")
            print("     - Token expired")
            print("     - Network connection issue")
            print("\n  Try getting a new token:")
            print("     python get_linkedin_token.py")
            test6_pass = False
    except KeyboardInterrupt:
        print("\n  {SKIP} Skipped by user")
        test6_pass = None
    except Exception as e:
        print(f"  {FAIL} Authentication error: {e}")
        test6_pass = False
else:
    print(f"  {SKIP} Skipped (previous tests failed)")
    test6_pass = None

# Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

tests = [
    ("Environment Variable", test1_pass),
    ("Import", test2_pass),
    ("Configuration", test3_pass),
    ("Watcher Instance", test4_pass),
    ("Methods", test5_pass),
    ("Authentication", test6_pass)
]

passed = sum(1 for _, result in tests if result is True)
failed = sum(1 for _, result in tests if result is False)
skipped = sum(1 for _, result in tests if result is None)
total = len(tests)

print(f"\nTotal: {total} tests")
print(f"Passed: {passed} {CHECK}")
print(f"Failed: {failed} {FAIL}")
print(f"Skipped: {skipped} {SKIP}")

if failed == 0 and passed > 0:
    print("\n[SUCCESS] LinkedIn Watcher is ready!")
    print("\n[INFO] Next Steps:")
    print("   1. Test polling: python Skills/linkedin_watcher.py poll")
    print("   2. Start monitoring: python Skills/linkedin_watcher.py start")
    print("   3. Integrate with AI: process_all_channels(linkedin_enabled=True)")
elif failed > 0:
    print("\n[WARNING] Some tests failed. Please review the errors above.")
    print("\n[INFO] Troubleshooting:")
    if not test1_pass:
        print("   - Set LINKEDIN_ACCESS_TOKEN environment variable")
        print("   - Or run: python get_linkedin_token.py")
    if not test2_pass:
        print("   - Check that requests library is installed: pip install requests")
    if test6_pass is False:
        print("   - Get a new access token: python get_linkedin_token.py")
        print("   - Check your internet connection")

print("\n" + "="*70)

# Exit code
sys.exit(0 if failed == 0 else 1)
