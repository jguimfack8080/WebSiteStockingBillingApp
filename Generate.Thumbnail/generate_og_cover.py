#!/usr/bin/env python3
"""Generate the BizCoRa social share image (Open Graph / Twitter card).

Outputs:
  - ../assets/images/og-cover-1200x630.png  -> the PUBLISHED image referenced by
                              og:image / twitter:image on every page.
  - ./og-cover-1200x630.svg  -> the EDITABLE vector source (open in Figma /
                              Illustrator / Inkscape / a browser, tweak
                              text/colours, re-export a 1200x630 PNG over the .png).

Both are emitted from the same geometry so they never drift. The emblem is
embedded as base64 in the SVG, so the file is self-contained and portable.

Unlike generate_thumbnails.py (stdlib only), this script needs Pillow + numpy:
    pip install pillow numpy

Social crawlers (Facebook, LinkedIn, WhatsApp, X) require a raster format, which
is why the live og:image is the PNG, not the SVG.

Run from this folder:  python generate_og_cover.py
"""
import base64
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
ROOT = Path(__file__).resolve().parent.parent          # site root
REPO = ROOT.parent                                      # stocking_billing_app
EMBLEM = REPO / "assets/logo/brand/bizcora_1024.png"
OUT_PNG = ROOT / "assets/images/og-cover-1200x630.png"
OUT_SVG = ROOT / "Generate.Thumbnail/og-cover-1200x630.svg"   # editable source, not a served asset

FONTS = Path("C:/Windows/Fonts")
F_BOLD = str(FONTS / "segoeuib.ttf")
F_LIGHT = str(FONTS / "segoeuisl.ttf")
SVG_FAMILY = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"

WHITE = (255, 255, 255, 255)
BRAND_300 = (165, 180, 252, 255)

# --- Layout constants (shared by PNG + SVG) ---------------------------------
X0 = 80
EMB_CX, EMB_CY, SIZE = 980, 300, 392
EX, EY = EMB_CX - SIZE // 2, EMB_CY - SIZE // 2
GRAD = [(0.0, (16, 14, 44)), (0.55, (54, 42, 158)), (1.0, (67, 97, 238))]
EYEBROW = "ALL-IN-ONE BUSINESS SOFTWARE"
LINE1 = "Run your whole business from a single app."
LINE2 = "It does all the maths for you, to the cent, in real time."
CHIPS = ["POS", "Inventory", "Invoicing", "Accounting", "AI"]


def font(path, size):
    return ImageFont.truetype(path, size)


f_eyebrow = font(F_BOLD, 22)
f_wm = font(F_BOLD, 122)
f_l1 = font(F_LIGHT, 39)
f_l2 = font(F_LIGHT, 32)
f_chip = font(F_BOLD, 23)
f_badge = font(F_BOLD, 25)


def hx(rgb):
    return "#%02x%02x%02x" % (rgb[0], rgb[1], rgb[2])


# ============================================================================
# PNG
# ============================================================================
xs = np.linspace(0, 1, W)[None, :]
ys = np.linspace(0, 1, H)[:, None]
t = np.clip(xs * 0.62 + ys * 0.38, 0, 1)
tp = [s[0] for s in GRAD]
base = np.stack([np.interp(t, tp, [s[1][i] for s in GRAD]) for i in range(3)], axis=-1)

X = np.arange(W)[None, :]
Y = np.arange(H)[:, None]


def glow(cx, cy, radius, color, strength):
    dd = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    f = np.clip(1 - dd / radius, 0, 1) ** 2 * strength
    return f[..., None] * np.array(color, dtype=float)


base = base + glow(1090, 20, 780, (124, 58, 237), 0.52)
base = base + glow(20, 680, 700, (34, 211, 238), 0.15)
base = np.clip(base, 0, 255).astype("uint8")
img = Image.fromarray(base, "RGB").convert("RGBA")

RINGS = [(320, 24), (250, 18), (180, 14)]
rings = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(rings)
for rr, a in RINGS:
    rd.ellipse([EMB_CX - rr, EMB_CY - rr, EMB_CX + rr, EMB_CY + rr],
               outline=(255, 255, 255, a), width=2)
img = Image.alpha_composite(img, rings)

emb = Image.open(EMBLEM).convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS)
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(halo).ellipse([EX - 26, EY - 26, EX + SIZE + 26, EY + SIZE + 26],
                             fill=(124, 58, 237, 135))
img = Image.alpha_composite(img, halo.filter(ImageFilter.GaussianBlur(72)))
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
shadow.paste((3, 5, 26, 175), (EX + 8, EY + 22), emb)
img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(28)))
img.alpha_composite(emb, (EX, EY))

ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(ov)


def tracked(xy, s, fnt, fill, tracking=0):
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tracking
    return x


def measure(s, fnt):
    asc, desc = fnt.getmetrics()
    return d.textlength(s, font=fnt), asc + desc, asc


# Eyebrow.
d.rounded_rectangle([X0, 92, X0 + 5, 120], radius=2, fill=BRAND_300)
tracked((X0 + 20, 90), EYEBROW, f_eyebrow, (203, 213, 255, 255), tracking=5)

# Wordmark.
SHX, SHY = X0 - 3, 132
tracked((SHX + 2, SHY + 4), "BizCoRa", f_wm, (6, 8, 28, 150))
biz_w = d.textlength("Biz", font=f_wm)
tracked((SHX, SHY), "Biz", f_wm, WHITE)
tracked((SHX + biz_w, SHY), "CoRa", f_wm, BRAND_300)

# Headline + benefit.
d.text((X0, 300), LINE1, font=f_l1, fill=(230, 235, 255, 255))
d.text((X0, 352), LINE2, font=f_l2, fill=(184, 194, 236, 255))

# Chips (store geometry for SVG too).
CHIP_Y, CHIP_PAD, CHIP_PH, CHIP_GAP = 424, 18, 11, 13
chip_geo = []
cx = X0
for label in CHIPS:
    tw, th, _ = measure(label, f_chip)
    w = tw + 2 * CHIP_PAD
    h = th + 2 * CHIP_PH
    d.rounded_rectangle([cx, CHIP_Y, cx + w, CHIP_Y + h], radius=h // 2,
                        fill=(255, 255, 255, 18), outline=(255, 255, 255, 150), width=2)
    d.text((cx + CHIP_PAD, CHIP_Y + CHIP_PH - 1), label, font=f_chip, fill=WHITE)
    chip_geo.append((cx, w, h, label))
    cx += w + CHIP_GAP

# Badge.
BADGE_Y, BADGE_PAD, BADGE_PH = 518, 20, 12
btw, bth, _ = measure("14-day free trial", f_badge)
bw, bh = btw + 2 * BADGE_PAD, bth + 2 * BADGE_PH
d.rounded_rectangle([X0, BADGE_Y, X0 + bw, BADGE_Y + bh], radius=bh // 2, fill=(110, 231, 183, 255))
d.text((X0 + BADGE_PAD, BADGE_Y + BADGE_PH - 1), "14-day free trial", font=f_badge, fill=(12, 20, 48, 255))

img = Image.alpha_composite(img, ov)
OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
img.convert("RGB").save(OUT_PNG, "PNG", optimize=True)
print(f"Wrote {OUT_PNG.name} ({OUT_PNG.stat().st_size // 1024} KB)")

# ============================================================================
# SVG (same geometry; text as real editable elements; emblem embedded)
# ============================================================================
emb_b64 = base64.b64encode(EMBLEM.read_bytes()).decode()


def baseline(top, fnt):
    _, _, asc = measure("Hg", fnt)
    return top + asc


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="{SVG_FAMILY}">',
    '<defs>',
    f'<linearGradient id="bg" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse">'
    + ''.join(f'<stop offset="{int(s[0]*100)}%" stop-color="{hx(s[1])}"/>' for s in GRAD)
    + '</linearGradient>',
    '<radialGradient id="violet" cx="1090" cy="20" r="780" gradientUnits="userSpaceOnUse">'
    '<stop offset="0%" stop-color="#7c3aed" stop-opacity="0.50"/>'
    '<stop offset="100%" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>',
    '<radialGradient id="cyan" cx="20" cy="680" r="700" gradientUnits="userSpaceOnUse">'
    '<stop offset="0%" stop-color="#22d3ee" stop-opacity="0.16"/>'
    '<stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>',
    '<filter id="halo" x="-50%" y="-50%" width="200%" height="200%">'
    '<feGaussianBlur stdDeviation="60"/></filter>',
    '<filter id="drop" x="-30%" y="-30%" width="160%" height="160%">'
    '<feDropShadow dx="8" dy="22" stdDeviation="22" flood-color="#03051a" flood-opacity="0.7"/></filter>',
    '</defs>',
    f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
    f'<rect width="{W}" height="{H}" fill="url(#violet)"/>',
    f'<rect width="{W}" height="{H}" fill="url(#cyan)"/>',
]
for rr, a in RINGS:
    parts.append(f'<circle cx="{EMB_CX}" cy="{EMB_CY}" r="{rr}" fill="none" '
                 f'stroke="#ffffff" stroke-opacity="{a/255:.3f}" stroke-width="2"/>')
parts.append(f'<ellipse cx="{EMB_CX}" cy="{EMB_CY}" rx="{SIZE//2+26}" ry="{SIZE//2+26}" '
             f'fill="#7c3aed" fill-opacity="0.53" filter="url(#halo)"/>')
parts.append(f'<image x="{EX}" y="{EY}" width="{SIZE}" height="{SIZE}" filter="url(#drop)" '
             f'href="data:image/png;base64,{emb_b64}"/>')

# Eyebrow.
parts.append(f'<rect x="{X0}" y="92" width="5" height="28" rx="2" fill="{hx(BRAND_300)}"/>')
parts.append(f'<text x="{X0+20}" y="{baseline(90, f_eyebrow)}" font-size="22" font-weight="700" '
             f'letter-spacing="5" fill="#cbd5ff">{EYEBROW}</text>')

# Wordmark (two-tone + shadow).
wm_base = baseline(SHY, f_wm)
parts.append(f'<text x="{SHX+2}" y="{wm_base+4}" font-size="122" font-weight="800" '
             f'fill="#06081c" fill-opacity="0.55">BizCoRa</text>')
parts.append(f'<text x="{SHX}" y="{wm_base}" font-size="122" font-weight="800">'
             f'<tspan fill="#ffffff">Biz</tspan><tspan fill="{hx(BRAND_300)}">CoRa</tspan></text>')

# Headline + benefit.
parts.append(f'<text x="{X0}" y="{baseline(300, f_l1)}" font-size="39" font-weight="350" '
             f'fill="#e6ebff">{LINE1}</text>')
parts.append(f'<text x="{X0}" y="{baseline(352, f_l2)}" font-size="32" font-weight="350" '
             f'fill="#b8c2ec">{LINE2}</text>')

# Chips.
for cxp, w, h, label in chip_geo:
    parts.append(f'<rect x="{cxp}" y="{CHIP_Y}" width="{int(w)}" height="{h}" rx="{h//2}" '
                 f'fill="#ffffff" fill-opacity="0.07" stroke="#ffffff" stroke-opacity="0.59" stroke-width="2"/>')
    parts.append(f'<text x="{cxp + CHIP_PAD}" y="{baseline(CHIP_Y + CHIP_PH - 1, f_chip)}" '
                 f'font-size="23" font-weight="700" fill="#ffffff">{label}</text>')

# Badge.
parts.append(f'<rect x="{X0}" y="{BADGE_Y}" width="{int(bw)}" height="{bh}" rx="{bh//2}" fill="#6ee7b7"/>')
parts.append(f'<text x="{X0 + BADGE_PAD}" y="{baseline(BADGE_Y + BADGE_PH - 1, f_badge)}" '
             f'font-size="25" font-weight="700" fill="#0c1430">14-day free trial</text>')

parts.append('</svg>')
OUT_SVG.write_text("\n".join(parts), encoding="utf-8")
print(f"Wrote {OUT_SVG.name} ({OUT_SVG.stat().st_size // 1024} KB)")
