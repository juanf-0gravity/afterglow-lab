from __future__ import annotations

import random
from typing import Tuple

import numpy as np
from PIL import Image


def chromatic_aberration(image: Image.Image, shift_pixels: int = 3) -> Image.Image:
    src = image.convert("RGB")
    arr = np.asarray(src)
    h, w = arr.shape[:2]

    shifted = np.zeros_like(arr)
    # shift red right, blue left
    shifted[..., 0] = np.roll(arr[..., 0], shift_pixels, axis=1)
    shifted[..., 1] = arr[..., 1]
    shifted[..., 2] = np.roll(arr[..., 2], -shift_pixels, axis=1)
    return Image.fromarray(shifted, mode="RGB")


essential_rng = random.Random()


def scanline_glitch(
    image: Image.Image,
    line_shift_px: int = 12,
    line_probability: float = 0.15,
    seed: int | None = 1234,
) -> Image.Image:
    """Randomly shift horizontal scanlines for a datamosh-y look."""
    if seed is not None:
        essential_rng.seed(seed)

    src = image.convert("RGB")
    arr = np.asarray(src)
    h, w = arr.shape[:2]

    out = arr.copy()
    for y in range(h):
        if essential_rng.random() < line_probability:
            shift = essential_rng.randint(-line_shift_px, line_shift_px)
            out[y, ...] = np.roll(out[y, ...], shift, axis=0)
        # subtle color drift every few lines
        if y % 23 == 0:
            out[y, :, 0] = np.roll(out[y, :, 0], 1, axis=0)
            out[y, :, 2] = np.roll(out[y, :, 2], -1, axis=0)

    return Image.fromarray(out, mode="RGB")
