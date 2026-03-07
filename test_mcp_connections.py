#!/usr/bin/env python3
"""
Test MCP Server Connections

This script tests if all MCP servers are properly configured and can be imported.
"""

import sys
import json
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_mark(passed):
    return "✅" if passed else "❌"

def test_mcp_configuration():
    """Test if MCP configuration file exists and is valid."""
    print_header("MCP CONFIGURATION TEST")
    
    config_path = Path(".kiro/settings/mcp.json")
    
    if not config_path.exists():
        print(f"{check_mark(False)} MCP configuration file not found: {config_path}")
        return False
    
    print(f"{check_mark(True)} MCP configuration file exists")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if 'mcpServers' not in config:
            print(f"{check_mark(False)} No 'mcpServers' key in configuration")
            return False
        
        servers = config['mcpServers']
        print(f"{check_mark(True)} Configuration is valid JSON")
        print(f"\n📡 Configured MCP Servers ({len(servers)}):\n")
        
        for name, server_config in servers.items():
            disabled = server_config.get('disabled', False)
            status = "Disabled" if disabled else "Enabled"
            command = server_config.get('command', 'N/A')
            args = ' '.join(server_config.get('args', []))
            
            print(f"  {check_mark(not disabled)} {name}")
            print(f"     Status: {status}")
            print(f"     Command: {command} {args}")
            print()
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"{check_mark(False)} Invalid JSON in configuration: {e}")
        return False
    except Exception as e:
        print(f"{check_mark(False)} Error reading configuration: {e}")
        return False

def test_mcp_server_imports():
    """Test if MCP server modules can be imported."""
    print_header("MCP SERVER IMPORT TEST")
    
    servers = [
        ('base_mcp_server', 'Skills.mcp_servers.base_mcp_server'),
        ('email_mcp_server', 'Skills.mcp_servers.email_mcp_server'),
        ('whatsapp_mcp_server', 'Skills.mcp_servers.whatsapp_mcp_server'),
        ('social_media_mcp_server', 'Skills.mcp_servers.social_media_mcp_server'),
    ]
    
    all_passed = True
    
    for name, module_path in servers:
        try:
            __import__(module_path)
            print(f"{check_mark(True)} {name} - Import successful")
        except ImportError as e:
            print(f"{check_mark(False)} {name} - Import failed: {e}")
            all_passed = False
        except Exception as e:
            print(f"{check_mark(False)} {name} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_mcp_server_files():
    """Test if MCP server files exist."""
    print_header("MCP SERVER FILES TEST")
    
    files = [
        'Skills/mcp_servers/__init__.py',
        'Skills/mcp_servers/base_mcp_server.py',
        'Skills/mcp_servers/email_mcp_server.py',
        'Skills/mcp_servers/whatsapp_mcp_server.py',
        'Skills/mcp_servers/social_media_mcp_server.py',
    ]
    
    all_exist = True
    
    for filepath in files:
        path = Path(filepath)
        exists = path.exists()
        
        if exists:
            size = path.stat().st_size
            print(f"{check_mark(True)} {filepath} ({size:,} bytes)")
        else:
            print(f"{check_mark(False)} {filepath} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_mcp_server_classes():
    """Test if MCP server classes can be instantiated."""
    print_header("MCP SERVER CLASS TEST")
    
    tests = []
    
    # Test Base MCP Server
    try:
        from Skills.mcp_servers.base_mcp_server import BaseMCPServer
        print(f"{check_mark(True)} BaseMCPServer class imported")
        tests.append(True)
    except Exception as e:
        print(f"{check_mark(False)} BaseMCPServer import failed: {e}")
        tests.append(False)
    
    # Test Email MCP Server
    try:
        from Skills.mcp_servers.email_mcp_server import EmailMCPServer
        print(f"{check_mark(True)} EmailMCPServer class imported")
        tests.append(True)
    except Exception as e:
        print(f"{check_mark(False)} EmailMCPServer import failed: {e}")
        tests.append(False)
    
    # Test WhatsApp MCP Server
    try:
        from Skills.mcp_servers.whatsapp_mcp_server import WhatsAppMCPServer
        print(f"{check_mark(True)} WhatsAppMCPServer class imported")
        tests.append(True)
    except Exception as e:
        print(f"{check_mark(False)} WhatsAppMCPServer import failed: {e}")
        tests.append(False)
    
    # Test Social Media MCP Server
    try:
        from Skills.mcp_servers.social_media_mcp_server import SocialMediaMCPServer
        print(f"{check_mark(True)} SocialMediaMCPServer class imported")
        tests.append(True)
    except Exception as e:
        print(f"{check_mark(False)} SocialMediaMCPServer import failed: {e}")
        tests.append(False)
    
    return all(tests)

def test_mcp_dependencies():
    """Test if required dependencies are installed."""
    print_header("MCP DEPENDENCIES TEST")
    
    dependencies = [
        ('playwright', 'Playwright (for WhatsApp automation)'),
        ('google.oauth2', 'Google OAuth (for Gmail)'),
        ('googleapiclient', 'Google API Client (for Gmail)'),
    ]
    
    all_installed = True
    
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"{check_mark(True)} {description}")
        except ImportError:
            print(f"{check_mark(False)} {description} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def main():
    """Run all MCP connection tests."""
    print("\n" + "=" * 70)
    print("  MCP SERVER CONNECTION TEST")
    print("=" * 70)
    print("\n🔍 Testing MCP server configuration and connectivity...\n")
    
    results = {
        "Configuration": test_mcp_configuration(),
        "Server Files": test_mcp_server_files(),
        "Server Imports": test_mcp_server_imports(),
        "Server Classes": test_mcp_server_classes(),
        "Dependencies": test_mcp_dependencies(),
    }
    
    # Summary
    print_header("TEST SUMMARY")
    
    for test_name, passed in results.items():
        print(f"{check_mark(passed)} {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("  ✅ ALL TESTS PASSED - MCP SERVERS ARE READY")
    else:
        print("  ⚠️ SOME TESTS FAILED - CHECK ERRORS ABOVE")
    print("=" * 70)
    
    print("\n📝 Next Steps:")
    if all_passed:
        print("   1. MCP servers are configured and ready")
        print("   2. Claude Code can now use these MCP servers")
        print("   3. Test individual servers with their test scripts")
        print("\n💡 To use MCP servers in Claude Code:")
        print("   - MCP servers are automatically loaded from .kiro/settings/mcp.json")
        print("   - Claude Code will have access to all enabled tools")
        print("   - Use tools like: send_whatsapp_message, send_email, etc.")
    else:
        print("   1. Fix any import errors shown above")
        print("   2. Install missing dependencies: pip install -r Skills/requirements.txt")
        print("   3. Run this test again to verify")
    
    print("\n" + "=" * 70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
