"""
GiftIQ - Power BI Home page background.

Title, two navigation cards and a metrics glossary, drawn on the same grid,
colours and shadows as make_backgrounds.py. Place blank buttons over the two
cards in Power BI (positions in NAV_CARDS, canvas units).

Usage:
    python scripts/design/make_home.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from make_backgrounds import (BG, CANVAS_H, CANVAS_W, CARD, EXPORT_SCALE, GOLD,
                              PLUM, SOFT_PLUM, draw_cards, px)

INK = (46, 26, 71)          # #2E1A47
MUTED = (106, 96, 119)      # #6A6077
PLUM_TINT = (239, 230, 247) # #EFE6F7
GOLD_TINT = (253, 240, 217) # #FDF0D9
LINE = (228, 220, 236)

FONTS = "C:/Windows/Fonts/"
BOLD = FONTS + "segoeuib.ttf"
SEMI = FONTS + "seguisb.ttf"
REG = FONTS + "segoeui.ttf"

NAV_CARDS = {
    "Business Overview": (100, 268, 520, 232),
    "RFM Analysis":      (660, 268, 520, 232),
}
GLOSSARY = {"Glossary": (100, 528, 1080, 164)}


def font(path, size):
    return ImageFont.truetype(path, px(size))


def text(d, xy, s, f, fill, anchor="la"):
    d.text((px(xy[0]), px(xy[1])), s, font=f, fill=fill, anchor=anchor)


def wrap(s, f, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if f.getlength(trial) <= px(max_w):
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def draw_paragraph(d, x, y, s, f, fill, max_w, leading):
    for i, line in enumerate(wrap(s, f, max_w)):
        text(d, (x, y + i * leading), line, f, fill)


def draw_decor(img):
    d = ImageDraw.Draw(img)
    d.polygon([(px(1080), px(0)), (px(1180), px(0)), (px(1280), px(100)), (px(1280), px(180))], fill=GOLD)
    d.polygon([(px(1000), px(0)), (px(1080), px(0)), (px(1280), px(180)), (px(1280), px(230)), (px(1230), px(230))], fill=PLUM)
    d.polygon([(px(0), px(560)), (px(160), px(720)), (px(0), px(720))], fill=GOLD)
    d.polygon([(px(0), px(500)), (px(90), px(590)), (px(0), px(640))], fill=PLUM)


def draw_bar_icon(d, cx, cy):
    for i, h in enumerate((30, 44, 58, 38)):
        x = cx - 30 + i * 16
        colour = PLUM if i != 2 else GOLD
        d.rounded_rectangle([px(x), px(cy + 26 - h), px(x + 11), px(cy + 26)], radius=px(2), fill=colour)


def draw_people_icon(d, cx, cy):
    for dx, colour, r in ((-20, GOLD, 10), (20, GOLD, 10), (0, PLUM, 13)):
        hx, hy = cx + dx, cy - 14 + (0 if dx == 0 else 4)
        d.ellipse([px(hx - r), px(hy - r), px(hx + r), px(hy + r)], fill=colour)
        bw = r * 1.9
        d.pieslice([px(hx - bw), px(hy + r + 2), px(hx + bw), px(hy + r + 2 + bw * 1.6)], 180, 360, fill=colour)


def draw_chevron(d, x, y, colour):
    d.line([(px(x), px(y - 10)), (px(x + 10), px(y)), (px(x), px(y + 10))], fill=colour, width=px(3.5), joint="curve")


def draw_corner_swoosh(img, box, colour, tint):
    x, y, w, h = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([px(x + w - 240), px(y + h - 36), px(x + w + 220), px(y + h + 160)], fill=tint + (255,))
    ld.ellipse([px(x + w - 120), px(y + h - 26), px(x + w + 200), px(y + h + 170)], fill=colour + (255,))
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([px(x), px(y), px(x + w), px(y + h)], radius=px(12), fill=255)
    clipped = Image.new("RGBA", img.size, (0, 0, 0, 0))
    clipped.paste(layer, (0, 0), Image.composite(layer.getchannel("A"), Image.new("L", img.size, 0), mask))
    img.alpha_composite(clipped)


def render(out_path):
    img = Image.new("RGBA", (px(CANVAS_W), px(CANVAS_H)), BG + (255,))
    draw_decor(img)
    rgb = img.convert("RGB")
    draw_cards(rgb, {**NAV_CARDS, **GLOSSARY})
    img = rgb.convert("RGBA")
    d = ImageDraw.Draw(img)

    # title block
    title_f = font(BOLD, 54)
    text(d, (640, 118), "GiftIQ Customer Analytics", title_f, INK, anchor="mm")
    gw = title_f.getlength("GiftIQ ") / px(1)
    tw = title_f.getlength("GiftIQ Customer Analytics") / px(1)
    text(d, (640 - tw / 2, 118), "GiftIQ", title_f, PLUM, anchor="lm")
    d.rounded_rectangle([px(572), px(160), px(632), px(165)], radius=px(3), fill=PLUM)
    d.rounded_rectangle([px(648), px(160), px(708), px(165)], radius=px(3), fill=GOLD)
    text(d, (640, 196), "Understand customers. Drive revenue.", font(REG, 22), INK, anchor="mm")
    text(d, (640, 230), "779K transactions  •  5,878 customers  •  41 countries  •  Dec 2009 – Dec 2011",
         font(REG, 14), MUTED, anchor="mm")

    # navigation cards
    cards = [
        ("Business Overview", "Track customers and revenue performance across months, quarters and years.",
         PLUM, PLUM_TINT, draw_bar_icon),
        ("RFM Analysis", "Deep dive into customer behaviour by Recency, Frequency and Monetary value.",
         GOLD, GOLD_TINT, draw_people_icon),
    ]
    for (name, desc, colour, tint, icon), box in zip(cards, NAV_CARDS.values()):
        x, y, w, h = box
        draw_corner_swoosh(img, box, colour, tint)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([px(x), px(y + 30), px(x + 5), px(y + h - 30)], radius=px(3), fill=colour)
        cx, cy = x + 112, y + h / 2 - 6
        d.ellipse([px(cx - 62), px(cy - 62), px(cx + 62), px(cy + 62)], fill=tint)
        icon(d, cx, cy)
        text(d, (x + 212, y + 62), name, font(BOLD, 28), INK)
        draw_paragraph(d, x + 212, y + 110, desc, font(REG, 17), INK, 250, 26)
        draw_chevron(d, x + w - 44, y + 80, PLUM)

    # glossary
    gx, gy, gw_, gh = GLOSSARY["Glossary"]
    head_f = font(BOLD, 21)
    text(d, (gx + 30, gy + 24), "Key Metrics Glossary", head_f, INK)
    hw = head_f.getlength("Key Metrics Glossary") / px(1)
    d.line([(px(gx + 30 + hw + 24), px(gy + 39)), (px(gx + gw_ - 30), px(gy + 39))], fill=LINE, width=px(1.5))
    items = [
        ("Churned %", "Customers with no purchase in 90+ days.", PLUM),
        ("Recency (R)", "Days since a customer's last purchase.", INK),
        ("Frequency (F)", "Number of separate orders a customer placed.", GOLD),
        ("Monetary (M)", "Total amount a customer has spent.", PLUM),
        ("Customer Value", "Average revenue generated per customer.", INK),
    ]
    col_w = (gw_ - 60) / 5
    for i, (name, desc, colour) in enumerate(items):
        x = gx + 30 + i * col_w
        if i:
            d.line([(px(x - 14), px(gy + 72)), (px(x - 14), px(gy + gh - 22))], fill=LINE, width=px(1.5))
        d.ellipse([px(x), px(gy + 80), px(x + 11), px(gy + 91)], fill=colour)
        text(d, (x + 20, gy + 74), name, font(SEMI, 17), INK)
        draw_paragraph(d, x + 20, gy + 104, desc, font(REG, 14), MUTED, col_w - 40, 20)

    final = (int(CANVAS_W * EXPORT_SCALE), int(CANVAS_H * EXPORT_SCALE))
    img.convert("RGB").resize(final, Image.LANCZOS).save(out_path, optimize=True)
    print(f"Saved {out_path} ({final[0]} x {final[1]})")


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[2] / "assets"
    out.mkdir(exist_ok=True)
    render(out / "GiftIQ_Home_Background.png")
