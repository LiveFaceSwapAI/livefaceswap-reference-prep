from pathlib import Path

from PIL import Image, ImageOps


VALID_SIZES = {512, 768, 1024}


def prepare_reference(
    source: Image.Image,
    size: int = 1024,
    focus_x: float = 0.5,
    focus_y: float = 0.42,
) -> Image.Image:
    if size not in VALID_SIZES:
        raise ValueError(f"size must be one of {sorted(VALID_SIZES)}")
    if not 0.0 <= focus_x <= 1.0 or not 0.0 <= focus_y <= 1.0:
        raise ValueError("focus_x and focus_y must be between 0 and 1")

    image = ImageOps.exif_transpose(source).convert("RGB")
    width, height = image.size
    side = min(width, height)
    max_left = width - side
    max_top = height - side
    left = round(max_left * focus_x)
    top = round(max_top * focus_y)
    cropped = image.crop((left, top, left + side, top + side))
    return cropped.resize((size, size), Image.Resampling.LANCZOS)


def prepare_reference_image(
    input_path: Path,
    output_path: Path,
    size: int = 1024,
    focus_x: float = 0.5,
    focus_y: float = 0.42,
) -> Path:
    with Image.open(input_path) as source:
        prepared = prepare_reference(source, size, focus_x, focus_y)
        prepared.save(output_path, format="PNG", optimize=True)

    return output_path
