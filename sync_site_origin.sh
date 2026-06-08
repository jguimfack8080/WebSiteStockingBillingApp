#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -f ".env" ]]; then
  echo "Missing .env in $(pwd)"
  exit 1
fi

set -a
. ./.env
set +a

if [[ -z "${SITE_ORIGIN:-}" ]]; then
  echo "SITE_ORIGIN is missing in .env"
  exit 1
fi

if [[ -z "${DEFAULT_LANGUAGE:-}" ]]; then
  echo "DEFAULT_LANGUAGE is missing in .env"
  exit 1
fi

python ./sync_site_origin.py

python - <<'PY'
import os
import re
from pathlib import Path
from urllib.parse import urlparse

root = Path.cwd()
site_origin = os.environ["SITE_ORIGIN"].rstrip("/")
default_language = os.environ.get("DEFAULT_LANGUAGE", "fr").strip().lower()

allowed_prefixes = ("/fr", "/en", "/de", "/assets/", "/robots.txt", "/sitemap.xml", "/#")
url_re = re.compile(r"https?://[^\s\"<>]+")

bad = []

for p in sorted((root / "fr").glob("*.html")) + sorted((root / "en").glob("*.html")) + sorted((root / "de").glob("*.html")):
    s = p.read_text(encoding="utf-8")
    for u in url_re.findall(s):
        parsed = urlparse(u)
        if not parsed.scheme or not parsed.netloc:
            continue
        if not parsed.path and not parsed.fragment:
            continue
        full_path = parsed.path or "/"
        if parsed.fragment:
            full_path = full_path + "#" + parsed.fragment
        if full_path.startswith(allowed_prefixes):
            if f"{parsed.scheme}://{parsed.netloc}" != site_origin:
                bad.append((str(p), u))

for p in (root / "robots.txt", root / "sitemap.xml"):
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    for u in url_re.findall(s):
        parsed = urlparse(u)
        if not parsed.scheme or not parsed.netloc:
            continue
        full_path = parsed.path or "/"
        if parsed.fragment:
            full_path = full_path + "#" + parsed.fragment
        if full_path.startswith(allowed_prefixes):
            if f"{parsed.scheme}://{parsed.netloc}" != site_origin:
                bad.append((str(p), u))

if bad:
    print("Found site URLs that do not match SITE_ORIGIN:")
    for file_path, url in bad[:50]:
        print(f"  - {file_path}: {url}")
    raise SystemExit(1)

parsed = urlparse(site_origin)
canonical_host = parsed.hostname
if not canonical_host:
    raise SystemExit("SITE_ORIGIN must contain a hostname")

mw = (root / "functions" / "_middleware.js")
if mw.exists():
    s = mw.read_text(encoding="utf-8")
    if f'const CANONICAL_HOST = "{canonical_host}";' not in s:
        raise SystemExit("functions/_middleware.js CANONICAL_HOST does not match SITE_ORIGIN hostname")
    if f'const DEFAULT_LANG = "{default_language}";' not in s:
        raise SystemExit("functions/_middleware.js DEFAULT_LANG does not match DEFAULT_LANGUAGE")

redirects = (root / "_redirects")
pages = ("about", "contact", "faq", "features", "pricing")
if redirects.exists():
    s = redirects.read_text(encoding="utf-8")
    for page in pages:
        expected = f"/{page}.html /{default_language}/{page}.html 301"
        if expected not in s:
            raise SystemExit(f"_redirects is missing: {expected}")

print("OK: all site URLs match SITE_ORIGIN for canonical, hreflang, assets, sitemap and robots.")
PY
