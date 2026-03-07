#!/usr/bin/env python3
"""
Unified Task Processor - Gold Tier

Processes tasks from all domains (Gmail, WhatsApp, LinkedIn)
Routes to appropriate handlers based on task type and priority.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import yaml
import json

class UnifiedTaskProcessor:
    """
    Processes tasks from multiple domains and routes them appropriately.
    
    Domains:
    - Email (Gmail)
    - Messaging (WhatsApp)
    - Professional (LinkedIn)
    """
    
    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / "Inbox"
        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.logger = logging.getLogger("UnifiedTaskProcessor")
        
        # Domain handlers
        self.domain_handlers = {
            "email": self._handle_email_task,
            "whatsapp": self._handle_whatsapp_task,
            "linkedin": self._handle_linkedin_task,
            "linkedin_message": self._handle_linkedin_task,
            "linkedin_connection": self._handle_linkedin_task,
            "linkedin_engagement": self._handle_linkedin_task,
        }
    
    def process_all_tasks(self) -> Dict[str, int]:
        """
        Process all tasks from inbox across all domains.
        
        Returns:
            Statistics dictionary
        """
        stats = {
            "total": 0,
            "processed": 0,
            "email": 0,
            "whatsapp": 0,
            "linkedin": 0,
            "errors": 0
        }
        
        # Get all markdown files from inbox
        inbox_files = list(self.inbox.glob("*.md"))
        stats["total"] = len(inbox_files)
        
        self.logger.info(f"Processing {stats['total']} tasks from inbox")
        
        for task_file in inbox_files:
            try:
                task = self._load_task(task_file)
                if task:
                    domain = task.get("type", "unknown")
                    
                    # Route to appropriate handler
                    if domain in self.domain_handlers:
                        self.domain_handlers[domain](task, task_file)
                        stats["processed"] += 1
                        
                        # Update domain stats
                        if "email" in domain:
                            stats["email"] += 1
                        elif "whatsapp" in domain:
                            stats["whatsapp"] += 1
                        elif "linkedin" in domain:
                            stats["linkedin"] += 1
                    else:
                        self.logger.warning(f"Unknown domain: {domain}")
            
            except Exception as e:
                self.logger.error(f"Error processing {task_file.name}: {e}")
                stats["errors"] += 1
        
        self.logger.info(f"Processed {stats['processed']}/{stats['total']} tasks")
        return stats

    
    def _load_task(self, task_file: Path) -> Optional[Dict]:
        """Load task from markdown file with frontmatter"""
        try:
            content = task_file.read_text(encoding='utf-8')
            
            # Parse frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2].strip()
                    
                    return {
                        **frontmatter,
                        'body': body,
                        'filename': task_file.name
                    }
            
            return None
        
        except Exception as e:
            self.logger.error(f"Failed to load task {task_file.name}: {e}")
            return None
    
    def _handle_email_task(self, task: Dict, task_file: Path):
        """Handle email tasks"""
        priority = task.get('priority', 'medium')
        sender = task.get('sender', 'Unknown')
        subject = task.get('subject', 'No Subject')
        
        self.logger.info(f"Processing email from {sender}: {subject} (Priority: {priority})")
        
        # Move to needs_action with priority prefix
        new_name = f"{priority}_{task_file.name}"
        new_path = self.needs_action / new_name
        task_file.rename(new_path)
        
        self.logger.info(f"Moved to Needs_Action: {new_name}")
    
    def _handle_whatsapp_task(self, task: Dict, task_file: Path):
        """Handle WhatsApp tasks"""
        sender = task.get('sender', 'Unknown')
        priority = task.get('priority', 'high')  # WhatsApp usually urgent
        
        self.logger.info(f"Processing WhatsApp from {sender} (Priority: {priority})")
        
        # WhatsApp messages are typically urgent
        new_name = f"urgent_{task_file.name}"
        new_path = self.needs_action / new_name
        task_file.rename(new_path)
        
        self.logger.info(f"Moved to Needs_Action: {new_name}")
    
    def _handle_linkedin_task(self, task: Dict, task_file: Path):
        """Handle LinkedIn tasks"""
        task_type = task.get('type', 'linkedin')
        priority = task.get('priority', 'medium')
        
        self.logger.info(f"Processing LinkedIn {task_type} (Priority: {priority})")
        
        # LinkedIn tasks are usually medium priority
        new_name = f"linkedin_{task_file.name}"
        new_path = self.needs_action / new_name
        task_file.rename(new_path)
        
        self.logger.info(f"Moved to Needs_Action: {new_name}")
    
    def generate_summary(self, stats: Dict) -> str:
        """Generate summary report"""
        summary = f"""
# Task Processing Summary

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Statistics

- **Total Tasks**: {stats['total']}
- **Processed**: {stats['processed']}
- **Errors**: {stats['errors']}

## By Domain

- **Email**: {stats['email']} tasks
- **WhatsApp**: {stats['whatsapp']} tasks
- **LinkedIn**: {stats['linkedin']} tasks

## Status

{'✅ All tasks processed successfully' if stats['errors'] == 0 else f'⚠️ {stats["errors"]} errors occurred'}
"""
        return summary


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified Task Processor")
    parser.add_argument("--vault", default=".", help="Vault path")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Process tasks
    processor = UnifiedTaskProcessor(args.vault)
    stats = processor.process_all_tasks()
    
    # Print summary
    print(processor.generate_summary(stats))
