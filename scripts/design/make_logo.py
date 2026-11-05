"""
GiftIQ - logo.

Badge logo: plum gift box with a gold oval label and a ribbon bow on top.
Exports transparent PNGs:

    images/GiftIQ_Logo.png       full badge, for the dashboard header
    images/GiftIQ_Icon.png       square icon (512 x 512), for favicon / profile use

Usage:
    python scripts/design/make_logo.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SS = 4  # supersample factor

PLUM = (91, 42, 134, 255)        # #5B2A86
PLUM_DARK = (61, 26, 92, 255)    # #3D1A5C
GOLD = (242, 165, 65, 255)       # #F2A541
GOLD_DARK = (201, 128, 30, 255)  # #C9801E
FONT_PATH = "C:/Windows/Fonts/seguibl.ttf"  # Segoe UI Black


def s(v):
    return int(round(v * SS))


def draw_bow(img, cx, cy, size):
    """Two rounded ribbon loops tilted upwards and a knot, centred at (cx, cy)."""
    lw, lh = size * 1.4, size * 0.8
    for angle, side in ((-30, -1), (30, 1)):
        layer = Image.new("RGBA", (s(lw * 2), s(lh * 2)), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse([s(lw * 0.5), s(lh * 0.5), s(lw * 1.5), s(lh * 1.5)],
                   fill=GOLD, outline=GOLD_DARK, width=s(4))
        ld.ellipse([s(lw * 0.78), s(lh * 0.8), s(lw * 1.22), s(lh * 1.2)], fill=GOLD_DARK)
        layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
        lx = cx + side * lw * 0.42
        img.alpha_composite(layer, (s(lx - lw), s(cy - size * 0.32 - lh)))
    d = ImageDraw.Draw(img)
    r = size * 0.3
    d.ellipse([s(cx - r), s(cy - r), s(cx + r), s(cy + r)], fill=GOLD, outline=GOLD_DARK, width=s(4))


def fit_font(text, max_w, max_h):
    size = 10
    while True:
        f = ImageFont.truetype(FONT_PATH, s(size + 2))
        l, t, r, b = f.getbbox(text)
        if (r - l) > s(max_w) or (b - t) > s(max_h):
            return ImageFont.truetype(FONT_PATH, s(size))
        size += 2


def draw_text_centered(d, text, cx, cy, font, fill):
    l, t, r, b = font.getbbox(text)
    d.text((s(cx) - (l + r) / 2, s(cy) - (t + b) / 2), text, font=font, fill=fill)


def make_logo(path):
    W, H = 1000, 470
    img = Image.new("RGBA", (s(W), s(H)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    box = (30, 110, 970, 440)
    d.rounded_rectangle([s(v) for v in box], radius=s(34), fill=PLUM)
    # lid line: a slightly darker band across the top of the box
    d.rounded_rectangle([s(30), s(110), s(970), s(150)], radius=s(34), fill=PLUM_DARK)
    d.rectangle([s(30), s(130), s(970), s(150)], fill=PLUM_DARK)

    oval = (85, 170, 915, 420)
    d.ellipse([s(v) for v in oval], fill=GOLD)

    font = fit_font("GiftIQ", 560, 150)
    draw_text_centered(d, "GiftIQ", 500, 297, font, PLUM)

    draw_bow(img, 500, 108, 78)

    img.resize((W, H), Image.LANCZOS).save(path)
    print(f"Saved {path} ({W} x {H})")


def make_icon(path):
    N = 512
    img = Image.new("RGBA", (s(N), s(N)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([s(36), s(120), s(476), s(476)], radius=s(48), fill=PLUM)
    d.rounded_rectangle([s(36), s(120), s(476), s(166)], radius=s(48), fill=PLUM_DARK)
    d.rectangle([s(36), s(140), s(476), s(166)], fill=PLUM_DARK)
    d.ellipse([s(84), s(196), s(428), s(440)], fill=GOLD)
    font = fit_font("IQ", 220, 150)
    draw_text_centered(d, "IQ", 256, 318, font, PLUM)
    draw_bow(img, 256, 118, 80)
    img.resize((N, N), Image.LANCZOS).save(path)
    print(f"Saved {path} ({N} x {N})")


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[2] / "assets"
    out.mkdir(exist_ok=True)
    make_logo(out / "GiftIQ_Logo.png")
    make_icon(out / "GiftIQ_Icon.png")
