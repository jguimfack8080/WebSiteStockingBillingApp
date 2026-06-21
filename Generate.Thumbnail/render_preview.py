#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rendu / export raster des thumbnails SVG (helper de QA et d'OG image).

Les vignettes du site sont des SVG (vectoriels) : c'est la version servie en
production. Ce script sert a deux choses annexes :

  1. preview : rendre les SVG en PNG pour les inspecter visuellement (QA) avant
     de pousser. Les PNG vont dans Generate.Thumbnail/previews/ (jetables).
  2. og      : regenerer l'image de partage social (Open Graph / Twitter) en
     RASTER, car les reseaux sociaux ne savent PAS afficher du SVG dans les
     balises og:image / twitter:image. On rend donc le dashboard SVG (francais)
     en PNG : assets/images/screenhot_app-1280.png (reference par les meta).

Moteur de rendu : navigateur Chromium headless (Microsoft Edge ou Google
Chrome), present d'office sur la plupart des postes. Aucune dependance Python.

Usage :
  python render_preview.py preview            # rend TOUS les SVG en PNG (QA)
  python render_preview.py preview screenhot_app.svg stock-management.de.svg
  python render_preview.py og                 # (re)genere l'image OG raster

Astuce : lancer d'abord `python generate_thumbnails.py` pour produire les SVG.
"""

import os
import sys
import glob
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.dirname(HERE)
IMG_DIR = os.path.join(SITE_ROOT, "assets", "images")
PREVIEW_DIR = os.path.join(HERE, "previews")

W, H = 1280, 676

# Candidats de navigateur Chromium headless (Windows / macOS / Linux).
BROWSER_CANDIDATES = [
    os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "msedge", "google-chrome", "chromium", "chromium-browser",
]


def find_browser():
    for c in BROWSER_CANDIDATES:
        if os.path.isfile(c):
            return c
        found = shutil.which(c)
        if found:
            return found
    raise SystemExit(
        "Aucun navigateur Chromium (Edge/Chrome) trouve pour le rendu. "
        "Installez Edge ou Chrome, ou adaptez BROWSER_CANDIDATES."
    )


def render(browser, svg_path, png_path, w=W, h=H):
    """Rend un SVG en PNG via un wrapper HTML marge zero (capture exacte)."""
    svg_uri = "file:///" + os.path.abspath(svg_path).replace("\\", "/")
    html = (f"<html><head><style>*{{margin:0;padding:0}}</style></head>"
            f"<body><img src='{svg_uri}' width='{w}' height='{h}'></body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        html_path = f.name
    try:
        subprocess.run(
            [browser, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", f"--window-size={w},{h}",
             f"--screenshot={os.path.abspath(png_path)}",
             "file:///" + html_path.replace("\\", "/")],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        )
    finally:
        try:
            os.remove(html_path)
        except OSError:
            pass
    return os.path.isfile(png_path)


def cmd_preview(names):
    browser = find_browser()
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    if names:
        svgs = [os.path.join(IMG_DIR, n) for n in names]
    else:
        svgs = sorted(glob.glob(os.path.join(IMG_DIR, "*.svg")))
    ok = 0
    for svg in svgs:
        if not os.path.isfile(svg):
            print(f"  introuvable: {svg}")
            continue
        base = os.path.splitext(os.path.basename(svg))[0]
        png = os.path.join(PREVIEW_DIR, base + ".png")
        if render(browser, svg, png):
            ok += 1
            print(f"  ok  {base}.png")
        else:
            print(f"  ECHEC  {base}")
    print(f"Previews dans {PREVIEW_DIR} ({ok} rendus)")


def cmd_og():
    """Regenere l'image OG raster (dashboard francais) referencee par les meta."""
    browser = find_browser()
    svg = os.path.join(IMG_DIR, "screenhot_app.svg")
    if not os.path.isfile(svg):
        raise SystemExit("screenhot_app.svg manquant - lancez generate_thumbnails.py d'abord.")
    out = os.path.join(IMG_DIR, "screenhot_app-1280.png")
    if render(browser, svg, out):
        print(f"Image OG raster regeneree : {out}")
    else:
        raise SystemExit("Echec du rendu de l'image OG.")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("preview", "og"):
        print(__doc__)
        raise SystemExit(1)
    if sys.argv[1] == "preview":
        cmd_preview(sys.argv[2:])
    else:
        cmd_og()


if __name__ == "__main__":
    main()
