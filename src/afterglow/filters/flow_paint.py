from __future__ import annotations

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def flow_paint(
    image: Image.Image,
    steps: int = 800,
    stride: int = 3,
    jitter: float = 0.3,
    blur: float = 1.2,
    seed: int = 7,
) -> Image.Image:
    """Painty flow-field effect using image gradients as a vector field.

    Starts from a blurred image and iteratively advects colors along the
    gradient flow with small jitter. Looks like wispy brush strokes.
    """
    rng = np.random.default_rng(seed)

    src = image.convert("RGB")
    arr = np.asarray(src).astype(np.float32) / 255.0

    # compute gradients on a blurred version
    gray = 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]
    gray_blur = ndi.gaussian_filter(gray, sigma=blur)
    gy, gx = np.gradient(gray_blur)
    # rotate gradients 90deg to follow isophotes (artistic)
    vx = -gy
    vy = gx

    h, w = gray.shape
    yy, xx = np.mgrid[0:h:stride, 0:w:stride]
    yy = yy.astype(np.float32)
    xx = xx.astype(np.float32)

    canvas = arr.copy()

    for _ in range(steps):
        # sample velocities at subpixel coords
        vxs = ndi.map_coordinates(vx, [yy, xx], order=1, mode="reflect")
        vys = ndi.map_coordinates(vy, [yy, xx], order=1, mode="reflect")
        # normalize and jitter
        mag = np.sqrt(vxs * vxs + vys * vys) + 1e-6
        vxs = (vxs / mag) + rng.normal(0.0, jitter, size=vxs.shape)
        vys = (vys / mag) + rng.normal(0.0, jitter, size=vys.shape)

        # advect sample points and splat color back to canvas
        yy = np.clip(yy + vys, 0, h - 1)
        xx = np.clip(xx + vxs, 0, w - 1)

        for c in range(3):
            color = ndi.map_coordinates(arr[..., c], [yy, xx], order=1, mode="reflect")
            canvas[..., c][::stride, ::stride] = color

        # slight blur to soften strokes over time
        for c in range(3):
            canvas[..., c] = ndi.gaussian_filter(canvas[..., c], 0.5)

    out = np.clip(canvas * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
