"""
Base Watcher Class

Provides common interface and functionality for all watcher implementations.
Watchers monitor external sources (Gmail, WhatsApp, LinkedIn, etc.) and create
inbox files in the Obsidian vault.
"""

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class WatcherConfig:
    """Base configuration for all watchers"""
    vault_path: str = "."
    polling_interval_ms: int = 300000  # 5 minutes default
    inbox_folder: str = "Inbox"
    needs_action_folder: str = "Needs_Action"
    log_folder: str = "Logs"
    index_path: str = ".index"
    dry_run: bool = False


class BaseWatcher(ABC):
    """
    Abstract base class for all watchers.
    
    Implements the Ralph Loop pattern:
    - PERCEPTION: Detect new items from external source
    - REASONING: Filter and prioritize items
    - ACTION: Create markdown files in vault
    """
    
    def __init__(self, config: WatcherConfig, watcher_name: str):
        """
        Initialize the watcher.
        
        Args:
            config: Watcher configuration
            watcher_name: Name of the watcher (e.g., "GmailWatcher")
        """
        self.config = config
        self.watcher_name = watcher_name
        self.logger = self._setup_logging()
        self.processed_items: Dict[str, Dict] = {}
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _setup_logging(self) -> logging.Logger:
        """Configure logging for the watcher"""
        logger = logging.getLogger(self.watcher_name)
        logger.setLevel(logging.INFO)
        
        # Create log directory
        log_dir = Path(self.config.log_folder) / self.watcher_name.lower()
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler
        log_file = log_dir / f"{self.watcher_name.lower()}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[%(name)s] %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _ensure_directories(self):
        """Create required directories if they don't exist"""
        Path(self.config.inbox_folder).mkdir(parents=True, exist_ok=True)
        Path(self.config.needs_action_folder).mkdir(parents=True, exist_ok=True)
        Path(self.config.log_folder).mkdir(parents=True, exist_ok=True)
        Path(self.config.index_path).mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the external service.
        
        Returns:
            True if authentication successful, False otherwise
        """
        pass
    
    @abstractmethod
    def check_for_new_items(self) -> List[str]:
        """
        Check for new items from the external source.
        
        This is the PERCEPTION phase of the Ralph Loop.
        
        Returns:
            List of item IDs to process
        """
        pass
    
    @abstractmethod
    def get_item_content(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch full content for a specific item.
        
        Args:
            item_id: Unique identifier for the item
            
        Returns:
            Dictionary with item metadata and content, or None if failed
        """
        pass
    
    @abstractmethod
    def is_important(self, item: Dict[str, Any]) -> bool:
        """
        Determine if an item is important enough to process.
        
        This is part of the REASONING phase of the Ralph Loop.
        
        Args:
            item: Item metadata and content
            
        Returns:
            True if item should be processed, False otherwise
        """
        pass
    
    @abstractmethod
    def detect_priority(self, item: Dict[str, Any]) -> str:
        """
        Detect the priority level of an item.
        
        This is part of the REASONING phase of the Ralph Loop.
        
        Args:
            item: Item metadata and content
            
        Returns:
            Priority level: "high", "medium", or "low"
        """
        pass
    
    @abstractmethod
    def generate_markdown(self, item: Dict[str, Any]) -> str:
        """
        Generate markdown content for the item.
        
        Args:
            item: Item metadata and content
            
        Returns:
            Markdown formatted string
        """
        pass
    
    def create_inbox_file(self, item: Dict[str, Any], content: str) -> Optional[str]:
        """
        Create markdown file in the inbox folder.
        
        This is the ACTION phase of the Ralph Loop.
        
        Args:
            item: Item metadata
            content: Markdown content to write
            
        Returns:
            Path to created file, or None if failed
        """
        # Generate filename
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        
        # Get safe title from item
        title = item.get('title', item.get('subject', 'untitled'))
        safe_title = self._sanitize_filename(title)
        
        filename = f"{timestamp}_{safe_title}.md"
        
        # Determine folder based on priority
        priority = item.get('priority', 'low')
        if priority == 'high' or priority == 'medium':
            folder = Path(self.config.needs_action_folder)
        else:
            folder = Path(self.config.inbox_folder)
        
        filepath = folder / filename
        
        if self.config.dry_run:
            self.logger.info(f"[DRY RUN] Would create file: {filepath}")
            return str(filepath)
        
        try:
            filepath.write_text(content, encoding='utf-8')
            self.logger.info(f"Created inbox file: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Failed to create inbox file: {e}")
            return None
    
    def _sanitize_filename(self, text: str, max_length: int = 50) -> str:
        """
        Sanitize text for use in filename.
        
        Args:
            text: Text to sanitize
            max_length: Maximum length of sanitized text
            
        Returns:
            Sanitized filename-safe string
        """
        import re
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^\w\s-]', '', text)
        
        # Replace spaces and multiple dashes with single dash
        text = re.sub(r'[-\s]+', '-', text)
        
        # Trim to max length
        text = text[:max_length]
        
        # Remove leading/trailing dashes
        text = text.strip('-')
        
        return text or 'untitled'
    
    def is_duplicate(self, item_id: str) -> bool:
        """
        Check if item has already been processed.
        
        Args:
            item_id: Unique identifier for the item
            
        Returns:
            True if already processed, False otherwise
        """
        return item_id in self.processed_items
    
    def mark_as_processed(self, item_id: str, metadata: Dict[str, Any]):
        """
        Mark an item as processed.
        
        Args:
            item_id: Unique identifier for the item
            metadata: Additional metadata to store
        """
        self.processed_items[item_id] = {
            **metadata,
            "processed_at": datetime.now(UTC).isoformat() + "Z"
        }
    
    def process_item(self, item_id: str) -> bool:
        """
        Process a single item through the Ralph Loop.
        
        Args:
            item_id: Unique identifier for the item
            
        Returns:
            True if processed successfully, False otherwise
        """
        # Check for duplicates
        if self.is_duplicate(item_id):
            self.logger.debug(f"Skipping duplicate item: {item_id}")
            return False
        
        # PERCEPTION: Get item content
        item = self.get_item_content(item_id)
        if not item:
            self.logger.warning(f"Failed to get content for item: {item_id}")
            return False
        
        # REASONING: Filter and prioritize
        if not self.is_important(item):
            self.logger.info(f"Skipping non-important item: {item_id}")
            return False
        
        priority = self.detect_priority(item)
        item['priority'] = priority
        
        self.logger.info(f"Processing item: {item_id} (Priority: {priority})")
        
        # ACTION: Create markdown file
        markdown_content = self.generate_markdown(item)
        filepath = self.create_inbox_file(item, markdown_content)
        
        if filepath:
            # Mark as processed
            self.mark_as_processed(item_id, {
                "filename": Path(filepath).name,
                "priority": priority
            })
            return True
        
        return False
    
    def poll_once(self) -> Dict[str, int]:
        """
        Execute one polling cycle.
        
        Returns:
            Dictionary with statistics about the poll
        """
        self.logger.info("Polling cycle initiated")
        start_time = time.time()
        
        stats = {
            "retrieved": 0,
            "processed": 0,
            "filtered": 0,
            "created": 0,
            "errors": 0
        }
        
        try:
            # Check for new items
            item_ids = self.check_for_new_items()
            stats["retrieved"] = len(item_ids)
            
            # Process each item
            for item_id in item_ids:
                try:
                    if self.process_item(item_id):
                        stats["processed"] += 1
                        stats["created"] += 1
                    else:
                        stats["filtered"] += 1
                except Exception as e:
                    self.logger.error(f"Error processing item {item_id}: {e}")
                    stats["errors"] += 1
            
            elapsed = time.time() - start_time
            self.logger.info(f"Polling cycle completed in {elapsed:.2f}s: {stats}")
            
        except Exception as e:
            self.logger.error(f"Polling cycle failed: {e}")
            stats["errors"] += 1
        
        return stats
    
    def start(self):
        """
        Start continuous polling.
        
        Runs indefinitely until interrupted.
        """
        self.logger.info(
            f"Starting {self.watcher_name} "
            f"(interval: {self.config.polling_interval_ms}ms)"
        )
        
        # Authenticate first
        if not self.authenticate():
            self.logger.error("Authentication failed, cannot start watcher")
            return
        
        if self.config.dry_run:
            self.logger.info("[DRY RUN] Running single poll cycle only")
            self.poll_once()
            return
        
        try:
            while True:
                self.poll_once()
                sleep_seconds = self.config.polling_interval_ms / 1000
                self.logger.info(f"Sleeping for {sleep_seconds}s until next poll")
                time.sleep(sleep_seconds)
        except KeyboardInterrupt:
            self.logger.info(f"{self.watcher_name} stopped by user")
        except Exception as e:
            self.logger.error(f"{self.watcher_name} stopped due to error: {e}")
    
    def stop(self):
        """
        Stop the watcher.
        
        Performs cleanup and graceful shutdown.
        """
        self.logger.info(f"Stopping {self.watcher_name}")
        # Subclasses can override to add cleanup logic
