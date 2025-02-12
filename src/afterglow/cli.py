from pathlib import Path
from typing import List, Optional

import typer
from PIL import Image

from afterglow.filters.halftone import halftone_dots
from afterglow.filters.perlin_warp import perlin_warp
from afterglow.filters.kaleidoscope import kaleidoscope as kaleidoscope_filter
from afterglow.filters.glitch import chromatic_aberration, scanline_glitch
from afterglow.filters.bloom import bloom
from afterglow.filters.pixel_sort import pixel_sort
from afterglow.filters.flow_paint import flow_paint
from afterglow.filters.reaction_diffusion import reaction_diffusion
from afterglow.filters.ascii_art import ascii_art
from afterglow.filters.crt import crt_tube
from afterglow.filters.kuwahara import kuwahara
from afterglow.filters.neon_edges import neon_edges

app = typer.Typer(add_completion=False, help="Afterglow Lab: creative image tinkering")


def _open_image(path: Path) -> Image.Image:
    image = Image.open(path)
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")
    return image


def _save_image(image: Image.Image, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)


@app.command()
def halftone(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    cell: int = typer.Option(8, help="Cell size in pixels"),
    contrast: float = typer.Option(1.0, help="Contrast multiplier for dot sizing"),
):
    image = _open_image(input)
    result = halftone_dots(image, cell_size=cell, contrast=contrast)
    _save_image(result, output)


@app.command("perlin-warp")
def perlin_warp_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    scale: float = typer.Option(10.0, help="Noise scale (larger = smoother)"),
    intensity: float = typer.Option(12.0, help="Pixel displacement in px"),
    octaves: int = typer.Option(3, help="Noise octaves for texture"),
    seed: int = typer.Option(42, help="Random seed for reproducibility"),
):
    image = _open_image(input)
    result = perlin_warp(image, scale=scale, intensity=intensity, octaves=octaves, seed=seed)
    _save_image(result, output)


@app.command()
def kaleidoscope(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    slices: int = typer.Option(8, min=2, help="Number of mirrored slices"),
    radius: float = typer.Option(1.0, help="Relative radius [0-1]"),
):
    image = _open_image(input)
    result = kaleidoscope_filter(image, slices=slices, radius=radius)
    _save_image(result, output)


@app.command()
def glow(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    threshold: float = typer.Option(0.85, help="Luminance threshold (0..1)"),
    strength: float = typer.Option(0.8, help="Blend amount (0..1)"),
    radius: int = typer.Option(12, help="Blur radius (px)"),
):
    image = _open_image(input)
    result = bloom(image, threshold=threshold, strength=strength, radius=radius)
    _save_image(result, output)


@app.command("pixel-sort")
def pixel_sort_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    threshold: float = typer.Option(0.7, help="Luminance threshold (0..1)"),
    direction: str = typer.Option("row", help="row or col"),
    reverse: bool = typer.Option(False, help="Reverse sort order"),
):
    image = _open_image(input)
    result = pixel_sort(image, threshold=threshold, direction=direction, reverse=reverse)
    _save_image(result, output)


@app.command("flow-paint")
def flow_paint_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    steps: int = typer.Option(400, help="Number of advection steps"),
    stride: int = typer.Option(3, help="Sampling stride"),
    jitter: float = typer.Option(0.3, help="Noise added to vectors"),
    blur: float = typer.Option(1.2, help="Blur for gradients"),
    seed: int = typer.Option(7, help="Random seed"),
):
    image = _open_image(input)
    result = flow_paint(image, steps=steps, stride=stride, jitter=jitter, blur=blur, seed=seed)
    _save_image(result, output)


@app.command("react-diff")
def reaction_diffusion_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    steps: int = typer.Option(300, help="Simulation steps"),
    feed: float = typer.Option(0.055, help="Feed rate"),
    kill: float = typer.Option(0.062, help="Kill rate"),
    mix: float = typer.Option(0.6, help="Blend with original"),
    seed: int = typer.Option(123, help="Random seed"),
):
    image = _open_image(input)
    result = reaction_diffusion(image, steps=steps, feed=feed, kill=kill, mix=mix, seed=seed)
    _save_image(result, output)


@app.command("ascii")
def ascii_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    cols: int = typer.Option(120, help="Characters across"),
    invert: bool = typer.Option(False, help="Invert brightness mapping"),
):
    image = _open_image(input)
    result = ascii_art(image, cols=cols, invert=invert)
    _save_image(result, output)


@app.command("crt")
def crt_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    scanline_strength: float = typer.Option(0.25),
    vignette: float = typer.Option(0.35),
    curvature: float = typer.Option(0.08),
    mask_strength: float = typer.Option(0.2),
):
    image = _open_image(input)
    result = crt_tube(
        image,
        scanline_strength=scanline_strength,
        vignette=vignette,
        curvature=curvature,
        mask_strength=mask_strength,
    )
    _save_image(result, output)


@app.command("oilpaint")
def kuwahara_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    radius: int = typer.Option(4, help="Neighborhood radius"),
):
    image = _open_image(input)
    result = kuwahara(image, radius=radius)
    _save_image(result, output)


@app.command("neon")
def neon_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    strength: float = typer.Option(1.4),
    glow_radius: float = typer.Option(1.8),
    hue_shift: float = typer.Option(0.1),
):
    image = _open_image(input)
    result = neon_edges(image, strength=strength, glow_radius=glow_radius, hue_shift=hue_shift)
    _save_image(result, output)

@app.command("glitch")
def glitch_cmd(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    aberration: bool = typer.Option(True, help="Apply chromatic aberration first"),
    shift: int = typer.Option(3, help="Aberration shift in pixels"),
    line_shift: int = typer.Option(12, help="Scanline horizontal shift range"),
    prob: float = typer.Option(0.15, help="Probability a line gets shifted"),
    seed: int = typer.Option(1234, help="Random seed for reproducibility"),
):
    image = _open_image(input)
    current = image
    if aberration:
        current = chromatic_aberration(current, shift_pixels=shift)
    current = scanline_glitch(current, line_shift_px=line_shift, line_probability=prob, seed=seed)
    _save_image(current, output)


@app.command()
def chain(
    input: Path = typer.Argument(..., exists=True, readable=True, help="Input image"),
    output: Path = typer.Option(..., "-o", "--output", help="Output path"),
    steps: List[str] = typer.Argument(..., help="Sequence like 'halftone:cell=8' 'perlin_warp:scale=10'"),
):
    image = _open_image(input)

    current = image
    for step in steps:
        if ":" in step:
            name, raw = step.split(":", 1)
        else:
            name, raw = step, ""
        params = {}
        if raw:
            for item in raw.split(","):
                if not item:
                    continue
                key, value = item.split("=", 1)
                # naive parsing: try int, then float, else string
                if value.isdigit():
                    params[key] = int(value)
                else:
                    try:
                        params[key] = float(value)
                    except ValueError:
                        params[key] = value
        name = name.strip().lower()
        if name in {"halftone"}:
            if "cell" in params and "cell_size" not in params:
                try:
                    params["cell_size"] = int(params.pop("cell"))
                except Exception:
                    params.pop("cell", None)
            current = halftone_dots(current, **params)
        elif name in {"perlin_warp", "perlin-warp", "warp"}:
            current = perlin_warp(current, **params)
        elif name in {"kaleidoscope", "kale"}:
            current = kaleidoscope_filter(current, **params)
        elif name in {"glitch", "scanline"}:
            # Map friendly params
            if "shift" in params:
                current = chromatic_aberration(current, shift_pixels=int(params.get("shift", 3)))
            current = scanline_glitch(
                current,
                line_shift_px=int(params.get("line_shift", params.get("line_shift_px", 12))),
                line_probability=float(params.get("prob", params.get("line_probability", 0.15))),
                seed=int(params.get("seed", 1234)),
            )
        elif name in {"glow", "bloom"}:
            current = bloom(
                current,
                threshold=float(params.get("threshold", 0.85)),
                strength=float(params.get("strength", 0.8)),
                radius=int(params.get("radius", 12)),
            )
        else:
            raise typer.BadParameter(f"Unknown step: {name}")

    _save_image(current, output)


if __name__ == "__main__":
    app()
