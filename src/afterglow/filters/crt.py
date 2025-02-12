from __future__ import annotations

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def crt_tube(
    image: Image.Image,
    scanline_strength: float = 0.25,
    vignette: float = 0.35,
    curvature: float = 0.08,
    mask_strength: float = 0.2,
) -> Image.Image:
    """Retro CRT effect with curvature, scanlines, and RGB mask.
    """
    src = image.convert("RGB")
    arr = np.asarray(src).astype(np.float32) / 255.0
    h, w = arr.shape[:2]

    # Curvature via barrel distortion
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = (w - 1) / 2.0, (h - 1) / 2.0
    x = (xx - cx) / cx
    y = (yy - cy) / cy
    r2 = x * x + y * y
    k = curvature
    x_d = x * (1 + k * r2)
    y_d = y * (1 + k * r2)
    X = cx + x_d * cx
    Y = cy + y_d * cy

    warped = np.zeros_like(arr)
    for c in range(3):
        warped[..., c] = ndi.map_coordinates(arr[..., c], [Y, X], order=1, mode="reflect")

    # Scanlines (darken every other row)
    lines = (np.sin(np.pi * (yy / 2.0)) * 0.5 + 0.5)
    warped *= (1.0 - scanline_strength + scanline_strength * lines)[..., None]

    # Trinitron-like RGB mask
    mask = np.zeros_like(arr)
    mask[..., 0] = ((xx % 3) == 0).astype(np.float32)
    mask[..., 1] = ((xx % 3) == 1).astype(np.float32)
    mask[..., 2] = ((xx % 3) == 2).astype(np.float32)
    warped = np.clip(warped * (1.0 - mask_strength) + warped * mask * (1.0 + mask_strength), 0.0, 1.0)

    # Vignette
    vign = 1.0 - vignette * (r2 / r2.max())
    warped *= vign[..., None]

    out = (np.clip(warped, 0.0, 1.0) * 255.0).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
