"""RO-07 round 3 full film: build.render_range(0, total) with the quiet music bed (bed.py, Pixabay acoustic_bg, the RO-06 bed).
Bed level -30 dB (the chain's ceiling): measured on the first minute against the audio gate's floor row before this render
(voice-over-floor against the reference: -24 dB -2.1/-1.6/+1.7, -30 dB +1.1/+1.2/+4.2, -36 dB +3.6/+4.0/+5.4; limit -3.0).
Pre-flights every clip against its slot first (RO-06: one short clip killed a full render at minute 11). usage: render_r3.py"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W = "/Volumes/Extreme/_edit_work/ro07"; OUT = f"{W}/round3/RO-07 round 3 - full film.mp4"
os.environ["RO07_BED"] = f"{W}/round3/bed/bed.wav"; os.environ["RO07_BED_DB"] = "-30"
import build as Bd, gfx as G
total = Bd.S[-1]["out_f1"]/Bd.FPS
assert Bd.fr(total) == Bd.S[-1]["out_f1"], (Bd.fr(total), Bd.S[-1]["out_f1"])
assert not Bd.jumps(), Bd.jumps()
assert not [i["id"] for i in Bd.R if i.get("pending") or i.get("frames")], "a placeholder is still in the plan"
for it in Bd.R:
    if it["kind"] != "clip": continue
    n = Bd.fr(it["t1"]) - Bd.fr(it["t0"]); s = it["src"]; per = n // len(s)
    for k, sp in enumerate(s):
        m = per if k < len(s)-1 else n - per*(len(s)-1)
        dur = float(subprocess.run([Bd.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", G.src_path(sp)], capture_output=True, text=True).stdout)
        assert dur - G.src_start(sp) >= m/Bd.FPS - 0.02, f"{it['id']}: {sp} too short for its slot"
print("rendering", Bd.S[-1]["out_f1"], "frames", round(total, 3), "s", flush=True)
Bd.render_range(0, total, OUT)
print("RENDER COMPLETE", flush=True)
