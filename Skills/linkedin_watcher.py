"""
LinkedIn Watcher

Monitors LinkedIn for messages, connection requests, and post engagement.
Uses LinkedIn API with OAuth2 authentication.

Note: Requires LinkedIn API access and proper OAuth2 setup.
"""

import logging
import time
from pathlib import Path
from datetime import datetime, UTC
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
import requests

from base_watcher import BaseWatcher, WatcherConfig


@dataclass
class LinkedInWatcherConfig(WatcherConfig):
    """Configuration for LinkedIn Watcher"""
    access_token: str = ""
    client_id: str = ""
    client_secret: str = ""
    polling_interval_ms: int = 300000  # 5 minutes (rate limit compliance)
    monitor_messages: bool = True
    monitor_connections: bool = True
    monitor_engagement: bool = True


class LinkedInWatcher(BaseWatcher):
    """
    LinkedIn Watcher implementation using LinkedIn API.
    
    Monitors:
    - Direct messages
    - Connection requests
    - Post engagement (likes, comments, shares)
    """
    
    def __init__(self, config: LinkedInWatcherConfig):
        super().__init__(config, "LinkedInWatcher")
        self.config: LinkedInWatcherConfig = config
        self.access_token = config.access_token
        self.api_base = "https://api.linkedin.com/v2"
        self.processed_items: set = set()
        
        # Rate limiting
        self.request_count = 0
        self.last_request_time = time.time()
        self.max_requests_per_minute = 60
    
    def authenticate(self) -> bool:
        """
        Authenticate with LinkedIn API.
        
        Returns:
            True if authentication successful, False otherwise
        """
        if not self.access_token:
            self.logger.error("No access token provided")
            self.logger.info("Please set LINKEDIN_ACCESS_TOKEN in your .env file")
            return False
        
        try:
            # Test authentication by getting user profile
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_base}/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                self.logger.info(f"Authenticated as: {user_data.get('localizedFirstName', 'Unknown')}")
                return True
            else:
                self.logger.error(f"Authentication failed: {response.status_code}")
                return False
        
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
        if self.request_count >= self.max_requests_per_minute:
            sleep_time = 60 - time_since_last
            self.logger.warning(f"Rate limit reached, sleeping for {sleep_time:.1f}s")
            time.sleep(sleep_time)
            self.request_count = 0
            self.last_request_time = time.time()
        
        self.request_count += 1
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make authenticated API request with rate limiting"""
        self._rate_limit_check()
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_base}/{endpoint}",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.warning(f"API request failed: {response.status_code}")
                return None
        
        except Exception as e:
            self.logger.error(f"API request error: {e}")
            return None
    
    def check_for_new_items(self) -> List[str]:
        """
        Check LinkedIn for new items to process.
        
        Returns:
            List of item IDs
        """
        item_ids = []
        
        try:
            # Check messages
            if self.config.monitor_messages:
                message_ids = self._check_messages()
                item_ids.extend(message_ids)
            
            # Check connection requests
            if self.config.monitor_connections:
                connection_ids = self._check_connections()
                item_ids.extend(connection_ids)
            
            # Check engagement
            if self.config.monitor_engagement:
                engagement_ids = self._check_engagement()
                item_ids.extend(engagement_ids)
            
            self.logger.info(f"Found {len(item_ids)} new items")
            return item_ids
        
        except Exception as e:
            self.logger.error(f"Failed to check for new items: {e}")
            return []
    
    def _check_messages(self) -> List[str]:
        """Check for new direct messages"""
        try:
            # Note: This is a simplified implementation
            # Real implementation would use LinkedIn Messaging API
            data = self._make_request("messages")
            
            if not data:
                return []
            
            message_ids = []
            for message in data.get('elements', []):
                msg_id = f"message_{message.get('id', '')}"
                if msg_id not in self.processed_items:
                    message_ids.append(msg_id)
            
            return message_ids
        
        except Exception as e:
            self.logger.error(f"Failed to check messages: {e}")
            return []
    
    def _check_connections(self) -> List[str]:
        """Check for new connection requests"""
        try:
            # Note: This is a simplified implementation
            data = self._make_request("invitations")
            
            if not data:
                return []
            
            connection_ids = []
            for invitation in data.get('elements', []):
                inv_id = f"connection_{invitation.get('id', '')}"
                if inv_id not in self.processed_items:
                    connection_ids.append(inv_id)
            
            return connection_ids
        
        except Exception as e:
            self.logger.error(f"Failed to check connections: {e}")
            return []
    
    def _check_engagement(self) -> List[str]:
        """Check for post engagement (likes, comments)"""
        try:
            # Note: This is a simplified implementation
            # Real implementation would check recent posts for engagement
            data = self._make_request("shares")
            
            if not data:
                return []
            
            engagement_ids = []
            for share in data.get('elements', []):
                # Check if post has new engagement
                engagement_count = share.get('totalShareStatistics', {}).get('likeCount', 0)
                if engagement_count > 0:
                    eng_id = f"engagement_{share.get('id', '')}"
                    if eng_id not in self.processed_items:
                        engagement_ids.append(eng_id)
            
            return engagement_ids
        
        except Exception as e:
            self.logger.error(f"Failed to check engagement: {e}")
            return []
    
    def get_item_content(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch full content for a specific LinkedIn item.
        
        Args:
            item_id: Item identifier (format: type_id)
            
        Returns:
            Dictionary with item metadata and content
        """
        try:
            item_type, item_ref = item_id.split('_', 1)
            
            if item_type == 'message':
                return self._get_message_content(item_ref)
            elif item_type == 'connection':
                return self._get_connection_content(item_ref)
            elif item_type == 'engagement':
                return self._get_engagement_content(item_ref)
            
            return None
        
        except Exception as e:
            self.logger.error(f"Failed to get item content: {e}")
            return None
    
    def _get_message_content(self, message_id: str) -> Optional[Dict]:
        """Get message details"""
        data = self._make_request(f"messages/{message_id}")
        
        if not data:
            return None
        
        return {
            'id': f"message_{message_id}",
            'type': 'message',
            'sender': data.get('from', {}).get('name', 'Unknown'),
            'subject': data.get('subject', 'No Subject'),
            'body': data.get('body', ''),
            'timestamp': datetime.now(UTC).isoformat() + 'Z',
            'source': 'linkedin'
        }
    
    def _get_connection_content(self, invitation_id: str) -> Optional[Dict]:
        """Get connection request details"""
        data = self._make_request(f"invitations/{invitation_id}")
        
        if not data:
            return None
        
        return {
            'id': f"connection_{invitation_id}",
            'type': 'connection',
            'from_name': data.get('from', {}).get('name', 'Unknown'),
            'from_headline': data.get('from', {}).get('headline', ''),
            'message': data.get('message', ''),
            'timestamp': datetime.now(UTC).isoformat() + 'Z',
            'source': 'linkedin'
        }
    
    def _get_engagement_content(self, share_id: str) -> Optional[Dict]:
        """Get post engagement details"""
        data = self._make_request(f"shares/{share_id}")
        
        if not data:
            return None
        
        stats = data.get('totalShareStatistics', {})
        
        return {
            'id': f"engagement_{share_id}",
            'type': 'engagement',
            'post_text': data.get('text', {}).get('text', ''),
            'likes': stats.get('likeCount', 0),
            'comments': stats.get('commentCount', 0),
            'shares': stats.get('shareCount', 0),
            'timestamp': datetime.now(UTC).isoformat() + 'Z',
            'source': 'linkedin'
        }
    
    def is_important(self, item: Dict[str, Any]) -> bool:
        """
        Check if LinkedIn item is important.
        
        Args:
            item: Item metadata
            
        Returns:
            True if item should be processed
        """
        item_type = item.get('type', '')
        
        # All messages and connections are important
        if item_type in ['message', 'connection']:
            return True
        
        # Engagement is important if it's significant
        if item_type == 'engagement':
            likes = item.get('likes', 0)
            comments = item.get('comments', 0)
            return likes > 5 or comments > 0
        
        return False
    
    def detect_priority(self, item: Dict[str, Any]) -> str:
        """
        Detect item priority.
        
        Args:
            item: Item metadata
            
        Returns:
            Priority level: "high", "medium", or "low"
        """
        item_type = item.get('type', '')
        
        # Messages are high priority
        if item_type == 'message':
            return 'high'
        
        # Connection requests are medium priority
        if item_type == 'connection':
            return 'medium'
        
        # Engagement depends on volume
        if item_type == 'engagement':
            comments = item.get('comments', 0)
            if comments > 5:
                return 'high'
            elif comments > 0:
                return 'medium'
        
        return 'low'
    
    def generate_markdown(self, item: Dict[str, Any]) -> str:
        """
        Generate markdown content for LinkedIn item.
        
        Args:
            item: Item metadata
            
        Returns:
            Markdown formatted string
        """
        item_type = item.get('type', '')
        priority = item.get('priority', 'low')
        
        priority_emoji = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }
        
        if item_type == 'message':
            content = f"""---
type: linkedin_message
sender: "{item.get('sender', 'Unknown')}"
subject: "{item.get('subject', 'No Subject')}"
timestamp: "{item.get('timestamp', '')}"
priority: "{priority}"
status: "pending"
source: "linkedin"
item_id: "{item.get('id', '')}"
---

# LinkedIn Message: {item.get('subject', 'No Subject')}

**From**: {item.get('sender', 'Unknown')}  
**Priority**: {priority_emoji.get(priority, '⚪')} {priority.capitalize()}  
**Received**: {item.get('timestamp', '')}

## Message Content

{item.get('body', '')}

---

## Action Items

- [ ] Review and respond to this message
- [ ] Check sender's profile

---

*Processed by LinkedIn Watcher v1.0.0*
"""
        
        elif item_type == 'connection':
            content = f"""---
type: linkedin_connection
from_name: "{item.get('from_name', 'Unknown')}"
from_headline: "{item.get('from_headline', '')}"
timestamp: "{item.get('timestamp', '')}"
priority: "{priority}"
status: "pending"
source: "linkedin"
item_id: "{item.get('id', '')}"
---

# LinkedIn Connection Request

**From**: {item.get('from_name', 'Unknown')}  
**Headline**: {item.get('from_headline', '')}  
**Priority**: {priority_emoji.get(priority, '⚪')} {priority.capitalize()}

## Message

{item.get('message', 'No message included')}

---

## Action Items

- [ ] Review profile
- [ ] Accept or decline connection

---

*Processed by LinkedIn Watcher v1.0.0*
"""
        
        elif item_type == 'engagement':
            content = f"""---
type: linkedin_engagement
likes: {item.get('likes', 0)}
comments: {item.get('comments', 0)}
shares: {item.get('shares', 0)}
timestamp: "{item.get('timestamp', '')}"
priority: "{priority}"
status: "pending"
source: "linkedin"
item_id: "{item.get('id', '')}"
---

# LinkedIn Post Engagement

**Priority**: {priority_emoji.get(priority, '⚪')} {priority.capitalize()}  
**Likes**: {item.get('likes', 0)}  
**Comments**: {item.get('comments', 0)}  
**Shares**: {item.get('shares', 0)}

## Post Content

{item.get('post_text', '')}

---

## Action Items

- [ ] Review comments
- [ ] Respond to engagement

---

*Processed by LinkedIn Watcher v1.0.0*
"""
        
        else:
            content = f"""---
type: linkedin_item
timestamp: "{item.get('timestamp', '')}"
priority: "{priority}"
status: "pending"
source: "linkedin"
---

# LinkedIn Item

{json.dumps(item, indent=2)}
"""
        
        return content


# CLI interface
if __name__ == "__main__":
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="LinkedIn Watcher for AI Employee")
    parser.add_argument(
        "command",
        choices=["auth", "poll", "start"],
        help="Command to execute"
    )
    parser.add_argument(
        "--vault-path",
        default=".",
        help="Path to vault root directory"
    )
    parser.add_argument(
        "--access-token",
        default=os.getenv("LINKEDIN_ACCESS_TOKEN", ""),
        help="LinkedIn API access token"
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
    
    # Create config
    config = LinkedInWatcherConfig(
        vault_path=args.vault_path,
        access_token=args.access_token,
        dry_run=args.dry_run
    )
    
    # Create watcher
    watcher = LinkedInWatcher(config)
    
    if args.command == "auth":
        if watcher.authenticate():
            print("✓ Authentication successful")
        else:
            print("✗ Authentication failed")
            print("\nTo get a LinkedIn access token:")
            print("1. Create a LinkedIn App at https://www.linkedin.com/developers/")
            print("2. Get OAuth2 credentials")
            print("3. Set LINKEDIN_ACCESS_TOKEN environment variable")
            exit(1)
    
    elif args.command == "poll":
        if not watcher.authenticate():
            print("✗ Authentication failed")
            exit(1)
        
        stats = watcher.poll_once()
        print(f"\nPoll Results:")
        print(f"  Retrieved: {stats['retrieved']}")
        print(f"  Processed: {stats['processed']}")
        print(f"  Filtered: {stats['filtered']}")
        print(f"  Created: {stats['created']}")
        print(f"  Errors: {stats['errors']}")
    
    elif args.command == "start":
        watcher.start()
