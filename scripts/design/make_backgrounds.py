"""
GiftIQ - Power BI canvas backgrounds.

All boxes are defined in Power BI canvas units (16:9 page = 1280 x 720), so
the same numbers can be typed into Format > General > Properties > Size and
position for each visual. The PNG is exported at 1920 x 1080 for sharpness;
set it as the page background with Image fit = Fit.

Usage:
    python scripts/design/make_backgrounds.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

CANVAS_W, CANVAS_H = 1280, 720
EXPORT_SCALE = 1.5          # 1920 x 1080 output
SUPERSAMPLE = 2             # draw at 2x export size, then downscale for smooth edges
RADIUS = 12

BG = (246, 242, 250)        # #F6F2FA
CARD = (255, 255, 255)
PLUM = (91, 42, 134)        # #5B2A86
GOLD = (242, 165, 65)       # #F2A541
SOFT_PLUM = (156, 123, 192) # #9C7BC0
SHADOW = (46, 26, 71)       # #2E1A47

# name: (x, y, width, height) in canvas units
OVERVIEW = {
    "Slicer bar":               (24, 80, 1232, 52),
    "KPI - Total Customers":    (24, 144, 185, 72),
    "KPI - Total Revenue":      (221, 144, 185, 72),
    "KPI - Churned %":          (418, 144, 185, 72),
    "KPI - Avg Customer Value": (615, 144, 185, 72),
    "Revenue | Customers toggle": (812, 144, 444, 40),
    "Total Revenue by Segment": (24, 228, 776, 232),
    "Retention by Segment":     (812, 196, 444, 264),
    "Revenue by Month":         (24, 472, 452, 220),
    "Revenue by Quarter":       (488, 472, 384, 220),
    "Revenue by Year":          (884, 472, 372, 220),
}

RFM = {
    "Slicer bar":                   (24, 80, 1232, 52),
    "Segment Performance Summary":  (24, 144, 776, 316),
    "Segment | Country toggle":     (812, 144, 444, 40),
    "Avg Customer Value by View":   (812, 196, 444, 264),
    "Churned % by Month":           (24, 472, 452, 220),
    "Churned % by Quarter":         (488, 472, 384, 220),
    "Churned % by Year":            (884, 472, 372, 220),
}


def px(v):
    return int(round(v * EXPORT_SCALE * SUPERSAMPLE))


def draw_decor(img):
    d = ImageDraw.Draw(img)
    # bottom-right ribbon bands
    d.polygon([(px(1105), px(720)), (px(1280), px(545)), (px(1280), px(600)), (px(1160), px(720))], fill=GOLD)
    d.polygon([(px(1185), px(720)), (px(1280), px(625)), (px(1280), px(720))], fill=PLUM)
    # left-edge ribbon, mostly tucked behind the cards
    d.polygon([(px(0), px(150)), (px(70), px(215)), (px(0), px(280))], fill=GOLD)
    d.polygon([(px(0), px(215)), (px(70), px(215)), (px(0), px(330))], fill=PLUM)
    # small soft-plum accent top-right, above the header buttons' row
    d.polygon([(px(1215), px(0)), (px(1280), px(0)), (px(1280), px(52))], fill=SOFT_PLUM)


def draw_cards(img, boxes):
    w, h = img.size
    # soft, wide shadow + tight contact shadow
    for blur, offset, alpha in ((14, 5, 34), (2.5, 1, 22)):
        layer = Image.new("L", (w, h), 0)
        ld = ImageDraw.Draw(layer)
        for x, y, bw, bh in boxes.values():
            ld.rounded_rectangle(
                [px(x), px(y + offset), px(x + bw), px(y + bh + offset)],
                radius=px(RADIUS), fill=alpha,
            )
        layer = layer.filter(ImageFilter.GaussianBlur(px(blur)))
        shadow = Image.new("RGB", (w, h), SHADOW)
        img.paste(shadow, (0, 0), layer)

    d = ImageDraw.Draw(img)
    for x, y, bw, bh in boxes.values():
        d.rounded_rectangle([px(x), px(y), px(x + bw), px(y + bh)], radius=px(RADIUS), fill=CARD)


def render(boxes, out_path):
    img = Image.new("RGB", (px(CANVAS_W), px(CANVAS_H)), BG)
    draw_decor(img)
    draw_cards(img, boxes)
    final = (int(CANVAS_W * EXPORT_SCALE), int(CANVAS_H * EXPORT_SCALE))
    img.resize(final, Image.LANCZOS).save(out_path, optimize=True)
    print(f"Saved {out_path} ({final[0]} x {final[1]})")


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[2] / "assets"
    out.mkdir(exist_ok=True)
    render(OVERVIEW, out / "GiftIQ_Overview_Background.png")
    render(RFM, out / "GiftIQ_RFM_Background.png")
