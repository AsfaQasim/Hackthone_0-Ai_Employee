#!/usr/bin/env python3
"""
Comprehensive Audit Logging System - Gold Tier

Logs all AI actions for compliance and audit trail.
Maintains 90+ day retention policy.
"""

import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

class ActionType(Enum):
    """Types of actions to log"""
    EMAIL_SEND = "email_send"
    EMAIL_READ = "email_read"
    WHATSAPP_SEND = "whatsapp_send"
    WHATSAPP_READ = "whatsapp_read"
    LINKEDIN_POST = "linkedin_post"
    LINKEDIN_READ = "linkedin_read"
    TASK_CREATE = "task_create"
    TASK_COMPLETE = "task_complete"
    APPROVAL_REQUEST = "approval_request"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_DENIED = "approval_denied"
    MCP_CALL = "mcp_call"
    ERROR = "error"
    SYSTEM_START = "system_start"
    SYSTEM_STOP = "system_stop"

class AuditLogger:
    """
    Comprehensive audit logging system.
    
    Features:
    - All actions logged with metadata
    - JSON format for easy parsing
    - 90+ day retention
    - Search and filter capabilities
    """
    
    def __init__(self, log_dir: str = "Logs/audit"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("AuditLogger")
        self.retention_days = 90
    
    def log_action(
        self,
        action_type: ActionType,
        actor: str,
        target: Optional[str] = None,
        parameters: Optional[Dict] = None,
        approval_status: Optional[str] = None,
        approved_by: Optional[str] = None,
        result: str = "success",
        error_message: Optional[str] = None
    ) -> str:
        """
        Log an action to audit trail.
        
        Args:
            action_type: Type of action
            actor: Who performed the action (e.g., "claude_code", "human")
            target: Target of action (e.g., email address, file path)
            parameters: Action parameters
            approval_status: "approved", "pending", "denied"
            approved_by: Who approved the action
            result: "success" or "failure"
            error_message: Error details if failed
        
        Returns:
            Log entry ID
        """
        timestamp = datetime.now()
        log_entry = {
            "id": self._generate_id(timestamp),
            "timestamp": timestamp.isoformat() + 'Z',
            "action_type": action_type.value,
            "actor": actor,
            "target": target,
            "parameters": parameters or {},
            "approval_status": approval_status,
            "approved_by": approved_by,
            "result": result,
            "error_message": error_message
        }
        
        # Write to daily log file
        log_file = self._get_log_file(timestamp)
        self._append_to_log(log_file, log_entry)
        
        self.logger.info(f"Logged action: {action_type.value} by {actor}")
        return log_entry["id"]
    
    def _generate_id(self, timestamp: datetime) -> str:
        """Generate unique log entry ID"""
        return f"{timestamp.strftime('%Y%m%d_%H%M%S_%f')}"
    
    def _get_log_file(self, timestamp: datetime) -> Path:
        """Get log file path for given timestamp"""
        return self.log_dir / f"{timestamp.strftime('%Y-%m-%d')}.json"
    
    def _append_to_log(self, log_file: Path, entry: Dict):
        """Append entry to log file"""
        # Read existing entries
        entries = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
            except json.JSONDecodeError:
                self.logger.warning(f"Corrupted log file: {log_file}")
                entries = []
        
        # Append new entry
        entries.append(entry)
        
        # Write back
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
    
    def search_logs(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        action_type: Optional[ActionType] = None,
        actor: Optional[str] = None,
        result: Optional[str] = None
    ) -> List[Dict]:
        """
        Search audit logs with filters.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            action_type: Filter by action type
            actor: Filter by actor
            result: Filter by result (success/failure)
        
        Returns:
            List of matching log entries
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=7)
        if not end_date:
            end_date = datetime.now()
        
        results = []
        
        # Iterate through log files in date range
        current_date = start_date.date()
        while current_date <= end_date.date():
            log_file = self.log_dir / f"{current_date.isoformat()}.json"
            
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    try:
                        entries = json.load(f)
                        
                        # Apply filters
                        for entry in entries:
                            if action_type and entry.get('action_type') != action_type.value:
                                continue
                            if actor and entry.get('actor') != actor:
                                continue
                            if result and entry.get('result') != result:
                                continue
                            
                            results.append(entry)
                    
                    except json.JSONDecodeError:
                        self.logger.warning(f"Skipping corrupted log: {log_file}")
            
            current_date += timedelta(days=1)
        
        return results
    
    def get_statistics(self, days: int = 7) -> Dict:
        """
        Get audit statistics for last N days.
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Statistics dictionary
        """
        start_date = datetime.now() - timedelta(days=days)
        all_logs = self.search_logs(start_date=start_date)
        
        stats = {
            "total_actions": len(all_logs),
            "by_type": {},
            "by_actor": {},
            "by_result": {"success": 0, "failure": 0},
            "approval_stats": {
                "pending": 0,
                "approved": 0,
                "denied": 0
            }
        }
        
        for entry in all_logs:
            # Count by type
            action_type = entry.get('action_type', 'unknown')
            stats["by_type"][action_type] = stats["by_type"].get(action_type, 0) + 1
            
            # Count by actor
            actor = entry.get('actor', 'unknown')
            stats["by_actor"][actor] = stats["by_actor"].get(actor, 0) + 1
            
            # Count by result
            result = entry.get('result', 'unknown')
            if result in stats["by_result"]:
                stats["by_result"][result] += 1
            
            # Count approvals
            approval = entry.get('approval_status')
            if approval in stats["approval_stats"]:
                stats["approval_stats"][approval] += 1
        
        return stats
    
    def cleanup_old_logs(self):
        """Remove logs older than retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        removed_count = 0
        
        for log_file in self.log_dir.glob("*.json"):
            try:
                # Parse date from filename
                date_str = log_file.stem
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                if file_date < cutoff_date:
                    log_file.unlink()
                    removed_count += 1
                    self.logger.info(f"Removed old log: {log_file.name}")
            
            except ValueError:
                self.logger.warning(f"Invalid log filename: {log_file.name}")
        
        self.logger.info(f"Cleanup complete. Removed {removed_count} old log files.")
        return removed_count
    
    def generate_report(self, days: int = 7) -> str:
        """Generate audit report"""
        stats = self.get_statistics(days)
        
        report = f"""
# Audit Report

**Period**: Last {days} days  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary

- **Total Actions**: {stats['total_actions']}
- **Success Rate**: {(stats['by_result']['success'] / max(stats['total_actions'], 1) * 100):.1f}%
- **Failures**: {stats['by_result']['failure']}

---

## Actions by Type

"""
        for action_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
            report += f"- **{action_type}**: {count}\n"
        
        report += "\n---\n\n## Actions by Actor\n\n"
        
        for actor, count in sorted(stats['by_actor'].items(), key=lambda x: x[1], reverse=True):
            report += f"- **{actor}**: {count}\n"
        
        report += f"""
---

## Approval Statistics

- **Pending**: {stats['approval_stats']['pending']}
- **Approved**: {stats['approval_stats']['approved']}
- **Denied**: {stats['approval_stats']['denied']}

---

*Generated by Audit Logger v1.0*
"""
        return report


# Global instance
audit_logger = AuditLogger()


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Audit Logger")
    parser.add_argument("command", choices=["stats", "report", "cleanup", "search"])
    parser.add_argument("--days", type=int, default=7, help="Number of days")
    parser.add_argument("--actor", help="Filter by actor")
    parser.add_argument("--type", help="Filter by action type")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    if args.command == "stats":
        stats = audit_logger.get_statistics(args.days)
        print(json.dumps(stats, indent=2))
    
    elif args.command == "report":
        report = audit_logger.generate_report(args.days)
        print(report)
    
    elif args.command == "cleanup":
        removed = audit_logger.cleanup_old_logs()
        print(f"Removed {removed} old log files")
    
    elif args.command == "search":
        logs = audit_logger.search_logs(
            actor=args.actor,
            action_type=ActionType(args.type) if args.type else None
        )
        print(json.dumps(logs, indent=2))
