# Image Converter to WebP with ImageMagick 

Batch convert images to `.webp`, rename them with a custom base name, and optionally apply [ImageMagick](https://imagemagick.org/) transformations. Wrapped in a fully portable **Docker + Conda** environment. No need to install Python, ImageMagick, or manage environments manually.

---


## Features

- Rename image files with a string such as `new-image-name`, to get files `new-image-name_01.webp`, `new-image-name_02.webp`, etc.
- Apply ImageMagick options like resizing, quality control, etc.
- Output directory is automatically created.
- Docker container includes Conda + ImageMagick, so no setup needed on your machine.

---

## Setup and Usage

### Build the Docker image

```bash
docker build -t image-converter .
```

### Run the container with Docker

```bash
docker run --rm \
  -v "$PWD/input":/data/input \
  -v "$PWD/output":/data/output \
  image-converter \
  /data/input product -o /data/output --magick_options "-resize 800x800 -quality 85"
```

### Run the container with Shell wrapper
This Shell script simplifies the commands and has default options of "```-resize 1080x720^ -quality 75 -strip```". Edit the script ```DEFAULT_MAGICK_OPTS``` to define default options or override with ```[imagemagick_options]```.

```bash
./image-convert.sh <input_dir> <output_dir> <basename> [imagemagick_options]
```

### 3. Show ImageMagick Help
To show the ImageMagick help and options.

```bash
docker run --rm image-converter --magick_help
```

