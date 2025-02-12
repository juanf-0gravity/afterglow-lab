from __future__ import annotations

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def bloom(image: Image.Image, threshold: float = 0.85, strength: float = 0.8, radius: int = 12) -> Image.Image:
    """Simple threshold bloom glow.

    - threshold: 0..1 luminance threshold to start glowing
    - strength: 0..1 blend amount for glow
    - radius: gaussian blur radius in pixels
    """
    src = image.convert("RGB")
    arr = np.asarray(src).astype(np.float32) / 255.0

    lum = 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]
    mask = (lum > threshold).astype(np.float32)

    # create a bright pass
    bright = arr * mask[..., None]

    # blur bright areas
    blurred = np.zeros_like(arr)
    for c in range(3):
        blurred[..., c] = ndi.gaussian_filter(bright[..., c], sigma=radius)

    # normalize blurred max to avoid overblow
    max_val = max(1e-6, blurred.max())
    blurred = blurred / max_val

    # composite
    out = np.clip(arr + blurred * strength, 0.0, 1.0)
    out = (out * 255.0).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
