#!/usr/bin/env python3
"""Watch-pass and negative-imagery evidence for one delivered master.

  s13_watch.py sheets 9x16 <master>     build the strips a human must LOOK at
  s13_watch.py log    9x16 <master> <reviewed> <notes.json>   record the pass

The sheets are CONSECUTIVE frames across every boundary (card in, card out, punch change, splice)
— the thing the metric gate cannot see. Nothing here writes `inspected: true` on its own; the log
subcommand is run only after the strips have actually been looked at, and it records how many
boundaries were reviewed.
"""
import hashlib, json, os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from PIL import Image

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

MODE, KEY, MASTER = sys.argv[1], sys.argv[2], sys.argv[3]
TL = json.load(open(f"timeline_{KEY}.json")); CUT = json.load(open("cut.json"))
FD = L.FD
acc, joins = 0.0, []
for a, b in CUT["keeps"][:-1]:
    acc += b - a; joins.append(round(acc, 3))
bounds = []
for it in TL["items"]:
    bounds.append((it["f0"], f"{it['kind']}:{it['name']} in"))
bounds.append((TL["total_frames"]-1, "end"))
for t in joins:
    bounds.append((int(round(t*L.FPS)), f"splice {t:.2f}"))
for s in CUT["seams"]:
    bounds.append((int(round(s["t"]*L.FPS)), f"SEAM {s['what']}"))
bounds = sorted(set(bounds))

def grab(master, frames, outdir, width):
    """ONE decode for every frame we need. `select=eq(n,F)` re-decodes the file from the start for
    each frame, which turns 230 grabs into hours on a 57 s master."""
    os.makedirs(outdir, exist_ok=True)
    expr = "+".join(f"eq(n\\,{f})" for f in frames)
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", master,
                    "-vf", f"select='{expr}',scale={width}:-1", "-vsync", "0",
                    "-y", os.path.join(outdir, "g%04d.png")], check=True)
    got = sorted(f for f in os.listdir(outdir) if f.startswith("g") and f.endswith(".png"))
    if len(got) != len(frames):
        raise SystemExit(f"grabbed {len(got)} frames, wanted {len(frames)} -- the strip would be wrong")
    return {fr: os.path.join(outdir, nm) for fr, nm in zip(frames, got)}

if MODE == "sheets":
    out = f"watch_{KEY}"; os.makedirs(out, exist_ok=True)
    W = 300 if KEY == "9x16" else 420
    per = 6
    want = sorted({max(0, min(TL["total_frames"]-1, f0+d))
                   for f0, _ in bounds for d in (-2, -1, 0, 1, 2)})
    frames = grab(MASTER, want, f"{out}/raw", W)
    for gi in range(0, len(bounds), per):
        grp = bounds[gi:gi+per]
        rows = []
        for f0, label in grp:
            tiles = [Image.open(frames[max(0, min(TL["total_frames"]-1, f0+d))]).convert("RGB")
                     for d in (-2, -1, 0, 1, 2)]
            h = tiles[0].height
            row = Image.new("RGB", (W*5, h), (0, 0, 0))
            for i, t in enumerate(tiles): row.paste(t, (i*W, 0))
            rows.append((row, label, f0))
        sheet = Image.new("RGB", (W*5, sum(r[0].height for r in rows)), (0, 0, 0))
        y = 0
        for row, label, f0 in rows:
            sheet.paste(row, (0, y)); y += row.height
        sheet.save(f"{out}/sheet_{gi//per:02d}.jpg", quality=88)
        print(f"{out}/sheet_{gi//per:02d}.jpg  " + " | ".join(f"{l} @f{f}" for f, l in grp))
    json.dump([{"frame": f, "t": round(f*FD, 3), "what": l} for f, l in bounds],
              open(f"{out}/boundaries.json", "w"), indent=1)
    print(f"{len(bounds)} boundaries")

elif MODE == "neg":
    out = f"neg_{KEY}"; os.makedirs(out, exist_ok=True)
    n = 40
    W = 250 if KEY == "9x16" else 340
    want = sorted({int(i/(n-1) * (TL["total_frames"]-1)) for i in range(n)})
    frames = grab(MASTER, want, f"{out}/raw", W)
    tiles = [Image.open(frames[f]).convert("RGB") for f in want]
    cols = 8; rows = (len(tiles)+cols-1)//cols
    h = tiles[0].height
    sheet = Image.new("RGB", (W*cols, h*rows), (0, 0, 0))
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols)*W, (i//cols)*h))
    sheet.save(f"{out}/negative_sheet.jpg", quality=88)
    print(f"{out}/negative_sheet.jpg  ({len(tiles)} frames)")

elif MODE == "log":
    reviewed = int(sys.argv[4]); notes = json.load(open(sys.argv[5]))
    d = {"sha256": sha256(MASTER), "video": os.path.basename(MASTER), "inspected": True,
         "boundaries": len(bounds), "reviewed": reviewed,
         "method": "consecutive frames (-2..+2) at every card in/out, punch change, pause splice "
                   "and take seam, rendered as strips and looked at",
         "findings": notes.get("findings", []), "when": notes.get("when")}
    os.makedirs("logs", exist_ok=True)
    json.dump(d, open(f"logs/watch_pass_{KEY}.json", "w"), indent=1)
    print(f"logs/watch_pass_{KEY}.json  {reviewed}/{len(bounds)} boundaries, sha {d['sha256'][:12]}")
