from __future__ import annotations

import numpy as np
from PIL import Image


def _luminance(arr: np.ndarray) -> np.ndarray:
    return 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]


def pixel_sort(
    image: Image.Image,
    threshold: float = 0.7,
    direction: str = "row",
    reverse: bool = False,
) -> Image.Image:
    """Sort pixels within bright segments along rows or columns.

    - threshold: luminance threshold [0..1] to include in segments
    - direction: 'row' or 'col'
    - reverse: reverse the sort order
    """
    src = image.convert("RGB")
    arr = np.asarray(src).astype(np.uint8)
    h, w = arr.shape[:2]

    lum = _luminance(arr.astype(np.float32) / 255.0)

    out = arr.copy()

    if direction not in {"row", "col"}:
        direction = "row"

    if direction == "row":
        for y in range(h):
            mask = lum[y, :] > threshold
            if not mask.any():
                continue
            # find contiguous segments
            x = 0
            while x < w:
                if not mask[x]:
                    x += 1
                    continue
                start = x
                while x < w and mask[x]:
                    x += 1
                end = x
                # sort this segment by luminance or value
                segment = out[y, start:end, :]
                seg_lum = lum[y, start:end]
                idx = np.argsort(seg_lum)
                if reverse:
                    idx = idx[::-1]
                out[y, start:end, :] = segment[idx]
    else:  # column-wise
        for x in range(w):
            mask = lum[:, x] > threshold
            if not mask.any():
                continue
            y = 0
            while y < h:
                if not mask[y]:
                    y += 1
                    continue
                start = y
                while y < h and mask[y]:
                    y += 1
                end = y
                segment = out[start:end, x, :]
                seg_lum = lum[start:end, x]
                idx = np.argsort(seg_lum)
                if reverse:
                    idx = idx[::-1]
                out[start:end, x, :] = segment[idx]

    return Image.fromarray(out, mode="RGB")
