#!/usr/bin/env python3
"""
Check Bronze and Silver Tier Status
"""

from pathlib import Path

def check_bronze_tier():
    """Check Bronze Tier requirements"""
    print("=" * 60)
    print("BRONZE TIER STATUS")
    print("=" * 60)
    
    checks = {
        "Dashboard.md": Path("Dashboard.md").exists(),
        "Company_Handbook.md": Path("Company_Handbook.md").exists(),
        "Inbox folder": Path("Inbox").exists(),
        "Needs_Action folder": Path("Needs_Action").exists(),
        "Done folder": Path("Done").exists(),
        "Plans folder": Path("Plans").exists(),
        "Pending_Approval folder": Path("Pending_Approval").exists(),
        "Gmail Watcher": Path("Skills/gmail_watcher.py").exists(),
        "Base Watcher": Path("Skills/base_watcher.py").exists(),
        "Claude Agent": Path("Skills/claude_agent.py").exists(),
        "Vault Manager": Path("Skills/vault_manager.py").exists(),
        "Agent Skills folder": Path("Skills/agent_skills").exists(),
        "base_skill.py": Path("Skills/agent_skills/base_skill.py").exists(),
        "summarize_task.py": Path("Skills/agent_skills/summarize_task.py").exists(),
        "create_plan.py": Path("Skills/agent_skills/create_plan.py").exists(),
        "draft_reply.py": Path("Skills/agent_skills/draft_reply.py").exists(),
    }
    
    passed = sum(checks.values())
    total = len(checks)
    
    for name, status in checks.items():
        print(f"{'✅' if status else '❌'} {name}")
    
    print(f"\nBronze Tier: {passed}/{total} ({(passed/total)*100:.0f}%)")
    
    if passed == total:
        print("🎉 BRONZE TIER: COMPLETE!")
        return True
    else:
        print("⚠️  BRONZE TIER: INCOMPLETE")
        return False

def check_silver_tier():
    """Check Silver Tier requirements"""
    print("\n" + "=" * 60)
    print("SILVER TIER STATUS")
    print("=" * 60)
    
    # Bronze requirements (must be complete)
    bronze_complete = check_bronze_tier_quick()
    
    # Silver-specific requirements
    checks = {
        "Bronze Tier Complete": bronze_complete,
        "WhatsApp Watcher": Path("Skills/whatsapp_watcher.py").exists(),
        "LinkedIn Watcher": Path("Skills/linkedin_watcher.py").exists() or Path("Skills/linkedin_watcher_simple.py").exists(),
        "Plan Reasoning Loop": Path("Skills/plan_reasoning_loop.py").exists(),
        "Plan Executor": Path("Skills/plan_executor.py").exists(),
        "MCP Servers folder": Path("Skills/mcp_servers").exists(),
        "Base MCP Server": Path("Skills/mcp_servers/base_mcp_server.py").exists(),
        "Email MCP Server": Path("Skills/mcp_servers/email_mcp_server.py").exists(),
        "Approval Workflow": Path("Skills/approval_workflow.py").exists(),
        "Scheduler": Path("Skills/scheduler.py").exists(),
    }
    
    passed = sum(checks.values())
    total = len(checks)
    
    for name, status in checks.items():
        print(f"{'✅' if status else '❌'} {name}")
    
    print(f"\nSilver Tier: {passed}/{total} ({(passed/total)*100:.0f}%)")
    
    if passed == total:
        print("🎉 SILVER TIER: COMPLETE!")
        return True
    elif passed >= total * 0.8:
        print("⚠️  SILVER TIER: ALMOST COMPLETE (80%+)")
        return False
    else:
        print("⚠️  SILVER TIER: IN PROGRESS")
        return False

def check_bronze_tier_quick():
    """Quick bronze tier check"""
    required = [
        Path("Dashboard.md"),
        Path("Company_Handbook.md"),
        Path("Skills/gmail_watcher.py"),
        Path("Skills/agent_skills/base_skill.py"),
    ]
    return all(f.exists() for f in required)

def main():
    print("\n🔍 Checking Tier Status...\n")
    
    bronze = check_bronze_tier()
    silver = check_silver_tier()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if bronze and silver:
        print("✅ BRONZE TIER: COMPLETE")
        print("✅ SILVER TIER: COMPLETE")
        print("\n🎉 Both tiers ready for submission!")
    elif bronze:
        print("✅ BRONZE TIER: COMPLETE")
        print("⚠️  SILVER TIER: IN PROGRESS")
        print("\n📝 Bronze Tier ready to submit!")
        print("💡 Continue working on Silver Tier")
    else:
        print("⚠️  BRONZE TIER: INCOMPLETE")
        print("⚠️  SILVER TIER: NOT READY")
        print("\n🔧 Complete Bronze Tier first")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
