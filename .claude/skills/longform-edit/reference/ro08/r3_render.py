"""RO-08 round 3 full film (A4 and A3 out, the two-shot A5, one shot reframed): build.render_range(0, total) with the quiet music bed (bed/bed.wav from bed.py, Pixabay acoustic_bg, the bed of the
approved home-workout and work-out-every-day films). Bed level -30 dB (the chain's ceiling), the level approved on this set and lav.
Pre-flights every clip against its slot first (one short clip once killed a full render at minute 11). usage: r3_render.py"""
import os, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W = "/Volumes/Extreme/_edit_work/ro08"; OUT = os.environ.get("RO08_R3_OUT", f"{W}/round3/RO-08 round 3 - full film.mp4")       # RO08_R3_OUT: render beside a file an independent reviewer is still reading, move it in afterwards
os.environ["RO08_BED"] = f"{W}/bed/bed.wav"; os.environ["RO08_BED_DB"] = "-30"
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
        dur = Bd.probe_dur(G.src_path(sp))
        assert dur - G.src_start(sp) >= m/Bd.FPS - 0.02, f"{it['id']}: {sp} too short for its slot"
print("rendering", Bd.S[-1]["out_f1"], "frames", round(total, 3), "s", flush=True)
Bd.render_range(0, total, OUT)
print("RENDER COMPLETE", flush=True)
