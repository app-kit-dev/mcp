# Installing App-Kit MCP (instructions for AI agents)

App-Kit is a **hosted remote MCP server**. There is nothing to clone, build or run locally:
just add the endpoint to the client's MCP settings.

- Endpoint: `https://mcp.app-kit.dev/mcp`
- Transport: Streamable HTTP (stateless). Not SSE, not stdio.
- Auth: none required. Anonymous calls work with small free limits.
- Optional: a free token (`mcpf_...`, no email) from https://app-kit.dev/mcp raises the limits.
  Pass it as the header `Authorization: Bearer mcpf_...`. Do not invent a token: if the user
  has none, install without headers.

## Cline

Add this to `cline_mcp_settings.json` (MCP Servers → Configure). The `type` field is required:
without it Cline falls back to the legacy SSE transport and the connection fails.

```json
{
  "mcpServers": {
    "app-kit": {
      "type": "streamableHttp",
      "url": "https://mcp.app-kit.dev/mcp",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

With a token:

```json
{
  "mcpServers": {
    "app-kit": {
      "type": "streamableHttp",
      "url": "https://mcp.app-kit.dev/mcp",
      "headers": { "Authorization": "Bearer mcpf_your_token" },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Check that it works

Call `quota_status`: it returns the access level (`anonymous` or `free`) and the remaining calls
per tool. Then try `text_check` with a short text.

## Tools

`seo_audit_fast`, `seo_audit_status`, `text_check`, `quota_status`, `image_convert`,
`image_compress`, `pdf_to_images`, `images_to_pdf`, `conversion_status`, `create_upload`.
Full reference: [docs/tools.md](docs/tools.md).
