#!/usr/bin/env python3
"""Rebuild the programme voice from the CLEAN MIC ONLY, frame-locked to the picture.

THE DEFECT ON THIS SHOOT. C1630/C1631/C1632/C1633 are not stereo recordings -- the
LEFT channel carries no speech at all. Measured over 40 s at 60 s on each roll:

    roll    LEFT SNR   RIGHT SNR   left peak    zero-lag corr
    C1630     1.1 dB     44.1 dB   -51.2 dBFS       -0.004
    C1631     0.9 dB     40.6 dB   -55.2 dBFS       -0.004
    C1632     0.6 dB     42.4 dB   -55.8 dBFS       -0.004
    C1633     1.4 dB     30.8 dB   -52.1 dBFS       -0.002

The left channel is a dead input recording room hiss 50+ dB down. The delivered edit
shipped those two channels as stereo, so Dan's voice comes out of the right speaker
and hiss out of the left for the whole nine minutes. This is NOT the 8/3 two-mic comb
filter -- it is simpler and worse. Fix: right channel only, folded to both channels.

FRAME LOCK. Each range's audio is cut to the duration its ALREADY-RENDERED video
segment actually has (read out of the segment cache), not to the EDL's float range --
render.py rounds every segment to whole frames and those roundings accumulate.
"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import segmap

B   = Path("/Volumes/Extreme/_edit_work/abwheel")
R2  = B / "r2"
FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP = FF.replace("ffmpeg", "ffprobe")
PICTURE = B / "roughcuts" / "CUT_v2_graded.mp4"
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"); from common import load_source

edl = json.load(open(B / "edl.json"))
rows, total = segmap.build()
tmp = R2 / "audio" / "parts"; tmp.mkdir(parents=True, exist_ok=True)

parts = []
for r in rows:
    assert r["exists"], f"segment cache miss: {r['beat']}"
    d = r["dur"]
    src = edl["sources"][r["source"]]
    out = tmp / f"a{r['i']:03d}.wav"
    fo = max(0.0, d - 0.03)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{r['start']:.3f}",
                    "-i", src, "-t", f"{d:.6f}", "-map", load_source(src)["map"],
                    # THE LAV TRACK ONLY (per pick_lav's audio_source.json) -- the fix that matters
                    "-af", f"{load_source(src)['filter']},afade=t=in:st=0:d=0.03,"
                           f"afade=t=out:st={fo:.3f}:d=0.03",
                    "-ac", "1", "-ar", "48000", "-c:a", "pcm_s24le", str(out)], check=True)
    parts.append(out)

lst = R2 / "audio" / "concat.txt"
lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", str(lst), "-c:a", "pcm_s24le", str(R2 / "audio" / "voice_raw.wav")],
               check=True)

def dur(p, sel):
    o = subprocess.run([FFP, "-v", "error", "-select_streams", sel, "-show_entries",
                        "stream=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True).stdout.strip()
    return float(o)

got = dur(R2 / "audio" / "voice_raw.wav", "a:0")
vid = dur(PICTURE, "v:0")
print(f"{len(parts)} ranges -> voice_raw.wav {got:.3f}s   picture {vid:.3f}s   drift {got-vid:+.3f}s")
assert abs(got - vid) < 0.12, "audio and picture would drift -- do not mux"
print("frame lock OK")
print("next: python3 /Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py --in audio/voice_raw.wav --out <FINAL>.mp4 --video <picture> ; then audio_gate.py on it")
