"""RO-37 round 2 context clips: every graphic, clip and AI slot playing in the new layout with about 3 s of narration either
side, cut from the rendered first minute or the rendered context ranges (context_ranges.json, rendered by chain2.sh), plus
a still at its most telling moment. Writes review/context/<ID>-context - REVIEW 540p.mp4, <ID>.jpg and items.json."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
C = f"{r2.W2}/review/context"; os.makedirs(C, exist_ok=True)
FM = f"{r2.W2}/review/first-minute/DRAFT - First Time At The Gym R2 - first minute.mp4"; FM_END = 61.0944
RANGES = json.load(open(f"{r2.W2}/context_ranges.json"))
END = r2.END_F / r2.FPS


def source(a, b):
    if b <= FM_END + 1e-3: return FM, 0.0
    for n, (x, y) in enumerate(RANGES):
        if x - 1e-3 <= a and b <= y + 1e-3: return f"{r2.W2}/ctx/range{n:02d}.mp4", x
    raise ValueError(f"no render covers {a:.2f}-{b:.2f}")


out = []
for it in r2.R:
    t0, t1 = it["t0"], it["t1"] or it["t0"] + 3
    a, b = max(0.0, t0 - 3), min(END, t1 + 3)
    if a < FM_END < b and t1 <= FM_END: b = FM_END
    src, base = source(a, b)
    clip = f"{C}/{it['id']}-context - REVIEW 540p.mp4"
    subprocess.run([r2.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{a - base:.3f}", "-t", f"{b - a:.3f}", "-i", src, "-vf", "scale=960:540",
                    "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", clip], check=True)
    ts = t0 + (t1 - t0) * (0.7 if it["kind"] in ("lt", "l3") else 0.5)
    subprocess.run([r2.FF, "-nostdin", "-v", "error", "-y", "-ss", f"{ts - base:.3f}", "-i", src, "-frames:v", "1", "-vf", "scale=960:540",
                    "-q:v", "3", f"{C}/{it['id']}.jpg"], check=True)
    out.append(dict(it, ctx=dict(clip=os.path.basename(clip), a=round(a, 2), b=round(b, 2), still=f"{it['id']}.jpg")))
json.dump(out, open(f"{C}/items.json", "w"), indent=1)
print(len(out), "context clips")
