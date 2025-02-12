from __future__ import annotations

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def kuwahara(
    image: Image.Image,
    radius: int = 4,
) -> Image.Image:
    """Kuwahara filter for oil-paint-like smoothing while preserving edges.
    """
    src = image.convert("RGB")
    arr = np.asarray(src).astype(np.float32)

    h, w = arr.shape[:2]
    r = max(1, radius)

    out = np.zeros_like(arr)

    # four quadrant means and variances
    def box_mean(img, size):
        return ndi.uniform_filter(img, size=size, mode="reflect")

    size = r
    regions = []
    for dy in (0, r):
        for dx in (0, r):
            patch = arr.copy()
            # shift image by dx,dy and take box mean/variance
            mean = box_mean(patch, size=(size, size, 1))
            mean_sq = box_mean(patch * patch, size=(size, size, 1))
            var = mean_sq - mean * mean
            regions.append((mean, var))

    # choose region with minimum variance per pixel
    means = [m for m, _ in regions]
    vars_ = [v for _, v in regions]
    var_stack = np.stack(vars_, axis=-1).sum(axis=2)  # sum variances across channels
    k = np.argmin(var_stack, axis=-1)

    out = np.zeros_like(arr)
    for i, mean in enumerate(means):
        mask = (k == i)[..., None]
        out = np.where(mask, mean, out)

    out = np.clip(out, 0, 255).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
