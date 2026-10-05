# App-Kit MCP

[![MCP](https://img.shields.io/badge/MCP-Streamable%20HTTP-0a7cff)](https://modelcontextprotocol.io)
[![Endpoint](https://img.shields.io/badge/endpoint-mcp.app--kit.dev-222)](https://mcp.app-kit.dev/mcp)
[![Free tier](https://img.shields.io/badge/free%20tier-no%20sign--up-2ea44f)](https://app-kit.dev/mcp)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Remote MCP server for **SEO audits**, **text readability and grammar checks**, **image conversion
(PNG/JPEG/WebP)** and **PDF to images** - for Claude, Cursor, VS Code, Windsurf and any other MCP client.
Free tier with daily limits, no sign-up.

```
https://mcp.app-kit.dev/mcp
```

[Русская версия](README.ru.md) | [Tools reference](docs/tools.md) | [app-kit.dev](https://app-kit.dev/mcp)

This repository holds the public documentation, client configs and registry metadata. The server
itself is a hosted service operated by [App-Kit](https://app-kit.dev); there is nothing to install.

## What it does

- **SEO audit of a website** - score 0-100 by group, failed checks and the five biggest losses.
  The engine runs 400 checks (technical SEO, performance, structured data, AI-readiness and more);
  the fast mode covers up to 10 pages in about a minute.
- **Text check** - readability, "water" and keyword stuffing metrics, stop phrases and grammar
  (LanguageTool) for Russian and English, up to 20 000 characters. Returns positions of issues,
  not copies of your text.
- **PDF and images** - PDF pages to PNG/JPEG/WebP, images to PDF, format conversion
  (WebP/AVIF compression is coming soon). Files are passed by URL or via a one-time upload link, never as huge
  base64 strings in the chat.

## Quick start

Works anonymously out of the box. For higher limits, get a free token on
[app-kit.dev/mcp](https://app-kit.dev/mcp) (one click, no email) and pass it either as a header
`Authorization: Bearer mcpf_...` or in the URL: `https://mcp.app-kit.dev/mcp/t/mcpf_...`.

### Claude Code

```bash
claude mcp add --transport http app-kit https://mcp.app-kit.dev/mcp

# with a free token
claude mcp add --transport http app-kit https://mcp.app-kit.dev/mcp \
  --header "Authorization: Bearer mcpf_your_token"
```

Add `--scope user` to make it available in every project. See [examples/claude-code.sh](examples/claude-code.sh).

### Claude.ai and Claude Desktop

Customize > Connectors > **+** > **Add custom connector**. Name: `App-Kit`, Remote MCP server URL:
`https://mcp.app-kit.dev/mcp/t/mcpf_your_token` (the token in the URL is recommended: requests from
claude.ai share Anthropic's IP addresses, so anonymous limits there are a small shared pool).
Authentication: no sign-in. Free Claude plans allow one custom connector. Details:
[examples/claude-desktop/claude.ai.md](examples/claude-desktop/claude.ai.md).

### Cursor

`.cursor/mcp.json` in the project or `~/.cursor/mcp.json` globally ([example](examples/cursor-mcp.json)):

```json
{
  "mcpServers": {
    "app-kit": {
      "url": "https://mcp.app-kit.dev/mcp",
      "headers": { "Authorization": "Bearer mcpf_your_token" }
    }
  }
}
```

### VS Code (GitHub Copilot agent mode)

`.vscode/mcp.json` ([example](examples/vscode-mcp.json)); VS Code asks for the token once and stores it securely:

```json
{
  "inputs": [
    { "type": "promptString", "id": "app-kit-token", "description": "App-Kit MCP free token (mcpf_...)", "password": true }
  ],
  "servers": {
    "app-kit": {
      "type": "http",
      "url": "https://mcp.app-kit.dev/mcp",
      "headers": { "Authorization": "Bearer ${input:app-kit-token}" }
    }
  }
}
```

### Windsurf (Devin Desktop)

Open the MCP config from the Cascade MCP settings (`mcp_config.json`) and add a server with
`serverUrl`. `${env:VAR}` is expanded in headers:

```json
{
  "mcpServers": {
    "app-kit": {
      "serverUrl": "https://mcp.app-kit.dev/mcp",
      "headers": { "Authorization": "Bearer ${env:APPKIT_MCP_TOKEN}" }
    }
  }
}
```

### Other clients

Any client that supports remote MCP over Streamable HTTP: URL `https://mcp.app-kit.dev/mcp`,
optional header `Authorization: Bearer mcpf_...`. Clients that cannot set headers can use
`https://mcp.app-kit.dev/mcp/t/mcpf_...`.

## Tools

Full descriptions and JSON Schemas: [docs/tools.md](docs/tools.md) (generated from the live `tools/list`).

| Tool | What it does | Example prompt |
|---|---|---|
| `seo_audit_fast` | Fast SEO audit of a site root (up to 10 pages): score, failed checks, top-5 losses. Waits up to 60 s, then returns a `handle` | "Run an SEO audit of example.com and tell me what to fix first" |
| `seo_audit_status` | Status and result of an audit by `handle` | (called by the model automatically) |
| `text_check` | Readability, water/spam metrics, stop phrases, grammar; `lang` ru/en, up to 20 000 chars | "Check this landing page copy for readability and grammar: ..." |
| `quota_status` | Your access level and remaining free calls per tool | "How many free App-Kit checks do I have left today?" |
| `image_convert` | Convert between PNG, JPEG, WebP, BMP, TIFF, GIF | "Convert this logo to PNG: https://example.com/logo.webp" |
| `pdf_to_images` | Render PDF pages (up to 20) to PNG/JPEG/WebP | "Turn pages 1-3 of https://example.com/deck.pdf into PNG at 150 dpi" |
| `images_to_pdf` | Merge up to 20 images into one PDF | "Make a PDF from these 3 screenshots: ..." |
| `conversion_status` | Status and result of a long conversion by `handle` | (called by the model automatically) |
| `create_upload` | One-time upload URL for a local file (agents with a shell) | "Convert ./scan.pdf to PNG pages" |
| `image_compress` *(coming soon)* | Compress to WebP/AVIF with quality and resize options | "Compress https://example.com/hero.png to AVIF" |

All tools are read-only: nothing is published or changed on your side. Results that are files come
back as short-lived download links (10 minutes) plus a small preview.

## Limits

| Tool | Anonymous | Free token | Notes |
|---|---|---|---|
| `text_check` | 10 / hour | 20 / hour | |
| `seo_audit_fast` | 5 / hour | 10 / hour | one domain: up to 20 audits per day from all users |
| `seo_audit_status`, `conversion_status`, `quota_status` | free | free | do not spend quota |
| `image_convert` | 5 / hour | 20 / hour | |
| `pdf_to_images`, `images_to_pdf` | 3 / hour | 10 / hour | up to 20 pages / files, 20 MB |
| `create_upload` | 10 / hour | 30 / hour | up to 20 MB, link valid 10 min |

Every response includes `quota` (`remaining`, `reset_at`, `tier`, `upgrade_url`). The free tier
also has a shared daily budget per tool; when it runs out, the tool says so and resets at 00:00 UTC.
Limits may be tuned without notice; the current values are always in the tool descriptions and
`quota_status`.

## Pricing

The free tier above stays free. Higher limits, full multi-page SEO audits with PDF reports and
larger files are part of the paid App-Kit API and are billed in App-Kit credits - see
[app-kit.dev](https://app-kit.dev).

## Privacy

- Processing happens in Germany (EU).
- Text you send to `text_check` is not stored; only metrics are returned.
- Files are kept only while being processed and deleted within 15 minutes; download links expire in 10 minutes.
- IP addresses are used only for anonymous rate limits, as a salted hash kept for at most 24 hours.
- Usage logs contain the tool name, timing and status - no IP addresses, texts, file contents or full URLs.
- Page content from audited sites is never returned verbatim: only scores, check codes and short,
  clipped fields marked as page data.

Full policy: [app-kit.dev/mcp](https://app-kit.dev/mcp).

## FAQ

**Do I need an account?** No. Anonymous use works; a free token (no email) raises the limits.

**Why do anonymous calls from claude.ai run out quickly?** claude.ai connects from Anthropic's
shared IP range, so all anonymous claude.ai users share one small pool. Use a token in the URL.

**Can it audit my staging site?** Only publicly reachable sites. Private networks, localhost and
non-standard ports are blocked.

**Which MCP protocol versions are supported?** Streamable HTTP, stateless: current MCP revisions and
clients on 2025-11-25. No stdio package is needed.

**A long audit returned `status: running`. What now?** The model calls `seo_audit_status` with the
`handle` after `poll_after_s` seconds. The handle works only for the caller and expires in 60 minutes.

**Is the server open source?** The server is a hosted service. This repository (docs, examples,
registry metadata) is MIT-licensed.

**Where do I report a bug or a security issue?** Bugs and ideas: [issues](../../issues).
Security: see [SECURITY.md](SECURITY.md).

## Links

- Free token and docs: [app-kit.dev/mcp](https://app-kit.dev/mcp)
- App-Kit: [app-kit.dev](https://app-kit.dev)
- MCP Registry name: `io.github.app-kit-dev/mcp` ([server.json](server.json))
