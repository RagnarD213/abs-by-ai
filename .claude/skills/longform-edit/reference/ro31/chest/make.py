"""D01 / D02 from the resolved plan: diagram configs on word starts, HyperFrames render, mp4 for the clip slot (0.4 s longer than the slot)."""
import json, subprocess, sys, re
W = "/Volumes/Expansion/_edit_work/RO-31/round1"; FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
R = {r["id"]: r for r in json.load(open(f"{W}/plan_resolved.json"))}
WO = [w for w in json.load(open(f"{W}/words_out.json")) if w["t0"] is not None]
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
def at(phrase, a):
    p = [norm(x) for x in phrase.split()]
    for i in range(len(WO)):
        if WO[i]["t0"] >= a - .05 and [norm(w["w"]) for w in WO[i:i+len(p)]] == p: return WO[i]["t0"]
    raise SystemExit(f"no {phrase!r}")
d1, d2 = R["D01"], R["D02"]
FAT = dict(kind="fat", head="Chest Fat", sub="Soft And Spread Across The Chest", labels=[dict(s="Fat", x=510, y=470), dict(s="Muscle", x=140, y=440, d=.2)])
GL = dict(kind="gland", head="True Gynecomastia", sub="Firm Disc Of Gland Under The Nipple", labels=[dict(s="Gland Tissue", x=450, y=440), dict(s="Muscle", x=140, y=440, d=.2)])
cfg = [dict(id="D01", a=d1["t0"], b=d1["t1"] + .4, eyebrow="TWO KINDS OF MAN BOOBS",
            panels=[dict(FAT, t=at("The first kind", d1["t0"])), dict(GL, t=at("The second kind", d1["t0"]))]),
       dict(id="D02", a=d2["t0"], b=d2["t1"] + .4, eyebrow="HOW TO TELL WHICH ONE YOU HAVE",
            panels=[dict(FAT, t=d2["t0"], calls=[dict(s="Soft And Spread Out = Fat", x=44, y=772, t=at("soft and spread", d2["t0"]))]),
                    dict(GL, t=d2["t0"], calls=[dict(s="Firm Disc = Gland", x=44, y=772, t=at("firm disc", d2["t0"]))])])]
json.dump(cfg, open(f"{W}/hf_extra/chest.json", "w"), indent=1)
subprocess.run(["python3", f"{W}/recipe/chest/build.py", f"{W}/hf_extra/chest.json", f"{W}/hf_extra", "--render"], check=True)
for k in ("D01", "D02"):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{W}/hf_extra/{k}.mov", "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", f"{W}/hf_extra/{k}.mp4"], check=True)
print("chest diagrams ok")
