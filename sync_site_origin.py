import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"


def load_env(path: Path) -> dict:
    env = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def normalize_origin(origin: str) -> str:
    origin = origin.strip()
    origin = origin.rstrip("/")
    if not re.match(r"^https?://", origin):
        raise ValueError("SITE_ORIGIN must start with http:// or https://")
    return origin


def normalize_default_language(lang: str) -> str:
  lang = (lang or "").strip().lower()
  if not lang:
    return "fr"
  if lang not in ("fr", "en", "de"):
    raise ValueError("DEFAULT_LANGUAGE must be one of: fr, en, de")
  return lang


SITE_URL_RE = re.compile(
    r"https?://[^/\s\"<>]+"
    r"(?P<path>"
    r"/(?:fr|en|de)(?:/[^\"\s<>]*)?"
    r"|/assets/[^\"\s<>]*"
    r"|/sitemap\.xml"
    r"|/robots\.txt"
    r"|/#[-A-Za-z0-9._~]+"
    r")"
)


def rewrite_file(path: Path, origin: str) -> bool:
    s = path.read_text(encoding="utf-8")
    updated = SITE_URL_RE.sub(lambda m: origin + m.group("path"), s)
    if updated == s:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def rewrite_middleware(path: Path, canonical_host: str, default_lang: str) -> bool:
  s = path.read_text(encoding="utf-8")
  if not re.search(r'const\s+CANONICAL_HOST\s*=\s*"[^"]*";', s):
    raise ValueError("functions/_middleware.js is missing CANONICAL_HOST")
  if not re.search(r'const\s+DEFAULT_LANG\s*=\s*"[^"]*";', s):
    raise ValueError("functions/_middleware.js is missing DEFAULT_LANG")

  updated = re.sub(
    r'const\s+CANONICAL_HOST\s*=\s*"[^"]*";',
    f'const CANONICAL_HOST = "{canonical_host}";',
    s,
  )
  updated = re.sub(
    r'const\s+DEFAULT_LANG\s*=\s*"[^"]*";',
    f'const DEFAULT_LANG = "{default_lang}";',
    updated,
  )
  if updated == s:
    return False
  path.write_text(updated, encoding="utf-8")
  return True


def rewrite_redirects(path: Path, default_lang: str) -> bool:
  s = path.read_text(encoding="utf-8")
  lines = s.splitlines()
  pages = ("about", "contact", "faq", "features", "pricing")

  changed = False
  out = []
  for raw in lines:
    line = raw.strip()
    if not line or line.startswith("#"):
      out.append(raw)
      continue
    parts = line.split()
    if len(parts) >= 3 and parts[0].endswith(".html") and parts[0].startswith("/"):
      src = parts[0]
      for page in pages:
        if src == f"/{page}.html":
          dst = f"/{default_lang}/{page}.html"
          if parts[1] != dst:
            parts[1] = dst
            changed = True
          break
      out.append(" ".join(parts))
      continue
    out.append(raw)

  updated = "\n".join(out) + ("\n" if s.endswith("\n") else "")
  if updated == s:
    return False
  path.write_text(updated, encoding="utf-8")
  return True


def main() -> None:
    env = load_env(ENV_PATH)
    origin = normalize_origin(env.get("SITE_ORIGIN", ""))
    default_lang = normalize_default_language(env.get("DEFAULT_LANGUAGE", "fr"))
    parsed = urlparse(origin)
    canonical_host = parsed.hostname
    if not canonical_host:
        raise ValueError("SITE_ORIGIN must contain a hostname")
    targets = []

    for lang in ("fr", "en", "de"):
        lang_dir = ROOT / lang
        targets.extend(sorted(lang_dir.glob("*.html")))

    targets.append(ROOT / "robots.txt")
    targets.append(ROOT / "sitemap.xml")

    changed = 0
    for p in targets:
        if not p.exists():
            continue
        if rewrite_file(p, origin):
            changed += 1

    middleware_path = ROOT / "functions" / "_middleware.js"
    redirects_path = ROOT / "_redirects"
    if middleware_path.exists() and rewrite_middleware(middleware_path, canonical_host, default_lang):
        changed += 1
    if redirects_path.exists() and rewrite_redirects(redirects_path, default_lang):
        changed += 1

    print(f"SITE_ORIGIN={origin}")
    print(f"DEFAULT_LANGUAGE={default_lang}")
    print(f"CANONICAL_HOST={canonical_host}")
    print(f"Files updated: {changed}/{len(targets) + 2}")


if __name__ == "__main__":
    main()
