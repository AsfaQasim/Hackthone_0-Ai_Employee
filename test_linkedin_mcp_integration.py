"""
Test LinkedIn MCP Integration
Verify the LinkedIn MCP server installation and configuration
"""

import sys
import codecs
import subprocess
from pathlib import Path

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


def check_installation():
    """Check if LinkedIn MCP server is installed"""
    print("="*70)
    print("LINKEDIN MCP INTEGRATION - INSTALLATION CHECK")
    print("="*70)
    print()
    
    checks = {
        "linkedin-scraper-mcp": False,
        "patchright": False,
        "playwright": False,
    }
    
    # Check installed packages using pip list
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            output = result.stdout.lower()
            checks["linkedin-scraper-mcp"] = "linkedin-scraper-mcp" in output
            checks["patchright"] = "patchright" in output
            checks["playwright"] = "playwright" in output
    except Exception as e:
        print(f"Warning: Could not check packages: {e}")
    
    # Print results
    print("📦 Package Installation:")
    print()
    
    for package, installed in checks.items():
        status = "✅" if installed else "❌"
        print(f"  {status} {package}")
    
    print()
    
    # Check profile directory
    profile_dir = Path.home() / ".linkedin-mcp" / "profile"
    print("📁 Profile Directory:")
    print()
    
    if profile_dir.exists():
        print(f"  ✅ Exists: {profile_dir}")
        
        # Check for session files
        session_files = list(profile_dir.glob("*"))
        if session_files:
            print(f"  ✅ Contains {len(session_files)} files/directories")
        else:
            print(f"  ⚠️  Directory is empty (run authentication)")
    else:
        print(f"  ❌ Not found: {profile_dir}")
        print(f"  💡 Run: python linkedin_mcp_auth.py")
    
    print()
    
    # Check scripts
    print("📄 Integration Scripts:")
    print()
    
    scripts = [
        "linkedin_mcp_auth.py",
        "linkedin_mcp_auto_post.py",
        "linkedin_mcp_auth.bat",
        "linkedin_mcp_auto_post.bat",
    ]
    
    for script in scripts:
        script_path = Path(__file__).parent / script
        status = "✅" if script_path.exists() else "❌"
        print(f"  {status} {script}")
    
    print()
    
    # Check tracking directory
    tracking_dir = Path("Social_Media_Tracking")
    print("📊 Tracking Directory:")
    print()
    
    if tracking_dir.exists():
        print(f"  ✅ Exists: {tracking_dir}")
        
        linkedin_posts = list(tracking_dir.glob("linkedin_*.md"))
        if linkedin_posts:
            print(f"  ✅ Contains {len(linkedin_posts)} LinkedIn post(s)")
        else:
            print(f"  ℹ️  No posts tracked yet")
    else:
        print(f"  ℹ️  Will be created on first post")
    
    print()
    print("="*70)
    
    # Summary
    all_installed = all(checks.values())
    all_scripts_exist = all((Path(__file__).parent / s).exists() for s in scripts)
    
    if all_installed and all_scripts_exist:
        print("✅ INSTALLATION COMPLETE!")
        print()
        print("Next steps:")
        print("  1. Authenticate: python linkedin_mcp_auth.py")
        print("  2. Post: python linkedin_mcp_auto_post.py \"Your topic\"")
    else:
        print("⚠️  INSTALLATION INCOMPLETE")
        print()
        if not all_installed:
            print("  Run: pip install linkedin-scraper-mcp patchright")
        if not all_scripts_exist:
            print("  Re-run the integration setup script")
    
    print("="*70)
    
    return all_installed and all_scripts_exist


def check_session():
    """Check LinkedIn session status"""
    print()
    print("="*70)
    print("SESSION STATUS CHECK")
    print("="*70)
    print()
    
    profile_dir = Path.home() / ".linkedin-mcp" / "profile"
    
    if not profile_dir.exists():
        print("❌ No LinkedIn profile found")
        print()
        print("Authenticate first:")
        print("  python linkedin_mcp_auth.py")
        return False
    
    # Try to check session status
    try:
        result = subprocess.run(
            [sys.executable, "-m", "linkedin_mcp_server", "--status"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Session is VALID")
            print()
            print("You can post to LinkedIn!")
            return True
        else:
            print("❌ Session may be EXPIRED")
            print()
            print("Re-authenticate:")
            print("  python linkedin_mcp_auth.py")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Session check timed out")
        return False
    except Exception as e:
        print(f"⚠️  Could not check session: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test LinkedIn MCP Integration"
    )
    
    parser.add_argument(
        '--session',
        action='store_true',
        help='Check LinkedIn session status'
    )
    
    args = parser.parse_args()
    
    # Check installation
    installed = check_installation()
    
    # Check session if requested
    if args.session:
        valid = check_session()
        sys.exit(0 if valid else 1)
    
    sys.exit(0 if installed else 1)


if __name__ == "__main__":
    main()
