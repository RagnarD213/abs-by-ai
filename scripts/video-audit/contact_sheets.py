#!/usr/bin/env python3
"""Create one evenly sampled 3x3 contact sheet for each source clip."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont


def duration(source: Path, ffprobe: str) -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(source)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ffmpeg", default="Media/video_edit/bin/ffmpeg")
    parser.add_argument("--ffprobe", default="Media/video_edit/bin/ffprobe")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for source in args.sources:
        if not source.is_file():
            raise SystemExit(f"Missing source: {source}")
        output = args.output_dir / f"{source.stem}.jpg"
        if output.exists() and output.stat().st_size:
            print(f"SKIP {source.name}: {output} exists", flush=True)
            continue
        seconds = max(duration(source, args.ffprobe), 0.1)
        # Seek before opening the input. This avoids decoding a 20-minute 5K
        # GoPro clip from the start nine times just to inspect nine frames.
        with tempfile.TemporaryDirectory(prefix=f"{source.stem}-sheet-") as temp_dir:
            frames: list[Image.Image] = []
            for index in range(9):
                timestamp = seconds * (index + 1) / 10
                frame_path = Path(temp_dir) / f"{index:02d}.jpg"
                subprocess.run(
                    [
                        args.ffmpeg,
                        "-v", "error", "-y", "-ss", f"{timestamp:.3f}",
                        "-i", str(source), "-frames:v", "1",
                        "-vf", "scale=480:-2", "-q:v", "2", str(frame_path),
                    ],
                    check=True,
                )
                frame = Image.open(frame_path).convert("RGB")
                label_height = 28
                labelled = Image.new("RGB", (frame.width, frame.height + label_height), "black")
                labelled.paste(frame, (0, label_height))
                ImageDraw.Draw(labelled).text(
                    (8, 6), f"{timestamp / 60:.1f} min", fill="white", font=ImageFont.load_default()
                )
                frames.append(labelled)

            tile_width = max(frame.width for frame in frames)
            tile_height = max(frame.height for frame in frames)
            sheet = Image.new("RGB", (tile_width * 3, tile_height * 3), "black")
            for index, frame in enumerate(frames):
                sheet.paste(frame, ((index % 3) * tile_width, (index // 3) * tile_height))
            sheet.save(output, quality=92)
        print(f"DONE {source.name}: {output}", flush=True)


if __name__ == "__main__":
    main()
