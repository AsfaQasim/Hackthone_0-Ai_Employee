"""
Unit tests for SocialMediaMCPServer

Tests social media posting functionality, parameter validation, and content tracking.
"""

import pytest
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.social_media_mcp_server import SocialMediaMCPServer
from mcp_servers.base_mcp_server import TextContent


class TestSocialMediaMCPServer:
    """Test suite for SocialMediaMCPServer."""
    
    @pytest.fixture
    def temp_vault(self):
        """Create a temporary vault directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def server(self, temp_vault):
        """Create a SocialMediaMCPServer instance with temp vault."""
        return SocialMediaMCPServer(vault_path=temp_vault)
    
    def test_server_initialization(self, server):
        """Test that Social Media MCP Server initializes correctly."""
        assert server.name == "social_media_mcp_server"
        assert "post_to_linkedin" in server.tools
        assert "post_to_facebook" in server.tools
        assert "post_to_instagram" in server.tools
        assert "post_to_twitter" in server.tools
    
    def test_tool_registration(self, server):
        """Test that all social media tools are registered correctly."""
        tools = server.list_tools()
        tool_names = [t['name'] for t in tools]
        
        assert "post_to_linkedin" in tool_names
        assert "post_to_facebook" in tool_names
        assert "post_to_instagram" in tool_names
        assert "post_to_twitter" in tool_names
    
    def test_linkedin_tool_schema(self, server):
        """Test LinkedIn tool schema."""
        linkedin_tool = server.get_tool("post_to_linkedin")
        
        assert linkedin_tool is not None
        assert linkedin_tool.name == "post_to_linkedin"
        
        schema = linkedin_tool.inputSchema
        assert "content" in schema["properties"]
        assert "visibility" in schema["properties"]
        assert schema["required"] == ["content"]
    
    def test_instagram_tool_schema(self, server):
        """Test Instagram tool schema requires media_url."""
        instagram_tool = server.get_tool("post_to_instagram")
        
        schema = instagram_tool.inputSchema
        assert "caption" in schema["properties"]
        assert "media_url" in schema["properties"]
        assert set(schema["required"]) == {"caption", "media_url"}
    
    def test_twitter_tool_schema(self, server):
        """Test Twitter tool schema."""
        twitter_tool = server.get_tool("post_to_twitter")
        
        schema = twitter_tool.inputSchema
        assert "content" in schema["properties"]
        assert schema["required"] == ["content"]
    
    @pytest.mark.asyncio
    async def test_post_to_linkedin_success(self, server):
        """Test successful LinkedIn posting."""
        result = await server.execute_tool(
            "post_to_linkedin",
            {
                "content": "Test LinkedIn post",
                "visibility": "public"
            }
        )
        
        assert result.type == "text"
        assert "Successfully posted to LinkedIn" in result.text
        assert "Post ID:" in result.text
        
        # Check tracking file was created
        tracking_files = list(server.tracking_dir.glob("linkedin_*.md"))
        assert len(tracking_files) == 1
    
    @pytest.mark.asyncio
    async def test_post_to_linkedin_with_media(self, server):
        """Test LinkedIn posting with media."""
        result = await server.execute_tool(
            "post_to_linkedin",
            {
                "content": "Test post with media",
                "visibility": "connections",
                "media_url": "https://example.com/image.jpg"
            }
        )
        
        assert "Successfully posted to LinkedIn" in result.text
    
    @pytest.mark.asyncio
    async def test_post_to_linkedin_content_too_long(self, server):
        """Test LinkedIn posting with content exceeding limit."""
        long_content = "A" * 3001  # Exceeds 3000 character limit
        
        result = await server.execute_tool(
            "post_to_linkedin",
            {
                "content": long_content
            }
        )
        
        assert "Error:" in result.text
        assert "exceeds 3000 characters" in result.text
    
    @pytest.mark.asyncio
    async def test_post_to_facebook_success(self, server):
        """Test successful Facebook posting."""
        result = await server.execute_tool(
            "post_to_facebook",
            {
                "content": "Test Facebook post",
                "visibility": "friends"
            }
        )
        
        assert "Successfully posted to Facebook" in result.text
        assert "Post ID:" in result.text
        
        # Check tracking file
        tracking_files = list(server.tracking_dir.glob("facebook_*.md"))
        assert len(tracking_files) == 1
    
    @pytest.mark.asyncio
    async def test_post_to_instagram_success(self, server):
        """Test successful Instagram posting."""
        result = await server.execute_tool(
            "post_to_instagram",
            {
                "caption": "Test Instagram post",
                "media_url": "https://example.com/photo.jpg",
                "location": "New York, NY"
            }
        )
        
        assert "Successfully posted to Instagram" in result.text
        assert "Post ID:" in result.text
        
        # Check tracking file
        tracking_files = list(server.tracking_dir.glob("instagram_*.md"))
        assert len(tracking_files) == 1
    
    @pytest.mark.asyncio
    async def test_post_to_instagram_missing_media(self, server):
        """Test Instagram posting fails without media_url."""
        result = await server.execute_tool(
            "post_to_instagram",
            {
                "caption": "Test post"
            }
        )
        
        assert "Error:" in result.text
        assert "Missing required parameter" in result.text
    
    @pytest.mark.asyncio
    async def test_post_to_twitter_success(self, server):
        """Test successful Twitter posting."""
        result = await server.execute_tool(
            "post_to_twitter",
            {
                "content": "Test tweet #testing"
            }
        )
        
        assert "Successfully posted to Twitter" in result.text
        assert "Post ID:" in result.text
        
        # Check tracking file
        tracking_files = list(server.tracking_dir.glob("twitter_*.md"))
        assert len(tracking_files) == 1
    
    @pytest.mark.asyncio
    async def test_post_to_twitter_content_too_long(self, server):
        """Test Twitter posting with content exceeding limit."""
        long_content = "A" * 281  # Exceeds 280 character limit
        
        result = await server.execute_tool(
            "post_to_twitter",
            {
                "content": long_content
            }
        )
        
        assert "Error:" in result.text
        assert "exceeds 280 characters" in result.text
    
    @pytest.mark.asyncio
    async def test_post_to_twitter_with_reply(self, server):
        """Test Twitter posting as a reply."""
        result = await server.execute_tool(
            "post_to_twitter",
            {
                "content": "This is a reply",
                "reply_to": "tweet_12345"
            }
        )
        
        assert "Successfully posted to Twitter" in result.text
    
    @pytest.mark.asyncio
    async def test_unknown_tool(self, server):
        """Test handling unknown tool."""
        result = await server.handle_tool_call(
            "post_to_unknown",
            {}
        )
        
        assert "Error: Unknown tool" in result.text
    
    @pytest.mark.asyncio
    async def test_content_tracking(self, server):
        """Test that posted content is tracked correctly."""
        # Post to LinkedIn
        await server.execute_tool(
            "post_to_linkedin",
            {
                "content": "Tracking test post",
                "visibility": "public"
            }
        )
        
        # Check tracking file exists and has correct content
        tracking_files = list(server.tracking_dir.glob("linkedin_*.md"))
        assert len(tracking_files) == 1
        
        tracking_file = tracking_files[0]
        content = tracking_file.read_text()
        
        # Check tracking file format
        assert "platform: linkedin" in content
        assert "post_id:" in content
        assert "timestamp:" in content
        assert "status: published" in content
        assert "Tracking test post" in content
        assert "## Engagement Metrics" in content
        assert "Likes:" in content
        assert "Comments:" in content
        assert "Shares:" in content
    
    @pytest.mark.asyncio
    async def test_parameter_validation(self, server):
        """Test parameter validation for all tools."""
        # LinkedIn - missing required content
        result = await server.execute_tool(
            "post_to_linkedin",
            {"visibility": "public"}
        )
        assert "Error:" in result.text
        
        # Instagram - missing required media_url
        result = await server.execute_tool(
            "post_to_instagram",
            {"caption": "Test"}
        )
        assert "Error:" in result.text
        
        # Twitter - missing required content
        result = await server.execute_tool(
            "post_to_twitter",
            {"media_url": "https://example.com/image.jpg"}
        )
        assert "Error:" in result.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
