from __future__ import annotations

from typing import Sequence

import numpy as np
from PIL import Image, ImageDraw, ImageFont


_ASCII_DEFAULT = "@%#*+=-:. "  # darkest -> lightest


def ascii_art(
    image: Image.Image,
    cols: int = 120,
    charset: str = _ASCII_DEFAULT,
    invert: bool = False,
    font_size: int = 10,
) -> Image.Image:
    """Render an ASCII art version of the image.

    - cols: approx number of characters across
    - charset: characters from dark to light
    - invert: invert brightness mapping
    - font_size: font size for drawing
    """
    src = image.convert("L")
    w, h = src.size
    # aspect correction: characters are tall; tweak cell ratio
    cell_w = max(1, w // cols)
    cell_h = int(cell_w * 2)
    rows = max(1, h // cell_h)

    small = src.resize((cols, rows), resample=Image.BICUBIC)
    arr = np.asarray(small).astype(np.float32) / 255.0
    if invert:
        arr = 1.0 - arr

    chars: Sequence[str] = list(charset)
    if len(chars) < 2:
        chars = list(_ASCII_DEFAULT)
    num = len(chars)

    # map brightness to charset
    idx = np.clip((arr * (num - 1)).round().astype(int), 0, num - 1)

    # draw text onto a white canvas using monospaced font
    out_w = cols * font_size
    out_h = rows * int(font_size * 1.9)
    canvas = Image.new("RGB", (out_w, out_h), "white")
    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    for y in range(rows):
        for x in range(cols):
            ch = chars[idx[y, x]]
            draw.text((x * font_size, y * int(font_size * 1.9)), ch, fill="black", font=font)

    return canvas
