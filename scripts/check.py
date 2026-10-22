#!/usr/bin/env python3
"""Fail if hand-synced bits of the CV have drifted. Run before every commit/deploy."""
import base64, hashlib, json, re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text()
errs = []

# CSP hash vs inline script
script = re.search(r"^<script>(.*?)</script>", html, re.S | re.M).group(1)
want = "sha256-" + base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
if f"'{want}'" not in html:
    errs.append(f"CSP hash stale; use '{want}'")

# JSON-LD parses; dateModified == sitemap lastmod
ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))
mod = re.search(r'"dateModified":\s*"([^"]+)"', html).group(1)
lastmod = re.search(r"<lastmod>([^<]+)</lastmod>", (root / "sitemap.xml").read_text()).group(1)
if mod != lastmod:
    errs.append(f"dateModified {mod} != sitemap lastmod {lastmod}")

# every JSON-LD role org appears in llms-full.txt
llms = (root / "llms-full.txt").read_text()
def walk(o):
    if isinstance(o, dict):
        if o.get("@type") == "OrganizationRole":
            yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)
for r in walk(ld):
    name = r.get("roleName")
    if name and name not in llms:
        errs.append(f"role '{name}' missing from llms-full.txt")

# local refs exist
for ref in re.findall(r'(?:href|src)="(/[^"#]+)"', html):
    if not (root / ref.lstrip("/")).exists():
        errs.append(f"missing file {ref}")

print("\n".join(errs) or "ok")
sys.exit(bool(errs))
