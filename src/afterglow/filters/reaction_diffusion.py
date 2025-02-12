from __future__ import annotations

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def reaction_diffusion(
    image: Image.Image,
    steps: int = 600,
    feed: float = 0.055,
    kill: float = 0.062,
    diff_a: float = 1.0,
    diff_b: float = 0.5,
    mix: float = 0.6,
    seed: int = 123,
) -> Image.Image:
    """Gray-Scott reaction-diffusion stylization mixed with original image.

    Uses Gray-Scott on a single channel and remaps to RGB.
    """
    rng = np.random.default_rng(seed)

    src = image.convert("RGB")
    arr = np.asarray(src).astype(np.float32) / 255.0

    h, w = arr.shape[:2]
    # start with a seed pattern from luminance
    lum = 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]

    A = np.ones((h, w), dtype=np.float32)
    B = (lum > lum.mean()).astype(np.float32) * 0.1
    B += rng.normal(0.0, 0.02, size=(h, w)).astype(np.float32)
    B = np.clip(B, 0.0, 1.0)

    lap_kernel = np.array([[0.05, 0.2, 0.05], [0.2, -1.0, 0.2], [0.05, 0.2, 0.05]], dtype=np.float32)

    for _ in range(steps):
        lapA = ndi.convolve(A, lap_kernel, mode="reflect")
        lapB = ndi.convolve(B, lap_kernel, mode="reflect")
        reaction = A * (B * B)
        A += diff_a * lapA - reaction + feed * (1 - A)
        B += diff_b * lapB + reaction - (kill + feed) * B
        A = np.clip(A, 0.0, 1.0)
        B = np.clip(B, 0.0, 1.0)

    # map pattern to colors via a simple palette
    pat = (B - A)
    pat = (pat - pat.min()) / (pat.max() - pat.min() + 1e-6)
    palette = np.stack([pat, np.sqrt(pat), 1.0 - pat], axis=-1)

    out = np.clip(arr * (1.0 - mix) + palette * mix, 0.0, 1.0)
    out = (out * 255.0).astype(np.uint8)
    return Image.fromarray(out, mode="RGB")
