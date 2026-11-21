import json, subprocess, sys
import ra01lib as L
from ra01lib import Aspect
A = Aspect("1x1"); B = json.load(open("beats.json")); CUT = json.load(open("cut.json"))
GR = L.grade()
def src_at(t):
    for p in CUT["pieces"]:
        if p["t_in"] - 1e-6 <= t < p["t_out"] + 1e-6: return p["src_in"] + (t - p["t_in"])
    raise SystemExit(t)
def probe(t, out):
    seg = next(p for p in B["punch"] if p["beat"][0] - 1e-6 <= t < p["beat"][1] + 1e-6)
    cw, ch = A.levels[seg["level"]]
    cy = int(round(seg["hair_min"] - 0.04*ch)); cy = max(0, min(3840-ch, cy - cy % 2))
    cx = int(round(seg["cx_sq"] - cw/2)); cx = max(0, min(2160-cw, cx - cx % 2))
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", f"{src_at(t):.3f}", "-i", L.ROLL, "-frames:v", "1",
                    "-vf", f"crop={cw}:{ch}:{cx}:{cy},{L.DECODE},{GR},scale=1080:1080:flags=lanczos", "-y", out], check=True)
    return seg
if __name__ == "__main__":
    import os; os.makedirs("probe", exist_ok=True)
    for t in [float(x) for x in sys.argv[1:]]:
        s = probe(t, f"probe/p_{t:.2f}.png"); print(t, s["level"])
