#!/usr/bin/env python3
"""
Quick Bronze Tier Verification Script
Verifies that all Bronze Tier requirements are met.
"""

from pathlib import Path
import sys

def check_component(name, condition, details=""):
    """Check a component and print result."""
    status = "✅ PASS" if condition else "❌ FAIL"
    print(f"{status} {name}")
    if details and not condition:
        print(f"    {details}")
    return condition

def main():
    print("🔍 Bronze Tier Verification")
    print("=" * 50)
    
    checks = []
    
    # 1. Vault Structure
    print("\n📁 Vault Structure:")
    folders = ["Inbox", "Needs_Action", "Done", "Plans", "Pending_Approval"]
    for folder in folders:
        exists = Path(folder).exists()
        checks.append(check_component(f"{folder}/", exists))
    
    # 2. Dashboard Files
    print("\n📄 Dashboard Files:")
    files = ["Dashboard.md", "Company_Handbook.md"]
    for file in files:
        exists = Path(file).exists()
        checks.append(check_component(file, exists))
    
    # 3. Watcher Scripts
    print("\n👁️ Watcher Scripts:")
    watchers = [
        "Skills/gmail_watcher.py",
        "Skills/base_watcher.py"
    ]
    watcher_exists = False
    for watcher in watchers:
        exists = Path(watcher).exists()
        if exists:
            watcher_exists = True
        check_component(watcher, exists)
    checks.append(watcher_exists)
    
    # 4. Claude Integration
    print("\n🤖 Claude Integration:")
    claude_files = [
        "Skills/claude_agent.py",
        "Skills/vault_manager.py"
    ]
    claude_exists = False
    for file in claude_files:
        exists = Path(file).exists()
        if exists:
            claude_exists = True
        check_component(file, exists)
    checks.append(claude_exists)
    
    # 5. Agent Skills
    print("\n🛠️ Agent Skills:")
    skills_dir = Path("Skills/agent_skills")
    skills_exists = skills_dir.exists()
    check_component("Skills/agent_skills/", skills_exists)
    
    if skills_exists:
        skills = [
            "base_skill.py",
            "summarize_task.py", 
            "create_plan.py",
            "draft_reply.py",
            "generate_linkedin_post.py"
        ]
        skill_count = 0
        for skill in skills:
            exists = (skills_dir / skill).exists()
            if exists:
                skill_count += 1
            check_component(f"  {skill}", exists)
        checks.append(skill_count >= 4)  # Need at least 4 skills
    else:
        checks.append(False)
    
    # 6. Configuration
    print("\n⚙️ Configuration:")
    config_files = [".env.example", "requirements.txt"]
    for file in config_files:
        exists = Path(file).exists()
        checks.append(check_component(file, exists))
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    percentage = (passed / total) * 100
    
    print(f"📊 Results: {passed}/{total} checks passed ({percentage:.0f}%)")
    
    if percentage == 100:
        print("🎉 BRONZE TIER COMPLETE!")
        print("\nYour AI Employee system is ready!")
        print("\nNext steps:")
        print("1. Test Gmail Watcher: python Skills/gmail_watcher.py auth")
        print("2. Test vault operations: python Skills/vault_manager.py verify")
        print("3. Move to Silver Tier requirements")
        return 0
    elif percentage >= 80:
        print("⚠️ BRONZE TIER ALMOST COMPLETE")
        print(f"\nYou're {percentage:.0f}% done with Bronze Tier!")
        return 1
    else:
        print("❌ BRONZE TIER INCOMPLETE")
        print(f"\nYou need to complete more components ({percentage:.0f}% done)")
        return 1

if __name__ == "__main__":
    sys.exit(main())