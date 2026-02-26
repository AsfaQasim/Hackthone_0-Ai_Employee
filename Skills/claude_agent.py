"""
Claude Code Agent

Integrates Claude Code with the Obsidian vault for reading, writing, and processing files.
Implements the reasoning loop for processing inbox items and updating the dashboard.
"""

import logging
import json
import re
from pathlib import Path
from datetime import datetime, UTC
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ClaudeAgentConfig:
    """Configuration for Claude Code Agent"""
    vault_path: str = "."
    inbox_folder: str = "Inbox"
    needs_action_folder: str = "Needs_Action"
    done_folder: str = "Done"
    plans_folder: str = "Plans"
    pending_approval_folder: str = "Pending_Approval"
    dashboard_file: str = "Dashboard.md"
    handbook_file: str = "Company_Handbook.md"
    log_folder: str = "Logs/claude_agent"
    dry_run: bool = False


class ClaudeCodeAgent:
    """
    Claude Code Agent for vault operations.
    
    Provides:
    - Vault file reading and writing
    - Inbox processing
    - Dashboard updates
    - Task routing and prioritization
    """
    
    def __init__(self, config: ClaudeAgentConfig):
        """
        Initialize the Claude Code Agent.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        self.vault_path = Path(config.vault_path).absolute()
        self.logger = self._setup_logging()
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the agent"""
        logger = logging.getLogger("ClaudeCodeAgent")
        logger.setLevel(logging.INFO)
        
        # Create log directory
        log_dir = Path(self.config.log_folder)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler
        log_file = log_dir / "claude-agent.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[ClaudeAgent] %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _ensure_directories(self):
        """Create required directories if they don't exist"""
        folders = [
            self.config.inbox_folder,
            self.config.needs_action_folder,
            self.config.done_folder,
            self.config.plans_folder,
            self.config.pending_approval_folder,
            self.config.log_folder
        ]
        
        for folder in folders:
            Path(folder).mkdir(parents=True, exist_ok=True)
    
    def read_file(self, filepath: str) -> Optional[str]:
        """
        Read a file from the vault.
        
        Args:
            filepath: Path to file (relative to vault root or absolute)
            
        Returns:
            File content as string, or None if failed
        """
        try:
            file_path = Path(filepath)
            if not file_path.is_absolute():
                file_path = self.vault_path / file_path
            
            if not file_path.exists():
                self.logger.warning(f"File not found: {file_path}")
                return None
            
            content = file_path.read_text(encoding='utf-8')
            self.logger.debug(f"Read file: {file_path}")
            return content
        
        except Exception as e:
            self.logger.error(f"Failed to read file {filepath}: {e}")
            return None
    
    def write_file(self, filepath: str, content: str) -> bool:
        """
        Write content to a file in the vault.
        
        Args:
            filepath: Path to file (relative to vault root or absolute)
            content: Content to write
            
        Returns:
            True if successful, False otherwise
        """
        if self.config.dry_run:
            self.logger.info(f"[DRY RUN] Would write to file: {filepath}")
            return True
        
        try:
            file_path = Path(filepath)
            if not file_path.is_absolute():
                file_path = self.vault_path / file_path
            
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_path.write_text(content, encoding='utf-8')
            self.logger.info(f"Wrote file: {file_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to write file {filepath}: {e}")
            return False
    
    def list_files(self, folder: str, pattern: str = "*.md") -> List[Path]:
        """
        List files in a folder.
        
        Args:
            folder: Folder path (relative to vault root)
            pattern: Glob pattern for files (default: *.md)
            
        Returns:
            List of file paths
        """
        try:
            folder_path = self.vault_path / folder
            if not folder_path.exists():
                self.logger.warning(f"Folder not found: {folder_path}")
                return []
            
            files = list(folder_path.glob(pattern))
            self.logger.debug(f"Found {len(files)} files in {folder}")
            return files
        
        except Exception as e:
            self.logger.error(f"Failed to list files in {folder}: {e}")
            return []
    
    def move_file(self, source: str, destination: str) -> bool:
        """
        Move a file from one location to another.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        if self.config.dry_run:
            self.logger.info(f"[DRY RUN] Would move {source} to {destination}")
            return True
        
        try:
            source_path = Path(source)
            if not source_path.is_absolute():
                source_path = self.vault_path / source_path
            
            dest_path = Path(destination)
            if not dest_path.is_absolute():
                dest_path = self.vault_path / dest_path
            
            # Ensure destination directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            source_path.rename(dest_path)
            self.logger.info(f"Moved file: {source} -> {destination}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to move file {source} to {destination}: {e}")
            return False
    
    def extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Extract YAML frontmatter from markdown content.
        
        Args:
            content: Markdown content with frontmatter
            
        Returns:
            Dictionary of frontmatter fields
        """
        import yaml
        
        # Match frontmatter between --- delimiters
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError as e:
                self.logger.warning(f"Failed to parse frontmatter: {e}")
                return {}
        return {}
    
    def update_frontmatter(self, content: str, updates: Dict[str, Any]) -> str:
        """
        Update frontmatter fields in markdown content.
        
        Args:
            content: Markdown content with frontmatter
            updates: Dictionary of fields to update
            
        Returns:
            Updated markdown content
        """
        import yaml
        
        # Extract existing frontmatter
        frontmatter = self.extract_frontmatter(content)
        
        # Update fields
        frontmatter.update(updates)
        
        # Remove old frontmatter
        content_without_frontmatter = re.sub(
            r'^---\n.*?\n---\n',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Generate new frontmatter
        new_frontmatter = "---\n" + yaml.dump(frontmatter, default_flow_style=False) + "---\n"
        
        return new_frontmatter + content_without_frontmatter
    
    def process_inbox(self) -> Dict[str, int]:
        """
        Process all files in the Inbox folder.
        
        Moves files to appropriate folders based on priority and type.
        
        Returns:
            Dictionary with processing statistics
        """
        self.logger.info("Processing inbox...")
        
        stats = {
            "total": 0,
            "processed": 0,
            "high_priority": 0,
            "medium_priority": 0,
            "low_priority": 0,
            "errors": 0
        }
        
        try:
            # Get all markdown files in inbox
            inbox_files = self.list_files(self.config.inbox_folder)
            stats["total"] = len(inbox_files)
            
            for file_path in inbox_files:
                try:
                    # Read file content
                    content = self.read_file(str(file_path))
                    if not content:
                        stats["errors"] += 1
                        continue
                    
                    # Extract frontmatter
                    frontmatter = self.extract_frontmatter(content)
                    priority = frontmatter.get('priority', 'low')
                    
                    # Determine destination
                    if priority in ['high', 'medium']:
                        destination_folder = self.config.needs_action_folder
                        stats[f"{priority}_priority"] += 1
                    else:
                        destination_folder = self.config.needs_action_folder
                        stats["low_priority"] += 1
                    
                    # Move file
                    destination = Path(destination_folder) / file_path.name
                    if self.move_file(str(file_path), str(destination)):
                        stats["processed"] += 1
                    else:
                        stats["errors"] += 1
                
                except Exception as e:
                    self.logger.error(f"Error processing file {file_path}: {e}")
                    stats["errors"] += 1
            
            self.logger.info(f"Inbox processing complete: {stats}")
            
        except Exception as e:
            self.logger.error(f"Inbox processing failed: {e}")
            stats["errors"] += 1
        
        return stats
    
    def update_dashboard(self, updates: Optional[Dict[str, Any]] = None) -> bool:
        """
        Update Dashboard.md with current statistics.
        
        Args:
            updates: Optional dictionary of specific updates to make
            
        Returns:
            True if successful, False otherwise
        """
        dashboard_path = self.vault_path / self.config.dashboard_file
        
        if not dashboard_path.exists():
            self.logger.warning("Dashboard.md does not exist")
            return False
        
        if self.config.dry_run:
            self.logger.info("[DRY RUN] Would update dashboard")
            return True
        
        try:
            # Read current dashboard
            content = self.read_file(str(dashboard_path))
            if not content:
                return False
            
            # Update timestamp
            content = re.sub(
                r'\*\*Last Updated\*\*: .*',
                f'**Last Updated**: {datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")}',
                content
            )
            
            # Get folder statistics
            inbox_count = len(self.list_files(self.config.inbox_folder))
            needs_action_count = len(self.list_files(self.config.needs_action_folder))
            pending_approval_count = len(self.list_files(self.config.pending_approval_folder))
            done_count = len(self.list_files(self.config.done_folder))
            
            # Update counts (if sections exist)
            if updates:
                for key, value in updates.items():
                    # Try to update specific fields
                    pattern = rf'(\*\*{key}\*\*:)\s*\d+'
                    replacement = rf'\1 {value}'
                    content = re.sub(pattern, replacement, content)
            
            # Write back
            self.write_file(str(dashboard_path), content)
            
            self.logger.info("Dashboard updated successfully")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to update dashboard: {e}")
            return False
    
    def get_vault_stats(self) -> Dict[str, int]:
        """
        Get statistics about the vault.
        
        Returns:
            Dictionary with folder file counts
        """
        stats = {
            "inbox": len(self.list_files(self.config.inbox_folder)),
            "needs_action": len(self.list_files(self.config.needs_action_folder)),
            "done": len(self.list_files(self.config.done_folder)),
            "plans": len(self.list_files(self.config.plans_folder)),
            "pending_approval": len(self.list_files(self.config.pending_approval_folder))
        }
        
        return stats
    
    def read_handbook(self) -> Optional[str]:
        """
        Read the Company Handbook.
        
        Returns:
            Handbook content, or None if failed
        """
        handbook_path = self.vault_path / self.config.handbook_file
        return self.read_file(str(handbook_path))
    
    def process_needs_action_item(self, filepath: str) -> bool:
        """
        Process a single item from Needs_Action folder.
        
        This is a placeholder for AI-driven processing logic.
        In production, this would call Claude Code or another AI model.
        
        Args:
            filepath: Path to the file to process
            
        Returns:
            True if processed successfully, False otherwise
        """
        self.logger.info(f"Processing needs action item: {filepath}")
        
        try:
            # Read file
            content = self.read_file(filepath)
            if not content:
                return False
            
            # Extract frontmatter
            frontmatter = self.extract_frontmatter(content)
            
            # TODO: Call AI model to determine action
            # For now, just log the item
            self.logger.info(f"Item type: {frontmatter.get('type', 'unknown')}")
            self.logger.info(f"Priority: {frontmatter.get('priority', 'unknown')}")
            
            # Update status
            updated_content = self.update_frontmatter(content, {
                "status": "reviewed",
                "reviewed_at": datetime.now(UTC).isoformat() + "Z"
            })
            
            self.write_file(filepath, updated_content)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to process needs action item: {e}")
            return False


# Convenience functions
def create_agent(vault_path: str = ".", dry_run: bool = False) -> ClaudeCodeAgent:
    """
    Create a Claude Code Agent instance.
    
    Args:
        vault_path: Path to vault root
        dry_run: Whether to run in dry-run mode
        
    Returns:
        ClaudeCodeAgent instance
    """
    config = ClaudeAgentConfig(vault_path=vault_path, dry_run=dry_run)
    return ClaudeCodeAgent(config)


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Code Agent for Vault Operations")
    parser.add_argument(
        "action",
        choices=["process-inbox", "update-dashboard", "stats", "read"],
        help="Action to perform"
    )
    parser.add_argument(
        "--vault-path",
        default=".",
        help="Path to vault root directory"
    )
    parser.add_argument(
        "--file",
        help="File path for read action"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (no modifications)"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create agent
    agent = create_agent(args.vault_path, args.dry_run)
    
    if args.action == "process-inbox":
        print("\n" + "="*60)
        print("PROCESSING INBOX")
        print("="*60 + "\n")
        
        stats = agent.process_inbox()
        
        print(f"Total files: {stats['total']}")
        print(f"Processed: {stats['processed']}")
        print(f"High priority: {stats['high_priority']}")
        print(f"Medium priority: {stats['medium_priority']}")
        print(f"Low priority: {stats['low_priority']}")
        print(f"Errors: {stats['errors']}")
    
    elif args.action == "update-dashboard":
        print("\n" + "="*60)
        print("UPDATING DASHBOARD")
        print("="*60 + "\n")
        
        if agent.update_dashboard():
            print("✓ Dashboard updated successfully")
        else:
            print("✗ Dashboard update failed")
    
    elif args.action == "stats":
        print("\n" + "="*60)
        print("VAULT STATISTICS")
        print("="*60 + "\n")
        
        stats = agent.get_vault_stats()
        
        for folder, count in stats.items():
            print(f"{folder}: {count} files")
    
    elif args.action == "read":
        if not args.file:
            print("Error: --file argument required for read action")
            exit(1)
        
        content = agent.read_file(args.file)
        if content:
            print(content)
        else:
            print(f"Failed to read file: {args.file}")
