"""
Unit tests for BaseMCPServer

Tests tool registration, parameter validation, and error handling.
"""

import pytest
import sys
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_servers.base_mcp_server import BaseMCPServer, Tool, TextContent


class TestMCPServer(BaseMCPServer):
    """Test implementation of BaseMCPServer."""
    
    def register_tools(self) -> None:
        """Register test tools."""
        # Simple tool with required parameters
        simple_tool = Tool(
            name="simple_tool",
            description="A simple test tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "count": {"type": "integer"}
                },
                "required": ["message"]
            }
        )
        self.add_tool(simple_tool)
        
        # Complex tool with optional parameters
        complex_tool = Tool(
            name="complex_tool",
            description="A complex test tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "active": {"type": "boolean"},
                    "tags": {"type": "array"},
                    "metadata": {"type": "object"}
                },
                "required": ["name", "age"]
            }
        )
        self.add_tool(complex_tool)
    
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> TextContent:
        """Handle test tool calls."""
        if name == "simple_tool":
            message = arguments['message']
            count = arguments.get('count', 1)
            return TextContent(type="text", text=f"{message} x {count}")
        
        elif name == "complex_tool":
            name_val = arguments['name']
            age = arguments['age']
            return TextContent(type="text", text=f"{name_val} is {age} years old")
        
        return TextContent(type="text", text=f"Unknown tool: {name}")


class TestBaseMCPServer:
    """Test suite for BaseMCPServer."""
    
    def test_server_initialization(self):
        """Test that server initializes correctly."""
        server = TestMCPServer("test_server")
        assert server.name == "test_server"
        assert len(server.tools) == 2
        assert "simple_tool" in server.tools
        assert "complex_tool" in server.tools
    
    def test_tool_registration(self):
        """Test tool registration."""
        server = TestMCPServer("test_server")
        
        # Check simple_tool
        simple_tool = server.get_tool("simple_tool")
        assert simple_tool is not None
        assert simple_tool.name == "simple_tool"
        assert simple_tool.description == "A simple test tool"
        
        # Check complex_tool
        complex_tool = server.get_tool("complex_tool")
        assert complex_tool is not None
        assert complex_tool.name == "complex_tool"
    
    def test_list_tools(self):
        """Test listing all tools."""
        server = TestMCPServer("test_server")
        tools = server.list_tools()
        
        assert len(tools) == 2
        tool_names = [t['name'] for t in tools]
        assert "simple_tool" in tool_names
        assert "complex_tool" in tool_names
    
    def test_parameter_validation_success(self):
        """Test successful parameter validation."""
        server = TestMCPServer("test_server")
        
        # Valid parameters for simple_tool
        is_valid, error = server.validate_parameters(
            "simple_tool",
            {"message": "Hello", "count": 5}
        )
        assert is_valid is True
        assert error is None
        
        # Valid parameters with only required fields
        is_valid, error = server.validate_parameters(
            "simple_tool",
            {"message": "Hello"}
        )
        assert is_valid is True
        assert error is None
    
    def test_parameter_validation_missing_required(self):
        """Test validation fails when required parameter is missing."""
        server = TestMCPServer("test_server")
        
        is_valid, error = server.validate_parameters(
            "simple_tool",
            {"count": 5}  # Missing required 'message'
        )
        assert is_valid is False
        assert "Missing required parameter: message" in error
    
    def test_parameter_validation_unknown_parameter(self):
        """Test validation fails for unknown parameters."""
        server = TestMCPServer("test_server")
        
        is_valid, error = server.validate_parameters(
            "simple_tool",
            {"message": "Hello", "unknown_param": "value"}
        )
        assert is_valid is False
        assert "Unknown parameter: unknown_param" in error
    
    def test_parameter_validation_wrong_type(self):
        """Test validation fails for wrong parameter types."""
        server = TestMCPServer("test_server")
        
        # String instead of integer
        is_valid, error = server.validate_parameters(
            "simple_tool",
            {"message": "Hello", "count": "five"}
        )
        assert is_valid is False
        assert "Invalid type" in error
    
    def test_parameter_validation_unknown_tool(self):
        """Test validation fails for unknown tool."""
        server = TestMCPServer("test_server")
        
        is_valid, error = server.validate_parameters(
            "nonexistent_tool",
            {"message": "Hello"}
        )
        assert is_valid is False
        assert "Tool 'nonexistent_tool' not found" in error
    
    def test_type_validation(self):
        """Test type validation for different types."""
        server = TestMCPServer("test_server")
        
        # String
        assert server._validate_type("hello", "string") is True
        assert server._validate_type(123, "string") is False
        
        # Integer
        assert server._validate_type(123, "integer") is True
        assert server._validate_type(123.5, "integer") is False
        
        # Number (int or float)
        assert server._validate_type(123, "number") is True
        assert server._validate_type(123.5, "number") is True
        assert server._validate_type("123", "number") is False
        
        # Boolean
        assert server._validate_type(True, "boolean") is True
        assert server._validate_type(False, "boolean") is True
        assert server._validate_type(1, "boolean") is False
        
        # Array
        assert server._validate_type([1, 2, 3], "array") is True
        assert server._validate_type({"a": 1}, "array") is False
        
        # Object
        assert server._validate_type({"a": 1}, "object") is True
        assert server._validate_type([1, 2], "object") is False
    
    @pytest.mark.asyncio
    async def test_execute_tool_success(self):
        """Test successful tool execution."""
        server = TestMCPServer("test_server")
        
        result = await server.execute_tool(
            "simple_tool",
            {"message": "Hello", "count": 3}
        )
        
        assert result.type == "text"
        assert result.text == "Hello x 3"
    
    @pytest.mark.asyncio
    async def test_execute_tool_validation_error(self):
        """Test tool execution with validation error."""
        server = TestMCPServer("test_server")
        
        result = await server.execute_tool(
            "simple_tool",
            {"count": 3}  # Missing required 'message'
        )
        
        assert result.type == "text"
        assert "Error:" in result.text
        assert "Missing required parameter" in result.text
    
    @pytest.mark.asyncio
    async def test_execute_tool_complex_parameters(self):
        """Test tool execution with complex parameters."""
        server = TestMCPServer("test_server")
        
        result = await server.execute_tool(
            "complex_tool",
            {
                "name": "Alice",
                "age": 30,
                "active": True,
                "tags": ["developer", "python"],
                "metadata": {"role": "engineer"}
            }
        )
        
        assert result.type == "text"
        assert "Alice is 30 years old" in result.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
