from pathlib import Path

from PIL import Image

from livefaceswap_reference_prep import prepare_reference, prepare_reference_image


def test_prepare_reference_image_creates_square_rgb_png(tmp_path: Path) -> None:
    source_path = tmp_path / "source.png"
    output_path = tmp_path / "output.png"
    Image.new("RGBA", (1200, 800), (30, 60, 90, 180)).save(source_path)

    result = prepare_reference_image(source_path, output_path, 512, 0.5, 0.4)

    assert result == output_path
    assert output_path.stat().st_size > 0
    with Image.open(output_path) as output:
        assert output.format == "PNG"
        assert output.mode == "RGB"
        assert output.size == (512, 512)


def test_prepare_reference_image_rejects_invalid_focus(tmp_path: Path) -> None:
    source_path = tmp_path / "source.png"
    Image.new("RGB", (20, 20), "white").save(source_path)

    try:
        prepare_reference_image(source_path, tmp_path / "output.png", 512, 1.1, 0.5)
    except ValueError as error:
        assert "between 0 and 1" in str(error)
    else:
        raise AssertionError("invalid focus must be rejected")


def test_prepare_reference_returns_square_rgb_image() -> None:
    source = Image.new("RGBA", (900, 1200), (12, 34, 56, 120))

    output = prepare_reference(source, 768, 0.4, 0.5)

    assert output.mode == "RGB"
    assert output.size == (768, 768)


def test_prepare_reference_applies_exif_orientation() -> None:
    source = Image.new("RGB", (40, 20), "blue")
    for x in range(20):
        for y in range(20):
            source.putpixel((x, y), (255, 0, 0))
    source.getexif()[274] = 6

    output = prepare_reference(source, 512, 0.5, 0.0)

    assert output.mode == "RGB"
    assert output.size == (512, 512)
    assert output.getpixel((256, 256)) == (255, 0, 0)


def test_prepared_png_does_not_copy_source_metadata(tmp_path: Path) -> None:
    source_path = tmp_path / "source.jpg"
    output_path = tmp_path / "output.png"
    source = Image.new("RGB", (40, 60), "white")
    exif = source.getexif()
    exif[270] = "synthetic metadata"
    source.save(source_path, exif=exif)

    prepare_reference_image(source_path, output_path, 512, 0.5, 0.5)

    with Image.open(output_path) as output:
        assert output.getexif().get(270) is None
        assert "exif" not in output.info
