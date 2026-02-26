#!/usr/bin/env python3
"""
Gmail Response Executor

Monitors Needs_Action folder for approved email tasks and executes responses.
Integrates with approval workflow and MCP email server.

Version: 1.0.0
"""

import os
import sys
import json
import logging
import re
import shutil
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
import yaml

# Import MCP email server
sys.path.append(str(Path(__file__).parent))
from mcp_servers.email_mcp_server import EmailMCPServer


@dataclass
class ResponseExecutorConfig:
    """Configuration for Response Executor"""
    vault_path: str = "."
    needs_action_folder: str = "Needs_Action"
    done_folder: str = "Done"
    log_folder: str = "Logs/gmail_response"
    credentials_path: str = "config/gmail-credentials.json"
    token_path: str = "config/gmail-token.json"
    dry_run: bool = False


class GmailResponseExecutor:
    """
    Executes email responses from approved tasks.
    
    Monitors Needs_Action folder for approved email tasks,
    generates responses using Claude, and sends via Gmail API.
    """
    
    def __init__(self, config: ResponseExecutorConfig):
        """Initialize the Response Executor"""
        self.config = config
        self.vault_path = Path(config.vault_path).absolute()
        self.needs_action_folder = self.vault_path / config.needs_action_folder
        self.done_folder = self.vault_path / config.done_folder
        self.logger = self._setup_logging()
        
        # Initialize email server
        self.email_server = EmailMCPServer(
            credentials_path=config.credentials_path,
            token_path=config.token_path
        )
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _setup_logging(self) -> logging.Logger:
        """Configure logging"""
        logger = logging.getLogger("GmailResponseExecutor")
        logger.setLevel(logging.INFO)
        
        # Create log directory
        log_dir = Path(self.config.log_folder)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler
        log_file = log_dir / "gmail-response.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _ensure_directories(self):
        """Create required directories"""
        self.needs_action_folder.mkdir(parents=True, exist_ok=True)
        self.done_folder.mkdir(parents=True, exist_ok=True)
        Path(self.config.log_folder).mkdir(parents=True, exist_ok=True)
    
    def list_email_tasks(self) -> list[Path]:
        """
        List all email task files in Needs_Action folder.
        
        Returns:
            List of email task file paths
        """
        try:
            # Find all markdown files with email metadata
            email_tasks = []
            for file_path in self.needs_action_folder.glob("*.md"):
                # Check if file contains email metadata
                content = file_path.read_text(e