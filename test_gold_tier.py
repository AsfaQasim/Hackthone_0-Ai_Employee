#!/usr/bin/env python3
"""
Gold Tier Testing Script
Tests unified task processor and CEO briefing generator
"""

import sys
from pathlib import Path

def test_unified_processor():
    """Test unified task processor"""
    print("=" * 60)
    print("Testing Unified Task Processor")
    print("=" * 60)
    
    try:
        sys.path.insert(0, 'Skills')
        from unified_task_processor import UnifiedTaskProcessor
        
        processor = UnifiedTaskProcessor(".")
        print("✅ Unified Task Processor loaded successfully")
        
        # Check if inbox exists
        if Path("Inbox").exists():
            stats = processor.process_all_tasks()
            print(f"✅ Processed {stats['processed']} tasks")
            print(f"   - Email: {stats['email']}")
            print(f"   - WhatsApp: {stats['whatsapp']}")
            print(f"   - LinkedIn: {stats['linkedin']}")
        else:
            print("⚠️  Inbox folder not found")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ceo_briefing():
    """Test CEO briefing generator"""
    print("\n" + "=" * 60)
    print("Testing CEO Briefing Generator")
    print("=" * 60)
    
    try:
        sys.path.insert(0, 'Skills')
        from ceo_briefing_generator import CEOBriefingGenerator
        
        generator = CEOBriefingGenerator(".")
        print("✅ CEO Briefing Generator loaded successfully")
        
        briefing = generator.generate_weekly_briefing()
        print("✅ Briefing generated successfully")
        print(f"   Length: {len(briefing)} characters")
        
        # Check if briefing file was created
        briefings_folder = Path("Briefings")
        if briefings_folder.exists():
            briefing_files = list(briefings_folder.glob("*_CEO_Briefing.md"))
            if briefing_files:
                print(f"✅ Briefing saved: {briefing_files[-1].name}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_gold_tier_files():
    """Check if Gold Tier files exist"""
    print("\n" + "=" * 60)
    print("Checking Gold Tier Files")
    print("=" * 60)
    
    files = {
        "GOLD_TIER_ROADMAP.md": "Gold Tier roadmap",
        "GOLD_TIER_PROGRESS.md": "Progress tracker",
        "Skills/unified_task_processor.py": "Unified task processor",
        "Skills/ceo_briefing_generator.py": "CEO briefing generator",
        "Briefings/.gitkeep": "Briefings folder",
    }
    
    all_exist = True
    for filepath, description in files.items():
        exists = Path(filepath).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {description}: {filepath}")
        if not exists:
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("\n🧪 Gold Tier Testing Suite\n")
    
    results = {
        "Files Check": check_gold_tier_files(),
        "Unified Processor": test_unified_processor(),
        "CEO Briefing": test_ceo_briefing(),
    }
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All Gold Tier tests passed!")
        print("\nNext steps:")
        print("1. Test with real tasks")
        print("2. Implement error recovery")
        print("3. Add audit logging")
        print("4. Complete documentation")
    else:
        print("\n⚠️  Some tests failed. Review errors above.")
    
    return 0 if passed_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())
