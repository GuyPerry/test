"""MCP tool loader — indirection layer for MCP tool discovery.

This agent has no SAP backend integrations, so no MCP tools are loaded.
Returns an empty list. Extend this module when MCP servers are added.
"""
from typing import List
from langchain_core.tools import BaseTool


async def get_mcp_tools() -> List[BaseTool]:
    """Return MCP tools for this agent. Currently returns empty list."""
    return []
