#!/usr/bin/env python3
"""Blind Codex-vs-Google image comparison (Dan, 2026-10-30). Rule: _shared/IMAGE-GENERATION.md, "Blind Google test".

Dan never learns which model made which image until he asks "which did I choose most?".

  blind.py add SETDIR --source codex|google --file img.png [--note "refused: shirtless"]
      Register one candidate. Originals stay untouched under SETDIR/originals/.
  blind.py build SETDIR --kind start-frame|thumbnail|cover|background|other --video "<title (code)>" --shot "<name>"
      Shuffle everything registered, write neutral copies (same size, no metadata, neutral names X1..Xn) to
      SETDIR/blind/ for the review page, and a key SETDIR/.blind-key.json. Never show or print the key to Dan.
  blind.py pick SETDIR --chose X3[,X5] [--words "<his words>"]
      Log Dan's pick(s) to ~/.absbyai-image-picks.jsonl and print ONLY the neutral labels back.
  blind.py scorecard [--since YYYY-MM-DD] [--kind K]
      Run ONLY when Dan asks "which ones did I choose the most?". Shows wins by source and kind.
  blind.py reveal SETDIR --label X3
      Which file/source is X3 (needed to install the winner). Say the source to Dan only if he asks.

Selected finals are installed from originals/, never from the normalized blind copies.
"""
import argparse, hashlib, json, os, random, shutil, sys, time
from PIL import Image

PICKS = os.environ.get("ABS_IMAGE_PICKS") or os.path.expanduser("~/.absbyai-image-picks.jsonl")


def now(): return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def reg_path(d): return os.path.join(d, ".blind-registry.json")


def load(p, default):
    return json.load(open(p)) if os.path.exists(p) else default


def cmd_add(a):
    os.makedirs(os.path.join(a.setdir, "originals"), exist_ok=True)
    reg = load(reg_path(a.setdir), [])
    h = hashlib.sha256(open(a.file, "rb").read()).hexdigest()[:12]
    ext = os.path.splitext(a.file)[1].lower() or ".png"
    dest = os.path.join(a.setdir, "originals", f"{a.source}-{h}{ext}")
    shutil.copy2(a.file, dest)
    reg.append({"source": a.source, "file": dest, "sha": h, "note": a.note or ""})
    json.dump(reg, open(reg_path(a.setdir), "w"), indent=1)
    print(f"registered {a.source} {h} ({len(reg)} total)")


def cmd_build(a):
    reg = load(reg_path(a.setdir), [])
    imgs = [r for r in reg if os.path.exists(r["file"]) and not r.get("refused")]
    if len(imgs) < 2 or len({r["source"] for r in imgs}) < 2:
        raise SystemExit("need at least one codex and one google image")
    random.shuffle(imgs)
    out = os.path.join(a.setdir, "blind"); shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    ims = [Image.open(r["file"]).convert("RGB") for r in imgs]
    # Same pixel size for all, so size never gives the model away: the common aspect, longest side capped at 1672.
    w0, h0 = ims[0].size
    ratio = w0 / h0
    W = 1672 if ratio >= 1 else int(1672 * ratio); H = int(W / ratio)
    key = {}
    for i, (r, im) in enumerate(zip(imgs, ims), 1):
        label = f"X{i}"
        im.resize((W, H), Image.LANCZOS).save(os.path.join(out, f"{label}.jpg"), quality=93)  # no metadata carried over
        key[label] = {"source": r["source"], "original": r["file"], "sha": r["sha"], "note": r["note"]}
    json.dump({"video": a.video, "shot": a.shot, "kind": a.kind, "built": now(), "labels": key},
              open(os.path.join(a.setdir, ".blind-key.json"), "w"), indent=1)
    print(f"{len(imgs)} neutral copies in {out}: {', '.join(sorted(key, key=lambda k: int(k[1:])))} (key hidden)")


def cmd_pick(a):
    k = load(os.path.join(a.setdir, ".blind-key.json"), None)
    if not k: raise SystemExit("run build first")
    chose = [c.strip() for c in a.chose.split(",") if c.strip()]
    for c in chose:
        if c not in k["labels"]: raise SystemExit(f"unknown label {c}")
    srcs = [v["source"] for v in k["labels"].values()]
    e = {"when": now(), "video": k["video"], "shot": k["shot"], "kind": k["kind"],
         "offered": {s: srcs.count(s) for s in set(srcs)},
         "chose": [{"label": c, "source": k["labels"][c]["source"], "sha": k["labels"][c]["sha"]} for c in chose],
         "dan_words": a.words}
    with open(PICKS, "a") as f: f.write(json.dumps(e) + "\n")
    print(f"recorded pick {','.join(chose)} for {k['shot']} (sources not shown)")


def cmd_scorecard(a):
    rows = [json.loads(l) for l in open(PICKS)] if os.path.exists(PICKS) else []
    if a.since: rows = [r for r in rows if r["when"][:10] >= a.since]
    if a.kind: rows = [r for r in rows if r["kind"] == a.kind]
    tab = {}
    for r in rows:
        t = tab.setdefault(r["kind"], {})
        for s, n in r["offered"].items():
            t.setdefault(s, {"offered": 0, "picked": 0})["offered"] += n
        for c in r["chose"]:
            t[c["source"]]["picked"] += 1
    print(f"{len(rows)} picks ({PICKS})")
    for kind, t in sorted(tab.items()):
        print(f"  {kind}")
        for s, v in sorted(t.items(), key=lambda kv: -kv[1]["picked"]):
            print(f"    {s:8s} picked {v['picked']:3d} of {v['offered']:3d} offered ({100 * v['picked'] / max(v['offered'], 1):.0f}%)")


def cmd_reveal(a):
    k = load(os.path.join(a.setdir, ".blind-key.json"), None)
    v = k["labels"][a.label]
    print(json.dumps(v))


p = argparse.ArgumentParser(); S = p.add_subparsers(dest="c", required=True)
s = S.add_parser("add"); s.add_argument("setdir"); s.add_argument("--source", choices=["codex", "google"], required=True)
s.add_argument("--file", required=True); s.add_argument("--note")
s = S.add_parser("build"); s.add_argument("setdir"); s.add_argument("--kind", required=True); s.add_argument("--video", required=True); s.add_argument("--shot", required=True)
s = S.add_parser("pick"); s.add_argument("setdir"); s.add_argument("--chose", required=True); s.add_argument("--words", default="")
s = S.add_parser("scorecard"); s.add_argument("--since"); s.add_argument("--kind")
s = S.add_parser("reveal"); s.add_argument("setdir"); s.add_argument("--label", required=True)
a = p.parse_args()
{"add": cmd_add, "build": cmd_build, "pick": cmd_pick, "scorecard": cmd_scorecard, "reveal": cmd_reveal}[a.c](a)
