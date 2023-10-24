from PIL import Image
from PIL.ImageChops import difference
from glob import glob
import argparse
import sys

COUNTER = 10
ENTROPY_THRESHOLD = 2  # From inspection, a non-diff frame resulted in a gray image with an entropy of 2

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog="""
manim renders PNG images to
      media/images/<scene_filename>/<scene_classname>NNNN.png

This script uses file globbing to find all numbered frames, so the numeric part
and file extension are not needed.

Be sure to clear out frames between runs, or frames from various renders could
end up in the same animation.
 
""")
DEFAULT_FPS=15
parser.add_argument('-f', type=int, dest="fps", default=DEFAULT_FPS, metavar="fps", help=f"Sets the output frames per second to fps. If omitted, assumes {DEFAULT_FPS}.")
parser.add_argument('-q', action='store_true', dest="high_quality", help="Uses higher-quality compression. Defaults to low quality.")
parser.add_argument('-o', dest="output_file", metavar="output_file", default="out.webp", help="Output file for the animation. Must be a webp file. Defaults to out.webp")
parser.add_argument('file_base', help="e.g., \"media/images/maze/MazeScene\"")

args = parser.parse_args()

BASE_FILE = args.file_base
# FRAME_DURATION = 1000 / 60
# FRAME_DURATION = 1000 / 15
FRAME_DURATION= 1000 / args.fps
output_file = args.output_file

compression_args = {}
if not args.high_quality:
    compression_args.update(dict(
        quality=30, 
        method=6,
    ))

if output_file.lower()[-5:] != ".webp":
    print("Output file must be a .webp file.", file=sys.stderr)
    exit(1)

print(args)
print(compression_args)

files = sorted(glob(f"{BASE_FILE}*.png")) #[:500]
if not files:
    print("No matching source files.", file=sys.stderr)
    exit(1)

# print(files)

keyframes = []
durations = []

keyframes.append(0)

print("Calculating durations", end="")
last_frame = keyframes[-1]
last_file = files[last_frame]
last_im = Image.open(last_file)
for i in range(len(files)):
    if i % COUNTER == 0:
        # print status mark every COUNTER frames
        print(".", end="", flush=True)

    next_file = files[i]
    next_im = Image.open(next_file)
    diff = difference(last_im, next_im).entropy()
    if diff > ENTROPY_THRESHOLD:
        # there was a difference
        keyframes.append(i)
        durations.append((i - last_frame) * FRAME_DURATION)

        # update the last frame values
        last_frame = i
        last_file = files[last_frame]
        last_im = Image.open(last_file)

durations.append((len(files) - last_frame) * FRAME_DURATION)
print("\nOpening component images...")

selected_files = [files[i] for i in keyframes]
selected_ims = [Image.open(file) for file in selected_files][1:]
start_im = Image.open(selected_files[0])

print("Saving... ", end="")
start_im.save(
    output_file, 
    save_all=True, 
    append_images=selected_ims, 
    duration=durations,
    **compression_args)

print("Done.")
