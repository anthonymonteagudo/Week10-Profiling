"""Pack same-size grayscale masks into RGB for Unreal import as linear data."""

import argparse
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for channel in ("ao", "roughness", "metallic", "output"):
        parser.add_argument(channel, type=Path)
    args = parser.parse_args()
    channels = []
    for path in (args.ao, args.roughness, args.metallic):
        with Image.open(path) as source:
            if source.mode != "L":
                parser.error(f"{path} must be an 8-bit grayscale image")
            channels.append(source.copy())
    if any(channel.size != channels[0].size for channel in channels):
        parser.error("all input images must have the same dimensions")
    if args.output.suffix.lower() != ".png":
        parser.error("output must be a PNG")
    with args.output.open("xb") as destination:
        Image.merge("RGB", channels).save(destination, format="PNG")


if __name__ == "__main__":
    main()
