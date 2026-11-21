"""Presentation options, moving: the same 9 s (film 0:39.8-0:47.4, 'Most guys walking into a gym for the first time...')
three ways: (a) the portrait panel on the moving Soft Blue field, (b) the panel on its own blurred, darkened, navy-tinted pool
picture (the locked green-screen 'soft' look), (c) only the full-frame close-up. With voice A. Plus a still of each."""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B, frames as F
W = B.W; O = f"{W}/options/presentation"; os.makedirs(O, exist_ok=True); FF = B.FF
S = json.load(open(f"{W}/shots.json"))
sh = next(s for s in S if s["framing"] == "W" and s["out_f1"] - s["out_f0"] >= B.fr(7.4) and s["out_f0"] > B.fr(20))
f0 = sh["out_f0"] + 3; f1 = f0 + B.fr(7.0); T0, T1 = f0 / B.FPS, f1 / B.FPS
print("window", round(T0, 2), round(T1, 2), sh["id"])
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(T0), "-t", str(T1 - T0), "-i", f"{W}/voice_A_full.wav" if os.path.exists(f"{W}/voice_A_full.wav") else f"{W}/review/first-minute/voice_A.wav", "-c:a", "aac", "-b:a", "160k", f"{O}/_a.m4a"], check=True)
for key, fm, bg in (("a", "W", "field"), ("b", "W", "soft"), ("c", "T", None)):
    s = dict(sh, framing=fm); tmp = f"{O}/_{key}.mp4"
    B.render_presenter(s, f0, f1, "center", tmp, bg=bg or "field")
    out = f"{O}/presentation-{key}.mp4"
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", tmp, "-i", f"{O}/_a.m4a", "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", out], check=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "22", "-c:a", "copy", "-movflags", "+faststart", out[:-4] + " - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", "3", "-i", out, "-frames:v", "1", "-q:v", "2", f"{O}/presentation-{key}.jpg"], check=True)
    print("built", key, flush=True)
# colour options moving (same window, the panel on the field so skin and the pool both show)
C = f"{W}/options/colour"
for k, (name, g) in F.GRADES.items():
    F.GRADE = g; tmp = f"{C}/_{k}.mp4"; s = dict(sh, framing="W")
    B.render_presenter(s, f0, f1, "center", tmp)
    out = f"{C}/colour-{k}.mp4"
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", tmp, "-i", f"{O}/_a.m4a", "-c:v", "copy", "-c:a", "copy", "-shortest", "-movflags", "+faststart", out], check=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "22", "-c:a", "copy", "-movflags", "+faststart", out[:-4] + " - REVIEW 540p.mp4"], check=True)
    print("colour", k, flush=True)
