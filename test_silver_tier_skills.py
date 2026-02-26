"""
Silver Tier Skills - Test Suite

Tests all Silver Tier skills to ensure they are properly implemented and importable.
"""

import sys
from pathlib import Path

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add Skills directory to path
skills_dir = Path(__file__).parent / "Skills"
sys.path.insert(0, str(skills_dir))

print("=" * 70)
print("SILVER TIER SKILLS - TEST SUITE")
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


# Test 1: Core Agent Skills
print("\n" + "=" * 70)
print("TEST 1: CORE AGENT SKILLS")
print("=" * 70)

core_skills_module = test_import(
    "Skills.agent_skills",
    [
        'summarize_task',
        'create_plan',
        'draft_reply',
        'generate_linkedin_post'
    ]
)

# Test 2: Integration Skills
print("\n" + "=" * 70)
print("TEST 2: INTEGRATION SKILLS")
print("=" * 70)

integration_skills_module = test_import(
    "Skills.agent_skills",
    [
        'process_whatsapp_messages',
        'process_gmail_messages',
        'auto_post_social_media',
        'approve_and_post'
    ]
)

# Test 3: Coordination Skills
print("\n" + "=" * 70)
print("TEST 3: COORDINATION SKILLS")
print("=" * 70)

coordination_skills_module = test_import(
    "Skills.agent_skills",
    [
        'process_all_channels'
    ]
)

# Test 4: MCP Servers
print("\n" + "=" * 70)
print("TEST 4: MCP SERVERS")
print("=" * 70)

mcp_servers_module = test_import(
    "Skills.mcp_servers",
    [
        'BaseMCPServer',
        'EmailMCPServer',
        'WhatsAppMCPServer',
        'SocialMediaMCPServer'
    ]
)

# Test 5: Base Classes
print("\n" + "=" * 70)
print("TEST 5: BASE CLASSES")
print("=" * 70)

base_classes_module = test_import(
    "Skills.agent_skills.base_skill",
    [
        'BaseSkill',
        'AIModelClient'
    ]
)

# Test 6: Individual Skill Modules
print("\n" + "=" * 70)
print("TEST 6: INDIVIDUAL SKILL MODULES")
print("=" * 70)

individual_modules = [
    ("Skills.agent_skills.summarize_task", ["summarize_task", "SummarizeTaskSkill"]),
    ("Skills.agent_skills.create_plan", ["create_plan", "CreatePlanSkill"]),
    ("Skills.agent_skills.draft_reply", ["draft_reply", "DraftReplySkill"]),
    ("Skills.agent_skills.generate_linkedin_post", ["generate_linkedin_post", "GenerateLinkedInPostSkill"]),
    ("Skills.agent_skills.process_whatsapp_messages", ["process_whatsapp_messages", "ProcessWhatsAppMessagesSkill"]),
    ("Skills.agent_skills.process_gmail_messages", ["process_gmail_messages", "ProcessGmailMessagesSkill"]),
    ("Skills.agent_skills.auto_post_social_media", ["auto_post_social_media", "approve_and_post", "AutoPostSocialMediaSkill"]),
    ("Skills.agent_skills.process_all_channels", ["process_all_channels", "ProcessAllChannelsSkill"]),
]

for module_name, import_names in individual_modules:
    test_import(module_name, import_names)

# Test 7: MCP Server Modules
print("\n" + "=" * 70)
print("TEST 7: MCP SERVER MODULES")
print("=" * 70)

mcp_modules = [
    ("Skills.mcp_servers.base_mcp_server", ["BaseMCPServer", "Tool", "TextContent"]),
    ("Skills.mcp_servers.email_mcp_server", ["EmailMCPServer"]),
    ("Skills.mcp_servers.whatsapp_mcp_server", ["WhatsAppMCPServer"]),
    ("Skills.mcp_servers.social_media_mcp_server", ["SocialMediaMCPServer"]),
]

for module_name, import_names in mcp_modules:
    test_import(module_name, import_names)

# Test 8: Skill Instantiation
print("\n" + "=" * 70)
print("TEST 8: SKILL INSTANTIATION")
print("=" * 70)

try:
    from Skills.agent_skills.base_skill import BaseSkill, AIModelClient
    
    tests_total += 1
    try:
        client = AIModelClient(model_name="gpt-4")
        print(f"  {CHECK} AIModelClient instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  {FAIL} AIModelClient instantiation failed: {e}")
        tests_failed += 1
    
    tests_total += 1
    try:
        skill = BaseSkill(model_name="gpt-4")
        print(f"  {CHECK} BaseSkill instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  {FAIL} BaseSkill instantiation failed: {e}")
        tests_failed += 1
        
except Exception as e:
    print(f"  {FAIL} Base class tests failed: {e}")
    tests_failed += 2

# Test 9: MCP Server Instantiation
print("\n" + "=" * 70)
print("TEST 9: MCP SERVER INSTANTIATION")
print("=" * 70)

try:
    from Skills.mcp_servers.email_mcp_server import EmailMCPServer
    from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer
    from Skills.mcp_servers.social_media_mcp_server import SocialMediaMCPServer
    
    tests_total += 1
    try:
        server = EmailMCPServer()
        print(f"  {CHECK} EmailMCPServer instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  {FAIL} EmailMCPServer instantiation failed: {e}")
        tests_failed += 1
    
    tests_total += 1
    try:
        server = WhatsAppMCPServer()
        print(f"  {CHECK} WhatsAppMCPServer instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  {FAIL} WhatsAppMCPServer instantiation failed: {e}")
        tests_failed += 1
    
    tests_total += 1
    try:
        server = SocialMediaMCPServer()
        print(f"  {CHECK} SocialMediaMCPServer instantiation")
        tests_passed += 1
    except Exception as e:
        print(f"  {FAIL} SocialMediaMCPServer instantiation failed: {e}")
        tests_failed += 1
        
except Exception as e:
    print(f"  {FAIL} MCP Server tests failed: {e}")
    tests_failed += 3

# Test 10: Tool Registration
print("\n" + "=" * 70)
print("TEST 10: TOOL REGISTRATION")
print("=" * 70)

try:
    from Skills.mcp_servers.email_mcp_server import EmailMCPServer
    from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer
    from Skills.mcp_servers.social_media_mcp_server import SocialMediaMCPServer
    
    tests_total += 1
    try:
        server = EmailMCPServer()
        tools = server.list_tools()
        if len(tools) > 0:
            print(f"  {CHECK} EmailMCPServer tools registered: {len(tools)} tools")
            tests_passed += 1
        else:
            print(f"  {FAIL} EmailMCPServer no tools registered")
            tests_failed += 1
    except Exception as e:
        print(f"  {FAIL} EmailMCPServer tool registration failed: {e}")
        tests_failed += 1
    
    tests_total += 1
    try:
        server = WhatsAppMCPServer()
        tools = server.list_tools()
        if len(tools) > 0:
            print(f"  {CHECK} WhatsAppMCPServer tools registered: {len(tools)} tools")
            tests_passed += 1
        else:
            print(f"  {FAIL} WhatsAppMCPServer no tools registered")
            tests_failed += 1
    except Exception as e:
        print(f"  {FAIL} WhatsAppMCPServer tool registration failed: {e}")
        tests_failed += 1
    
    tests_total += 1
    try:
        server = SocialMediaMCPServer()
        tools = server.list_tools()
        if len(tools) > 0:
            print(f"  {CHECK} SocialMediaMCPServer tools registered: {len(tools)} tools")
            tests_passed += 1
        else:
            print(f"  {FAIL} SocialMediaMCPServer no tools registered")
            tests_failed += 1
    except Exception as e:
        print(f"  {FAIL} SocialMediaMCPServer tool registration failed: {e}")
        tests_failed += 1
        
except Exception as e:
    print(f"  {FAIL} Tool registration tests failed: {e}")
    tests_failed += 3

# Final Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"\nTotal Tests: {tests_total}")
print(f"Passed: {tests_passed} [OK]")
print(f"Failed: {tests_failed} [FAIL]")
print(f"Success Rate: {(tests_passed/tests_total*100):.1f}%")

if tests_failed == 0:
    print("\n[OK] ALL TESTS PASSED! SILVER TIER SKILLS ARE READY!")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Set up API keys (OPENAI_API_KEY)")
    print("2. Configure Gmail OAuth (python Skills/gmail_watcher.py auth)")
    print("3. Configure WhatsApp session (python Skills/whatsapp_watcher.py auth)")
    print("4. Test end-to-end workflows")
    print("5. Move to Gold Tier!")
else:
    print("\n[WARN] Some tests failed. Please review the errors above.")
    print("=" * 70)
    print("\nTroubleshooting:")
    print("1. Ensure you're in the project root directory")
    print("2. Check that all dependencies are installed")
    print("3. Verify PYTHONPATH includes the Skills directory")

print("\n" + "=" * 70)

# Exit with appropriate code
sys.exit(0 if tests_failed == 0 else 1)
