#!/usr/bin/env python3
"""Transcribe raw camera rolls into the shared timestamped footage index.

The source video is never modified. Audio is extracted to a temporary mono WAV,
transcribed with local Whisper, and deleted before the next roll starts.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import tempfile
import time

import whisper


def timestamp(seconds: float) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(int(minutes), 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:04.1f}"
    return f"{minutes}:{seconds:04.1f}"


def transcribe_one(model, source: Path, output_dir: Path, ffmpeg: str) -> None:
    output = output_dir / f"{source.stem}.txt"
    if output.exists() and output.stat().st_size:
        print(f"SKIP {source.name}: {output} exists", flush=True)
        return

    wav_path: Path | None = None
    started = time.time()
    try:
        with tempfile.NamedTemporaryFile(prefix=f"rx01-{source.stem}-", suffix=".wav", delete=False) as wav:
            wav_path = Path(wav.name)
        subprocess.run(
            [ffmpeg, "-v", "error", "-y", "-i", str(source), "-map", "0:a:0", "-ac", "1", "-ar", "16000", str(wav_path)],
            check=True,
        )
        result = model.transcribe(str(wav_path), language="en", verbose=False)
        lines = [f"[{timestamp(float(segment['start']))}] {segment['text'].strip()}" for segment in result["segments"]]
        output.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        print(f"DONE {source.name}: {output} ({time.time() - started:.1f}s)", flush=True)
    finally:
        if wav_path is not None:
            wav_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--model", default="base.en")
    parser.add_argument("--ffmpeg", default="Media/video_edit/bin/ffmpeg")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    ffmpeg_path = Path(args.ffmpeg).resolve()
    os.environ["PATH"] = f"{ffmpeg_path.parent}:{os.environ.get('PATH', '')}"
    args.ffmpeg = str(ffmpeg_path)
    model = whisper.load_model(args.model)
    for source in args.sources:
        if not source.is_file():
            raise SystemExit(f"Missing source: {source}")
        transcribe_one(model, source, args.output_dir, args.ffmpeg)


if __name__ == "__main__":
    main()
