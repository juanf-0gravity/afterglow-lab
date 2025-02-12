from __future__ import annotations

import math
from typing import Tuple

import numpy as np
from PIL import Image
from scipy import ndimage as ndi


def _generate_value_noise(height: int, width: int, scale: float, octaves: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    noise = np.zeros((height, width), dtype=np.float32)
    amplitude = 1.0
    frequency = 1.0 / max(1e-6, scale)
    total_amp = 0.0

    for i in range(octaves):
        # coarse random grid interpolated to full size
        step_y = max(1, int(height * frequency))
        step_x = max(1, int(width * frequency))
        grid = rng.random((height // step_y + 2, width // step_x + 2)).astype(np.float32)
        grid_resized = ndi.zoom(grid, (step_y, step_x), order=3)
        grid_resized = grid_resized[:height, :width]
        noise += grid_resized * amplitude
        total_amp += amplitude
        amplitude *= 0.5
        frequency *= 2.0

    noise /= max(1e-6, total_amp)
    noise = (noise - noise.min()) / max(1e-6, (noise.max() - noise.min()))
    noise = noise * 2.0 - 1.0  # [-1, 1]
    return noise


def perlin_warp(image: Image.Image, scale: float = 10.0, intensity: float = 12.0, octaves: int = 3, seed: int = 42) -> Image.Image:
    """Warp image coordinates using multi-octave value noise.

    This is not strict Perlin noise but similar enough for visual effect.
    """
    src = image.convert("RGB")
    np_img = np.asarray(src).astype(np.float32)
    h, w = np_img.shape[:2]

    noise_x = _generate_value_noise(h, w, scale=scale, octaves=octaves, seed=seed)
    noise_y = _generate_value_noise(h, w, scale=scale * 1.3, octaves=octaves, seed=seed + 1)

    # build coordinate maps
    yy, xx = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    map_y = yy + noise_y * intensity
    map_x = xx + noise_x * intensity

    warped = np.zeros_like(np_img)
    for c in range(3):
        warped[..., c] = ndi.map_coordinates(np_img[..., c], [map_y, map_x], order=1, mode="reflect")

    warped = np.clip(warped, 0, 255).astype(np.uint8)
    return Image.fromarray(warped, mode="RGB")
