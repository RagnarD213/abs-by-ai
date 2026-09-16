#!/usr/bin/env python3
"""Compare an editor's HD export with the reviewed copy it should preserve.

The comparison deliberately separates three claims:
1. timeline/stream structure still matches;
2. the AAC packet payload is byte-identical;
3. sampled picture changes are confined to explicitly allowed revision windows.

It does not approve the content inside an allowed window. Those frames still need
to be inspected against the written revision.
"""

from __future__ import annotations

import argparse
import audioop
import hashlib
import json
import math
import statistics
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_FFMPEG = ROOT / "Media/video_edit/bin/ffmpeg"
DEFAULT_FFPROBE = ROOT / "Media/video_edit/bin/ffprobe"
FRAME_W = 96
FRAME_H = 54


def run(command: list[str], *, stdout=None) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, stdout=stdout, stderr=subprocess.PIPE)


def probe(path: Path, ffprobe: Path) -> dict:
    result = run([
        str(ffprobe), "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(path),
    ], stdout=subprocess.PIPE)
    return json.loads(result.stdout)


def stream(probe_data: dict, kind: str) -> dict | None:
    return next((item for item in probe_data["streams"] if item.get("codec_type") == kind), None)


def fraction(value: str | None) -> float | None:
    if not value or value == "0/0":
        return None
    numerator, denominator = value.split("/", 1)
    return float(numerator) / float(denominator)


def duration(probe_data: dict) -> float:
    value = probe_data.get("format", {}).get("duration")
    if value is not None:
        return float(value)
    values = [float(s["duration"]) for s in probe_data["streams"] if s.get("duration")]
    if not values:
        raise RuntimeError("No duration in ffprobe output")
    return max(values)


def audio_packet_hash(path: Path, ffmpeg: Path) -> tuple[str, int]:
    result = run([
        str(ffmpeg), "-v", "error", "-i", str(path), "-map", "0:a:0",
        "-c", "copy", "-f", "data", "pipe:1",
    ], stdout=subprocess.PIPE)
    return hashlib.sha256(result.stdout).hexdigest(), len(result.stdout)


def decoded_audio(path: Path, ffmpeg: Path) -> bytes:
    result = run([
        str(ffmpeg), "-v", "error", "-i", str(path), "-map", "0:a:0",
        "-ac", "1", "-ar", "16000", "-f", "s16le", "pipe:1",
    ], stdout=subprocess.PIPE)
    return result.stdout


def compare_decoded_audio(approved: bytes, hd: bytes) -> dict:
    sample_rate = 16000
    sample_width = 2
    pad_samples = int(0.1 * sample_rate)
    anchor_samples = int(10 * sample_rate)
    segment_samples = int(20 * sample_rate)
    reference = approved[
        anchor_samples * sample_width:(anchor_samples + segment_samples) * sample_width
    ]
    fragment = hd[
        (anchor_samples - pad_samples) * sample_width:
        (anchor_samples + segment_samples + pad_samples) * sample_width
    ]
    found_offset, fitted_gain = audioop.findfit(fragment, reference)
    shift_samples = found_offset - pad_samples
    approved_start = max(0, -shift_samples)
    hd_start = max(0, shift_samples)
    common_samples = min(
        len(approved) // sample_width - approved_start,
        len(hd) // sample_width - hd_start,
    )
    approved_common = approved[
        approved_start * sample_width:(approved_start + common_samples) * sample_width
    ]
    hd_common = hd[hd_start * sample_width:(hd_start + common_samples) * sample_width]
    approved_rms = audioop.rms(approved_common, 2)
    hd_rms = audioop.rms(hd_common, 2)
    residual = audioop.add(approved_common, audioop.mul(hd_common, 2, -1.0), 2)
    residual_rms = audioop.rms(residual, 2)
    gain_db = 20 * math.log10(hd_rms / approved_rms) if approved_rms and hd_rms else float("inf")
    residual_db_relative = (
        20 * math.log10(residual_rms / approved_rms)
        if approved_rms and residual_rms else -120.0
    )
    cosine_similarity = (
        (approved_rms ** 2 + hd_rms ** 2 - residual_rms ** 2)
        / (2 * approved_rms * hd_rms)
        if approved_rms and hd_rms else 0.0
    )
    length_delta_seconds = abs(len(approved) - len(hd)) / sample_width / sample_rate
    equivalent = (
        length_delta_seconds <= 0.05
        and abs(shift_samples / sample_rate) <= 0.1
        and abs(gain_db) <= 0.15
        and cosine_similarity >= 0.99
    )
    return {
        "sample_rate": sample_rate,
        "channels": 1,
        "approved_pcm_bytes": len(approved),
        "hd_pcm_bytes": len(hd),
        "length_delta_seconds": round(length_delta_seconds, 6),
        "alignment_shift_ms": round(shift_samples / sample_rate * 1000, 3),
        "alignment_fit_gain": round(fitted_gain, 9),
        "approved_rms": approved_rms,
        "hd_rms": hd_rms,
        "gain_delta_db": round(gain_db, 6),
        "residual_db_relative_to_approved": round(residual_db_relative, 6),
        "cosine_similarity": round(cosine_similarity, 9),
        "equivalent": equivalent,
    }


def decode_samples(path: Path, ffmpeg: Path, sample_fps: float, target: Path) -> int:
    run([
        str(ffmpeg), "-nostdin", "-v", "error", "-y", "-i", str(path),
        "-vf", f"fps={sample_fps},scale={FRAME_W}:{FRAME_H}:flags=area,format=gray",
        "-an", "-f", "rawvideo", str(target),
    ])
    size = target.stat().st_size
    frame_size = FRAME_W * FRAME_H
    if size % frame_size:
        raise RuntimeError(f"Unexpected raw frame byte count for {path}: {size}")
    return size // frame_size


def parse_time(value: str) -> float:
    parts = [float(part) for part in value.split(":")]
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    raise argparse.ArgumentTypeError(f"Bad time value: {value}")


def parse_window(value: str) -> tuple[float, float]:
    try:
        start, end = value.split("-", 1)
        parsed = parse_time(start), parse_time(end)
    except (ValueError, argparse.ArgumentTypeError) as error:
        raise argparse.ArgumentTypeError("Window must be START-END, using seconds or MM:SS") from error
    if parsed[1] <= parsed[0]:
        raise argparse.ArgumentTypeError(f"Window end must follow start: {value}")
    return parsed


def in_windows(second: float, windows: list[tuple[float, float]], pad: float) -> bool:
    return any(start - pad <= second <= end + pad for start, end in windows)


def stretches(indices: list[int], sample_fps: float) -> list[dict]:
    if not indices:
        return []
    groups: list[list[int]] = [[indices[0]]]
    for index in indices[1:]:
        if index == groups[-1][-1] + 1:
            groups[-1].append(index)
        else:
            groups.append([index])
    return [
        {
            "start": round(group[0] / sample_fps, 3),
            "end": round((group[-1] + 1) / sample_fps, 3),
            "samples": len(group),
        }
        for group in groups
    ]


def compare_picture(
    approved_raw: Path,
    hd_raw: Path,
    frame_count: int,
    sample_fps: float,
    threshold: float,
    windows: list[tuple[float, float]],
    window_pad: float,
) -> dict:
    frame_size = FRAME_W * FRAME_H
    diffs: list[float] = []
    with approved_raw.open("rb") as approved, hd_raw.open("rb") as hd:
        for _ in range(frame_count):
            left = approved.read(frame_size)
            right = hd.read(frame_size)
            if len(left) != frame_size or len(right) != frame_size:
                raise RuntimeError("Raw sample files ended early")
            diffs.append(sum(abs(a - b) for a, b in zip(left, right)) / frame_size)

    changed = [index for index, value in enumerate(diffs) if value > threshold]
    outside = [index for index in changed if not in_windows(index / sample_fps, windows, window_pad)]
    window_counts = []
    for start, end in windows:
        count = sum(
            1 for index in changed
            if start - window_pad <= index / sample_fps <= end + window_pad
        )
        window_counts.append({"start": start, "end": end, "changed_samples": count})

    ordered = sorted(diffs)
    p99_index = min(len(ordered) - 1, math.ceil(len(ordered) * 0.99) - 1)
    return {
        "sample_fps": sample_fps,
        "sample_frames": frame_count,
        "mean_absolute_luma_difference": round(statistics.fmean(diffs), 6),
        "p99_absolute_luma_difference": round(ordered[p99_index], 6),
        "max_absolute_luma_difference": round(max(diffs), 6),
        "change_threshold": threshold,
        "changed_samples": len(changed),
        "changed_stretches": stretches(changed, sample_fps),
        "outside_allowed_samples": len(outside),
        "outside_allowed_stretches": stretches(outside, sample_fps),
        "allowed_window_counts": window_counts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("approved", type=Path)
    parser.add_argument("hd", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--allow-window", action="append", default=[], type=parse_window)
    parser.add_argument("--window-pad", type=float, default=0.5)
    parser.add_argument("--sample-fps", type=float, default=5.0)
    parser.add_argument("--change-threshold", type=float, default=2.0)
    parser.add_argument("--ffmpeg", type=Path, default=DEFAULT_FFMPEG)
    parser.add_argument("--ffprobe", type=Path, default=DEFAULT_FFPROBE)
    args = parser.parse_args()

    for path in (args.approved, args.hd, args.ffmpeg, args.ffprobe):
        if not path.exists():
            parser.error(f"Missing: {path}")

    approved_probe = probe(args.approved, args.ffprobe)
    hd_probe = probe(args.hd, args.ffprobe)
    approved_video = stream(approved_probe, "video") or {}
    hd_video = stream(hd_probe, "video") or {}
    approved_audio = stream(approved_probe, "audio")
    hd_audio = stream(hd_probe, "audio")
    approved_duration = duration(approved_probe)
    hd_duration = duration(hd_probe)
    approved_fps = fraction(approved_video.get("avg_frame_rate"))
    hd_fps = fraction(hd_video.get("avg_frame_rate"))
    one_frame = 1 / min(value for value in (approved_fps, hd_fps) if value)

    structure = {
        "approved": {
            "width": approved_video.get("width"),
            "height": approved_video.get("height"),
            "fps": approved_fps,
            "duration": approved_duration,
            "frames": approved_video.get("nb_frames"),
            "video_codec": approved_video.get("codec_name"),
            "audio_codec": approved_audio.get("codec_name") if approved_audio else None,
        },
        "hd": {
            "width": hd_video.get("width"),
            "height": hd_video.get("height"),
            "fps": hd_fps,
            "duration": hd_duration,
            "frames": hd_video.get("nb_frames"),
            "video_codec": hd_video.get("codec_name"),
            "audio_codec": hd_audio.get("codec_name") if hd_audio else None,
        },
    }
    aspect_approved = approved_video.get("width", 0) / approved_video.get("height", 1)
    aspect_hd = hd_video.get("width", 0) / hd_video.get("height", 1)
    structure_pass = (
        abs(approved_duration - hd_duration) <= one_frame + 0.002
        and approved_fps is not None
        and hd_fps is not None
        and abs(approved_fps - hd_fps) < 0.001
        and abs(aspect_approved - aspect_hd) < 0.005
        and approved_audio is not None
        and hd_audio is not None
    )

    approved_audio_hash, approved_audio_bytes = audio_packet_hash(args.approved, args.ffmpeg)
    hd_audio_hash, hd_audio_bytes = audio_packet_hash(args.hd, args.ffmpeg)
    approved_pcm = decoded_audio(args.approved, args.ffmpeg)
    hd_pcm = decoded_audio(args.hd, args.ffmpeg)
    decoded_audio_result = compare_decoded_audio(approved_pcm, hd_pcm)
    packet_exact = approved_audio_hash == hd_audio_hash and approved_audio_bytes == hd_audio_bytes
    audio = {
        "approved_aac_payload_sha256": approved_audio_hash,
        "approved_aac_payload_bytes": approved_audio_bytes,
        "hd_aac_payload_sha256": hd_audio_hash,
        "hd_aac_payload_bytes": hd_audio_bytes,
        "packet_exact": packet_exact,
        "decoded": decoded_audio_result,
        "equivalent": packet_exact or decoded_audio_result["equivalent"],
    }

    with tempfile.TemporaryDirectory(prefix="compare-hd-") as temp_dir:
        temp = Path(temp_dir)
        approved_samples = temp / "approved.gray"
        hd_samples = temp / "hd.gray"
        approved_count = decode_samples(args.approved, args.ffmpeg, args.sample_fps, approved_samples)
        hd_count = decode_samples(args.hd, args.ffmpeg, args.sample_fps, hd_samples)
        common_count = min(approved_count, hd_count)
        picture = compare_picture(
            approved_samples, hd_samples, common_count, args.sample_fps,
            args.change_threshold, args.allow_window, args.window_pad,
        )
        picture["approved_sample_frames"] = approved_count
        picture["hd_sample_frames"] = hd_count

    every_expected_window_changed = all(
        item["changed_samples"] > 0 for item in picture["allowed_window_counts"]
    )
    if not args.allow_window:
        every_expected_window_changed = True
    picture_pass = (
        approved_count == hd_count
        and picture["outside_allowed_samples"] == 0
        and every_expected_window_changed
    )
    report = {
        "approved": str(args.approved.resolve()),
        "hd": str(args.hd.resolve()),
        "allowed_windows": [list(item) for item in args.allow_window],
        "window_pad": args.window_pad,
        "structure": structure,
        "structure_pass": structure_pass,
        "audio": audio,
        "picture": picture,
        "picture_pass": picture_pass,
        "pass": structure_pass and audio["equivalent"] and picture_pass,
        "interpretation": (
            "PASS proves matching timeline, an exact or transparently re-encoded audio mix, and no sampled "
            "picture changes outside the declared windows. Inspect every declared window against the written revision."
        ),
    }
    rendered = json.dumps(report, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered + "\n")
    print(rendered)
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
