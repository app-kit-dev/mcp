# Changelog

All notable changes to the public App-Kit MCP server and this repository.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versions follow `server.json`.

## [Unreleased]

### Planned
- `image_compress`, `image_convert`, `pdf_to_images`, `create_upload` (files by URL or one-time upload).
- Sign-in with an App-Kit account (OAuth) instead of free tokens.

## [0.1.0] - 2026-10-04

### Added
- Remote endpoint `https://mcp.app-kit.dev/mcp` (Streamable HTTP, stateless).
- Tools: `text_check`, `seo_audit_fast`, `seo_audit_status`, `quota_status`.
- Free tier: anonymous limits and free tokens (`mcpf_...`) via header or URL.
- Docs, client examples (Claude Code, Claude.ai, Cursor, VS Code, Windsurf), `server.json` for the MCP Registry.
