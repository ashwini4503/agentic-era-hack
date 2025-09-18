"""
MCP Server Script to expose ADK's load_web_page tool via a custom MCP server.
This allows any MCP client to access the ADK tool remotely.
"""
from google.adk.tools import load_web_page
try:
    from model_context_protocol.server import MCPServer
except ImportError:
    MCPServer = None

# Wrap the ADK load_web_page tool for MCP exposure
def load_web_page_tool(url: str) -> dict:
    """
    Wrapper for ADK's load_web_page tool to expose via MCP server.
    Args:
        url (str): The URL of the web page to load.
    Returns:
        dict: The loaded web page content and metadata.
    """
    return load_web_page(url)

# List of tools to expose via MCP
exposed_tools = [load_web_page_tool]

if MCPServer:
    mcp_server = MCPServer(
        tools=exposed_tools,
        host="0.0.0.0",
        port=8081
    )
    if __name__ == "__main__":
        print("Starting MCP server exposing ADK load_web_page tool on port 8081...")
        mcp_server.run()
else:
    print("model_context_protocol.server.MCPServer not available. Please install the required package.")
