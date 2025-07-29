#!/bin/bash

# Usage: ./run.sh <input_dir> <output_dir> <basename> [ImageMagick options]
# Example:
#   ./run.sh ./images ./converted product
#   ./run.sh ./images ./converted product "-resize 800x800 -quality 90"

set -e

# Defaults
DEFAULT_MAGICK_OPTS="-resize 1080x720^ -quality 75 -strip"

# Parse args
INPUT_DIR="$1"
OUTPUT_DIR="$2"
BASENAME="$3"
MAGICK_OPTS="${4:-$DEFAULT_MAGICK_OPTS}"

# Help message
if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT_DIR" ] || [ -z "$BASENAME" ]; then
  echo "Usage: $0 <input_dir> <output_dir> <basename> [magick_options]"
  echo "Example: $0 ./images ./converted product"
  echo "         $0 ./images ./converted product \"-resize 800x800 -quality 90\""
  exit 1
fi

# Verify and prepare paths
if [ ! -d "$INPUT_DIR" ]; then
  echo "❌ Error: Input directory '$INPUT_DIR' does not exist."
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
INPUT_PATH=$(realpath "$INPUT_DIR")
OUTPUT_PATH=$(realpath "$OUTPUT_DIR")

# Run Docker
docker run --rm \
  -v "$INPUT_PATH":/input \
  -v "$OUTPUT_PATH":/output \
  image-converter "$BASENAME" -m "$MAGICK_OPTS"
