# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static single-page CV for fasoulas.com. No build, no package manager, no tests. Open `index.html` directly or serve the directory (`python3 -m http.server`).

## Layout

- `index.html` — whole site: inline `<style>`, inline JSON-LD, one inline `<script>` (earlier-career toggle). Fonts self-hosted in `fonts/` (woff2).
- `llms.txt` / `llms-full.txt` — agent-readable summary and full markdown CV. Keep content in sync with `index.html` when roles/text change.
- `robots.txt`, `sitemap.xml`, `og.png`, `apple-touch-icon.png` — SEO/social assets.

## Gotchas

- **CSP script hash**: `index.html` has a `Content-Security-Policy` meta with `script-src 'sha256-…'` for the inline script. Any edit to that `<script>` (even whitespace) breaks it. Regenerate hash and update the meta (comment above it flags this). `style-src 'unsafe-inline'` is allowed; no other external origins.
- **JSON-LD** (`@graph` in head): Person/ProfilePage/WebSite plus 20 `OrganizationRole` entries (6 detailed roles + 14 earlier). Adding/changing a role in the body means updating JSON-LD and `llms-full.txt` too.
- **Earlier career** list uses `hidden="until-found"` (find-in-page reveals it via `beforematch`); a `<noscript><style>` block forces it visible without JS.
- **Dates**: bump `dateModified` in JSON-LD and `<lastmod>` in `sitemap.xml` on content changes.
- Print stylesheet targets A4; check print render after layout changes.
- HSTS, `frame-ancestors`, `X-Content-Type-Options`, `Permissions-Policy` can't be set via meta tags — need real headers from the host (Cloudflare/Netlify), not yet configured.
- `.playwright-mcp/` is untracked scratch output; don't commit.
