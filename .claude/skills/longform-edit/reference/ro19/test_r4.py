"""RO-19 round 4: test renders of the two changed stretches before the full render (README, round 3: 2 minutes, not 90). usage: test_r4.py pic | listen"""
import sys, os
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro19/recipe"); W = "/Volumes/Extreme/_edit_work/ro19"; what = sys.argv[1]; sys.argv = ["x", "x"]
os.environ["RO07_BED"] = f"{W}/round3/bed/bed.wav"; os.environ["RO07_BED_DB"] = "-30"
import build as Bd
if what == "pic":
    Bd.render_range(40.0, 70.0, f"{W}/round4/test/p02_40-70.mp4", audio=False); Bd.render_range(530.0, 560.0, f"{W}/round4/test/cut_530-560.mp4", audio=False)
if what == "listen": Bd.render_range(536.0, 556.0, f"{W}/round4/test/listen_536-556.mp4")
print("TEST DONE", what, flush=True)
