"""
Setup Scheduler

Interactive script to set up the AI Employee System scheduler.
"""

import sys
from pathlib import Path

# Add Skills to path
sys.path.insert(0, str(Path(__file__).parent / "Skills"))

from scheduler import Scheduler


def main():
    """Interactive scheduler setup."""
    print("\n" + "="*60)
    print("AI EMPLOYEE SYSTEM - SCHEDULER SETUP")
    print("="*60)
    
    # Create scheduler
    scheduler = Scheduler(script_path="main_loop.py", interval_minutes=5)
    
    print(f"\nPlatform: {scheduler.platform}")
    print(f"Script: {scheduler.script_path}")
    print(f"Interval: Every 5 minutes")
    
    # Check current status
    print("\nChecking current status...")
    status = scheduler.status()
    
    if status.get("scheduled"):
        print("\n⚠️  Scheduler is already set up!")
        print("\nOptions:")
        print("  1. Keep existing scheduler")
        print("  2. Remove and recreate")
        print("  3. Remove scheduler")
        print("  4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print("\n✓ Keeping existing scheduler")
            return 0
        elif choice == "2":
            print("\nRemoving existing scheduler...")
            scheduler.remove()
            print("Creating new scheduler...")
            success = scheduler.setup()
        elif choice == "3":
            print("\nRemoving scheduler...")
            success = scheduler.remove()
            if success:
                print("\n✓ Scheduler removed successfully!")
            return 0
        else:
            print("\nExiting...")
            return 0
    else:
        print("\n✓ No existing scheduler found")
        print("\nDo you want to set up the scheduler?")
        print("This will run main_loop.py every 5 minutes automatically.")
        
        choice = input("\nProceed? (y/n): ").strip().lower()
        
        if choice != 'y':
            print("\nSetup cancelled")
            return 0
        
        print("\nSetting up scheduler...")
        success = scheduler.setup()
    
    # Show result
    print("\n" + "="*60)
    if success:
        print("✓ SCHEDULER SET UP SUCCESSFULLY!")
        print("="*60)
        print("\nThe main loop will now run automatically every 5 minutes.")
        print("\nWhat happens every 5 minutes:")
        print("  1. Watchers check for new emails, messages, etc.")
        print("  2. Inbox items are processed")
        print("  3. Pending plans are executed")
        print("  4. Dashboard is updated")
        
        if scheduler.platform == "Windows":
            print("\nTo view the scheduled task:")
            print("  1. Press Win+R")
            print("  2. Type: taskschd.msc")
            print("  3. Look for 'AIEmployeeMainLoop'")
            
            print("\nTo remove the scheduler later:")
            print("  python setup_scheduler.py")
        else:
            print("\nTo view the cron job:")
            print("  crontab -l")
            
            print("\nTo remove the scheduler later:")
            print("  python setup_scheduler.py")
        
        print("\nLogs will be saved to: Logs/main_loop.log")
        
    else:
        print("✗ SCHEDULER SETUP FAILED")
        print("="*60)
        print("\nPlease check the error messages above.")
        
        if scheduler.platform == "Windows":
            print("\nNote: You may need to run this script as Administrator")
            print("Right-click Command Prompt → Run as Administrator")
        
        return 1
    
    print("\n" + "="*60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
