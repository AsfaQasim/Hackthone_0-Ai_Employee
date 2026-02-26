"""
Email MCP Server

Implements email sending functionality through the Gmail API.
Provides the send_email tool for composing and sending emails.
"""

from typing import Dict, Any, List, Optional
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .base_mcp_server import BaseMCPServer, Tool, TextContent


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class EmailMCPServer(BaseMCPServer):
    """
    Email MCP Server for sending emails via Gmail API.
    
    Provides the send_email tool with parameter validation and error handling.
    """
    
    def __init__(self, name: str = "email_mcp_server", credentials_path: str = "config/gmail-credentials.json", token_path: str = "config/gmail-token.json"):
        """
        Initialize the Email MCP Server.
        
        Args:
            name: Server name
            credentials_path: Path to Gmail API credentials file
            token_path: Path to store/load OAuth token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        super().__init__(name)
    
    def register_tools(self) -> None:
        """Register the send_email tool."""
        send_email_tool = Tool(
            name="send_email",
            description="Send an email message via Gmail",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "body": {
                        "type": "string",
                        "description": "Email body content (plain text or HTML)"
                    },
                    "cc": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "CC recipients (optional)"
                    },
                    "bcc": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "BCC recipients (optional)"
                    },
                    "html": {
                        "type": "boolean",
                        "description": "Whether the body is HTML (default: false)"
                    }
                },
                "required": ["to", "subject", "body"]
            }
        )
        self.add_tool(send_email_tool)
    
    def _authenticate(self) -> None:
        """
        Authenticate with Gmail API using OAuth2.
        
        Raises:
            Exception: If authentication fails
        """
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise Exception(f"Credentials file not found: {self.credentials_path}")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        # Build Gmail service
        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info("Gmail API authentication successful")
    
    def _create_message(self, to: str, subject: str, body: str, cc: Optional[List[str]] = None, bcc: Optional[List[str]] = None, html: bool = False) -> Dict[str, Any]:
        """
        Create an email message.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            cc: CC recipients
            bcc: BCC recipients
            html: Whether body is HTML
            
        Returns:
            Email message dict ready for sending
        """
        # Create message
        if html:
            message = MIMEMultipart('alternative')
            part = MIMEText(body, 'html')
            message.attach(part)
        else:
            message = MIMEText(body, 'plain')
        
        message['to'] = to
        message['subject'] = subject
        
        if cc:
            message['cc'] = ', '.join(cc)
        
        if bcc:
            message['bcc'] = ', '.join(bcc)
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        return {'raw': raw_message}
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> TextContent:
        """
        Handle tool call requests.
        
        Args:
            name: Tool name (should be "send_email")
            arguments: Tool arguments
            
        Returns:
            TextContent with success or error message
        """
        if name != "send_email":
            return TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )
        
        try:
            # Authenticate if not already done
            if self.service is None:
                self._authenticate()
            
            # Extract arguments
            to = arguments['to']
            subject = arguments['subject']
            body = arguments['body']
            cc = arguments.get('cc', [])
            bcc = arguments.get('bcc', [])
            html = arguments.get('html', False)
            
            # Create and send message
            message = self._create_message(to, subject, body, cc, bcc, html)
            
            result = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            message_id = result.get('id')
            self.logger.info(f"Email sent successfully. Message ID: {message_id}")
            
            return TextContent(
                type="text",
                text=f"Email sent successfully to {to}. Message ID: {message_id}"
            )
            
        except HttpError as error:
            error_msg = f"Gmail API error: {error.reason}"
            self.logger.error(error_msg, exc_info=True)
            return TextContent(
                type="text",
                text=f"Error: {error_msg}"
            )
        
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return TextContent(
                type="text",
                text=f"Error: {error_msg}"
            )


# Example usage
if __name__ == "__main__":
    import asyncio
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    async def test_email_server():
        """Test the Email MCP Server."""
        server = EmailMCPServer()
        
        # List available tools
        print("Available tools:")
        for tool in server.list_tools():
            print(f"  - {tool['name']}: {tool['description']}")
        
        # Test send_email (with dry run - comment out to actually send)
        # result = await server.execute_tool(
        #     "send_email",
        #     {
        #         "to": "recipient@example.com",
        #         "subject": "Test Email from MCP Server",
        #         "body": "This is a test email sent from the Email MCP Server."
        #     }
        # )
        # print(f"\nResult: {result.text}")
    
    asyncio.run(test_email_server())
