"""
Bronze Tier Verification Script

Checks if all Bronze Tier requirements are met for the AI Employee Hackathon.
"""

import sys
from pathlib import Path
import importlib.util


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(text)
    print("="*60 + "\n")


def check_mark(passed):
    """Return check mark or X."""
    return "✓" if passed else "✗"


def check_vault_structure():
    """Check if Obsidian vault structure exists."""
    print_header("1. Vault Structure")
    
    required_folders = {
        "Inbox": "Incoming items from watchers",
        "Needs_Action": "Items requiring action",
        "Done": "Completed items",
        "Plans": "Execution plans",
        "Pending_Approval": "Items awaiting approval"
    }
    
    all_exist = True
    for folder, description in required_folders.items():
        folder_path = Path(folder)
        exists = folder_path.exists() and folder_path.is_dir()
        print(f"{check_mark(exists)} {folder}/ - {description}")
        if not exists:
            all_exist = False
    
    return all_exist


def check_dashboard_files():
    """Check if Dashboard.md and Company_Handbook.md exist."""
    print_header("2. Dashboard Files")
    
    files = {
        "Dashboard.md": "System status and activity",
        "Company_Handbook.md": "Business rules and context"
    }
    
    all_exist = True
    for filename, description in files.items():
        file_path = Path(filename)
        exists = file_path.exists() and file_path.is_file()
        print(f"{check_mark(exists)} {filename} - {description}")
        if not exists:
            all_exist = False
    
    return all_exist


def check_watcher_script():
    """Check if at least one watcher script exists."""
    print_header("3. Watcher Script")
    
    watchers = {
        "Skills/gmail_watcher.py": "Gmail monitoring",
        "Skills/filesystem_watcher.py": "File system monitoring"
    }
    
    found = False
    for watcher_path, description in watchers.items():
        file_path = Path(watcher_path)
        exists = file_path.exists() and file_path.is_file()
        if exists:
            print(f"{check_mark(True)} {watcher_path} - {description}")
            found = True
        else:
            print(f"{check_mark(False)} {watcher_path} - {description} (optional)")
    
    if found:
        print("\n✓ At least one watcher script exists")
    else:
        print("\n✗ No watcher scripts found")
    
    return found


def check_agent_skills():
    """Check if Agent Skills are implemented."""
    print_header("4. Agent Skills")
    
    skills_dir = Path("Skills/agent_skills")
    
    if not skills_dir.exists():
        print("✗ Skills/agent_skills/ directory not found")
        return False
    
    required_skills = [
        "base_skill.py",
        "summarize_task.py",
        "create_plan.py",
        "draft_reply.py",
        "generate_linkedin_post.py"
    ]
    
    all_exist = True
    for skill in required_skills:
        skill_path = skills_dir / skill
        exists = skill_path.exists()
        print(f"{check_mark(exists)} {skill}")
        if not exists:
            all_exist = False
    
    return all_exist


def check_dependencies():
    """Check if required Python packages are installed."""
    print_header("5. Python Dependencies")
    
    required_packages = {
        "watchdog": "File system monitoring",
        "dotenv": "Environment variables (python-dotenv)",
        "yaml": "YAML parsing (pyyaml)",
        "pytest": "Testing framework",
        "google.auth": "Google authentication"
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            if package == "dotenv":
                importlib.import_module("dotenv")
            elif package == "yaml":
                importlib.import_module("yaml")
            else:
                importlib.import_module(package)
            print(f"✓ {package} - {description}")
        except ImportError:
            print(f"✗ {package} - {description} (NOT INSTALLED)")
            all_installed = False
    
    return all_installed


def check_configuration():
    """Check if configuration files exist."""
    print_header("6. Configuration Files")
    
    config_files = {
        ".env": "Environment variables (copy from .env.example)",
        ".env.example": "Environment variable template",
        "requirements.txt": "Python dependencies list"
    }
    
    all_exist = True
    for filename, description in config_files.items():
        file_path = Path(filename)
        exists = file_path.exists()
        print(f"{check_mark(exists)} {filename} - {description}")
        if not exists:
            all_exist = False
    
    return all_exist


def check_claude_integration():
    """Check if Claude Code integration exists."""
    print_header("7. Claude Code Integration")
    
    # Check if there's any Claude-related code
    claude_files = [
        "Skills/claude_agent.py",
        "Skills/vault_manager.py"
    ]
    
    found = False
    for claude_file in claude_files:
        file_path = Path(claude_file)
        exists = file_path.exists()
        if exists:
            print(f"✓ {claude_file}")
            found = True
        else:
            print(f"✗ {claude_file} (not yet implemented)")
    
    if not found:
        print("\n⚠️  Claude Code integration not yet implemented")
        print("   This is required for Bronze Tier completion")
    
    return found


def calculate_score(checks):
    """Calculate completion percentage."""
    passed = sum(1 for check in checks if check)
    total = len(checks)
    percentage = (passed / total) * 100
    return passed, total, percentage


def main():
    """Main verification function."""
    print_header("BRONZE TIER VERIFICATION")
    print("Checking AI Employee Hackathon Bronze Tier requirements...")
    
    # Run all checks
    checks = {
        "Vault Structure": check_vault_structure(),
        "Dashboard Files": check_dashboard_files(),
        "Watcher Script": check_watcher_script(),
        "Agent Skills": check_agent_skills(),
        "Dependencies": check_dependencies(),
        "Configuration": check_configuration(),
        "Claude Integration": check_claude_integration()
    }
    
    # Summary
    print_header("BRONZE TIER SUMMARY")
    
    for check_name, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {check_name}")
    
    passed, total, percentage = calculate_score(checks.values())
    
    print(f"\n{'='*60}")
    print(f"Score: {passed}/{total} checks passed ({percentage:.0f}%)")
    print(f"{'='*60}")
    
    if percentage == 100:
        print("\n🎉 BRONZE TIER COMPLETE!")
        print("You have met all Bronze Tier requirements.")
        print("\nNext steps:")
        print("1. Test end-to-end: Gmail → Inbox → Claude → Action")
        print("2. Verify vault structure is working")
        print("3. Move to Silver Tier requirements")
    elif percentage >= 70:
        print("\n⚠️  BRONZE TIER ALMOST COMPLETE")
        print(f"You have completed {percentage:.0f}% of Bronze Tier requirements.")
        print("\nMissing components:")
        for check_name, passed in checks.items():
            if not passed:
                print(f"  - {check_name}")
    else:
        print("\n❌ BRONZE TIER INCOMPLETE")
        print(f"You have completed {percentage:.0f}% of Bronze Tier requirements.")
        print("\nRequired components:")
        for check_name, passed in checks.items():
            if not passed:
                print(f"  - {check_name}")
    
    print("\n" + "="*60)
    print("For detailed requirements, see:")
    print("  - HACKATHON_STATUS.md")
    print("  - BRONZE_TIER_PROGRESS.md")
    print("  - Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md")
    print("="*60 + "\n")
    
    return 0 if percentage == 100 else 1


if __name__ == "__main__":
    sys.exit(main())
