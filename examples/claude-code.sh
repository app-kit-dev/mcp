#!/usr/bin/env sh
# App-Kit MCP for Claude Code (remote, Streamable HTTP).

# Anonymous, current project only:
claude mcp add --transport http app-kit https://mcp.app-kit.dev/mcp

# With a free token from https://app-kit.dev/mcp, available in all projects:
# claude mcp add --transport http app-kit https://mcp.app-kit.dev/mcp \
#   --scope user \
#   --header "Authorization: Bearer mcpf_your_token"

# Check the connection:
# claude mcp list
