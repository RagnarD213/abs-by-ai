"""One context clip per plan item (item -/+ 4 s, 960x540, with sound) and one still at its most telling moment, cut from the
internal full-length render. Writes review/context/<ID>-context - REVIEW 540p.mp4 and <ID>.jpg."""
import json, subprocess, os
W = "/Volumes/Expansion/_edit_work/RO-37/round1"; C = f"{W}/review/context"; FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
import sys
R = json.load(open(f"{W}/plan_resolved.json")); FULL = f"{W}/internal_full.mp4"
FM = f"{W}/review/first-minute/DRAFT - First Time At The Gym R1 - first minute.mp4"; FM_END = 61.09
ONLY = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else None
OLD = json.load(open(f"{C}/items.json")) if ONLY and os.path.exists(f"{C}/items.json") else []
END = json.load(open(f"{W}/shots.json"))[-1]["out_f1"] / (30000/1001)
for it in R:
    if ONLY and it['id'] not in ONLY:
        o = next((x for x in OLD if x['id'] == it['id']), None)
        if o and 'ctx' in o: it['ctx'] = o['ctx']
        continue
    t0, t1 = it["t0"], it["t1"] or it["t0"] + 3
    a, b = max(0, t0 - 4), min(END, t1 + 4)
    src = FM if b <= FM_END else FULL
    out = f"{C}/{it['id']}-context - REVIEW 540p.mp4"
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", src, "-vf", "scale=960:540",
                    "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
    ts = t0 + (t1 - t0) * (0.7 if it["kind"] in ("lt", "l3") else 0.5)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", f"{ts:.3f}", "-i", src, "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", f"{C}/{it['id']}.jpg"], check=True)
    it["ctx"] = dict(clip=os.path.basename(out), a=round(a, 2), b=round(b, 2), still=f"{it['id']}.jpg")
json.dump(R, open(f"{W}/review/context/items.json", "w"), indent=1)
print(len(R), "context clips")
