#!/usr/bin/env python3
"""DS-17 R4 opening revision.

R3 is the frozen baseline. This helper renders only the replacement opening and
concatenates it with the ten unchanged R3 shot encodes. It does not touch raw
media or invalidate the downstream picture caches.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI")
WORK = Path(__file__).resolve().parents[1]
FFMPEG = ROOT / "Media/video_edit/bin/ffmpeg"
LIBRARY = Path("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/jump rope 30 sec - 9x16.mov")
C1674 = Path("/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1674.MP4")
FPS = "30000/1001"
OPENING_FRAMES = 142


def run(args):
    subprocess.run([str(FFMPEG), "-nostdin", "-v", "error", "-y", *map(str, args)], check=True)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_and_filter(candidate):
    if candidate == "library-crop":
        # The file is 1280x720 with actual action in x=320..959. A true 9:16
        # full-height crop is 405x720 and necessarily clips outer hands/rope.
        return LIBRARY, "crop=405:720:438:0,scale=1080:1920:flags=lanczos,setsar=1"
    if candidate == "library-fit":
        # Full-frame action over a blurred full-bleed copy. This preserves head,
        # torso, hands and feet while removing the source's black pillars.
        return LIBRARY, (
            "crop=640:720:320:0,split=2[bg][fg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1080:1920,gblur=sigma=34,eq=brightness=-0.12[bg2];"
            "[fg]scale=1080:1215:flags=lanczos[fg2];"
            "[bg2][fg2]overlay=0:120,format=yuv420p,setsar=1"
        )
    if candidate == "c1674":
        # Full-height 9:16 crop from the 4K landscape roll.
        return C1674, (
            "crop=1215:2160:1312:0,scale=1080:1920:flags=lanczos:"
            "in_color_matrix=bt709:in_range=tv,"
            f"lut3d=file={WORK}/assets/source-grade.cube:interp=tetrahedral,"
            "eq=saturation=0.88,format=yuv420p,setsar=1"
        )
    raise ValueError(candidate)


def render_opening(candidate, start, output, captioned=False, frames=OPENING_FRAMES):
    src, vf = source_and_filter(candidate)
    if captioned:
        vf += f",ass={WORK}/captions.ass"
    run(["-ss", f"{start:.6f}", "-i", src, "-map", "0:v:0", "-an", "-vf", vf,
         "-frames:v", frames, "-r", FPS, "-c:v", "libx264", "-preset", "fast",
         "-crf", "18", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
         "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
         "-metadata:s:v:0", "rotate=0", "-movflags", "+faststart", output])


def render_two_shot(output):
    side = WORK / "build/r4-opening-side.mp4"
    front = WORK / "build/r4-opening-front.mp4"
    render_opening("library-crop", 5.8, side, frames=75)
    render_opening("library-crop", 16.3, front, frames=67)
    run(["-i", side, "-i", front, "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0[v]",
         "-map", "[v]", "-frames:v", OPENING_FRAMES, "-r", FPS, "-c:v", "libx264",
         "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
         "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
         "-movflags", "+faststart", output])


def build(candidate, start):
    opening = WORK / "build/shot-00-r4.mp4"
    if candidate == "library-two-shot":
        render_two_shot(opening)
    else:
        render_opening(candidate, start, opening)
    downstream = [WORK / f"build/shot-{i:02d}.mp4" for i in range(1, 11)]
    missing = [str(p) for p in downstream if not p.exists()]
    if missing:
        raise SystemExit("Missing frozen R3 cache(s): " + ", ".join(missing))
    concat = WORK / "build/concat-r4.txt"
    concat.write_text("".join("file '" + str(p) + "'\n" for p in [opening, *downstream]))
    run(["-f", "concat", "-safe", "0", "-i", concat, "-c", "copy", WORK / "picture.mp4"])
    receipt = {
        "revision": "R4",
        "candidate": candidate,
        "source": str(LIBRARY if candidate == "library-two-shot" else source_and_filter(candidate)[0]),
        "source_sha256": sha256(LIBRARY if candidate == "library-two-shot" else source_and_filter(candidate)[0]),
        "source_start": start,
        "source_cuts": ([{"angle": "side", "start": 5.8, "frames": 75},
                         {"angle": "front", "start": 16.3, "frames": 67}]
                        if candidate == "library-two-shot" else None),
        "frames": OPENING_FRAMES,
        "seconds": OPENING_FRAMES / (30000 / 1001),
        "choice": "Full first spoken sentence; avoids a 22-frame presenter flash before the existing cut.",
        "opening_sha256": sha256(opening),
        "picture_sha256": sha256(WORK / "picture.mp4"),
        "downstream_shots": "Frozen R3 build/shot-01.mp4 through shot-10.mp4 reused unchanged."
    }
    (WORK / "records/r4-opening.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", choices=["library-crop", "library-fit", "library-two-shot", "c1674"])
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--output")
    ap.add_argument("--captioned", action="store_true")
    ap.add_argument("--build", action="store_true")
    args = ap.parse_args()
    if args.build:
        build(args.candidate, args.start)
    else:
        if not args.output:
            ap.error("--output is required without --build")
        if args.candidate == "library-two-shot":
            render_two_shot(Path(args.output))
            if args.captioned:
                raise SystemExit("Captioned two-shot preview is built separately after this helper.")
        else:
            render_opening(args.candidate, args.start, Path(args.output), args.captioned)


if __name__ == "__main__":
    main()
