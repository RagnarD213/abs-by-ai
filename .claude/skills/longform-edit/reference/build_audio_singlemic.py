#!/usr/bin/env python3
"""REV2: rebuild the programme audio from the CLEAN MIC ONLY, frame-locked to the
finished picture.

THE DEFECT. C1512 is not a stereo recording. It carries two different microphones
hard-panned against each other: measured over 60 s at 300 s, the same voice appears
in the left channel 7.46 ms after the right, and the zero-lag correlation between
them is only +0.07. Summed - which is what every phone, laptop and TV speaker does -
a 7.46 ms offset is a comb filter with notches every ~134 Hz, and no EQ can undo it.
Measured on this roll:

    channel           SNR      comb ripple
    right (close lav) 45.5 dB     0.53 dB
    left  (far mic)   34.1 dB     0.49 dB
    naive L+R sum     36.8 dB     0.69 dB      <- what rev-1 shipped

The right channel wins by 11.4 dB of SNR and the sum is the worst of the three.
Same finding, same rig and nearly the same delay as the ad roll in the modern-edit
task (7.83 ms there), so the fix is the same: use the right channel, as mono.

FRAME LOCK. The video is NOT re-rendered for rev 2, so the new audio has to land on
the existing picture exactly. render.py rounds each segment to whole frames, and
those roundings accumulate (+0.65 s over 44 ranges here). Rebuilding from the EDL's
float ranges would therefore drift most of a second by the end. Instead each range's
audio is cut to the duration its ALREADY-RENDERED video segment actually has, read
back out of the segment cache, so the sum matches the picture by construction.

usage: build_audio.py            # writes voice_raw.wav
"""
import hashlib, json, subprocess, wave
from pathlib import Path

B = Path("/Volumes/Extreme/_edit_work/spraytan")
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FFP = FF.replace("ffmpeg", "ffprobe")
edl = json.load(open(B / "edl.json"))
SRC = edl["sources"]["C1512"]
FPS = str(edl.get("fps") or "24")

def resolve_grade(g):
    return g or ""

def seg_path(r):
    """Reproduce render.py's cache key so we can read back the segment it made."""
    seg_filter = resolve_grade(edl.get("grade"))
    if "grade" in r: seg_filter = resolve_grade(r["grade"])
    if r.get("vf"): seg_filter = ",".join(p for p in (seg_filter, r["vf"]) if p)
    key = f"{SRC}|{float(r['start']):.3f}|{float(r['end']):.3f}|{seg_filter}|final|{FPS}"
    h = hashlib.sha1(key.encode()).hexdigest()[:12]
    return B / "clips_graded" / f"seg_C1512_{h}.mp4"

def dur_of(p, stream="a:0"):
    o = subprocess.run([FFP, "-v", "error", "-select_streams", stream, "-show_entries",
                        "stream=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True).stdout.strip()
    return float(o) if o and o != "N/A" else None

parts, total, missing = [], 0.0, []
tmp = B / "_audio_parts"; tmp.mkdir(exist_ok=True)
for i, r in enumerate(edl["ranges"]):
    p = seg_path(r)
    if not p.exists(): missing.append((i, r["beat"], p.name)); continue
    # lock to the segment's VIDEO duration, not its audio duration. Each AAC
    # segment's audio STREAM reads ~15 ms short of its video (encoder priming),
    # and summing those shorts loses 0.56 s over 44 ranges. The concat demuxer
    # already compensates for that padding - measured: base.mp4 ends up with
    # video 1133.866 s and audio 1133.873 s, i.e. the shipped file does NOT
    # drift - so the video duration is the honest target for a rebuild.
    d = dur_of(p, "v:0") or (r["end"] - r["start"])
    out = tmp / f"a{i:03d}.wav"
    fo = max(0.0, d - 0.03)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{r['start']:.3f}",
                    "-i", SRC, "-t", f"{d:.6f}",
                    # RIGHT CHANNEL ONLY, as mono -- this is the fix that matters
                    "-af", f"pan=mono|c0=c1,afade=t=in:st=0:d=0.03,"
                           f"afade=t=out:st={fo:.3f}:d=0.03",
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_s24le", str(out)], check=True)
    parts.append(out); total += d
if missing:
    raise SystemExit(f"segment cache miss for {len(missing)} ranges: {missing[:3]} ...")

lst = B / "_audio_concat.txt"
lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", str(lst), "-c:a", "pcm_s24le", str(B / "voice_raw.wav")], check=True)
got = dur_of(B / "voice_raw.wav", "a:0")
vid = float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(B / "roughcuts" / "FINAL_spraytan.mp4")],
                           capture_output=True, text=True).stdout.strip())
print(f"{len(parts)} ranges -> voice_raw.wav  {got:.3f}s   (summed plan {total:.3f}s)")
print(f"finished picture {vid:.3f}s   drift {got - vid:+.3f}s")
assert abs(got - vid) < 0.10, "audio and picture would drift -- do not mux"
print("frame lock OK")
