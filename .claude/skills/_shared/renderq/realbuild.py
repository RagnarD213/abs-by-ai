"""A small REAL build for measuring the render queue, made of the shared pipeline's own pieces, writing only to
a scratch folder. Reads one 4K 10-bit roll from the 10/15 shoot (read-only).

    python3 realbuild.py OUTDIR [--start 60] [--dur 20]

Steps (each timed): picture pass (4K decode, scale and grade, x264 medium), audio extract, a Soft Blue lower
third rendered by softblue.lower_third_patch (Python frames piped between a decoder and an encoder), master
mux (overlay plus AAC, x264 medium), 540p review copy, and Whisper on the master through cut/speech.py.
Whatever ffmpeg is at Media/video_edit/bin/ffmpeg is used, so with the wrapper installed every step queues."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent
sys.path.insert(0, str(SHARED))
sys.path.insert(0, str(SHARED.parent))
import softblue as SB  # noqa: E402

FF = str(SHARED.parents[2] / "Media" / "video_edit" / "bin" / "ffmpeg")
ROLL = ("/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, "
        "studio backdrop/C1725.MP4")


def main(argv):
    out = Path(argv[0])
    start = float(argv[argv.index("--start") + 1]) if "--start" in argv else 60.0
    dur = float(argv[argv.index("--dur") + 1]) if "--dur" in argv else 20.0
    out.mkdir(parents=True, exist_ok=True)
    t, steps = time.time(), {}

    def step(name, fn):
        s = time.time()
        fn()
        steps[name] = round(time.time() - s, 2)
        print("{} {:.1f}s".format(name, steps[name]), flush=True)

    base, wav, lt, master, review = (out / n for n in ("base.mp4", "audio.wav", "lt.mp4", "master.mp4", "review.mp4"))
    step("picture", lambda: subprocess.run([
        FF, "-v", "error", "-y", "-ss", str(start), "-i", ROLL, "-t", str(dur), "-vf",
        "scale=1920:1080:in_color_matrix=bt709:out_color_matrix=bt709:flags=bicubic,eq=saturation=1.08:contrast=1.03",
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(base)], check=True))
    step("audio", lambda: subprocess.run([FF, "-v", "error", "-y", "-ss", str(start), "-i", ROLL, "-t", str(dur),
                                          "-vn", "-ac", "1", "-c:a", "pcm_s16le", str(wav)], check=True))
    geo = {}

    def lower():
        _, x, y = SB.lower_third_patch(base, lt, 1.0, 6.0, "Render queue", "Real build test")
        geo.update(x=x, y=y)
    step("lower_third", lower)
    step("master", lambda: subprocess.run([
        FF, "-v", "error", "-y", "-i", str(base), "-itsoffset", "1.0", "-i", str(lt), "-i", str(wav),
        "-filter_complex", "[0:v][1:v]overlay={}:{}:enable='between(t,1,7)'[v]".format(geo["x"], geo["y"]),
        "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", str(master)], check=True))
    step("review", lambda: subprocess.run([
        FF, "-v", "error", "-y", "-i", str(master), "-vf", "scale=-2:540", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "26", "-c:a", "aac", str(review)], check=True))

    def whisper():
        from _shared.cut import speech
        speech.transcribe(str(master), model="small", force=True, quiet=True)
    step("whisper", whisper)
    steps["total"] = round(time.time() - t, 2)
    (out / "timings.json").write_text(json.dumps(steps))
    print(json.dumps(steps), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
