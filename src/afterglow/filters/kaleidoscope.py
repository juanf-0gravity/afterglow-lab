from __future__ import annotations

import math
from typing import Tuple

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def kaleidoscope(image: Image.Image, slices: int = 8, radius: float = 1.0) -> Image.Image:
    assert slices >= 2
    src = image.convert("RGB")
    np_img = np.asarray(src).astype(np.float32)
    h, w = np_img.shape[:2]

    cx, cy = w / 2.0, h / 2.0
    yy, xx = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")

    dx = xx - cx
    dy = yy - cy
    r = np.sqrt(dx * dx + dy * dy)
    theta = np.arctan2(dy, dx)

    # fold angle into 0..(2*pi/slices)
    sector = (2.0 * math.pi) / slices
    theta_folded = np.mod(theta, sector)
    mirror_mask = theta_folded > (sector / 2.0)
    theta_folded = np.where(mirror_mask, sector - theta_folded, theta_folded)

    # Map back to coords
    x_m = cx + r * np.cos(theta_folded)
    y_m = cy + r * np.sin(theta_folded)

    # Clamp radius
    r_max = radius * min(cx, cy)
    mask = r <= r_max

    out = np.zeros_like(np_img)
    for c in range(3):
        sampled = ndi.map_coordinates(np_img[..., c], [y_m, x_m], order=1, mode="reflect")
        channel = out[..., c]
        channel[mask] = sampled[mask]
        # leave outside radius black
        out[..., c] = channel

    out = np.clip(out, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
