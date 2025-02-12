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

2) Either use the module CLI or the installed console script:

   ```bash
   # After `pip install -e .`, you can run:
   afterglow --help
   ```

   Or directly via python module:

   ```bash
   # Halftone dots
   python -m afterglow.cli halftone input.jpg -o examples/output/halftone.png --cell 10 --contrast 1.2

   # Perlin-style warp
   python -m afterglow.cli perlin-warp input.jpg -o examples/output/warp.png --scale 12 --intensity 18

   # Kaleidoscope
   python -m afterglow.cli kaleidoscope input.jpg -o examples/output/kale.png --slices 8 --radius 0.95

   # Glow / simple bloom
   python -m afterglow.cli glow input.jpg -o examples/output/glow.png --threshold 0.88 --strength 0.9 --radius 10

   # Glitch (aberration + scanlines)
   python -m afterglow.cli glitch input.jpg -o examples/output/glitch.png --shift 2 --line-shift 18 --prob 0.2

   # Pixel sort (rows)
   python -m afterglow.cli pixel-sort input.jpg -o examples/output/pixelsort.png --threshold 0.65 --direction row

   # Flow-field painterly effect
   python -m afterglow.cli flow-paint input.jpg -o examples/output/flow.png --steps 300

   # Reaction-diffusion stylization
   python -m afterglow.cli react-diff input.jpg -o examples/output/react.png --steps 250 --mix 0.5

   # Chain effects (quick and dirty parser)
   python -m afterglow.cli chain input.jpg -o examples/output/chain.png \
     "halftone:cell=8,contrast=1.1" \
     "perlin_warp:scale=10,intensity=14" \
     "kaleidoscope:slices=12"
     "glitch:shift=2,line_shift=18,prob=0.2"
     "glow:threshold=0.9,strength=0.8,radius=12"
     "pixel_sort:threshold=0.7,direction=row"
     "flow_paint:steps=200"
     "reaction_diffusion:steps=200,mix=0.6"
   ```

Notes
- This is for fun. If something feels janky, you're probably using it correctly.
- Results are resolution-dependent. Try bigger images and adjust parameters.
- SciPy is used for coordinate mapping; if install is slow, grab a coffee.

License
- MIT. Use it for whatever. If you make something cool, I’d love to see it.
