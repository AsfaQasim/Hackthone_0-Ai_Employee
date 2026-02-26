"""
MCP Servers Package

This package contains Model Context Protocol (MCP) server implementations
for the AI Employee System.
"""

from .base_mcp_server import BaseMCPServer, Tool, TextContent
from .email_mcp_server import EmailMCPServer
from .whatsapp_mcp_server import WhatsAppMCPServer
from .social_media_mcp_server import SocialMediaMCPServer

__all__ = [
    'BaseMCPServer',
    'Tool',
    'TextContent',
    'EmailMCPServer',
    'WhatsAppMCPServer',
    'SocialMediaMCPServer'
]
