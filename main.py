#!/usr/bin/env python3
"""THE GLOBAL LEDGER — a one-page newspaper front page summing up the world
news of Wednesday, November 18, 2026, in a single 1024x1024 image.

The program is fully offline and deterministic: it only reads the committed
assets (photos and fonts) next to this file and writes one JPEG image to
<output_dir>/entry.png. No network, no randomness, no timestamps.
"""

import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"

W, H = 1024, 1024
MARGIN = 40
CW = W - 2 * MARGIN  # content width = 944

PAPER = (248, 246, 238)
INK = (17, 17, 17)
GRAY = (92, 90, 84)
ACCENT = (163, 28, 28)
RULE = (30, 30, 30)

SERIF_BOLD = str(FONTS / "DejaVuSerif-Bold.ttf")
SERIF = str(FONTS / "DejaVuSerif.ttf")
SANS_BOLD = str(FONTS / "DejaVuSans-Bold.ttf")
SANS = str(FONTS / "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_one_line(draw, text, path, start_size, max_width, min_size=10):
    """Largest font size (<= start_size) at which text fits on one line."""
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, min_size)


def wrap(draw, text, f, max_width):
    """Greedy word wrap; returns a list of lines that each fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, f, x, y, line_h, fill=INK, align="left", width=CW):
    for line in lines:
        if align == "center":
            lx = x + (width - draw.textlength(line, font=f)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=f, fill=fill)
        y += line_h
    return y


def hrule(draw, y, x0=MARGIN, x1=W - MARGIN, width=2, fill=RULE):
    draw.rectangle([x0, y, x1, y + width - 1], fill=fill)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- Masthead ----------------
    hrule(d, 20, width=2)
    name = "THE GLOBAL LEDGER"
    f_name = fit_one_line(d, name, SERIF_BOLD, 68, CW)
    draw_lines(d, [name], f_name, MARGIN, 30, 78, align="center")
    hrule(d, 112, width=6)
    hrule(d, 122, width=1)
    f_date = font(SANS_BOLD, 17)
    date_line = "WEDNESDAY, NOVEMBER 18, 2026  ·  THE WORLD IN ONE PAGE"
    draw_lines(d, [date_line], f_date, MARGIN, 130, 22, align="center")
    hrule(d, 158, width=2)

    # ---------------- Hero photo ----------------
    hero = Image.open(ASSETS / "hero.jpg").convert("RGB")
    hero = ImageOps.fit(hero, (CW, 296), Image.LANCZOS)
    img.paste(hero, (MARGIN, 168))
    d = ImageDraw.Draw(img)
    f_cap = font(SERIF, 15)
    caption = ("SHENZHEN — Trump is greeted by Xi Jinping on the tarmac "
               "after landing for the APEC summit.")
    y = draw_lines(d, wrap(d, caption, f_cap, CW), f_cap, MARGIN, 470, 19, fill=GRAY)

    # ---------------- Hero headline + deck ----------------
    f_head = font(SANS_BOLD, 43)
    head = "TRUMP, XI AND PUTIN TO MEET IN SHENZHEN"
    y = draw_lines(d, wrap(d, head, f_head, CW), f_head, MARGIN, y + 6, 50, align="center")
    f_deck = font(SERIF, 19)
    deck = ("Xi welcomes the U.S. president at the airport ahead of Thursday's "
            "first-ever three-way summit — and sits down with Putin the same day.")
    y = draw_lines(d, wrap(d, deck, f_deck, CW), f_deck, MARGIN, y + 4, 24, align="center")
    hrule(d, y + 8, width=2)
    panels_top = y + 20

    # ---------------- Photo panels ----------------
    panels = [
        ("tanker.jpg",
         "U.S. SINKS FIVE IRANIAN TANKERS",
         "Iran strikes back at a U.S. base in Kuwait and sites in Bahrain "
         "after U.S. strikes on Qeshm Island; Hormuz shipping is in chaos."),
        ("bridge.jpg",
         "UKRAINE HITS KERCH BRIDGE AGAIN",
         "A second straight night of strikes shuts the Crimean crossing, "
         "Putin's flagship link to the occupied peninsula."),
    ]
    pw = (CW - 16) // 2  # 464
    panels_bottom = panels_top
    for i, (file, head, sub) in enumerate(panels):
        x = MARGIN + i * (pw + 16)
        ph = Image.open(ASSETS / file).convert("RGB")
        ph = ImageOps.fit(ph, (pw, 150), Image.LANCZOS)
        img.paste(ph, (x, panels_top))
        d = ImageDraw.Draw(img)
        f_ph = font(SANS_BOLD, 20)
        yy = draw_lines(d, wrap(d, head, f_ph, pw), f_ph, x, panels_top + 156, 24)
        f_ps = font(SANS, 14)
        yy = draw_lines(d, wrap(d, sub, f_ps, pw), f_ps, x, yy + 2, 18, fill=(40, 40, 40))
        panels_bottom = max(panels_bottom, yy)
    hrule(d, panels_bottom + 10, width=2)
    cols_top = panels_bottom + 20

    # ---------------- Bottom text columns ----------------
    cols = [
        ("ANTHROPIC RAISES $81.3 BILLION",
         "The largest stock offering ever recorded, as investors pile into AI."),
        ("DEMOCRATS HOLD SENATE, 56–44",
         "Peltola beats Sullivan in Alaska to seal the projected majority."),
        ("ISRAELI FORCES ENTER GAZA",
         "First entry into Hamas-held areas since the 2025 ceasefire; truce at risk."),
    ]
    col_w = (CW - 2 * 24) // 3  # 298

    def columns_bottom(f_ch, f_cb, head_lh, body_lh):
        """Bottom edge the three columns would reach with these fonts."""
        bottom = cols_top
        for head, body in cols:
            yy = cols_top + head_lh * len(wrap(d, head, f_ch, col_w))
            yy += 3 + body_lh * len(wrap(d, body, f_cb, col_w))
            bottom = max(bottom, yy)
        return bottom

    # Text metrics vary slightly between Pillow/FreeType builds, which can
    # push a column one wrapped line lower than it sat when this page was
    # designed. Measure before drawing and step the column fonts down until
    # the columns fit above the footer rule; the first size that fits is the
    # designed one, so the page stays unchanged wherever metrics allow it.
    for head_size, body_size in ((18, 15), (17, 14), (16, 13), (15, 12), (14, 11)):
        f_ch = font(SANS_BOLD, head_size)
        f_cb = font(SANS, body_size)
        head_lh, body_lh = head_size + 4, body_size + 4
        if columns_bottom(f_ch, f_cb, head_lh, body_lh) <= 996:
            break
    cols_bottom = cols_top
    for i, (head, body) in enumerate(cols):
        x = MARGIN + i * (col_w + 24)
        yy = draw_lines(d, wrap(d, head, f_ch, col_w), f_ch, x, cols_top, head_lh, fill=ACCENT)
        yy = draw_lines(d, wrap(d, body, f_cb, col_w), f_cb, x, yy + 3, body_lh)
        cols_bottom = max(cols_bottom, yy)
        if i:
            d.line([x - 12, cols_top + 2, x - 12, cols_bottom], fill=(170, 166, 156), width=1)
    hrule(d, 1002, width=1)
    f_foot = font(SANS, 12)
    draw_lines(d, ["COMPILED FROM WIRE REPORTS · PRICES AND SCORES INSIDE"],
               f_foot, MARGIN, 1006, 14, fill=GRAY, align="center")

    return img


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or
                   (sys.argv[1] if len(sys.argv) > 1 else "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    img = build()
    img.save(out_dir / "entry.png", format="JPEG", quality=88)
    print("wrote", out_dir / "entry.png")


if __name__ == "__main__":
    main()
