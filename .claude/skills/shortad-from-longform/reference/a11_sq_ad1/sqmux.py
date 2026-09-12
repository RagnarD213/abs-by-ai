#!/usr/bin/env python3
"""Mux the square picture + captions with the APPROVED VERTICAL'S AUDIO STREAM, bit for bit.

  python3 sqmux.py picture.mp4 captions.mov ad1_square_1x1.mp4

⚠ THE AUDIO IS NOT REBUILT AND NOT RE-ENCODED. The square must sound exactly like the cut
Dan approved on 2026-09-10, so its AAC stream is COPIED out of
`… | claude | 9x16 | ad 1.mp4` and the md5 of the muxed stream is asserted equal to the
md5 of his. (Step 4 of the skill: an editor's -- or an approved build's -- finished mix
ships untouched. The rejected Zeeshan verticals are what "improving" it sounds like.)

⚠ AND THE PICTURE LANDS ON MUHAMMAD'S FRAME COUNT, 6,976. The approved vertical is 6,977:
attempt 3 predates the frame-count assert, so its final mux took its length from the
longest input (the captions stream) instead of the plan. The square asserts the count here
and at every step upstream. The audio therefore runs 33 ms (one frame) longer than the
picture -- inside qc check 16's 0.15 s bound, and the only way to keep the stream identical.
"""
import json, os, subprocess, sys

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace("ffmpeg", "ffprobe")
VERT = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/"
        "this picture got me abs - ad 1/this picture got me abs | claude | 9x16 | ad 1.mp4")
TARGET_FRAMES = 6976            # Muhammad's own count, measured


def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode:
        print(" ".join(str(x) for x in c[:40]), "\n", r.stderr[-2000:]); raise SystemExit(1)
    return r


def audio_md5(path):
    r = sh([FF, "-nostdin", "-v", "error", "-i", path, "-map", "0:a", "-c", "copy", "-f", "md5", "-"])
    return r.stdout.strip().split("=")[-1]


def nframes(path):
    j = json.loads(subprocess.run([FP, "-v", "error", "-select_streams", "v", "-count_frames",
        "-show_entries", "stream=nb_read_frames", "-of", "json", path],
        capture_output=True, text=True).stdout)["streams"][0]
    return int(j["nb_read_frames"])


def main():
    pic = sys.argv[1] if len(sys.argv) > 1 else "picture.mp4"
    cap = sys.argv[2] if len(sys.argv) > 2 else "captions.mov"
    out = sys.argv[3] if len(sys.argv) > 3 else "ad1_square_1x1.mp4"
    audio_src = sys.argv[4] if len(sys.argv) > 4 else VERT
    want = int(sys.argv[5]) if len(sys.argv) > 5 else TARGET_FRAMES

    got = nframes(pic)
    assert got == want, f"{pic} is {got} frames, must be {want}"
    his = audio_md5(audio_src)

    sh([FF, "-nostdin", "-v", "error", "-y", "-i", pic, "-i", cap, "-i", audio_src,
        "-filter_complex", "[0:v][1:v]overlay=0:0:eof_action=pass[v]",
        "-map", "[v]", "-map", "2:a",
        "-frames:v", str(want),
        "-r", "30000/1001", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.2",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "copy", "-movflags", "+faststart", out])

    got = nframes(out)
    ours = audio_md5(out)
    j = json.loads(subprocess.run([FP, "-v", "error", "-show_entries",
        "stream=codec_type,width,height,r_frame_rate,duration,bit_rate", "-of", "json", out],
        capture_output=True, text=True).stdout)["streams"]
    v = [s for s in j if s["codec_type"] == "video"][0]
    a = [s for s in j if s["codec_type"] == "audio"][0]
    print(f"{out}: {v['width']}x{v['height']} @ {v['r_frame_rate']}  {got} frames  "
          f"video {float(v['duration']):.3f}s  audio {float(a['duration']):.3f}s")
    print(f"audio stream md5  ours {ours}  his {his}")
    assert got == want, f"muxed {got} frames, must be {want}"
    assert ours == his, "THE AUDIO STREAM IS NOT THE APPROVED VERTICAL'S, BIT FOR BIT"
    print("OK: frame count is Muhammad's, audio stream is the approved vertical's bit for bit")


if __name__ == "__main__":
    main()
