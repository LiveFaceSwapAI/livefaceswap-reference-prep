from pathlib import Path

from PIL import Image

from image_prep import prepare_reference_image


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

