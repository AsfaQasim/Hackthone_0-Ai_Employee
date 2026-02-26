"""
Watcher Test Suite - Gmail and LinkedIn

Tests the Gmail Watcher and LinkedIn Watcher implementations.
"""

import sys
from pathlib import Path

# Add Skills directory to path
skills_dir = Path(__file__).parent / "Skills"
sys.path.insert(0, str(skills_dir))

print("=" * 70)
print("WATCHER TEST SUITE - Gmail & LinkedIn")
print("=" * 70)

# Test results tracking
tests_passed = 0
tests_failed = 0
tests_total = 0

# Use ASCII-safe checkmarks for Windows compatibility
CHECK = "[OK]"
FAIL = "[FAIL]"


def test_import(module_name, import_names):
    """Test importing from a module."""
    global tests_passed, tests_failed, tests_total
    
    print(f"\n{'='*60}")
    print(f"Testing: {module_name}")
    print(f"{'='*60}")
    
    try:
        module = __import__(module_name, fromlist=import_names)
        
        for name in import_names:
            tests_total += 1
            if hasattr(module, name):
                print(f"  {CHECK} {name}")
                tests_passed += 1
            else:
                print(f"  {FAIL} {name} - NOT FOUND")
                tests_failed += 1
        
        return module
    
    except Exception as e:
        print(f"  {FAIL} Failed to import {module_name}: {e}")
        tests_failed += len(import_names)
        tests_total += len(import_names)
        return None


def test_instantiation(class_name, class_obj, config=None):
    """Test class instantiation."""
    global tests_passed, tests_failed, tests_total
    
    tests_total += 1
    try:
        if config:
            instance = class_obj(config)
        else:
            instance = class_obj()
        print(f"  {CHECK} {class_name} instantiation")
        tests_passed += 1
        return instance
    except Exception as e:
        print(f"  {FAIL} {class_name} instantiation failed: {e}")
        tests_failed += 1
        return None


def test_method_exists(instance, method_name):
    """Test if a method exists on an instance."""
    global tests_passed, tests_failed, tests_total
    
    tests_total += 1
    if hasattr(instance, method_name) and callable(getattr(instance, method_name)):
        print(f"  {CHECK} Method: {method_name}()")
        tests_passed += 1
        return True
    else:
        print(f"  {FAIL} Method: {method_name}() - NOT FOUND")
        tests_failed += 1
        return False


# Test 1: Base Watcher
print("\n" + "=" * 70)
print("TEST 1: BASE WATCHER")
print("=" * 70)

base_watcher_module = test_import(
    "Skills.base_watcher",
    ['BaseWatcher', 'WatcherConfig']
)

# Test WatcherConfig instantiation
if base_watcher_module:
    from Skills.base_watcher import WatcherConfig
    config = test_instantiation('WatcherConfig', WatcherConfig)

# Test 2: Gmail Watcher
print("\n" + "=" * 70)
print("TEST 2: GMAIL WATCHER")
print("=" * 70)

gmail_watcher_module = test_import(
    "Skills.gmail_watcher",
    ['GmailWatcher', 'GmailWatcherConfig']
)

# Test GmailWatcherConfig instantiation
if gmail_watcher_module:
    from Skills.gmail_watcher import GmailWatcherConfig, GmailWatcher
    gmail_config = test_instantiation('GmailWatcherConfig', GmailWatcherConfig)
    
    # Test GmailWatcher instantiation
    if gmail_config:
        gmail_watcher = test_instantiation('GmailWatcher', GmailWatcher, gmail_config)
        
        # Test required methods exist
        if gmail_watcher:
            print(f"\n  Testing GmailWatcher methods:")
            test_method_exists(gmail_watcher, 'authenticate')
            test_method_exists(gmail_watcher, 'fetch_unread_emails')
            test_method_exists(gmail_watcher, 'get_email_content')
            test_method_exists(gmail_watcher, 'is_important')
            test_method_exists(gmail_watcher, 'detect_priority')
            test_method_exists(gmail_watcher, 'generate_markdown')
            test_method_exists(gmail_watcher, 'create_markdown_file')
            test_method_exists(gmail_watcher, 'poll_once')
            test_method_exists(gmail_watcher, 'start_polling')

# Test 3: LinkedIn Watcher
print("\n" + "=" * 70)
print("TEST 3: LINKEDIN WATCHER")
print("=" * 70)

linkedin_watcher_module = test_import(
    "Skills.linkedin_watcher",
    ['LinkedInWatcher', 'LinkedInWatcherConfig']
)

# Test LinkedInWatcherConfig instantiation
if linkedin_watcher_module:
    from Skills.linkedin_watcher import LinkedInWatcherConfig, LinkedInWatcher
    linkedin_config = test_instantiation('LinkedInWatcherConfig', LinkedInWatcherConfig)
    
    # Test LinkedInWatcher instantiation
    if linkedin_config:
        linkedin_watcher = test_instantiation('LinkedInWatcher', LinkedInWatcher, linkedin_config)
        
        # Test required methods exist
        if linkedin_watcher:
            print(f"\n  Testing LinkedInWatcher methods:")
            test_method_exists(linkedin_watcher, 'authenticate')
            test_method_exists(linkedin_watcher, 'check_for_new_items')
            test_method_exists(linkedin_watcher, 'get_item_content')
            test_method_exists(linkedin_watcher, 'is_important')
            test_method_exists(linkedin_watcher, 'detect_priority')
            test_method_exists(linkedin_watcher, 'generate_markdown')
            test_method_exists(linkedin_watcher, 'poll_once')
            test_method_exists(linkedin_watcher, 'start')

# Test 4: Watcher Inheritance
print("\n" + "=" * 70)
print("TEST 4: WATCHER INHERITANCE")
print("=" * 70)

try:
    # Import from modules directly
    import Skills.base_watcher
    import Skills.gmail_watcher
    import Skills.linkedin_watcher
    
    tests_total += 1
    # Check if GmailWatcher has BaseWatcher in its MRO (Method Resolution Order)
    if Skills.base_watcher.BaseWatcher in Skills.gmail_watcher.GmailWatcher.__mro__:
        print(f"  {CHECK} GmailWatcher inherits from BaseWatcher")
        tests_passed += 1
    else:
        print(f"  {FAIL} GmailWatcher does not inherit from BaseWatcher")
        tests_failed += 1
    
    tests_total += 1
    if Skills.base_watcher.BaseWatcher in Skills.linkedin_watcher.LinkedInWatcher.__mro__:
        print(f"  {CHECK} LinkedInWatcher inherits from BaseWatcher")
        tests_passed += 1
    else:
        print(f"  {FAIL} LinkedInWatcher does not inherit from BaseWatcher")
        tests_failed += 1
        
except Exception as e:
    print(f"  {FAIL} Inheritance tests failed: {e}")
    tests_failed += 2

# Test 5: Configuration Files
print("\n" + "=" * 70)
print("TEST 5: CONFIGURATION FILES")
print("=" * 70)

# Check for Gmail watcher config
gmail_config_path = Path("Skills/config/gmail_watcher_config.yaml")
tests_total += 1
if gmail_config_path.exists():
    print(f"  {CHECK} Gmail watcher config exists: {gmail_config_path}")
    tests_passed += 1
else:
    print(f"  {FAIL} Gmail watcher config not found: {gmail_config_path}")
    tests_failed += 1
    print(f"      Creating default config...")
    # Create default config
    gmail_config_path.parent.mkdir(parents=True, exist_ok=True)
    default_config = """# Gmail Watcher Configuration

pollingIntervalMs: 300000  # 5 minutes

importanceCriteria:
  senderWhitelist: []
  keywordPatterns:
    - "urgent"
    - "important"
    - "action required"
  requiredLabels:
    - "IMPORTANT"
    - "STARRED"
  logicMode: "OR"

priorityRules:
  highPriorityKeywords:
    - "urgent"
    - "asap"
    - "critical"
    - "emergency"
  vipSenders: []
  highPriorityLabels:
    - "IMPORTANT"
    - "STARRED"
  mediumPriorityKeywords:
    - "follow up"
    - "reminder"
    - "deadline"

rateLimitConfig:
  maxRequestsPerMinute: 60
  initialBackoffMs: 1000
  maxBackoffMs: 60000
  backoffMultiplier: 2

needsActionFolder: "Needs_Action"
pendingApprovalFolder: "Pending_Approval"
logFolder: "Logs/gmail_watcher"
credentialsPath: "config/gmail-credentials.json"
tokenPath: "config/gmail-token.json"
indexPath: ".index/gmail-watcher-processed.json"
markAsRead: false
useApprovalWorkflow: true
"""
    gmail_config_path.write_text(default_config)
    print(f"      Created default config at {gmail_config_path}")

# Test 6: Directory Structure
print("\n" + "=" * 70)
print("TEST 6: DIRECTORY STRUCTURE")
print("=" * 70)

required_dirs = [
    "Inbox",
    "Needs_Action",
    "Done",
    "Plans",
    "Pending_Approval",
    "config",
    ".index",
    "Logs"
]

for dir_name in required_dirs:
    tests_total += 1
    dir_path = Path(dir_name)
    if dir_path.exists() and dir_path.is_dir():
        print(f"  {CHECK} {dir_name}/")
        tests_passed += 1
    else:
        print(f"  {FAIL} {dir_name}/ - NOT FOUND")
        tests_failed += 1
        # Create missing directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"      Created {dir_name}/")

# Test 7: Dependencies Check
print("\n" + "=" * 70)
print("TEST 7: DEPENDENCIES CHECK")
print("=" * 70)

dependencies = {
    'google-auth': 'google.auth',
    'google-auth-oauthlib': 'google_auth_oauthlib',
    'google-api-python-client': 'googleapiclient',
    'pyyaml': 'yaml',
    'html2text': 'html2text',
    'requests': 'requests'
}

for package_name, import_name in dependencies.items():
    tests_total += 1
    try:
        __import__(import_name)
        print(f"  {CHECK} {package_name}")
        tests_passed += 1
    except ImportError:
        print(f"  {FAIL} {package_name} - NOT INSTALLED")
        tests_failed += 1

# Final Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"\nTotal Tests: {tests_total}")
print(f"Passed: {tests_passed} [OK]")
print(f"Failed: {tests_failed} [FAIL]")
print(f"Success Rate: {(tests_passed/tests_total*100):.1f}%")

if tests_failed == 0:
    print("\n[OK] ALL TESTS PASSED! WATCHERS ARE READY!")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Gmail Watcher:")
    print("   python Skills/gmail_watcher.py auth")
    print("   python Skills/gmail_watcher.py poll")
    print("\n2. LinkedIn Watcher:")
    print("   Set LINKEDIN_ACCESS_TOKEN environment variable")
    print("   python Skills/linkedin_watcher.py auth")
    print("   python Skills/linkedin_watcher.py poll")
else:
    print("\n[WARN] Some tests failed. Please review the errors above.")
    print("=" * 70)
    print("\nTroubleshooting:")
    print("1. Install missing dependencies:")
    print("   pip install google-auth google-auth-oauthlib google-api-python-client pyyaml html2text requests")
    print("2. Ensure you're in the project root directory")
    print("3. Check that configuration files exist")

print("\n" + "=" * 70)

# Exit with appropriate code
sys.exit(0 if tests_failed == 0 else 1)
