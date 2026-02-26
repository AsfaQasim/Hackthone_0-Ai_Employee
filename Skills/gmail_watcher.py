#!/usr/bin/env python3
"""
Gmail Watcher Agent Skill - Python Implementation

Monitors Gmail inbox for important emails and creates actionable markdown files
in the Obsidian vault. Implements the Ralph Loop (Perception → Reasoning → Action).

Version: 1.0.0
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, asdict
import re
import yaml
from enum import Enum

# Third-party imports (install via: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml html2text)
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import html2text
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pyyaml html2text")
    sys.exit(1)


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify']


class Priority(Enum):
    """Email priority levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class EmailMetadata:
    """Structured email metadata"""
    email_id: str
    sender: str
    sender_email: str
    sender_name: str
    subject: str
    date: str
    priority: str
    labels: List[str]
    body_text: str
    body_html: str


@dataclass
class GmailWatcherConfig:
    """Configuration for Gmail Watcher"""
    polling_interval_ms: int = 300000  # 5 minutes
    importance_criteria: Dict[str, Any] = None
    priority_rules: Dict[str, Any] = None
    rate_limit_config: Dict[str, Any] = None
    needs_action_folder: str = "Needs_Action"
    pending_approval_folder: str = "Pending_Approval"
    log_folder: str = "Logs/gmail_watcher"
    credentials_path: str = "config/gmail-credentials.json"
    token_path: str = "config/gmail-token.json"
    index_path: str = ".index/gmail-watcher-processed.json"
    mark_as_read: bool = False
    use_approval_workflow: bool = True
    
    def __post_init__(self):
        if self.importance_criteria is None:
            self.importance_criteria = {
                "senderWhitelist": [],
                "keywordPatterns": ["urgent", "important", "action required"],
                "requiredLabels": ["IMPORTANT", "STARRED"],
                "logicMode": "OR"
            }
        if self.priority_rules is None:
            self.priority_rules = {
                "highPriorityKeywords": ["urgent", "asap", "critical", "emergency"],
                "vipSenders": [],
                "highPriorityLabels": ["IMPORTANT", "STARRED"],
                "mediumPriorityKeywords": ["follow up", "reminder", "deadline"]
            }
        if self.rate_limit_config is None:
            self.rate_limit_config = {
                "maxRequestsPerMinute": 60,
                "initialBackoffMs": 1000,
                "maxBackoffMs": 60000,
                "backoffMultiplier": 2
            }


class GmailWatcher:
    """Main Gmail Watcher implementation"""
    
    def __init__(self, config: GmailWatcherConfig, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        self.logger = self._setup_logging()
        self.service = None
        self.processed_index: Dict[str, Dict] = {}
        self.request_count = 0
        self.last_request_time = time.time()
        self.current_backoff_ms = config.rate_limit_config["initialBackoffMs"]
        
        # Initialize
        self._load_processed_index()
        self._ensure_directories()
        
    def _setup_logging(self) -> logging.Logger:
        """Configure logging with file and console handlers"""
        logger = logging.getLogger("GmailWatcher")
        logger.setLevel(logging.INFO)
        
        # Create log directory
        log_dir = Path(self.config.log_folder)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # File handler (JSON format for audit trail)
        log_file = log_dir / "gmail-watcher.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}')
        file_handler.setFormatter(file_formatter)
        
        # Console handler (human-readable)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _ensure_directories(self):
        """Create required directories if they don't exist"""
        Path(self.config.needs_action_folder).mkdir(parents=True, exist_ok=True)
        Path(self.config.pending_approval_folder).mkdir(parents=True, exist_ok=True)
        Path(self.config.log_folder).mkdir(parents=True, exist_ok=True)
        Path(self.config.index_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _load_processed_index(self):
        """Load the processed email index from disk"""
        index_path = Path(self.config.index_path)
        if index_path.exists():
            try:
                with open(index_path, 'r') as f:
                    self.processed_index = json.load(f)
                self.logger.info(f"Loaded processed index with {len(self.processed_index)} entries")
            except Exception as e:
                self.logger.error(f"Failed to load processed index: {e}")
                self.processed_index = {}
        else:
            self.processed_index = {}
    
    def _save_processed_index(self):
        """Save the processed email index to disk"""
        if self.dry_run:
            self.logger.info(f"[DRY RUN] Would save processed index with {len(self.processed_index)} entries")
            return
        
        try:
            index_path = Path(self.config.index_path)
            with open(index_path, 'w') as f:
                json.dump(self.processed_index, f, indent=2)
            self.logger.info(f"Saved processed index with {len(self.processed_index)} entries")
        except Exception as e:
            self.logger.error(f"Failed to save processed index: {e}")
    
    def authenticate(self) -> bool:
        """Authenticate with Gmail API using OAuth 2.0"""
        try:
            creds = None
            token_path = Path(self.config.token_path)
            creds_path = Path(self.config.credentials_path)
            
            # Load existing token
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
            
            # Refresh or get new token
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    self.logger.info("Refreshing expired token")
                    creds.refresh(Request())
                else:
                    if not creds_path.exists():
                        self.logger.error(f"Credentials file not found: {creds_path}")
                        return False
                    
                    self.logger.info("Starting OAuth flow")
                    flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save token
                if not self.dry_run:
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())
                    self.logger.info("Saved authentication token")
            
            # Build service
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Successfully authenticated with Gmail API")
            return True
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return False
    
    def _rate_limit_check(self):
        """Check and enforce rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Reset counter every minute
        if time_since_last >= 60:
            self.request_count = 0
            self.last_request_time = current_time
        
        # Check if we're over the limit
        max_per_minute = self.config.rate_limit_config["maxRequestsPerMinute"]
        if self.request_count >= max_per_minute:
            sleep_time = 60 - time_since_last
            self.logger.warning(f"Rate limit reached, sleeping for {sleep_time:.1f}s")
            time.sleep(sleep_time)
            self.request_count = 0
            self.last_request_time = time.time()
        
        self.request_count += 1
    
    def _retry_with_backoff(self, func, *args, max_attempts=7, **kwargs):
        """Execute function with exponential backoff retry logic"""
        attempt = 0
        backoff_ms = self.config.rate_limit_config["initialBackoffMs"]
        max_backoff_ms = self.config.rate_limit_config["maxBackoffMs"]
        multiplier = self.config.rate_limit_config["backoffMultiplier"]
        
        while attempt < max_attempts:
            try:
                return func(*args, **kwargs)
            except HttpError as e:
                attempt += 1
                
                # Don't retry on 4xx errors (except 429)
                if 400 <= e.resp.status < 500 and e.resp.status != 429:
                    self.logger.error(f"Client error {e.resp.status}: {e}")
                    raise
                
                if attempt >= max_attempts:
                    self.logger.error(f"Max retry attempts ({max_attempts}) reached")
                    raise
                
                sleep_time = min(backoff_ms / 1000, max_backoff_ms / 1000)
                self.logger.warning(f"Request failed (attempt {attempt}/{max_attempts}), retrying in {sleep_time}s: {e}")
                time.sleep(sleep_time)
                backoff_ms *= multiplier
                
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                raise
        
        raise Exception(f"Failed after {max_attempts} attempts")
    
    def fetch_unread_emails(self, max_results: int = 50) -> List[str]:
        """Fetch unread email IDs from inbox"""
        self._rate_limit_check()
        
        try:
            results = self._retry_with_backoff(
                self.service.users().messages().list,
                userId='me',
                q='is:unread in:inbox',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            email_ids = [msg['id'] for msg in messages]
            
            self.logger.info(f"Retrieved {len(email_ids)} unread emails")
            return email_ids
            
        except Exception as e:
            self.logger.error(f"Failed to fetch unread emails: {e}")
            return []
    
    def get_email_content(self, email_id: str) -> Optional[EmailMetadata]:
        """Fetch full email content and parse metadata"""
        self._rate_limit_check()
        
        try:
            message = self._retry_with_backoff(
                self.service.users().messages().get,
                userId='me',
                id=email_id,
                format='full'
            ).execute()
            
            # Extract headers
            headers = {h['name']: h['value'] for h in message['payload']['headers']}
            sender = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            date = headers.get('Date', '')
            
            # Parse sender
            sender_match = re.match(r'(.+?)\s*<(.+?)>', sender)
            if sender_match:
                sender_name = sender_match.group(1).strip('"')
                sender_email = sender_match.group(2)
            else:
                sender_name = sender
                sender_email = sender
            
            # Extract body
            body_text = ""
            body_html = ""
            
            def extract_body(parts):
                nonlocal body_text, body_html
                for part in parts:
                    if part.get('mimeType') == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            import base64
                            body_text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    elif part.get('mimeType') == 'text/html':
                        data = part['body'].get('data', '')
                        if data:
                            import base64
                            body_html = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    elif 'parts' in part:
                        extract_body(part['parts'])
            
            if 'parts' in message['payload']:
                extract_body(message['payload']['parts'])
            else:
                # Single part message
                data = message['payload']['body'].get('data', '')
                if data:
                    import base64
                    body_text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            
            # Get labels
            labels = message.get('labelIds', [])
            
            return EmailMetadata(
                email_id=email_id,
                sender=sender,
                sender_email=sender_email,
                sender_name=sender_name,
                subject=subject,
                date=date,
                priority=Priority.LOW.value,  # Will be set later
                labels=labels,
                body_text=body_text,
                body_html=body_html
            )
            
        except Exception as e:
            self.logger.error(f"Failed to get email content for {email_id}: {e}")
            return None
    
    def is_important(self, email: EmailMetadata) -> bool:
        """Check if email matches importance criteria"""
        criteria = self.config.importance_criteria
        logic_mode = criteria.get("logicMode", "OR")
        
        matches = []
        
        # Check sender whitelist
        sender_whitelist = criteria.get("senderWhitelist", [])
        if sender_whitelist:
            sender_match = any(s.lower() in email.sender_email.lower() for s in sender_whitelist)
            matches.append(sender_match)
        
        # Check keyword patterns
        keyword_patterns = criteria.get("keywordPatterns", [])
        if keyword_patterns:
            text_to_search = f"{email.subject} {email.body_text}".lower()
            keyword_match = any(kw.lower() in text_to_search for kw in keyword_patterns)
            matches.append(keyword_match)
        
        # Check required labels
        required_labels = criteria.get("requiredLabels", [])
        if required_labels:
            label_match = any(label in email.labels for label in required_labels)
            matches.append(label_match)
        
        # Apply logic mode
        if logic_mode == "OR":
            return any(matches) if matches else False
        else:  # AND
            return all(matches) if matches else False
    
    def detect_priority(self, email: EmailMetadata) -> Priority:
        """Detect email priority based on rules"""
        rules = self.config.priority_rules
        text_to_search = f"{email.subject} {email.body_text}".lower()
        
        # Check high priority
        high_keywords = rules.get("highPriorityKeywords", [])
        if any(kw.lower() in text_to_search for kw in high_keywords):
            return Priority.HIGH
        
        vip_senders = rules.get("vipSenders", [])
        if any(s.lower() in email.sender_email.lower() for s in vip_senders):
            return Priority.HIGH
        
        high_labels = rules.get("highPriorityLabels", [])
        if any(label in email.labels for label in high_labels):
            return Priority.HIGH
        
        # Check medium priority
        medium_keywords = rules.get("mediumPriorityKeywords", [])
        if any(kw.lower() in text_to_search for kw in medium_keywords):
            return Priority.MEDIUM
        
        return Priority.LOW
    
    def is_duplicate(self, email_id: str) -> bool:
        """Check if email has already been processed"""
        return email_id in self.processed_index
    
    def generate_markdown(self, email: EmailMetadata) -> str:
        """Generate markdown content for email"""
        # Convert HTML to markdown if available
        if email.body_html:
            h = html2text.HTML2Text()
            h.ignore_links = False
            body_content = h.handle(email.body_html)
        else:
            body_content = email.body_text
        
        # Priority emoji
        priority_emoji = {
            Priority.HIGH.value: "🔴",
            Priority.MEDIUM.value: "🟡",
            Priority.LOW.value: "🟢"
        }
        
        # Generate frontmatter
        frontmatter = f"""---
email_id: "{email.email_id}"
sender: "{email.sender}"
sender_email: "{email.sender_email}"
sender_name: "{email.sender_name}"
subject: "{email.subject}"
date: "{email.date}"
priority: "{email.priority}"
labels: {json.dumps(email.labels)}
processed_at: "{datetime.now(UTC).isoformat()}Z"
source: "gmail"
type: "email_task"
status: "pending"
---

# Email: {email.subject}

**From**: {email.sender}  
**Date**: {email.date}  
**Priority**: {priority_emoji.get(email.priority, '⚪')} {email.priority.capitalize()}  
**Labels**: {', '.join(email.labels)}

## Email Content

{body_content.strip()}

---

## Action Items

- [ ] Review and respond to this email

## Links

- [View in Gmail](https://mail.google.com/mail/u/0/#inbox/{email.email_id})

---

*Processed by Gmail Watcher Skill v1.0.0*
"""
        return frontmatter
    
    def create_markdown_file(self, email: EmailMetadata, content: str) -> Optional[str]:
        """Create markdown file in Pending_Approval or Needs_Action folder"""
        # Generate filename
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        safe_subject = re.sub(r'[^\w\s-]', '', email.subject.lower())
        safe_subject = re.sub(r'[-\s]+', '-', safe_subject)[:50]
        filename = f"{timestamp}_{safe_subject}.md"
        
        # Choose folder based on approval workflow setting
        if self.config.use_approval_workflow:
            folder = Path(self.config.pending_approval_folder)
        else:
            folder = Path(self.config.needs_action_folder)
        
        filepath = folder / filename
        
        if self.dry_run:
            self.logger.info(f"[DRY RUN] Would create file: {filepath}")
            return str(filepath)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Created markdown file: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Failed to create markdown file: {e}")
            return None
    
    def mark_as_read(self, email_id: str) -> bool:
        """Mark email as read in Gmail"""
        if not self.config.mark_as_read:
            return True
        
        if self.dry_run:
            self.logger.info(f"[DRY RUN] Would mark email {email_id} as read")
            return True
        
        self._rate_limit_check()
        
        try:
            self._retry_with_backoff(
                self.service.users().messages().modify,
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            
            self.logger.info(f"Marked email {email_id} as read")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to mark email as read: {e}")
            return False
    
    def process_email(self, email_id: str) -> bool:
        """Process a single email through the Ralph Loop"""
        # PERCEPTION: Fetch email content
        email = self.get_email_content(email_id)
        if not email:
            return False
        
        # Check for duplicates
        if self.is_duplicate(email_id):
            self.logger.info(f"Skipping duplicate email: {email_id}")
            return False
        
        # REASONING: Filter and prioritize
        if not self.is_important(email):
            self.logger.info(f"Skipping non-important email: {email.subject}")
            return False
        
        priority = self.detect_priority(email)
        email.priority = priority.value
        
        self.logger.info(f"Important email detected: {email.subject} (Priority: {priority.value})")
        
        # ACTION: Create markdown and update index
        markdown_content = self.generate_markdown(email)
        filepath = self.create_markdown_file(email, markdown_content)
        
        if filepath:
            # Update processed index
            self.processed_index[email_id] = {
                "filename": Path(filepath).name,
                "processedAt": datetime.now(UTC).isoformat() + "Z",
                "priority": priority.value
            }
            self._save_processed_index()
            
            # Mark as read (optional)
            self.mark_as_read(email_id)
            
            return True
        
        return False
    
    def poll_once(self) -> Dict[str, int]:
        """Execute one polling cycle"""
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
            # Fetch unread emails
            email_ids = self.fetch_unread_emails()
            stats["retrieved"] = len(email_ids)
            
            # Process each email
            for email_id in email_ids:
                try:
                    if self.process_email(email_id):
                        stats["processed"] += 1
                        stats["created"] += 1
                    else:
                        stats["filtered"] += 1
                except Exception as e:
                    self.logger.error(f"Error processing email {email_id}: {e}")
                    stats["errors"] += 1
            
            elapsed = time.time() - start_time
            self.logger.info(f"Polling cycle completed in {elapsed:.2f}s: {stats}")
            
        except Exception as e:
            self.logger.error(f"Polling cycle failed: {e}")
            stats["errors"] += 1
        
        return stats
    
    def start_polling(self):
        """Start continuous polling"""
        self.logger.info(f"Starting continuous polling (interval: {self.config.polling_interval_ms}ms)")
        
        if self.dry_run:
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
            self.logger.info("Polling stopped by user")
        except Exception as e:
            self.logger.error(f"Polling stopped due to error: {e}")


def load_config(config_path: str) -> GmailWatcherConfig:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        return GmailWatcherConfig(
            polling_interval_ms=config_dict.get('pollingIntervalMs', 300000),
            importance_criteria=config_dict.get('importanceCriteria'),
            priority_rules=config_dict.get('priorityRules'),
            rate_limit_config=config_dict.get('rateLimitConfig'),
            needs_action_folder=config_dict.get('needsActionFolder', 'Needs_Action'),
            pending_approval_folder=config_dict.get('pendingApprovalFolder', 'Pending_Approval'),
            log_folder=config_dict.get('logFolder', 'Logs/gmail_watcher'),
            credentials_path=config_dict.get('credentialsPath', 'config/gmail-credentials.json'),
            token_path=config_dict.get('tokenPath', 'config/gmail-token.json'),
            index_path=config_dict.get('indexPath', '.index/gmail-watcher-processed.json'),
            mark_as_read=config_dict.get('markAsRead', False),
            use_approval_workflow=config_dict.get('useApprovalWorkflow', True)
        )
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        print("Using default configuration")
        return GmailWatcherConfig()
    except Exception as e:
        print(f"Error loading config: {e}")
        print("Using default configuration")
        return GmailWatcherConfig()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Gmail Watcher Agent Skill')
    parser.add_argument('command', choices=['poll', 'start', 'auth'], 
                       help='Command to execute')
    parser.add_argument('--config', default='Skills/config/gmail_watcher_config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--dry-run', action='store_true',
                       help='Run in dry-run mode (no modifications)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Create watcher
    watcher = GmailWatcher(config, dry_run=args.dry_run)
    
    # Execute command
    if args.command == 'auth':
        if watcher.authenticate():
            print("[OK] Authentication successful")
        else:
            print("[FAIL] Authentication failed")
            sys.exit(1)

    elif args.command == 'poll':
        if not watcher.authenticate():
            print("[FAIL] Authentication failed")
            sys.exit(1)
        stats = watcher.poll_once()
        print(f"\nPoll Results:")
        print(f"  Retrieved: {stats['retrieved']}")
        print(f"  Processed: {stats['processed']}")
        print(f"  Filtered: {stats['filtered']}")
        print(f"  Created: {stats['created']}")
        print(f"  Errors: {stats['errors']}")

    elif args.command == 'start':
        if not watcher.authenticate():
            print("[FAIL] Authentication failed")
            sys.exit(1)
        watcher.start_polling()


if __name__ == '__main__':
    main()
