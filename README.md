Afterglow Lab

A small personal playground where I mess around with creative image processing ideas that probably shouldn't work as well as they do. Expect rough edges, happy accidents, and a few "whoa" moments.

Why?
- I wanted a place to experiment with weird visual transformations (warp fields, kaleidoscopes, halftone textures) without pulling in half the ML ecosystem.
- The goal is to get interesting, tactile results from relatively simple building blocks (Pillow + NumPy + a pinch of SciPy).

Quick start
1) Create a virtualenv and install deps:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2) Run the CLI against an image:

   ```bash
   # Halftone dots
   python -m afterglow.cli halftone input.jpg -o examples/output/halftone.png --cell 10 --contrast 1.2

   # Perlin-style warp
   python -m afterglow.cli perlin-warp input.jpg -o examples/output/warp.png --scale 12 --intensity 18

   # Kaleidoscope
   python -m afterglow.cli kaleidoscope input.jpg -o examples/output/kale.png --slices 8 --radius 0.95

   # Chain effects (quick and dirty parser)
   python -m afterglow.cli chain input.jpg -o examples/output/chain.png \
     "halftone:cell=8,contrast=1.1" \
     "perlin_warp:scale=10,intensity=14" \
     "kaleidoscope:slices=12"
   ```

Notes
- This is for fun. If something feels janky, you're probably using it correctly.
- Results are resolution-dependent. Try bigger images and adjust parameters.
- SciPy is used for coordinate mapping; if install is slow, grab a coffee.

License
- MIT. Use it for whatever. If you make something cool, I’d love to see it.
