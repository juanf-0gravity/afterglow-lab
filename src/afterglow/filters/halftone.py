from __future__ import annotations

import math
from typing import Tuple

import numpy as np
from PIL import Image, ImageDraw


def _luminance(rgb: np.ndarray) -> np.ndarray:
    # perceptual luminance from sRGB
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def halftone_dots(image: Image.Image, cell_size: int = 8, contrast: float = 1.0) -> Image.Image:
    """Simple circular-dots halftone.

    - cell_size: grid size in pixels
    - contrast: scales dot size response (1.0 is linear)
    """
    src = image.convert("RGB")
    w, h = src.size

    pixels = np.asarray(src).astype(np.float32) / 255.0
    lum = _luminance(pixels)

    # Adjust contrast by raising to a power (gamma-like)
    if contrast != 1.0:
        lum = np.clip(lum, 0.0, 1.0) ** (1.0 / max(1e-5, contrast))

    out = Image.new("RGB", (w, h), color="white")
    draw = ImageDraw.Draw(out)

    radius_max = cell_size * math.sqrt(2) / 2.0

    for y in range(0, h, cell_size):
        for x in range(0, w, cell_size):
            y1 = min(y + cell_size, h)
            x1 = min(x + cell_size, w)
            block = lum[y:y1, x:x1]
            # mean luminance -> smaller dots for brighter areas
            m = float(np.mean(block))
            # invert so darker areas have larger dots
            size = (1.0 - m) * radius_max
            cx = x + (x1 - x) / 2.0
            cy = y + (y1 - y) / 2.0
            r = max(0.0, size)
            if r > 0.5:
                bbox = (cx - r, cy - r, cx + r, cy + r)
                draw.ellipse(bbox, fill="black")

    return out
