from __future__ import annotations

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def neon_edges(
    image: Image.Image,
    strength: float = 1.4,
    glow_radius: float = 1.8,
    hue_shift: float = 0.1,
) -> Image.Image:
    """Detect edges and light them with neon-like glow and hue shift."""
    src = image.convert("RGB")
    arr = np.asarray(src).astype(np.float32) / 255.0

    # edge magnitude via Sobel
    gray = 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]
    sx = ndi.sobel(gray, axis=1)
    sy = ndi.sobel(gray, axis=0)
    mag = np.sqrt(sx * sx + sy * sy)
    mag = (mag - mag.min()) / (mag.max() - mag.min() + 1e-6)

    # neon color mask
    neon = np.stack([
        np.clip(np.sin(6.283 * (mag + hue_shift)) * 0.5 + 0.5, 0, 1),
        np.clip(np.sin(6.283 * (mag + hue_shift + 1/3)) * 0.5 + 0.5, 0, 1),
        np.clip(np.sin(6.283 * (mag + hue_shift + 2/3)) * 0.5 + 0.5, 0, 1),
    ], axis=-1)

    # blur to glow
    glow = np.zeros_like(neon)
    for c in range(3):
        glow[..., c] = ndi.gaussian_filter(neon[..., c] * mag, glow_radius)

    out = np.clip(arr * (1.0 - strength * mag[..., None]) + glow * strength, 0.0, 1.0)
    out = (out * 255.0).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
