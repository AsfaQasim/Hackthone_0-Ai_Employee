python test_scheduler.py
"""
Scheduler

Manages periodic execution of the main reasoning loop and watchers.
Supports both Windows Task Scheduler and Cron (Linux/Mac).
"""

import os
import sys
import platform
import subprocess
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime


class Scheduler:
    """
    Manages scheduling of periodic tasks.
    
    Supports:
    - Windows Task Scheduler (schtasks)
    - Cron (Linux/Mac)
    """
    
    def __init__(self, script_path: str = "main_loop.py", interval_minutes: int = 5):
        """
        Initialize the Scheduler.
        
        Args:
            script_path: Path to the script to run periodically
            interval_minutes: Interval in minutes between executions
        """
        self.script_path = Path(script_path).absolute()
        self.interval_minutes = interval_minutes
        self.platform = platform.system()
        self.logger = logging.getLogger("scheduler")
        
        # Detect Python executable
        self.python_exe = sys.executable
        
        # Configure logging
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
    
    def setup(self) -> bool:
        """
        Set up the scheduled task based on the platform.
        
        Returns:
            True if successful, False otherwise
        """
        if self.platform == "Windows":
            return self._setup_windows_task()
        elif self.platform in ["Linux", "Darwin"]:  # Darwin is macOS
            return self._setup_cron()
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return False
    
    def remove(self) -> bool:
        """
        Remove the scheduled task.
        
        Returns:
            True if successful, False otherwise
        """
        if self.platform == "Windows":
            return self._remove_windows_task()
        elif self.platform in ["Linux", "Darwin"]:
            return self._remove_cron()
        else:
            self.logger.error(f"Unsupported platform: {self.platform}")
            return False
    
    def _setup_windows_task(self) -> bool:
        """
        Set up Windows Task Scheduler task.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            task_name = "AIEmployeeMainLoop"
            
            # Create command to run
            command = f'"{self.python_exe}" "{self.script_path}"'
            
            # Remove existing task if it exists
            self._remove_windows_task()
            
            # Create new task
            # /SC MINUTE /MO 5 = Run every 5 minutes
            # /TN = Task name
            # /TR = Task to run
            # /ST = Start time (now)
            # /F = Force create (overwrite if exists)
            
            create_cmd = [
                "schtasks",
                "/Create",
                "/SC", "MINUTE",
                "/MO", str(self.interval_minutes),
                "/TN", task_name,
                "/TR", command,
                "/F"  # Force create
            ]
            
            result = subprocess.run(
                create_cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            self.logger.info(f"Windows Task Scheduler task created: {task_name}")
            self.logger.info(f"Command: {command}")
            self.logger.info(f"Interval: Every {self.interval_minutes} minutes")
            
            return True
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create Windows task: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Error setting up Windows task: {e}", exc_info=True)
            return False
    
    def _remove_windows_task(self) -> bool:
        """
        Remove Windows Task Scheduler task.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            task_name = "AIEmployeeMainLoop"
            
            delete_cmd = [
                "schtasks",
                "/Delete",
                "/TN", task_name,
                "/F"  # Force delete without confirmation
            ]
            
            result = subprocess.run(
                delete_cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f"Windows task removed: {task_name}")
                return True
            else:
                # Task might not exist, which is fine
                self.logger.debug(f"Task {task_name} not found or already removed")
                return True
        
        except Exception as e:
            self.logger.error(f"Error removing Windows task: {e}", exc_info=True)
            return False
    
    def _setup_cron(self) -> bool:
        """
        Set up Cron job (Linux/Mac).
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create cron entry
            # */5 * * * * = Every 5 minutes
            cron_entry = f"*/{self.interval_minutes} * * * * {self.python_exe} {self.script_path}\n"
            
            # Get current crontab
            try:
                result = subprocess.run(
                    ["crontab", "-l"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                current_crontab = result.stdout if result.returncode == 0 else ""
            except Exception:
                current_crontab = ""
            
            # Check if entry already exists
            if str(self.script_path) in current_crontab:
                self.logger.info("Cron job already exists, updating...")
                # Remove old entry
                lines = current_crontab.split('\n')
                current_crontab = '\n'.join([
                    line for line in lines 
                    if str(self.script_path) not in line
                ])
            
            # Add new entry
            new_crontab = current_crontab.rstrip() + '\n' + cron_entry
            
            # Install new crontab
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                self.logger.info(f"Cron job created: {cron_entry.strip()}")
                self.logger.info(f"Interval: Every {self.interval_minutes} minutes")
                return True
            else:
                self.logger.error(f"Failed to create cron job: {stderr}")
                return False
        
        except Exception as e:
            self.logger.error(f"Error setting up cron job: {e}", exc_info=True)
            return False
    
    def _remove_cron(self) -> bool:
        """
        Remove Cron job.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current crontab
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                self.logger.info("No crontab found")
                return True
            
            current_crontab = result.stdout
            
            # Remove entries containing our script path
            lines = current_crontab.split('\n')
            new_crontab = '\n'.join([
                line for line in lines 
                if str(self.script_path) not in line
            ])
            
            # Install new crontab
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                self.logger.info("Cron job removed")
                return True
            else:
                self.logger.error(f"Failed to remove cron job: {stderr}")
                return False
        
        except Exception as e:
            self.logger.error(f"Error removing cron job: {e}", exc_info=True)
            return False
    
    def status(self) -> dict:
        """
        Get the status of the scheduled task.
        
        Returns:
            Dictionary with status information
        """
        if self.platform == "Windows":
            return self._status_windows()
        elif self.platform in ["Linux", "Darwin"]:
            return self._status_cron()
        else:
            return {
                "platform": self.platform,
                "supported": False,
                "scheduled": False
            }
    
    def _status_windows(self) -> dict:
        """
        Get Windows Task Scheduler status.
        
        Returns:
            Dictionary with status information
        """
        try:
            task_name = "AIEmployeeMainLoop"
            
            query_cmd = [
                "schtasks",
                "/Query",
                "/TN", task_name,
                "/FO", "LIST",
                "/V"
            ]
            
            result = subprocess.run(
                query_cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                # Parse output
                output = result.stdout
                status_info = {
                    "platform": "Windows",
                    "supported": True,
                    "scheduled": True,
                    "task_name": task_name,
                    "interval_minutes": self.interval_minutes,
                    "script_path": str(self.script_path),
                    "details": output
                }
                
                # Extract status from output
                if "Status:" in output:
                    for line in output.split('\n'):
                        if "Status:" in line:
                            status_info["task_status"] = line.split("Status:")[1].strip()
                            break
                
                return status_info
            else:
                return {
                    "platform": "Windows",
                    "supported": True,
                    "scheduled": False,
                    "message": "Task not found"
                }
        
        except Exception as e:
            return {
                "platform": "Windows",
                "supported": True,
                "scheduled": False,
                "error": str(e)
            }
    
    def _status_cron(self) -> dict:
        """
        Get Cron status.
        
        Returns:
            Dictionary with status information
        """
        try:
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                crontab = result.stdout
                
                # Check if our script is scheduled
                scheduled = str(self.script_path) in crontab
                
                # Extract our cron entry
                cron_entry = None
                if scheduled:
                    for line in crontab.split('\n'):
                        if str(self.script_path) in line:
                            cron_entry = line
                            break
                
                return {
                    "platform": self.platform,
                    "supported": True,
                    "scheduled": scheduled,
                    "interval_minutes": self.interval_minutes,
                    "script_path": str(self.script_path),
                    "cron_entry": cron_entry
                }
            else:
                return {
                    "platform": self.platform,
                    "supported": True,
                    "scheduled": False,
                    "message": "No crontab found"
                }
        
        except Exception as e:
            return {
                "platform": self.platform,
                "supported": True,
                "scheduled": False,
                "error": str(e)
            }


def setup_scheduler(script_path: str = "main_loop.py", interval_minutes: int = 5) -> bool:
    """
    Convenience function to set up the scheduler.
    
    Args:
        script_path: Path to the script to run periodically
        interval_minutes: Interval in minutes between executions
        
    Returns:
        True if successful, False otherwise
    """
    scheduler = Scheduler(script_path, interval_minutes)
    return scheduler.setup()


def remove_scheduler(script_path: str = "main_loop.py") -> bool:
    """
    Convenience function to remove the scheduler.
    
    Args:
        script_path: Path to the script
        
    Returns:
        True if successful, False otherwise
    """
    scheduler = Scheduler(script_path)
    return scheduler.remove()


def get_scheduler_status(script_path: str = "main_loop.py") -> dict:
    """
    Convenience function to get scheduler status.
    
    Args:
        script_path: Path to the script
        
    Returns:
        Dictionary with status information
    """
    scheduler = Scheduler(script_path)
    return scheduler.status()


# Example usage and CLI
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage AI Employee Scheduler")
    parser.add_argument(
        "action",
        choices=["setup", "remove", "status"],
        help="Action to perform"
    )
    parser.add_argument(
        "--script",
        default="main_loop.py",
        help="Path to the script to schedule (default: main_loop.py)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Interval in minutes (default: 5)"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    scheduler = Scheduler(args.script, args.interval)
    
    if args.action == "setup":
        print(f"\n{'='*60}")
        print("SETTING UP SCHEDULER")
        print(f"{'='*60}")
        print(f"Script: {scheduler.script_path}")
        print(f"Interval: Every {args.interval} minutes")
        print(f"Platform: {scheduler.platform}")
        print(f"{'='*60}\n")
        
        success = scheduler.setup()
        
        if success:
            print("\n✓ Scheduler set up successfully!")
            print(f"\nThe script will run automatically every {args.interval} minutes.")
            
            if scheduler.platform == "Windows":
                print("\nTo view the task:")
                print("  1. Open Task Scheduler (taskschd.msc)")
                print("  2. Look for 'AIEmployeeMainLoop'")
            else:
                print("\nTo view the cron job:")
                print("  crontab -l")
        else:
            print("\n✗ Failed to set up scheduler")
            sys.exit(1)
    
    elif args.action == "remove":
        print(f"\n{'='*60}")
        print("REMOVING SCHEDULER")
        print(f"{'='*60}\n")
        
        success = scheduler.remove()
        
        if success:
            print("\n✓ Scheduler removed successfully!")
        else:
            print("\n✗ Failed to remove scheduler")
            sys.exit(1)
    
    elif args.action == "status":
        print(f"\n{'='*60}")
        print("SCHEDULER STATUS")
        print(f"{'='*60}\n")
        
        status = scheduler.status()
        
        for key, value in status.items():
            if key != "details":
                print(f"{key}: {value}")
        
        if status.get("scheduled"):
            print("\n✓ Scheduler is active")
        else:
            print("\n✗ Scheduler is not active")
