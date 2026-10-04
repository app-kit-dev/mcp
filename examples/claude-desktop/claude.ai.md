# App-Kit MCP in Claude.ai and Claude Desktop

Claude.ai and Claude Desktop connect to remote MCP servers as **custom connectors**. The connector
is added once in your Claude account and is then available in both.

1. Get a free token on [app-kit.dev/mcp](https://app-kit.dev/mcp) (one click, no email).
2. Open **Customize > Connectors**, click **+**, then **Add custom connector**.
   On Team and Enterprise plans an owner adds it in **Organization settings > Connectors**.
3. Fill in:
   - Name: `App-Kit`
   - Remote MCP server URL: `https://mcp.app-kit.dev/mcp/t/mcpf_your_token`
   - Authentication: no sign-in
4. Save, then enable the connector in a chat from the tools menu.

Why the token goes into the URL: claude.ai reaches MCP servers from Anthropic's shared IP range, so
anonymous requests from all claude.ai users fall into one small shared pool. With a token you get
your own limits. Alternatively, put `Authorization: Bearer mcpf_your_token` into the connector's
request headers, if your plan shows that section, and use `https://mcp.app-kit.dev/mcp` as the URL.

Treat the URL with the token like a password: anyone who has it spends your limits. If it leaks,
get a new token on app-kit.dev/mcp.

Free Claude plans allow one custom connector.

Try it:

- "Run an SEO audit of example.com and list the five most important fixes."
- "Check this text for readability and grammar: ..."
- "How many free App-Kit checks do I have left?"
