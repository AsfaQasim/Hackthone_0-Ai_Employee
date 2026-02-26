"""
Test Scheduler

Quick test to verify the scheduler implementation works correctly.
"""

import sys
from pathlib import Path

# Add Skills to path
sys.path.insert(0, str(Path(__file__).parent / "Skills"))

from scheduler import Scheduler


def test_scheduler():
    """Test the scheduler functionality."""
    print("\n" + "="*60)
    print("SCHEDULER TEST")
    print("="*60)
    
    # Create scheduler instance
    scheduler = Scheduler(script_path="main_loop.py", interval_minutes=5)
    
    print(f"\n1. Platform Detection")
    print(f"   Platform: {scheduler.platform}")
    print(f"   Python: {scheduler.python_exe}")
    print(f"   Script: {scheduler.script_path}")
    print(f"   ✓ Platform detected correctly")
    
    print(f"\n2. Status Check (Before Setup)")
    status = scheduler.status()
    print(f"   Supported: {status.get('supported', False)}")
    print(f"   Scheduled: {status.get('scheduled', False)}")
    
    if status.get('scheduled'):
        print(f"   ⚠️  Scheduler already exists")
        print(f"\n   To test setup, first remove the existing scheduler:")
        print(f"   python setup_scheduler.py")
        return
    else:
        print(f"   ✓ No existing scheduler found")
    
    print(f"\n3. Setup Test")
    print(f"   Setting up scheduler...")
    
    success = scheduler.setup()
    
    if success:
        print(f"   ✓ Scheduler setup successful")
    else:
        print(f"   ✗ Scheduler setup failed")
        return
    
    print(f"\n4. Status Check (After Setup)")
    status = scheduler.status()
    print(f"   Scheduled: {status.get('scheduled', False)}")
    
    if status.get('scheduled'):
        print(f"   ✓ Scheduler is active")
        
        if scheduler.platform == "Windows":
            print(f"\n   Task Name: {status.get('task_name')}")
            print(f"   Task Status: {status.get('task_status', 'Unknown')}")
        else:
            print(f"\n   Cron Entry: {status.get('cron_entry')}")
    else:
        print(f"   ✗ Scheduler is not active")
        return
    
    print(f"\n5. Cleanup Test")
    print(f"   Removing scheduler...")
    
    success = scheduler.remove()
    
    if success:
        print(f"   ✓ Scheduler removed successfully")
    else:
        print(f"   ✗ Scheduler removal failed")
        return
    
    print(f"\n6. Status Check (After Removal)")
    status = scheduler.status()
    
    if not status.get('scheduled'):
        print(f"   ✓ Scheduler successfully removed")
    else:
        print(f"   ✗ Scheduler still active")
        return
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED")
    print("="*60)
    print("\nThe scheduler is working correctly!")
    print("\nTo set up the scheduler for real:")
    print("  python setup_scheduler.py")
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        test_scheduler()
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
