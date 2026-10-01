#!/usr/bin/env python3
"""VALIDATE AN EDIT SHEET (README.md here). Exit 0 = complete; exit 1 names every missing or wrong field.

  python3 validate.py SHEET.json [--hash] [--json OUT.json]

Run at 16:9 DELIVERY (a failing sheet blocks the delivery gate stamp), and again by any reader before it builds.
--hash also re-hashes the master and checks that every path in the sheet exists.
"""
import argparse
import hashlib
import json
import os
import sys

SCHEMA = "abs-edit-sheet/1"
FPS = 30000 / 1001
TOP = {"schema", "job", "title", "type", "editor", "video", "grade", "edl", "framing", "words", "graphics", "pictures",
       "audio", "approvals", "provenance"}
TYPES = {"LFC", "SFC", "AD"}
LABELS = {"ai", "real", "none"}
PEOPLE = {"dan", "other", "none"}
LAYERS = {"overlay", "side", "full"}
HF_TEMPLATES = {"lower-third", "before-card", "side-list", "cycle", "title-card", "cta", "media-card"}


def strings(o):
    """Every string inside a nested config."""
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from strings(v)


def check(S, do_hash=False):
    E = []
    err = E.append

    def need(d, keys, where):
        ok = True
        if not isinstance(d, dict):
            err(f"{where}: missing or not an object"); return False
        for k in keys:
            if k not in d or d[k] is None or d[k] == "" or d[k] == []:
                err(f"{where}.{k}: missing"); ok = False
        return ok

    if S.get("schema") != SCHEMA:
        err(f"schema: expected {SCHEMA!r}, got {S.get('schema')!r}")
    for k in sorted(set(S) - TOP):
        err(f"{k}: unknown top-level key (a typo does not pass as an optional field)")
    need(S, ["job", "title", "type", "editor"], "sheet")
    if S.get("type") not in TYPES:
        err(f"type: {S.get('type')!r} is not one of {sorted(TYPES)}")

    # ---- video
    V = S.get("video") or {}
    paths = []
    if need(V, ["master", "sha256", "fps", "frames", "duration", "width", "height", "rolls"], "video"):
        paths.append(("video.master", V["master"]))
        if abs(V["frames"] / FPS - V["duration"]) > 0.05:
            err(f"video: {V['frames']} frames is {V['frames'] / FPS:.3f} s, duration says {V['duration']}")
        for name, r in V["rolls"].items():
            if need(r, ["path", "width", "height"], f"video.rolls.{name}"):
                paths.append((f"video.rolls.{name}.path", r["path"]))
    rolls = V.get("rolls") or {}
    nframes = V.get("frames") or 0
    dur = V.get("duration") or 0.0

    # ---- grade
    G = S.get("grade") or {}
    if G.get("order") not in ("after_scale_1080", "at_source_size"):
        err(f"grade.order: {G.get('order')!r} is not after_scale_1080 / at_source_size")
    if need(G, ["filter", "decode"], "grade") and G.get("lut"):
        paths.append(("grade.lut", G["lut"]))

    # ---- edl
    edl = S.get("edl") or []
    if not edl:
        err("edl: missing")
    prev = 0
    for i, s in enumerate(edl):
        w = f"edl[{i}]"
        if not need(s, ["roll", "src_in", "src_out", "out_in", "out_out", "out_f0", "out_f1", "audio", "join"], w) and \
                not all(k in s for k in ("out_f0", "out_f1")):
            continue
        if s.get("roll") not in rolls:
            err(f"{w}.roll: {s.get('roll')!r} is not in video.rolls")
        if s["out_f0"] != prev:
            err(f"{w}: starts on frame {s['out_f0']}, the previous segment ended on {prev} (gap or overlap)")
        if s["out_f1"] <= s["out_f0"]:
            err(f"{w}: no frames")
        prev = s["out_f1"]
        if s.get("join") not in ("cut", "reframe", "first"):
            err(f"{w}.join: {s.get('join')!r} is not cut / reframe / first")
        if s.get("audio") != "sync" and not (isinstance(s.get("audio"), dict) and "src_in" in s["audio"]):
            err(f"{w}.audio: 'sync' or {{src_in, src_out}}")
    if edl and nframes and prev != nframes:
        err(f"edl: ends on frame {prev}, the master has {nframes}")

    # ---- framing
    fr = S.get("framing") or []
    if len(fr) != len(edl):
        err(f"framing: {len(fr)} rows for {len(edl)} edl segments (one per segment)")
    for i, f in enumerate(fr):
        w = f"framing[{i}]"
        if not need(f, ["name", "crop", "head", "measured"], w):
            continue
        roll = rolls.get(edl[i]["roll"]) if i < len(edl) else None
        cw, ch, cx, cy = f["crop"]
        if roll and (cx < 0 or cy < 0 or cx + cw > roll["width"] or cy + ch > roll["height"]):
            err(f"{w}.crop: {f['crop']} is outside the {roll['width']}x{roll['height']} roll")
        h = f["head"]
        if need(h, ["hair_top", "cx", "chin"], w + ".head"):
            if not h["hair_top"] < h["chin"]:
                err(f"{w}.head: hair_top {h['hair_top']} is not above chin {h['chin']}")
            if roll and not (0 <= h["cx"] <= roll["width"]):
                err(f"{w}.head.cx: {h['cx']} is outside the roll")

    # ---- words
    W = S.get("words") or {}
    if need(W, ["list", "timing"], "words"):
        last = -1.0
        for i, x in enumerate(W["list"]):
            if not all(k in x for k in ("w", "t0", "t1")):
                err(f"words.list[{i}]: needs w, t0, t1"); break
            if x["t0"] < last - 0.35 or x["t1"] < x["t0"] or x["t0"] < -0.01 or (dur and x["t1"] > dur + 0.5):
                err(f"words.list[{i}] {x['w']!r}: time {x['t0']}-{x['t1']} out of order or outside the film"); break
            last = x["t0"]
        if "fixes" not in W:
            err("words.fixes: missing (an empty list if no caption fix was applied)")

    # ---- graphics
    seen = set()
    for i, g in enumerate(S.get("graphics") or []):
        w = f"graphics[{i}] {g.get('id', '?')}"
        if not need(g, ["id", "template", "config", "t1", "layer"], w) or "t0" not in g:
            continue
        if not isinstance(g.get("text"), list):
            err(f"{w}.text: missing (an empty list if the graphic shows no words)"); continue
        if g["id"] in seen:
            err(f"{w}: duplicate id")
        seen.add(g["id"])
        t = g["template"]
        if not (t in HF_TEMPLATES or t.startswith("softblue:") or t.startswith("adkit:") or t.startswith("codex:")):
            err(f"{w}.template: {t!r} is not a hyperframes template, softblue:<fn>, adkit:<fn> or codex:<name>")
        if not g["t0"] < g["t1"]:
            err(f"{w}: t0 {g['t0']} is not before t1 {g['t1']}")
        if g["layer"] not in LAYERS:
            err(f"{w}.layer: {g['layer']!r} is not one of {sorted(LAYERS)}")
        cfg_text = " ".join(strings(g["config"]))
        for s in g["text"]:
            if s not in cfg_text:
                err(f"{w}.text: {s!r} is not in its config (text is copied, never retyped)")
        if "driven_by" not in g:
            err(f"{w}.driven_by: missing (an empty list if nothing lands on a word)")
    if "graphics" not in S:
        err("graphics: missing (an empty list if the film has none)")

    # ---- pictures
    for i, p in enumerate(S.get("pictures") or []):
        w = f"pictures[{i}] {p.get('id', '?')}"
        if not need(p, ["id", "t0", "t1", "kind", "sources", "label_kind", "people", "label_source"], w):
            continue
        if p["label_kind"] not in LABELS:
            err(f"{w}.label_kind: {p['label_kind']!r} is not one of {sorted(LABELS)}")
        if p["people"] not in PEOPLE:
            err(f"{w}.people: {p['people']!r} is not one of {sorted(PEOPLE)}")
        if "physique" not in p:
            err(f"{w}.physique: missing (true / false)")
        if p.get("people") == "dan" and p.get("physique") and p["label_kind"] == "none":
            err(f"{w}: a physique picture of Dan carries exactly one label (ai or real), not none")
        if p["label_kind"] != "none" and not p.get("label"):
            err(f"{w}.label: the chip text is missing")
        if "approved_crop" not in p:
            err(f"{w}.approved_crop: missing (null if Dan approved no crop)")
        for k, s in enumerate(p["sources"]):
            if need(s, ["path"], f"{w}.sources[{k}]"):
                paths.append((f"{w}.sources[{k}].path", s["path"]))
    if "pictures" not in S:
        err("pictures: missing (an empty list if the film has none)")

    # ---- audio, approvals, provenance
    A = S.get("audio") or {}
    if need(A, ["mix", "untreated"], "audio"):
        paths += [("audio.mix", A["mix"]), ("audio.untreated", A["untreated"])]
    P = S.get("approvals") or {}
    if need(P, ["status"], "approvals"):
        if P["status"] not in ("approved", "pending"):
            err(f"approvals.status: {P['status']!r} is not approved / pending")
        if "decisions" not in P:
            err("approvals.decisions: missing (an empty list if Dan made none)")
    need(S.get("provenance") or {}, ["written", "by", "build_dir"], "provenance")

    if do_hash:
        for where, p in paths:
            if not os.path.exists(p):
                err(f"{where}: file not found: {p}")
        m = V.get("master")
        if m and os.path.exists(m):
            h = hashlib.sha256()
            with open(m, "rb") as f:
                for b in iter(lambda: f.read(1 << 22), b""):
                    h.update(b)
            if h.hexdigest() != V.get("sha256"):
                err(f"video.sha256: the master on disk hashes to {h.hexdigest()}, the sheet says {V.get('sha256')}")
    return E


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet")
    ap.add_argument("--hash", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    S = json.load(open(a.sheet))
    E = check(S, a.hash)
    if a.json:
        json.dump(dict(sheet=os.path.abspath(a.sheet), ok=not E, errors=E), open(a.json, "w"), indent=1)
    if E:
        print(f"EDIT SHEET INCOMPLETE: {len(E)} problem(s) in {a.sheet}")
        for e in E:
            print("  -", e)
        return 1
    print(f"edit sheet OK: {S['job']} {S['title']!r}: {len(S['edl'])} segments, {len(S['words']['list'])} words, "
          f"{len(S['graphics'])} graphics, {len(S['pictures'])} pictures, approvals {S['approvals']['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
