#!/usr/bin/env python3
"""Composite the finished gta6-meme-x-01 meme from a generated base image.

Steps:
  1. Fit the base image to 1200x675 (center crop), the size the judge sees
     shrunk to 768x480, so caption text must be large.
  2. Paste the real make.fun ghost (assets/mark-1024.png, from the press
     kit) into the scene with its alpha channel, at a chosen corner and
     scale, so it reads as part of the scene rather than a sticker.
  3. Draw the caption in Noto Sans CJK Bold, white with a black stroke,
     centred on a translucent dark band at the top or bottom.

Usage:
  python3 make-meme.py --base base.png --out meme.jpg --text "..."
  python3 make-meme.py --base base.png --out meme.jpg --text "..." \\
      --ghost-corner bottom-right --ghost-scale 0.22 --text-pos bottom
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
GHOST = HERE / "assets" / "mark-1024.png"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

TARGET_W, TARGET_H = 1200, 675


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """Noto Sans CJK Bold; fall back to the default font if it is missing."""
    try:
        return ImageFont.truetype(FONT_BOLD, size, index=0)
    except OSError:
        print(f"warning: {FONT_BOLD} not found, using default font",
              file=sys.stderr)
        return ImageFont.load_default()


def fit_cover(img: Image.Image, width: int, height: int) -> Image.Image:
    """Resize and centre-crop so the image exactly covers width x height."""
    scale = max(width / img.width, height / img.height)
    resized = img.resize(
        (round(img.width * scale), round(img.height * scale)),
        Image.LANCZOS,
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def wrap_text(draw: ImageDraw.ImageDraw, text: str,
              font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Greedy wrap on characters (Chinese has no spaces to split on)."""
    lines, current = [], ""
    for ch in text:
        trial = current + ch
        if draw.textlength(trial, font=font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def paste_ghost(canvas: Image.Image, corner: str, scale: float) -> None:
    """Paste the ghost into a corner of the canvas, keeping its alpha."""
    ghost = Image.open(GHOST).convert("RGBA")
    size = round(TARGET_W * scale)
    ghost = ghost.resize((size, size), Image.LANCZOS)
    margin = 24
    positions = {
        "top-left": (margin, margin),
        "top-right": (TARGET_W - size - margin, margin),
        "bottom-left": (margin, TARGET_H - size - margin),
        "bottom-right": (TARGET_W - size - margin, TARGET_H - size - margin),
    }
    if corner not in positions:
        raise ValueError(f"unknown corner {corner!r}, want one of "
                         f"{sorted(positions)}")
    canvas.paste(ghost, positions[corner], ghost)


def draw_caption(canvas: Image.Image, text: str, position: str) -> None:
    """Caption on a translucent dark band, large white bold type."""
    draw = ImageDraw.Draw(canvas, "RGBA")
    font_size = 64
    font = load_font(font_size)
    max_width = TARGET_W - 80
    lines = wrap_text(draw, text, font, max_width)
    while len(lines) > 2 and font_size > 40:  # keep it to two lines at most
        font_size -= 6
        font = load_font(font_size)
        lines = wrap_text(draw, text, font, max_width)

    line_height = round(font_size * 1.25)
    band_height = line_height * len(lines) + 36
    band_top = 0 if position == "top" else TARGET_H - band_height
    draw.rectangle([0, band_top, TARGET_W, band_top + band_height],
                   fill=(0, 0, 0, 150))
    y = band_top + 18
    for line in lines:
        width = draw.textlength(line, font=font)
        draw.text(((TARGET_W - width) / 2, y), line, font=font,
                  fill=(255, 255, 255, 255),
                  stroke_width=3, stroke_fill=(0, 0, 0, 255))
        y += line_height


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="generated base image")
    parser.add_argument("--out", default="meme.jpg", help="output JPEG")
    parser.add_argument("--text", required=True, help="meme caption text")
    parser.add_argument("--text-pos", default="bottom",
                        choices=["top", "bottom"])
    parser.add_argument("--ghost-corner", default="bottom-right",
                        choices=["top-left", "top-right",
                                 "bottom-left", "bottom-right"])
    parser.add_argument("--ghost-scale", type=float, default=0.22,
                        help="ghost width as a fraction of 1200")
    args = parser.parse_args()

    base = Image.open(args.base).convert("RGB")
    canvas = fit_cover(base, TARGET_W, TARGET_H).convert("RGBA")
    paste_ghost(canvas, args.ghost_corner, args.ghost_scale)
    draw_caption(canvas, args.text, args.text_pos)
    canvas.convert("RGB").save(args.out, "JPEG", quality=92)
    print(f"wrote {args.out} ({TARGET_W}x{TARGET_H})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
