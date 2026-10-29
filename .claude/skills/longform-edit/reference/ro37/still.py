"""still.py ROLL T FRAMING BG PX OUT [GRADE] : one graded 1920x1080 frame (field bg = a softblue.field frame at t)."""
import sys, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import frames as F
roll, t, fm, bg, px, out = sys.argv[1:7]; g = F.GRADES[sys.argv[7]][1] if len(sys.argv) > 7 else None
t = float(t); cmd = [F.FF, "-nostdin", "-v", "error", "-y", "-ss", str(t), "-i", F.ROLLS[roll], "-loop", "1", "-framerate", "30000/1001", "-i", F.ensure_mask()]
if fm == "W" and bg == "field":
    sys.path.insert(0, f"{F.P}/.claude/skills/_shared"); import softblue as SB
    fp = f"/tmp/absbyai-scratch/RO-37/field_{t:.2f}.png"; os.makedirs(os.path.dirname(fp), exist_ok=True); SB.field(t, 1920, 1080).save(fp)
    cmd += ["-loop", "1", "-framerate", "30000/1001", "-i", fp]
cmd += ["-filter_complex", F.graph(fm, roll, t - 3, t + 3, bg, px, g), "-map", "[v]", "-frames:v", "4", "-update", "1", "-q:v", "2", out]
subprocess.run(cmd, check=True)
