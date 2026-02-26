"""
Base MCP Server

Provides the foundational class for all MCP server implementations.
Handles tool registration, parameter validation, and request handling.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
import logging


@dataclass
class Tool:
    """Represents an MCP tool with its schema."""
    name: str
    description: str
    inputSchema: Dict[str, Any]


@dataclass
class TextContent:
    """Represents text content returned from tool execution."""
    type: str = "text"
    text: str = ""


class BaseMCPServer(ABC):
    """
    Base class for all MCP servers.
    
    Provides common functionality for tool registration, parameter validation,
    and request handling. Subclasses should implement register_tools() and
    handle_tool_call() methods.
    """
    
    def __init__(self, name: str):
        """
        Initialize the MCP server.
        
        Args:
            name: The name of the MCP server
        """
        self.name = name
        self.tools: Dict[str, Tool] = {}
        self.logger = logging.getLogger(f"mcp.{name}")
        self.register_tools()
    
    @abstractmethod
    def register_tools(self) -> None:
        """
        Register available tools with the server.
        
        Subclasses must implement this method to define their tools.
        Use add_tool() to register each tool.
        """
        pass
    
    def add_tool(self, tool: Tool) -> None:
        """
        Add a tool to the server's registry.
        
        Args:
            tool: The Tool object to register
        """
        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name}")
    
    def validate_parameters(self, tool_name: str, arguments: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate request parameters against the tool's input schema.
        
        Args:
            tool_name: Name of the tool being called
            arguments: Arguments provided for the tool
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if tool_name not in self.tools:
            return False, f"Tool '{tool_name}' not found"
        
        tool = self.tools[tool_name]
        schema = tool.inputSchema
        
        # Check required fields
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in arguments:
                return False, f"Missing required parameter: {field}"
        
        # Check field types
        properties = schema.get("properties", {})
        for field, value in arguments.items():
            if field not in properties:
                return False, f"Unknown parameter: {field}"
            
            expected_type = properties[field].get("type")
            if expected_type:
                if not self._validate_type(value, expected_type):
                    return False, f"Invalid type for parameter '{field}': expected {expected_type}"
        
        return True, None
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """
        Validate that a value matches the expected JSON schema type.
        
        Args:
            value: The value to validate
            expected_type: The expected type (string, number, boolean, array, object)
            
        Returns:
            True if the type matches, False otherwise
        """
        type_mapping = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict
        }
        
        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type is None:
            return True  # Unknown type, skip validation
        
        return isinstance(value, expected_python_type)
    
    @abstractmethod
    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> TextContent:
        """
        Handle incoming tool call requests.
        
        Args:
            name: Name of the tool to execute
            arguments: Arguments for the tool
            
        Returns:
            TextContent with the result or error message
        """
        pass
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> TextContent:
        """
        Execute a tool with parameter validation.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments for the tool
            
        Returns:
            TextContent with the result or error message
        """
        # Validate parameters
        is_valid, error_message = self.validate_parameters(tool_name, arguments)
        if not is_valid:
            self.logger.error(f"Parameter validation failed: {error_message}")
            return TextContent(type="text", text=f"Error: {error_message}")
        
        # Execute the tool
        try:
            result = await self.handle_tool_call(tool_name, arguments)
            self.logger.info(f"Tool '{tool_name}' executed successfully")
            return result
        except Exception as e:
            error_msg = f"Error executing tool '{tool_name}': {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return TextContent(type="text", text=error_msg)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        Get a list of all registered tools with their schemas.
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema
            }
            for tool in self.tools.values()
        ]
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """
        Get a specific tool by name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool object or None if not found
        """
        return self.tools.get(tool_name)
