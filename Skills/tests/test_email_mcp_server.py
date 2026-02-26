"""
Unit tests for EmailMCPServer

Tests email sending functionality, parameter validation, and error handling.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.email_mcp_server import EmailMCPServer
from mcp_servers.base_mcp_server import TextContent


class TestEmailMCPServer:
    """Test suite for EmailMCPServer."""
    
    def test_server_initialization(self):
        """Test that Email MCP Server initializes correctly."""
        server = EmailMCPServer()
        assert server.name == "email_mcp_server"
        assert "send_email" in server.tools
    
    def test_tool_registration(self):
        """Test that send_email tool is registered correctly."""
        server = EmailMCPServer()
        
        send_email_tool = server.get_tool("send_email")
        assert send_email_tool is not None
        assert send_email_tool.name == "send_email"
        assert send_email_tool.description == "Send an email message via Gmail"
        
        # Check schema
        schema = send_email_tool.inputSchema
        assert "to" in schema["properties"]
        assert "subject" in schema["properties"]
        assert "body" in schema["properties"]
        assert schema["required"] == ["to", "subject", "body"]
    
    def test_parameter_validation_success(self):
        """Test successful parameter validation for send_email."""
        server = EmailMCPServer()
        
        # Minimal valid parameters
        is_valid, error = server.validate_parameters(
            "send_email",
            {
                "to": "recipient@example.com",
                "subject": "Test Subject",
                "body": "Test body"
            }
        )
        assert is_valid is True
        assert error is None
        
        # With optional parameters
        is_valid, error = server.validate_parameters(
            "send_email",
            {
                "to": "recipient@example.com",
                "subject": "Test Subject",
                "body": "Test body",
                "cc": ["cc1@example.com", "cc2@example.com"],
                "bcc": ["bcc@example.com"],
                "html": True
            }
        )
        assert is_valid is True
        assert error is None
    
    def test_parameter_validation_missing_required(self):
        """Test validation fails when required parameters are missing."""
        server = EmailMCPServer()
        
        # Missing 'to'
        is_valid, error = server.validate_parameters(
            "send_email",
            {"subject": "Test", "body": "Test body"}
        )
        assert is_valid is False
        assert "Missing required parameter: to" in error
        
        # Missing 'subject'
        is_valid, error = server.validate_parameters(
            "send_email",
            {"to": "test@example.com", "body": "Test body"}
        )
        assert is_valid is False
        assert "Missing required parameter: subject" in error
        
        # Missing 'body'
        is_valid, error = server.validate_parameters(
            "send_email",
            {"to": "test@example.com", "subject": "Test"}
        )
        assert is_valid is False
        assert "Missing required parameter: body" in error
    
    def test_parameter_validation_wrong_types(self):
        """Test validation fails for wrong parameter types."""
        server = EmailMCPServer()
        
        # 'to' should be string, not array
        is_valid, error = server.validate_parameters(
            "send_email",
            {
                "to": ["recipient@example.com"],
                "subject": "Test",
                "body": "Test body"
            }
        )
        assert is_valid is False
        assert "Invalid type" in error
        
        # 'cc' should be array, not string
        is_valid, error = server.validate_parameters(
            "send_email",
            {
                "to": "recipient@example.com",
                "subject": "Test",
                "body": "Test body",
                "cc": "cc@example.com"
            }
        )
        assert is_valid is False
        assert "Invalid type" in error
    
    def test_create_message_plain_text(self):
        """Test creating a plain text email message."""
        server = EmailMCPServer()
        
        message = server._create_message(
            to="recipient@example.com",
            subject="Test Subject",
            body="Test body content"
        )
        
        assert "raw" in message
        assert isinstance(message["raw"], str)
    
    def test_create_message_html(self):
        """Test creating an HTML email message."""
        server = EmailMCPServer()
        
        message = server._create_message(
            to="recipient@example.com",
            subject="Test Subject",
            body="<h1>Test</h1><p>HTML body</p>",
            html=True
        )
        
        assert "raw" in message
        assert isinstance(message["raw"], str)
    
    def test_create_message_with_cc_bcc(self):
        """Test creating a message with CC and BCC recipients."""
        server = EmailMCPServer()
        
        message = server._create_message(
            to="recipient@example.com",
            subject="Test Subject",
            body="Test body",
            cc=["cc1@example.com", "cc2@example.com"],
            bcc=["bcc@example.com"]
        )
        
        assert "raw" in message
        assert isinstance(message["raw"], str)
    
    @pytest.mark.asyncio
    @patch('mcp_servers.email_mcp_server.build')
    @patch('mcp_servers.email_mcp_server.Credentials')
    async def test_handle_tool_call_success(self, mock_creds, mock_build):
        """Test successful email sending."""
        # Mock Gmail API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Mock send response
        mock_send = MagicMock()
        mock_send.execute.return_value = {"id": "msg_12345"}
        mock_service.users().messages().send.return_value = mock_send
        
        # Mock credentials
        mock_creds_instance = MagicMock()
        mock_creds_instance.valid = True
        mock_creds.from_authorized_user_file.return_value = mock_creds_instance
        
        server = EmailMCPServer()
        server.service = mock_service  # Set service directly to skip auth
        
        result = await server.handle_tool_call(
            "send_email",
            {
                "to": "recipient@example.com",
                "subject": "Test Subject",
                "body": "Test body"
            }
        )
        
        assert result.type == "text"
        assert "Email sent successfully" in result.text
        assert "msg_12345" in result.text
    
    @pytest.mark.asyncio
    async def test_handle_tool_call_unknown_tool(self):
        """Test handling unknown tool."""
        server = EmailMCPServer()
        
        result = await server.handle_tool_call(
            "unknown_tool",
            {}
        )
        
        assert result.type == "text"
        assert "Error: Unknown tool" in result.text
    
    @pytest.mark.asyncio
    @patch('mcp_servers.email_mcp_server.build')
    async def test_handle_tool_call_api_error(self, mock_build):
        """Test handling Gmail API errors."""
        from googleapiclient.errors import HttpError
        from http.client import HTTPResponse
        from io import BytesIO
        
        # Mock Gmail API service that raises HttpError
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Create a mock HttpError
        resp = Mock()
        resp.status = 400
        resp.reason = "Bad Request"
        
        mock_send = MagicMock()
        mock_send.execute.side_effect = HttpError(resp, b'{"error": "Invalid request"}')
        mock_service.users().messages().send.return_value = mock_send
        
        server = EmailMCPServer()
        server.service = mock_service
        
        result = await server.handle_tool_call(
            "send_email",
            {
                "to": "recipient@example.com",
                "subject": "Test",
                "body": "Test"
            }
        )
        
        assert result.type == "text"
        assert "Error:" in result.text
        assert "Gmail API error" in result.text
    
    @pytest.mark.asyncio
    @patch('mcp_servers.email_mcp_server.build')
    async def test_execute_tool_with_validation(self, mock_build):
        """Test execute_tool with parameter validation."""
        # Mock Gmail API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        mock_send = MagicMock()
        mock_send.execute.return_value = {"id": "msg_12345"}
        mock_service.users().messages().send.return_value = mock_send
        
        server = EmailMCPServer()
        server.service = mock_service
        
        # Valid parameters
        result = await server.execute_tool(
            "send_email",
            {
                "to": "recipient@example.com",
                "subject": "Test",
                "body": "Test body"
            }
        )
        
        assert "Email sent successfully" in result.text
        
        # Invalid parameters (missing required field)
        result = await server.execute_tool(
            "send_email",
            {
                "subject": "Test",
                "body": "Test body"
            }
        )
        
        assert "Error:" in result.text
        assert "Missing required parameter" in result.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
