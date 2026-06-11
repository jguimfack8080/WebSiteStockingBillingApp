"""
W-BIL05: Update navigation in all 18 existing HTML files.
Adds Telecharger link and changes CTA from demo to register.
Skips billing pages (download, register, verify-email) already generated.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

SKIP_PAGES = {"download.html", "register.html", "verify-email.html", "pricing.html"}

NAV_LABELS = {
    "fr": {"download": "Télécharger", "cta": "Essai gratuit 14j"},
    "en": {"download": "Download", "cta": "Free trial 14d"},
    "de": {"download": "Download", "cta": "Kostenlos 14 Tage"},
}

def update_nav(filepath, lang):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    labels = NAV_LABELS[lang]
    changed = False

    # 1. Add Download link before FAQ in nav (if not already present)
    if '"download"' not in html and "download" not in html:
        # Insert after features link
        old_faq_link = re.search(r'<a href="faq"[^>]*>.*?</a>', html)
        if old_faq_link:
            insert_pos = old_faq_link.start()
            download_link = f'<a href="download">{labels["download"]}</a>\n        '
            html = html[:insert_pos] + download_link + html[insert_pos:]
            changed = True
    elif f'<a href="download">' not in html:
        # Try to insert after faq link
        match = re.search(r'(<a href="faq"[^>]*>.*?</a>)', html)
        if match:
            html = html[:match.end()] + f'\n        <a href="download">{labels["download"]}</a>' + html[match.end():]
            changed = True

    # 2. Update CTA button text in nav: "Demander une démo" -> "Essai gratuit 14j" for register href
    # Update nav-cta button
    old_nav_cta = re.search(
        r'<a href="contact"( class="btn btn--primary btn--sm nav-cta">)[^<]+</a>',
        html
    )
    if old_nav_cta:
        html = html[:old_nav_cta.start()] + \
            f'<a href="register" class="btn btn--primary btn--sm nav-cta">{labels["cta"]}</a>' + \
            html[old_nav_cta.end():]
        changed = True

    # 3. Update btn-desktop CTA
    old_desktop_cta = re.search(
        r'<a href="contact"( class="btn btn--primary btn--sm btn-desktop">)[^<]+</a>',
        html
    )
    if old_desktop_cta:
        html = html[:old_desktop_cta.start()] + \
            f'<a href="register" class="btn btn--primary btn--sm btn-desktop">{labels["cta"]}</a>' + \
            html[old_desktop_cta.end():]
        changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  updated nav: {os.path.relpath(filepath, BASE)}")
    else:
        print(f"  skipped (already updated or no match): {os.path.relpath(filepath, BASE)}")


def update_redirects():
    path = os.path.join(BASE, "_redirects")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    additions = """
/download       /fr/download    302
/register       /fr/register    302
/signup         /fr/register    301
/essai          /fr/register    301
/trial          /en/register    301
/telecharger    /fr/download    301
/verify-email   /fr/verify-email 302
/pricing        /fr/pricing     302
"""
    if "/download" not in content:
        content += additions
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  updated _redirects")
    else:
        print("  _redirects already up to date")


def update_sitemap():
    path = os.path.join(BASE, "sitemap.xml")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_urls = []
    for lang in ["fr", "en", "de"]:
        for page in ["download", "register", "pricing"]:
            url = f"https://www.jgjpaystock.com/{lang}/{page}"
            if url not in content:
                new_urls.append(f"""  <url>
    <loc>{url}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    if new_urls:
        content = content.replace("</urlset>", "\n".join(new_urls) + "\n</urlset>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  added {len(new_urls)} URLs to sitemap.xml")
    else:
        print("  sitemap.xml already up to date")


if __name__ == "__main__":
    print("W-BIL05: Updating nav in existing HTML files...")
    for lang in ["fr", "en", "de"]:
        lang_dir = os.path.join(BASE, lang)
        for fname in os.listdir(lang_dir):
            if fname.endswith(".html") and fname not in SKIP_PAGES:
                update_nav(os.path.join(lang_dir, fname), lang)

    print("\nUpdating _redirects...")
    update_redirects()

    print("\nUpdating sitemap.xml...")
    update_sitemap()

    print("\nW-BIL05 complete.")
