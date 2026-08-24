import argparse
from pathlib import Path
from typing import Sequence

from .core import VALID_SIZES, prepare_reference_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Normalize, square-crop, and resize an authorized portrait reference."
    )
    parser.add_argument("input", type=Path, help="Input JPG, PNG, or WebP image")
    parser.add_argument("output", type=Path, help="Output PNG path")
    parser.add_argument("--size", type=int, choices=sorted(VALID_SIZES), default=1024)
    parser.add_argument("--focus-x", type=float, default=0.5)
    parser.add_argument("--focus-y", type=float, default=0.42)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    prepare_reference_image(
        args.input,
        args.output,
        size=args.size,
        focus_x=args.focus_x,
        focus_y=args.focus_y,
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
