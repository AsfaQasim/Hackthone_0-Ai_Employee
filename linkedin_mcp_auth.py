"""
LinkedIn MCP Authentication Script
Create and manage LinkedIn browser sessions for the MCP server
"""

import sys
import subprocess
from pathlib import Path


def authenticate_linkedin():
    """
    Authenticate with LinkedIn and create a persistent browser profile
    """
    print("="*70)
    print("LINKEDIN MCP AUTHENTICATION")
    print("="*70)
    print()
    print("This will open a browser window for you to log in to LinkedIn.")
    print("Your session will be saved for future automated posting.")
    print()
    print("⚠️  IMPORTANT:")
    print("- You have 5 minutes to complete login (including 2FA)")
    print("- Complete any captcha challenges if they appear")
    print("- Once logged in, you can close the browser window")
    print()
    input("Press Enter to continue...")
    
    # Get the profile directory
    profile_dir = Path.home() / ".linkedin-mcp" / "profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Profile directory: {profile_dir}")
    print()
    
    # Run the login command
    try:
        subprocess.run([
            sys.executable, "-m", "linkedin_mcp_server",
            "--login",
            "--no-headless",  # Show browser for user to login
            "--user-data-dir", str(profile_dir)
        ], check=True)
        
        print()
        print("="*70)
        print("✅ AUTHENTICATION SUCCESSFUL!")
        print("="*70)
        print()
        print("Your LinkedIn session has been saved.")
        print("You can now use the auto-posting features.")
        print()
        print("To verify your session, run:")
        print("   python linkedin_mcp_auth.py --status")
        print()
        
    except subprocess.CalledProcessError as e:
        print()
        print("="*70)
        print("❌ AUTHENTICATION FAILED")
        print("="*70)
        print(f"Error: {e}")
        print()
        print("Please try again.")
        sys.exit(1)


def check_session_status():
    """
    Check if the current LinkedIn session is valid
    """
    print("="*70)
    print("LINKEDIN SESSION STATUS")
    print("="*70)
    print()
    
    profile_dir = Path.home() / ".linkedin-mcp" / "profile"
    
    if not profile_dir.exists():
        print("❌ No LinkedIn profile found.")
        print()
        print("Run authentication first:")
        print("   python linkedin_mcp_auth.py")
        return False
    
    # Check session status
    try:
        result = subprocess.run([
            sys.executable, "-m", "linkedin_mcp_server",
            "--status",
            "--user-data-dir", str(profile_dir)
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Session is VALID")
            print()
            print("You can use auto-posting features.")
            return True
        else:
            print("❌ Session has EXPIRED")
            print()
            print("Please re-authenticate:")
            print("   python linkedin_mcp_auth.py")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Session check timed out")
        print()
        print("Try re-authenticating:")
        print("   python linkedin_mcp_auth.py")
        return False
    except Exception as e:
        print(f"❌ Error checking session: {e}")
        print()
        print("Try re-authenticating:")
        print("   python linkedin_mcp_auth.py")
        return False


def logout_linkedin():
    """
    Clear the stored LinkedIn browser profile
    """
    print("="*70)
    print("LINKEDIN LOGOUT")
    print("="*70)
    print()
    
    profile_dir = Path.home() / ".linkedin-mcp" / "profile"
    
    if not profile_dir.exists():
        print("No LinkedIn profile found.")
        return
    
    confirm = input(f"Are you sure you want to delete the profile at {profile_dir}? (y/N): ")
    
    if confirm.lower() == 'y':
        import shutil
        shutil.rmtree(profile_dir)
        print()
        print("✅ LinkedIn profile deleted successfully.")
        print()
        print("To use LinkedIn features again, run:")
        print("   python linkedin_mcp_auth.py")
    else:
        print("Logout cancelled.")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="LinkedIn MCP Authentication Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python linkedin_mcp_auth.py              # Authenticate with LinkedIn
  python linkedin_mcp_auth.py --status     # Check session status
  python linkedin_mcp_auth.py --logout     # Clear stored profile
        """
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Check if current session is valid'
    )
    
    parser.add_argument(
        '--logout',
        action='store_true',
        help='Clear stored LinkedIn browser profile'
    )
    
    args = parser.parse_args()
    
    if args.status:
        check_session_status()
    elif args.logout:
        logout_linkedin()
    else:
        authenticate_linkedin()


if __name__ == "__main__":
    main()
