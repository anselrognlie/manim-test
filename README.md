# Manim-Test

Sample animation generation using Manim

## Table of Contents

- [Manim-Test](#manim-test)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Acknowledgments](#acknowledgments)

## Installation

`pycairo` and `ffmpeg` must be installed globally for manim to function properly.
```bash
brew install py3cairo ffmpeg
```

Apple Silicon machines require the following additional dependencies:
```bash
brew install pango scipy
```

Once installed, this project can be set up as any other `venv`-based project.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

`maze.py` generates the sample animation. It should be run as
```bash
manim -ql --disable_caching --format png maze.py MazeScene
```

This instructs manim to use lower-quality animations (`-ql`), disable caching (`--disable_caching`), and output the animation as a series of PNG files (`--format png`). The resulting images will be placed in `media/images/maze/` named like `MazeSceneNNNN.png`.

`make_anim.py` takes a collection of PNG images and combines them into an animated webp file, looking for frames that are identical, and using frame duration to minimize file size. It should be run as
```bash
python make_anim.py media/images/maze/MazeScene
```

This will generate the animation from the files matching the given pattern. With no options, it will assume the desired output is 15 FPS with high compression. The resulting animation will be written to `out.webp`. For more options, run `python make_anim.py --help`.

```text
usage: make_anim.py [-h] [-f fps] [-q] [-o output_file] file_base

positional arguments:
  file_base       e.g., "media/images/maze/MazeScene"

options:
  -h, --help      show this help message and exit
  -f fps          Sets the output frames per second to fps. If omitted, assumes
                  15.
  -q              Uses higher-quality compression. Defaults to low quality.
  -o output_file  Output file for the animation. Must be a webp file. Defaults to
                  out.webp

manim renders PNG images to
      media/images/<scene_filename>/<scene_classname>NNNN.png

This script uses file globbing to find all numbered frames, so the numeric part
and file extension are not needed.

Be sure to clear out frames between runs, or frames from various renders could
end up in the same animation.
```

## Acknowledgments

This project used Manim community build.

- The Manim Community Developers. (2023). Manim – Mathematical Animation Framework (Version v0.17.3) [Computer software]. https://www.manim.community/