"""
Process Gmail Messages Skill

Reads Gmail messages via Gmail API, analyzes them with AI,
and creates task files in the vault for processing.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import base64
from email import message_from_bytes
from .base_skill import BaseSkill


def process_gmail_messages(
    credentials_path: str = "config/gmail-credentials.json",
    token_path: str = "config/gmail-token.json",
    output_dir: str = "Inbox",
    max_results: int = 10,
    model_name: str = "gpt-4"
) -> List[Dict[str, Any]]:
    """
    Process Gmail messages and create task files.

    Args:
        credentials_path: Path to Gmail API credentials
        token_path: Path to OAuth token
        output_dir: Directory to save task files
        max_results: Maximum number of emails to process
        model_name: AI model to use for analysis

    Returns:
        List of processed email dictionaries with keys:
        - email_id: Gmail message ID
        - subject: Email subject
        - sender: Sender name/email
        - task_file: Path to created task file
        - priority: Detected priority (high/medium/low)
        - summary: AI-generated summary

    Example:
        >>> results = process_gmail_messages()
        >>> for result in results:
        ...     print(f"Created task: {result['task_file']} (Priority: {result['priority']})")
    """
    skill = ProcessGmailMessagesSkill(model_name)
    return skill.execute(credentials_path, token_path, output_dir, max_results)


class ProcessGmailMessagesSkill(BaseSkill):
    """Implementation of Gmail message processing skill."""

    def execute(
        self,
        credentials_path: str,
        token_path: str,
        output_dir: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """
        Execute Gmail message processing.

        Args:
            credentials_path: Gmail API credentials path
            token_path: OAuth token path
            output_dir: Output directory for tasks
            max_results: Max emails to process

        Returns:
            List of processing results
        """
        self.logger.info(f"Processing Gmail messages (max: {max_results})")

        # Ensure output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        try:
            # Import Gmail API dependencies
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build

            # Authenticate with Gmail API
            service = self._authenticate(credentials_path, token_path)
            if service is None:
                self.logger.error("Gmail authentication failed")
                return []

            # Fetch unread emails
            messages = self._fetch_emails(service, max_results)

            # Load processed index
            processed_index = self._load_processed_index()

            results = []
            for msg in messages:
                # Skip already processed emails
                if msg['id'] in processed_index:
                    continue

                # Process the email
                result = self._process_single_email(msg, output_path, service)
                results.append(result)

                # Mark as processed
                if result.get('task_file'):
                    processed_index.append(msg['id'])
                    self._save_processed_index(processed_index)

            self.logger.info(f"Processed {len(results)} Gmail messages")
            return results

        except ImportError as e:
            self.logger.error(f"Missing Gmail API dependencies: {e}")
            self.logger.error("Install with: pip install google-auth google-auth-oauthlib google-api-python-client")
            return []
        except Exception as e:
            self.logger.error(f"Failed to process Gmail messages: {e}")
            return []

    def _authenticate(self, credentials_path: str, token_path: str) -> Optional[Any]:
        """
        Authenticate with Gmail API.

        Args:
            credentials_path: Path to credentials file
            token_path: Path to token file

        Returns:
            Gmail API service object or None
        """
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

        creds = None

        # Load existing token
        if Path(token_path).exists():
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # Refresh or authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not Path(credentials_path).exists():
                    self.logger.error(f"Credentials file not found: {credentials_path}")
                    return None

                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save token
            with open(token_path, 'w', encoding='utf-8') as token:
                token.write(creds.to_json())

        # Build service
        service = build('gmail', 'v1', credentials=creds)
        self.logger.info("Gmail API authentication successful")
        return service

    def _fetch_emails(self, service: Any, max_results: int) -> List[Dict]:
        """
        Fetch unread emails from Gmail.

        Args:
            service: Gmail API service
            max_results: Maximum emails to fetch

        Returns:
            List of email message dicts
        """
        # Fetch unread messages
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])

        email_data = []
        for msg in messages:
            # Fetch full message details
            full_msg = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = full_msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')

            # Extract body
            body = self._extract_body(full_msg['payload'])

            email_data.append({
                'id': msg['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'body': body,
                'threadId': full_msg.get('threadId')
            })

        self.logger.info(f"Fetched {len(email_data)} emails")
        return email_data

    def _extract_body(self, payload: Dict) -> str:
        """
        Extract email body from payload.

        Args:
            payload: Email payload

        Returns:
            Email body text
        """
        body = ""

        if 'parts' in payload:
            # Multipart message
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
        elif 'body' in payload and 'data' in payload['body']:
            # Simple message
            data = payload['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8')

        return body

    def _process_single_email(
        self,
        email: Dict,
        output_path: Path,
        service: Any
    ) -> Dict[str, Any]:
        """
        Process a single email and create task file.

        Args:
            email: Email data dictionary
            output_path: Output directory
            service: Gmail API service

        Returns:
            Processing result dictionary
        """
        try:
            # Analyze email with AI
            analysis = self._analyze_email(email)

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_subject = self._sanitize_filename(email['subject'])[:50]
            filename = f"email_{timestamp}_{safe_subject}.md"
            filepath = output_path / filename

            # Create task file content
            content = self._create_task_file(email, analysis)
            self.write_markdown(str(filepath), content)

            # Mark email as read in Gmail
            self._mark_as_read(service, email['id'])

            self.logger.info(f"Created task for: {email['subject']}")

            return {
                'email_id': email['id'],
                'subject': email['subject'],
                'sender': email['sender'],
                'task_file': str(filepath),
                'priority': analysis['priority'],
                'summary': analysis['summary'],
                'status': 'success'
            }

        except Exception as e:
            self.logger.error(f"Failed to process email {email['id']}: {e}")
            return {
                'email_id': email['id'],
                'subject': email['subject'],
                'sender': email['sender'],
                'task_file': '',
                'priority': 'unknown',
                'summary': '',
                'status': 'error',
                'error': str(e)
            }

    def _analyze_email(self, email: Dict) -> Dict[str, str]:
        """
        Analyze email content with AI.

        Args:
            email: Email data

        Returns:
            Analysis results (priority, summary, action_items)
        """
        system_prompt = """You are an email analysis assistant.
Analyze emails and determine:
1. Priority level (high/medium/low)
2. Concise summary
3. Action items

Priority criteria:
- HIGH: Urgent keywords (urgent, asap, emergency, deadline), important senders
- MEDIUM: Action required, questions, requests
- LOW: Informational, newsletters, notifications"""

        user_prompt = f"""Analyze this email:

From: {email['sender']}
Subject: {email['subject']}
Date: {email['date']}

Content:
{email['body']}

Provide analysis in this format:
Priority: [high/medium/low]
Summary: [2-3 sentence summary]
Action Items: [bullet list of required actions]
"""

        # Call AI model
        analysis_text = self.ai_client.call(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=500
        )

        # Parse analysis
        priority = 'medium'
        summary = ''
        action_items = []

        for line in analysis_text.split('\n'):
            if line.startswith('Priority:'):
                priority = line.split(':', 1)[1].strip().lower()
            elif line.startswith('Summary:'):
                summary = line.split(':', 1)[1].strip()
            elif line.startswith('Action Items:'):
                action_items.append(line.split(':', 1)[1].strip())

        return {
            'priority': priority,
            'summary': summary,
            'action_items': action_items
        }

    def _create_task_file(self, email: Dict, analysis: Dict) -> str:
        """
        Create markdown task file content.

        Args:
            email: Email data
            analysis: AI analysis results

        Returns:
            Markdown content
        """
        # Parse sender
        sender_parts = email['sender'].split('<')
        sender_name = sender_parts[0].strip() if sender_parts else 'Unknown'
        sender_email = sender_parts[1].strip('>') if len(sender_parts) > 1 else ''

        content = f"""---
type: email_task
source: gmail
email_id: "{email['id']}"
sender_name: "{sender_name}"
sender_email: "{sender_email}"
subject: "{email['subject']}"
received: "{email['date']}"
priority: "{analysis['priority']}"
status: "pending"
---

# Email: {email['subject']}

**From**: {email['sender']}
**Received**: {email['date']}
**Priority**: {"🔴 High" if analysis['priority'] == 'high' else "🟡 Medium" if analysis['priority'] == 'medium' else "🟢 Low"}

## Summary

{analysis['summary']}

## Email Content

{email['body']}

## Action Items

"""
        # Add action items as checkboxes
        for item in analysis.get('action_items', ['Review and respond to this email']):
            content += f"- [ ] {item}\n"

        content += """
## Notes

_Add your notes here_

---

*Processed by Gmail Watcher Skill*
"""
        return content

    def _mark_as_read(self, service: Any, email_id: str) -> None:
        """
        Mark email as read in Gmail.

        Args:
            service: Gmail API service
            email_id: Gmail message ID
        """
        try:
            service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            self.logger.info(f"Marked email {email_id} as read")
        except Exception as e:
            self.logger.warning(f"Failed to mark email as read: {e}")

    def _sanitize_filename(self, subject: str) -> str:
        """
        Sanitize subject for filename.

        Args:
            subject: Email subject

        Returns:
            Sanitized filename-safe string
        """
        # Remove invalid filename characters
        invalid_chars = '<>:"/\\|？*'
        for char in invalid_chars:
            subject = subject.replace(char, '')
        return subject.replace(' ', '_').lower()

    def _load_processed_index(self) -> List[str]:
        """Load processed emails index."""
        index_file = Path(".index/gmail-processed.json")
        if index_file.exists():
            import json
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save_processed_index(self, index: List[str]) -> None:
        """Save processed emails index."""
        index_file = Path(".index/gmail-processed.json")
        import json
        index_file.parent.mkdir(parents=True, exist_ok=True)
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)


# Example usage
if __name__ == "__main__":
    results = process_gmail_messages()
    print(f"\nProcessed {len(results)} emails:")
    for result in results:
        status = "✅" if result['status'] == 'success' else "❌"
        print(f"  {status} [{result['priority'].upper()}] {result['subject'][:50]}")
        print(f"      → {result['task_file']}")
