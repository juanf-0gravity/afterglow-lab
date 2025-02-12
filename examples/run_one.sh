#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 /path/to/image [OUT_DIR]" >&2
  exit 1
fi

IMG="$1"
OUT_BASE="${2:-}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
EX_DIR="$ROOT_DIR/examples"

# pick runner: console script if available, else module
if command -v afterglow >/dev/null 2>&1; then
  RUN="afterglow"
else
  RUN="python -m afterglow.cli"
fi

# compute output dir
stem="$(basename "$IMG")"
stem_noext="${stem%.*}"
OUT_DIR="${OUT_BASE:-$EX_DIR/output/$stem_noext}"
mkdir -p "$OUT_DIR"

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
