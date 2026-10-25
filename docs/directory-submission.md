# Claude Connectors Directory - submission materials

Field-by-field answers for the submission form at `claude.ai/directory/manage` -> **Submit new** ->
**MCP connector**. Requirements and the review checklist: `appkit-mcp/docs/stores.md` (section 1).
Limits and auth: ADR-0026. Status: draft, not submitted.

## Connection

| Field | Value |
|---|---|
| Server URL | `https://mcp.app-kit.dev/mcp/account` |
| Transport | Streamable HTTP (stateless) |
| Authentication | OAuth 2.1 - authorization code + PKCE (S256), public clients. Client registration: CIMD (`client_id` = HTTPS URL of the client metadata document); DCR (RFC 7591) also available |
| Authorization server | `https://admin.app-kit.dev` (RFC 8414 metadata at `/.well-known/oauth-authorization-server`) |
| Protected resource metadata | `https://mcp.app-kit.dev/.well-known/oauth-protected-resource/mcp/account` (RFC 9728) |
| Scope | `mcp` |
| Resource indicator | `https://mcp.app-kit.dev/mcp/account` (RFC 8707, required) |
| Token lifetimes | access 1 hour, refresh 30 days (rotation) |
| Unauthenticated request | HTTP 401 with `WWW-Authenticate: Bearer resource_metadata="..."` |

The same tools are also served without sign-in at `https://mcp.app-kit.dev/mcp` (documented on the
docs page); that address is not part of this listing.

## Listing

| Field | Limit | Value |
|---|---|---|
| Name | 100 | `App-Kit` |
| Tagline | 60 | `SEO audits and text checks for your AI agent` (44) |
| Short description (one-liner) | 200 | see below |
| Long description | 2000 | see below |
| Categories | 1-5 | Developer tools, Marketing, Productivity |
| Docs URL | | `https://app-kit.dev/mcp` |
| Privacy policy URL | | `https://app-kit.dev/privacy` (section "MCP accounts and sign-in") |
| Terms URL | | `https://app-kit.dev/terms` |
| Support contact | | `hi@wm2.dev` |
| Icon | | `assets/logo-400.png` (400x400 PNG, this repo) |
| Slug (permanent) | | `app-kit` (proposal) |

### Short description (one-liner, 140 characters)

```
Technical SEO audit of any public page and readability, spam and grammar checks for English and Russian text, plus PDF and image conversion.
```

### Long description (about 1,430 characters)

```
App-Kit gives Claude practical tools for website and content work. They run on App-Kit's own services in Germany.

- SEO audit: seo_audit_fast checks a public page against about 400 technical SEO, performance, structured data and AI-readiness checks. It returns an overall score, scores by group, the failed checks and the five issues that cost the most. Longer audits return a handle, and seo_audit_status returns the result.
- Text check: text_check measures readability, filler, spam and keyword stuffing, stop phrases and grammar for English or Russian text up to 20,000 characters. It returns pass/fail verdicts and the positions of issues, not copies of your text. The text is not stored.
- PDF and images: pdf_to_images renders PDF pages to PNG, JPEG or WebP, images_to_pdf combines images into one PDF, and image_convert converts existing images between PNG, JPEG, WebP, BMP, TIFF and GIF. Pass a public file URL, or upload a local file with create_upload. Results are download links that expire in 10 minutes; files are deleted within 15 minutes.
- Usage: quota_status shows what is left of each tool's daily limit.

All tools only read and compute. App-Kit never publishes anything or changes your website, files or accounts. Private network addresses are rejected.

Connecting signs you in with an App-Kit account (email and password). Usage is rate-limited per tool and per day. Privacy: https://app-kit.dev/privacy.
```

## Tools (synced from the server)

| Tool | Title | readOnlyHint | destructiveHint | openWorldHint |
|---|---|---|---|---|
| `seo_audit_fast` | App-Kit quick SEO audit | true | false | true |
| `seo_audit_status` | App-Kit SEO audit status | true | false | true |
| `text_check` | App-Kit text check | true | false | false |
| `pdf_to_images` | App-Kit PDF to images | true | false | true |
| `images_to_pdf` | App-Kit images to PDF | true | false | true |
| `image_convert` | App-Kit image conversion | true | false | true |
| `conversion_status` | App-Kit conversion status | true | false | false |
| `create_upload` | App-Kit file upload | false | false | false |
| `quota_status` | App-Kit usage limits | true | false | false |

Titles and hints as in [tools.md](tools.md) (generated from `tools/list`; regenerate before
submitting). `create_upload` is `readOnlyHint=false` because it creates an upload
slot; the other tools compute results without changing user state (temporary result links are
deleted within 15 minutes).

## Use cases

Read: SEO audit of a public page, text quality check, quota lookup.
Write: none on the user's side; `create_upload` creates a temporary upload slot on App-Kit.

## Data handling

- First-party API only: all calls go to App-Kit services (`*.app-kit.dev`), hosted in Germany.
- Account data: email, password hash, sign-up date and source. OAuth tokens are stored as hashes;
  expired tokens are deleted daily. Account deletion: email hi@wm2.dev.
- Tool inputs: text is not stored (only a hash remains in the analysis log); files are deleted within
  15 minutes; the engines receive nothing that identifies the user.
- IP addresses: only as an HMAC with a daily-rotating salt for rate limits, not stored.
- No AI generation of images, audio or video; no financial transactions.

## Test cases

All prompts were written for a fresh conversation with only the App-Kit connector enabled.
Sample files are stable public files on app-kit.dev.

### Positive

| # | Prompt | Expected tools | Expected behavior |
|---|---|---|---|
| P1 | `Run a quick SEO audit of https://app-kit.dev and tell me the top issues to fix first.` | `seo_audit_fast` (then `seo_audit_status` if a handle is returned) | Returns an overall score, group scores and the top losses; Claude lists the most important fixes. |
| P2 | `Check this English text for readability, spam and grammar: "Our new app helps small teams plan their week. It is very very easy to use and it is the best app for teams who want to plan there week fast."` | `text_check` (`lang=en`) | Returns pass/fail verdicts, readability and filler metrics and grammar issue positions (for example the repeated "very very"); Claude explains what to fix. |
| P3 | `Turn pages 1-2 of https://app-kit.dev/seo-audit-sample-report.en.pdf into PNG images.` | `pdf_to_images` (`first_page=1`, `last_page=2`) | Returns two download links (valid 10 minutes) and a preview of page 1. |
| P4 | `Convert https://app-kit.dev/icon-512.png to WebP.` | `image_convert` (`target_format=webp`) | Returns a download link, the output size and a preview. |
| P5 | `How many App-Kit SEO audits and text checks do I have left today?` | `quota_status` | Returns the access tier (`L2`) and remaining calls per tool with the reset time (00:00 UTC). |

### Negative

| # | Prompt | Expected behavior |
|---|---|---|
| N1 | `Write a 500-word blog post about SEO for my bakery.` | No App-Kit tool is called: App-Kit checks text but does not write it. |
| N2 | `Generate a logo image of a cat.` | No App-Kit tool is called: App-Kit converts existing images and does not generate new ones. |
| N3 | `Run an SEO audit of http://192.168.1.1/admin.` | `seo_audit_fast` rejects the private address with a clear `invalid_url` error without contacting it; Claude explains that a public URL is needed. |

## Note for the reviewer

```
App-Kit uses OAuth sign-in with an App-Kit account. Registration is open: when you connect, the
sign-in page offers "Create account" (or go directly to https://admin.app-kit.dev/oauth/signup).
Sign-up needs only an email address and a password (no email confirmation) and a Cloudflare
Turnstile check. A test account with pre-set credentials is available on request at hi@wm2.dev.

All tools are read-only except create_upload, which only creates a temporary upload slot. Sample
public files for testing: https://app-kit.dev/seo-audit-sample-report.en.pdf and
https://app-kit.dev/icon-512.png. Daily limits for an account: text_check 20, seo_audit_fast 5,
pdf_to_images / images_to_pdf 5, image_convert 10, create_upload 15 (reset at 00:00 UTC).
```

## Before submitting

- [ ] MCP-015 deployed: EN titles/descriptions, `create_upload` hints, `icons`; regenerate `docs/tools.md`
      and re-check the tools table above against the live `tools/list`.
- [ ] Every tool run once through a claude.ai custom connector on `/mcp/account` (Test & launch).
- [ ] `hi@wm2.dev` is read by whoever answers reviewer and user mail.
- [ ] Submitting account/organization chosen (the listing belongs to it; slug is permanent).
