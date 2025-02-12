#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
EX_DIR="$ROOT_DIR/examples"
OUT_DIR="$EX_DIR/output"
IMG="$EX_DIR/sample.png"

# pick runner: console script if available, else module
if command -v afterglow >/dev/null 2>&1; then
  RUN="afterglow"
else
  RUN="python -m afterglow.cli"
fi

mkdir -p "$OUT_DIR"

# generate sample if missing
if [ ! -f "$IMG" ]; then
  python - <<'PY'
from PIL import Image, ImageDraw
from pathlib import Path
p = Path(__file__).resolve().parent / 'sample.png'
img = Image.new('RGB', (768, 512), 'white')
d = ImageDraw.Draw(img)
for i in range(0, 512, 24):
    d.line((0, i, 768, 512-i), fill=(i%256, (i*3)%256, (i*7)%256), width=3)
d.rectangle((40, 40, 300, 220), outline=(0,0,0), width=6)
d.ellipse((380,120,700,420), outline=(0,0,0), width=6)
d.text((60, 180), 'afterglow', fill=(10,10,10))
img.save(p)
print('Wrote sample:', p)
PY
fi

set -x

$RUN halftone "$IMG" -o "$OUT_DIR/halftone.png" --cell 10 --contrast 1.2
$RUN perlin-warp "$IMG" -o "$OUT_DIR/warp.png" --scale 12 --intensity 18
$RUN kaleidoscope "$IMG" -o "$OUT_DIR/kale.png" --slices 8 --radius 0.95
$RUN glitch "$IMG" -o "$OUT_DIR/glitch.png" --shift 2 --line-shift 18 --prob 0.2
$RUN glow "$IMG" -o "$OUT_DIR/glow.png" --threshold 0.88 --strength 0.9 --radius 10
$RUN pixel-sort "$IMG" -o "$OUT_DIR/pixelsort.png" --threshold 0.65 --direction row
$RUN flow-paint "$IMG" -o "$OUT_DIR/flow.png" --steps 120
$RUN react-diff "$IMG" -o "$OUT_DIR/react.png" --steps 150 --mix 0.55
$RUN ascii "$IMG" -o "$OUT_DIR/ascii.png" --cols 140
$RUN crt "$IMG" -o "$OUT_DIR/crt.png"
$RUN oilpaint "$IMG" -o "$OUT_DIR/oil.png" --radius 5
$RUN neon "$IMG" -o "$OUT_DIR/neon.png" --strength 1.6 --glow-radius 2.2

# chain example
$RUN chain "$IMG" -o "$OUT_DIR/chain.png" \
  "halftone:cell=8,contrast=1.1" \
  "perlin_warp:scale=10,intensity=14" \
  "kaleidoscope:slices=12" \
  "glitch:shift=2,line_shift=18,prob=0.2" \
  "glow:threshold=0.9,strength=0.8,radius=12"
