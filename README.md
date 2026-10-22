# fasoulas.com

Static single-page CV. No build step, no dependencies. `index.html` plus a few assets, served as-is.

## How deployment works

```
git push origin master ──► GitHub ──► Vercel (Git integration) ──► Production
                                                                      │
                                                    Cloudflare (DNS / proxy) ──► visitors
```

- **Hosting:** Vercel project `cv` (team `vas-projects-caa4dcb6`). Repo root is served directly; no build command, no output directory.
- **Trigger:** every push to `master` deploys to Production automatically (Vercel GitHub app; deploys show up as `Production` in the repo's GitHub deployments). Takes about 30 seconds.
- **Other branches:** Vercel creates a Preview deployment per branch/PR. The URL appears as a commit status on GitHub. Previews are not at `fasoulas.com`.
- **DNS / edge:** `fasoulas.com` is proxied through Cloudflare in front of Vercel. Responses carry both `server: cloudflare` and `x-vercel-id`.
- **Rollback:** Vercel dashboard → Deployments → pick an earlier Production deployment → *Promote to Production*. Or `git revert` and push.

### Configuration lives in `vercel.json`

- Security headers (HSTS, `nosniff`, `X-Frame-Options`, `frame-ancestors`, `Permissions-Policy`, COOP).
- Cache headers for fonts and images (1 week).
- `Accept: text/markdown` on `/` rewrites to `llms-full.txt` (`Vary: Accept` set).

The page's own CSP is a `<meta>` tag in `index.html`. The header CSP only adds `frame-ancestors`, which meta tags cannot set. Browsers enforce both.

### Domain settings (Vercel dashboard, not in repo)

The canonical host is the apex `https://fasoulas.com`. `index.html`, `sitemap.xml`, `robots.txt`, `llms*.txt` and the JSON-LD all use it. In Vercel → Domains the apex must be the primary domain and `www` must redirect to it. Redirects cannot be set from this repo.

## Before every push

```sh
python3 scripts/check.py
```

Fails if hand-synced pieces have drifted:

- the CSP `sha256` hash no longer matches the inline `<script>`
- JSON-LD `dateModified` differs from the `<lastmod>` in `sitemap.xml`
- a JSON-LD role is missing from `llms-full.txt`
- a local `href`/`src` points at a missing file

When changing content, update together: `index.html` body, the JSON-LD in its `<head>`, `llms-full.txt`, `dateModified`, and `sitemap.xml` `lastmod`.

## After a deploy

```sh
scripts/indexnow.sh                                  # notify Bing/Yandex etc. (expects 200 or 202)
curl -sI https://fasoulas.com/ | grep -i -E 'x-frame|x-content|strict'
curl -s -H 'Accept: text/markdown' https://fasoulas.com/ | head -3
```

The IndexNow key file is `4033fa35f5fc2b7efdce9edf7ee74c26.txt` in the repo root. It must stay public and its contents must equal its filename.

## Local preview

```sh
python3 -m http.server 8000
```

This does not apply `vercel.json`, so headers and the markdown rewrite only exist on Vercel.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The whole site: inline CSS, JSON-LD, one inline script |
| `fonts/` | Self-hosted woff2 |
| `llms.txt`, `llms-full.txt` | Agent-readable summary and full markdown CV |
| `robots.txt`, `sitemap.xml` | Crawler config |
| `og.png`, `apple-touch-icon.png`, `favicon.svg` | Social and icon assets |
| `vercel.json` | Headers and rewrites |
| `scripts/check.py`, `scripts/indexnow.sh` | Pre-push check, post-deploy ping |
