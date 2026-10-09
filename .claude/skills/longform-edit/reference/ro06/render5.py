"""Round 5 full film: build.render_range(0, total) with the music bed. usage: render5.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["RO06_BED"] = "/Volumes/Extreme/_edit_work/ro06/round5/bed/bed.wav"; os.environ["RO06_BED_DB"] = "-15"   # third render: at -20 the bed sat level with the outdoor noise on his mic (review); -15 lifts the pauses 3 to 4 dB and still passes the floor row
import build as Bd
total = Bd.S[-1]["out_f1"]/Bd.FPS
assert Bd.fr(total) == Bd.S[-1]["out_f1"], (Bd.fr(total), Bd.S[-1]["out_f1"])
assert not Bd.jumps(), Bd.jumps()
print("rendering", Bd.S[-1]["out_f1"], "frames", round(total, 3), "s", flush=True)
Bd.render_range(0, total, "/Volumes/Extreme/_edit_work/ro06/round5/RO-06 round 5 - full film.mp4")
print("RENDER COMPLETE", flush=True)
