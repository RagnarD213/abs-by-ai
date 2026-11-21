"""DS-40 R6 graphics: the four HyperFrames scenes at 1080x1920 and their manifest for the compositor.

    python3 build.py [--render] [--snap] [--only G1,G3]

G1 name lower third (lower-third template, placed right of the small Dan, under Maher's face), G2 key point (lower-third,
the shorts key-point position 68,1130..1012), G3 BMI table (new bmi-table template, full screen), G4 subscribe (cta).
"""
import json, pathlib, sys
WT = pathlib.Path("/Users/danielrose/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude/Projects/Abs By AI/"
                  ".claude/worktrees/stoic-cartwright-8bfcc9/.claude/skills/_shared/hyperframes")
sys.path.insert(0, str(WT))
import vertical as V            # noqa: E402
sys.path.insert(0, str(WT / "bmi-table"))
import importlib.util
spec = importlib.util.spec_from_file_location("bmi_build", WT / "bmi-table" / "build.py"); BM = importlib.util.module_from_spec(spec); spec.loader.exec_module(BM)

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "hf"
U = 2.0
G1_X0, G1_X1, G1_TOP = 452, 1000, 1318     # right of the small Dan (x < 432), under Maher's face (bottom <= 1014), above the
                                           # platform's lower caption area; captions sit above it (top 1040) during the clip
KP_TOP = 1130                              # shorts key-point bar position (GRAPHICS-STANDARDS, Soft Blue shorts standard)


def g1_scenes(c):
    scenes, meta = V.lt_scenes(dict(c, top_y=G1_TOP))
    dx = G1_X0 - scenes[0][1]["strip"][0]
    cfg = scenes[0][1]                     # the content and mask configs share these nested objects: shift them once
    cfg["strip"][0] = G1_X0; cfg["strip"][2] = G1_X1 - G1_X0
    cfg["accent"][0] += dx; cfg["topic"]["x"] += dx
    for p in cfg["parts"]: p["x"] += dx
    assert all(sc[1]["strip"][0] == G1_X0 for sc in scenes)
    meta["box"][0], meta["box"][2] = G1_X0, G1_X1
    return scenes, meta


def scenes_for(g):
    c = g["config"]
    if g["id"] == "G1": return g1_scenes(c)
    if g["template"] == "lower-third": return V.lt_scenes(dict(c, top_y=KP_TOP))
    if g["template"] == "cta": return V.cta_scenes(g["id"], g["t1"] - g["t0"], c["top"], c["big"], hold_out=c.get("hold_out", False), top_y=KP_TOP)
    if g["template"] == "bmi-table":
        cfg = BM.layout(dict(c, canvas=[1080, 1920]))
        return [(BM.TPL, cfg, ())], dict(kind="opaque")
    raise SystemExit(g["id"])


if __name__ == "__main__":
    plan = json.load(open(HERE.parent / "plan.json"))
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    man = []
    for g in plan["graphics"]:
        scenes, meta = scenes_for(g)
        dur = scenes[0][1]["dur"]
        m = dict(id=g["id"], template=g["template"], a=g["t0"], b=g["t1"], canvas=[1080, 1920], mov=str(OUT / "renders" / f"{g['id']}.mov"), **meta)
        if meta["kind"] == "glass": m["mask"] = str(OUT / "renders" / f"{g['id']}_mask.mov")
        man.append(m)
        if only and g["id"] not in only: continue
        snap = None
        if "--snap" in sys.argv: snap = round(dur - 0.6, 2) if g["id"] != "G3" else round(dur - 0.6, 2)
        V.build(scenes, OUT, render="--render" in sys.argv, snap=snap)
        print(g["id"], meta["kind"], round(g["t0"], 3), round(g["t1"], 3), flush=True)
    (OUT).mkdir(exist_ok=True)
    json.dump(man, open(OUT / "manifest.json", "w"), indent=1)
