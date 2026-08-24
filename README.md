# LiveFaceSwap Reference Image Prep

A small, deterministic image utility for preparing authorized portrait reference images. It normalizes EXIF orientation, converts the image to RGB, crops it to a square around an adjustable focal point, and returns a consistently sized PNG.

This utility does not perform face swapping or identity transformation. It is intended as a transparent preprocessing step for portrait and camera workflows such as [LiveFaceSwap AI](https://livefaceswap.ai/).

## Inputs

- `image`: JPG, PNG, or WebP input image.
- `size`: Output width and height: 512, 768, or 1024 pixels.
- `focus_x`: Horizontal crop focus from 0 (left) to 1 (right).
- `focus_y`: Vertical crop focus from 0 (top) to 1 (bottom).

## Output

A square RGB PNG with normalized orientation and metadata removed.

Only process images you have permission to use, and do not use portrait references for impersonation, fraud, harassment, or other deceptive activity.

## Local development

```bash
cog predict -i image=@portrait.jpg -i size=1024 -i focus_x=0.5 -i focus_y=0.42
```

Install the Python package locally and use the CLI:

```bash
python -m pip install .
livefaceswap-reference-prep portrait.jpg prepared.png --size 1024
```

Run the Streamlit application:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Run the published container with mounted input and output directories:

```bash
docker run --rm \
  -v "$PWD/input:/input:ro" \
  -v "$PWD/output:/output" \
  ghcr.io/livefaceswapai/livefaceswap-reference-prep:latest \
  /input/portrait.jpg /output/prepared.png --size 1024
```

## License

MIT
