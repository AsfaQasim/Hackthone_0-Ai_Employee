#!/usr/bin/env python3
"""
Gold Tier Verification Script

Verifies all Gold Tier requirements are complete.
Run this to confirm your Gold Tier implementation.
"""

import sys
import os
from pathlib import Path

class GoldTierVerifier:
    """Verify Gold Tier completion"""
    
    def __init__(self):
        self.root = Path(".")
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        
    def check_file_exists(self, path: str, required: bool = True) -> bool:
        """Check if file exists"""
        file_path = self.root / path
        exists = file_path.exists()
        
        if exists:
            print(f"  [OK] {path}")
            self.passed += 1
            return True
        else:
            if required:
                print(f"  [FAIL] {path} (REQUIRED)")
                self.failed += 1
                return False
            else:
                print(f"  [WARN] {path} (optional)")
                self.warnings += 1
                return False
    
    def check_env_variable(self, name: str, required: bool = True) -> bool:
        """Check if environment variable is set"""
        value = os.getenv(name)
        
        if value:
            print(f"  [OK] {name} is set")
            self.passed += 1
            return True
        else:
            if required:
                print(f"  [FAIL] {name} not set (REQUIRED)")
                self.failed += 1
                return False
            else:
                print(f"  [WARN] {name} not set (optional)")
                self.warnings += 1
                return False
    
    def check_docker_running(self) -> bool:
        """Check if Docker is running"""
        import subprocess
        
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"  [OK] Docker is running")
                self.passed += 1
                return True
            else:
                print(f"  [FAIL] Docker is not running (REQUIRED)")
                self.failed += 1
                return False
        except Exception as e:
            print(f"  [FAIL] Docker not available: {e}")
            self.failed += 1
            return False
    
    def verify_section(self, title: str, checks: list):
        """Verify a section of checks"""
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        
        for check in checks:
            check()
    
    def verify_odoo_setup(self):
        """Verify Odoo setup"""
        self.check_file_exists("odoo/docker-compose.yml")
        self.check_file_exists("odoo/nginx.conf")
        self.check_file_exists("odoo/config/odoo.conf")
        self.check_file_exists("odoo/README.md")
        self.check_file_exists("Skills/mcp_servers/odoo_mcp_server.py")
    
    def verify_social_media_setup(self):
        """Verify social media setup"""
        self.check_file_exists("Skills/mcp_servers/facebook_instagram_mcp_server.py")
        self.check_file_exists(".env.example")
    
    def verify_gold_features(self):
        """Verify Gold Tier features"""
        self.check_file_exists("Skills/ceo_briefing_generator.py")
        self.check_file_exists("Skills/error_recovery.py")
        self.check_file_exists("Skills/audit_logger.py")
        self.check_file_exists("Skills/ralph_loop.py")
        self.check_file_exists("Skills/unified_task_processor.py")
    
    def verify_documentation(self):
        """Verify documentation"""
        self.check_file_exists("GOLD_TIER_SETUP_GUIDE.md")
        self.check_file_exists("GOLD_TIER_COMPLETE.md")
        self.check_file_exists("GOLD_TIER_QUICK_REFERENCE.md")
    
    def verify_scripts(self):
        """Verify helper scripts"""
        self.check_file_exists("start_odoo.bat")
        self.check_file_exists("stop_odoo.bat")
        self.check_file_exists("test_gold_tier_integrations.bat")
    
    def verify_environment(self):
        """Verify environment configuration"""
        # Check .env file exists
        if self.check_file_exists(".env", required=False):
            # Check key variables
            self.check_env_variable("ODOO_URL", required=False)
            self.check_env_variable("ODOO_DB", required=False)
            self.check_env_variable("FACEBOOK_PAGE_ACCESS_TOKEN", required=False)
            self.check_env_variable("INSTAGRAM_BUSINESS_ACCOUNT_ID", required=False)
        else:
            print("  ℹ️  Copy .env.example to .env and configure")
            self.warnings += 1
    
    def verify_docker(self):
        """Verify Docker setup"""
        self.check_docker_running()
    
    def run_verification(self):
        """Run complete verification"""
        print("\n" + "="*60)
        print("  GOLD TIER VERIFICATION")
        print("="*60)
        
        # Verify all sections
        self.verify_section("1. Odoo Setup", [self.verify_odoo_setup])
        self.verify_section("2. Social Media Setup", [self.verify_social_media_setup])
        self.verify_section("3. Gold Tier Features", [self.verify_gold_features])
        self.verify_section("4. Documentation", [self.verify_documentation])
        self.verify_section("5. Helper Scripts", [self.verify_scripts])
        self.verify_section("6. Environment", [self.verify_environment])
        self.verify_section("7. Docker", [self.verify_docker])
        
        # Summary
        print(f"\n{'='*60}")
        print("VERIFICATION SUMMARY")
        print(f"{'='*60}")
        print(f"[OK] Passed: {self.passed}")
        print(f"[FAIL] Failed: {self.failed}")
        print(f"[WARN] Warnings: {self.warnings}")
        print()
        
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        if self.failed == 0:
            print(f"[SUCCESS] GOLD TIER VERIFICATION: PASSED ({percentage:.0f}%)")
            print("\nAll required files are present!")
            print("Next steps:")
            print("1. Configure .env file with your credentials")
            print("2. Start Odoo: start_odoo.bat")
            print("3. Run integration tests: test_gold_tier_integrations.bat")
            return True
        else:
            print(f"[INCOMPLETE] GOLD TIER VERIFICATION: INCOMPLETE ({percentage:.0f}%)")
            print(f"\n{self.failed} required items missing!")
            print("Please review the failed checks above.")
            return False


def main():
    """Main entry point"""
    verifier = GoldTierVerifier()
    success = verifier.run_verification()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
