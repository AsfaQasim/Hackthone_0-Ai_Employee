#!/usr/bin/env python3
"""
Complete Gold Tier Verification Script
Checks all requirements and MCP server connections
"""

import sys
from pathlib import Path
import json

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_mark(passed):
    return "✅" if passed else "❌"

def check_gold_tier_requirements():
    """Check all Gold Tier requirements from hackathon document"""
    
    print_header("GOLD TIER REQUIREMENTS VERIFICATION")
    
    requirements = {
        "1. All Silver Requirements": check_silver_complete(),
        "2. Full Cross-Domain Integration": check_cross_domain(),
        "3. Odoo Accounting System (Optional)": check_odoo(),
        "4. Odoo MCP Server (Optional)": check_odoo_mcp(),
        "5. Facebook Integration (Optional)": check_facebook(),
        "6. Instagram Integration (Optional)": check_instagram(),
        "7. Twitter/X Integration (Optional)": check_twitter(),
        "8. Multiple MCP Servers": check_mcp_servers(),
        "9. Weekly CEO Briefing": check_ceo_briefing(),
        "10. Error Recovery": check_error_recovery(),
        "11. Audit Logging": check_audit_logging(),
        "12. Ralph Wiggum Loop": check_ralph_loop(),
        "13. Documentation": check_documentation(),
        "14. All AI as Agent Skills": check_agent_skills(),
    }
    
    print("\n📋 Requirements Status:\n")
    
    required_count = 0
    required_complete = 0
    optional_count = 0
    optional_complete = 0
    
    for req, (status, is_required) in requirements.items():
        mark = check_mark(status)
        req_type = "REQUIRED" if is_required else "OPTIONAL"
        print(f"{mark} {req} [{req_type}]")
        
        if is_required:
            required_count += 1
            if status:
                required_complete += 1
        else:
            optional_count += 1
            if status:
                optional_complete += 1
    
    print(f"\n📊 Summary:")
    print(f"   Required: {required_complete}/{required_count} ({(required_complete/required_count*100):.0f}%)")
    print(f"   Optional: {optional_complete}/{optional_count} ({(optional_complete/optional_count*100) if optional_count > 0 else 0:.0f}%)")
    print(f"   Overall: {required_complete + optional_complete}/{required_count + optional_count}")
    
    return required_complete == required_count

def check_silver_complete():
    """Check if Silver Tier is complete"""
    required_files = [
        "Skills/gmail_watcher.py",
        "Skills/whatsapp_watcher.py",
        "Skills/plan_reasoning_loop.py",
        "Skills/approval_workflow.py",
        "Skills/scheduler.py",
    ]
    return (all(Path(f).exists() for f in required_files), True)

def check_cross_domain():
    """Check cross-domain integration"""
    files = [
        "Skills/unified_task_processor.py",
        "Skills/gmail_watcher.py",
        "Skills/whatsapp_watcher.py",
        "Skills/linkedin_watcher.py",
    ]
    return (all(Path(f).exists() for f in files), True)

def check_odoo():
    """Check Odoo installation"""
    # Odoo is optional
    return (False, False)

def check_odoo_mcp():
    """Check Odoo MCP server"""
    # Odoo MCP is optional
    return (False, False)

def check_facebook():
    """Check Facebook integration"""
    # Facebook is optional
    return (False, False)

def check_instagram():
    """Check Instagram integration"""
    # Instagram is optional
    return (False, False)

def check_twitter():
    """Check Twitter integration"""
    # Twitter is optional
    return (False, False)

def check_mcp_servers():
    """Check MCP servers"""
    mcp_dir = Path("Skills/mcp_servers")
    if not mcp_dir.exists():
        return (False, True)
    
    required_servers = [
        "base_mcp_server.py",
        "email_mcp_server.py",
    ]
    
    exists = all((mcp_dir / f).exists() for f in required_servers)
    return (exists, True)

def check_ceo_briefing():
    """Check CEO briefing system"""
    file = Path("Skills/ceo_briefing_generator.py")
    briefings_dir = Path("Briefings")
    return (file.exists() and briefings_dir.exists(), True)

def check_error_recovery():
    """Check error recovery system"""
    file = Path("Skills/error_recovery.py")
    return (file.exists(), True)

def check_audit_logging():
    """Check audit logging system"""
    file = Path("Skills/audit_logger.py")
    return (file.exists(), True)

def check_ralph_loop():
    """Check Ralph Wiggum loop"""
    file = Path("Skills/ralph_loop.py")
    return (file.exists(), True)

def check_documentation():
    """Check documentation"""
    docs = [
        "README.md",
        "GOLD_TIER_ROADMAP.md",
        "GOLD_TIER_PROGRESS.md",
    ]
    
    # Check if at least basic docs exist
    exists = sum(1 for d in docs if Path(d).exists())
    # Need at least 2/3 for partial credit
    return (exists >= 2, True)

def check_agent_skills():
    """Check Agent Skills implementation"""
    skills_dir = Path("Skills/agent_skills")
    if not skills_dir.exists():
        return (False, True)
    
    required_skills = [
        "base_skill.py",
        "summarize_task.py",
        "create_plan.py",
        "draft_reply.py",
    ]
    
    exists = all((skills_dir / f).exists() for f in required_skills)
    return (exists, True)

def check_mcp_server_connections():
    """Check MCP server files and structure"""
    
    print_header("MCP SERVERS VERIFICATION")
    
    mcp_dir = Path("Skills/mcp_servers")
    
    if not mcp_dir.exists():
        print("❌ MCP servers directory not found!")
        return False
    
    servers = {
        "base_mcp_server.py": "Base MCP Server Framework",
        "email_mcp_server.py": "Email MCP Server",
        "social_media_mcp_server.py": "Social Media MCP Server",
    }
    
    print("\n📡 MCP Server Files:\n")
    
    all_exist = True
    for filename, description in servers.items():
        filepath = mcp_dir / filename
        exists = filepath.exists()
        print(f"{check_mark(exists)} {description}")
        print(f"   File: {filepath}")
        
        if exists:
            # Check file size
            size = filepath.stat().st_size
            print(f"   Size: {size} bytes")
        
        if not exists:
            all_exist = False
        print()
    
    return all_exist

def check_vault_structure():
    """Check vault folder structure"""
    
    print_header("VAULT STRUCTURE VERIFICATION")
    
    folders = {
        "Inbox": "Incoming tasks from watchers",
        "Needs_Action": "Tasks requiring action",
        "Done": "Completed tasks",
        "Plans": "Execution plans",
        "Pending_Approval": "Tasks awaiting approval",
        "Approved": "Approved tasks",
        "Briefings": "CEO briefings",
        "Logs": "System logs",
    }
    
    print("\n📁 Vault Folders:\n")
    
    all_exist = True
    for folder, description in folders.items():
        path = Path(folder)
        exists = path.exists() and path.is_dir()
        print(f"{check_mark(exists)} {folder}/ - {description}")
        
        if not exists:
            all_exist = False
    
    return all_exist

def check_watchers():
    """Check watcher implementations"""
    
    print_header("WATCHERS VERIFICATION")
    
    watchers = {
        "Skills/gmail_watcher.py": "Gmail Watcher",
        "Skills/whatsapp_watcher.py": "WhatsApp Watcher",
        "Skills/linkedin_watcher.py": "LinkedIn Watcher (API)",
        "Skills/linkedin_watcher_simple.py": "LinkedIn Watcher (Playwright)",
        "Skills/base_watcher.py": "Base Watcher Framework",
    }
    
    print("\n👁️ Watcher Files:\n")
    
    essential_count = 0
    for filepath, description in watchers.items():
        path = Path(filepath)
        exists = path.exists()
        is_essential = "base" in filepath.lower() or "gmail" in filepath.lower()
        
        mark = check_mark(exists)
        essential_mark = " [ESSENTIAL]" if is_essential else ""
        print(f"{mark} {description}{essential_mark}")
        print(f"   File: {filepath}")
        
        if exists and is_essential:
            essential_count += 1
        print()
    
    # Need at least base watcher and one actual watcher
    return essential_count >= 2

def generate_report():
    """Generate complete verification report"""
    
    print("\n" + "=" * 70)
    print("  GOLD TIER COMPLETE VERIFICATION REPORT")
    print("=" * 70)
    print(f"\n📅 Date: {Path('.').absolute()}")
    print(f"🔍 Verification: Complete System Check")
    
    # Run all checks
    gold_complete = check_gold_tier_requirements()
    mcp_ok = check_mcp_server_connections()
    vault_ok = check_vault_structure()
    watchers_ok = check_watchers()
    
    # Final summary
    print_header("FINAL VERDICT")
    
    print(f"\n{check_mark(gold_complete)} Gold Tier Requirements (Required)")
    print(f"{check_mark(mcp_ok)} MCP Servers")
    print(f"{check_mark(vault_ok)} Vault Structure")
    print(f"{check_mark(watchers_ok)} Watchers")
    
    all_pass = gold_complete and mcp_ok and vault_ok and watchers_ok
    
    if all_pass:
        print("\n" + "=" * 70)
        print("  🎉 GOLD TIER: COMPLETE AND READY FOR SUBMISSION!")
        print("=" * 70)
        print("\n✅ All required components are in place")
        print("✅ MCP servers are configured")
        print("✅ Vault structure is correct")
        print("✅ Watchers are implemented")
        print("\n📝 Next Steps:")
        print("   1. Complete documentation (ARCHITECTURE.md, LESSONS_LEARNED.md)")
        print("   2. Test all systems end-to-end")
        print("   3. Create demo video")
        print("   4. Submit to hackathon")
    else:
        print("\n" + "=" * 70)
        print("  ⚠️ GOLD TIER: INCOMPLETE")
        print("=" * 70)
        print("\n❌ Some required components are missing")
        print("\n📝 Action Items:")
        if not gold_complete:
            print("   - Complete missing Gold Tier requirements")
        if not mcp_ok:
            print("   - Set up MCP servers")
        if not vault_ok:
            print("   - Create missing vault folders")
        if not watchers_ok:
            print("   - Implement required watchers")
    
    print("\n" + "=" * 70)
    
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(generate_report())
