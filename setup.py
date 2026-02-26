"""
AI Employee System - Setup Script

Run this script to set up your development environment.
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(text)
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print("Please upgrade Python and try again.")
        return False
    
    print("✓ Python version is compatible")
    return True


def create_virtual_environment():
    """Create a Python virtual environment."""
    print_header("Creating Virtual Environment")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("⚠️  Virtual environment already exists")
        response = input("Do you want to recreate it? (y/n): ").strip().lower()
        if response != 'y':
            print("Skipping virtual environment creation")
            return True
        
        print("Removing existing virtual environment...")
        import shutil
        shutil.rmtree(venv_path)
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✓ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def get_pip_command():
    """Get the pip command for the current platform."""
    if sys.platform == "win32":
        return str(Path("venv") / "Scripts" / "pip.exe")
    else:
        return str(Path("venv") / "bin" / "pip")


def install_dependencies():
    """Install Python dependencies."""
    print_header("Installing Dependencies")
    
    pip_cmd = get_pip_command()
    
    if not Path(pip_cmd).exists():
        print("❌ Virtual environment not found. Please create it first.")
        return False
    
    print("Upgrading pip...")
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
        print("✓ Pip upgraded")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to upgrade pip: {e}")
    
    print("\nInstalling dependencies from requirements.txt...")
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    print_header("Setting Up Environment Variables")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✓ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    print("Creating .env file from .env.example...")
    try:
        import shutil
        shutil.copy(env_example, env_file)
        print("✓ .env file created")
        print("\n⚠️  IMPORTANT: Edit .env file and add your actual credentials!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def verify_vault_structure():
    """Verify that the Obsidian vault structure exists."""
    print_header("Verifying Vault Structure")
    
    required_folders = [
        "Inbox",
        "Needs_Action",
        "Done",
        "Plans",
        "Pending_Approval",
        "Approved",
        "Logs"
    ]
    
    all_exist = True
    for folder in required_folders:
        folder_path = Path(folder)
        if folder_path.exists():
            print(f"✓ {folder}/ exists")
        else:
            print(f"❌ {folder}/ missing")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️  Some folders are missing. They will be created by VaultManager.")
    
    return True


def print_next_steps():
    """Print next steps for the user."""
    print_header("Setup Complete!")
    
    print("Next steps:")
    print("\n1. Activate the virtual environment:")
    
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Edit .env file and add your credentials:")
    print("   - Gmail API credentials")
    print("   - Other API keys as needed")
    
    print("\n3. Set up Gmail OAuth2:")
    print("   - Go to https://console.cloud.google.com/")
    print("   - Create OAuth2 credentials")
    print("   - Download credentials.json to config/")
    
    print("\n4. Run the Gmail Watcher to test:")
    print("   python Skills/gmail_watcher.py")
    
    print("\n5. Set up the scheduler:")
    print("   python setup_scheduler.py")
    
    print("\n" + "="*60)


def main():
    """Main setup function."""
    print_header("AI Employee System - Setup")
    
    print("This script will set up your development environment.")
    print("It will:")
    print("  1. Check Python version")
    print("  2. Create a virtual environment")
    print("  3. Install dependencies")
    print("  4. Create .env file")
    print("  5. Verify vault structure")
    
    response = input("\nContinue? (y/n): ").strip().lower()
    if response != 'y':
        print("Setup cancelled.")
        return 1
    
    # Step 1: Check Python version
    if not check_python_version():
        return 1
    
    # Step 2: Create virtual environment
    if not create_virtual_environment():
        return 1
    
    # Step 3: Install dependencies
    if not install_dependencies():
        return 1
    
    # Step 4: Create .env file
    if not create_env_file():
        return 1
    
    # Step 5: Verify vault structure
    verify_vault_structure()
    
    # Print next steps
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
