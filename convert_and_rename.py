#!/usr/bin/env python

import os
import sys
import subprocess
from pathlib import Path
import argparse
import textwrap
import shlex

DEFAULT_INPUT = "/input"
DEFAULT_OUTPUT = "/output"

def get_image_files(input_dir):
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    return sorted([f for f in Path(input_dir).iterdir() if f.suffix.lower() in image_extensions])

def convert_and_rename_images(input_dir, output_dir, basename, magick_args):
    input_files = get_image_files(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_files:
        print(f"No supported image files found in {input_dir}")
        sys.exit(1)

    print(f"Converting {len(input_files)} images...")

    for i, img_path in enumerate(input_files, start=1):
        suffix = f"-{i:02d}.webp"
        output_path = output_dir / f"{basename}{suffix}"

        cmd = [
            "magick",
            str(img_path),
            *magick_args,
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True)
            print(f"✓ {img_path.name} → {output_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to convert {img_path.name}: {e}")
            continue

def get_arg_parser():
    parser = argparse.ArgumentParser(
        description="Convert images to .webp using ImageMagick and rename them.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("basename", help="Base name for renamed images (e.g., 'product')")
    parser.add_argument(
        "-i", "--input_dir",
        help=f"Input directory (default: {DEFAULT_INPUT})",
        default=DEFAULT_INPUT
    )
    parser.add_argument(
        "-o", "--output_dir",
        help=f"Output directory (default: {DEFAULT_OUTPUT})",
        default=DEFAULT_OUTPUT
    )
    parser.add_argument(
        "-m", "--magick_options",
        help=textwrap.dedent("""\
            Additional ImageMagick options (quoted string).
            Example: --magick_options "-resize 800x800 -quality 90"
        """),
        default="",
        type=str
    )
    parser.add_argument(
        "--magick_help",
        action="store_true",
        help="Show ImageMagick help and exit"
    )
    return parser

def show_magick_help():
    subprocess.run(["magick", "-help"], check=True)
    sys.exit(0)

def main():
    parser = get_arg_parser()
    args = parser.parse_args()

    if args.magick_help:
        show_magick_help()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)

    magick_args = shlex.split(args.magick_options.strip()) if args.magick_options else []

    convert_and_rename_images(
        input_dir=input_dir,
        output_dir=args.output_dir,
        basename=args.basename,
        magick_args=magick_args
    )

if __name__ == "__main__":
    main()
