#!/usr/bin/env python3
"""AN EDITOR'S MASTER, REDRAWN IN SOFT BLUE LIGHT: the recovered content of the master path (auto_content.py's
content.json, olive dialect) -> the sheet path's Soft Blue Light dialect, so `sbl_graphics.py` and `render_sbl.py`
draw every graphic with the HyperFrames templates (Dan, 2026-10-01: no more olive graphics, in any vertical).

  python3 master_to_sbl.py --build B [--copy sbl_copy.json]

Run after `content`, before `setup`. Keeps the first content as B/content_auto.json and rewrites B/content.json:

  his graphic (recovered)                 Soft Blue Light, 9:16
  lower third (olive tab + black bar)  -> lower-third/ (Motivation): topic + the point, each part rising on its word
  window (text left, Dan right)        -> side-list/ (the 3A card at the bottom, Dan full frame above; items on words)
  title / statement card               -> title-card/ (eyebrow + headline on the field)
  phone or clip beside Dan (winmedia)  -> media-card/ (the whole phone in a card)
  card / bleed                         -> unchanged (media-card/ plates; full-bleed pictures with the measured chip)
  CTA pill                             -> cta/ (glass button)
  running total chip (corner)          -> tally/ (only from the copy file: the recovery does not read corner chips)
  his white flash                      -> kept, in Soft Blue white (render_sbl.py), where the kit schedules it

Also writes B/sbl_sheet.json ({"graphics": [...]}, the part of an edit sheet sbl_graphics.py reads) and
B/sbl_report.json (every graphic: his words, ours, and where each part lands).

THE COPY FILE (editorial, written by the session, reviewed by Dan on the graphic-lock page; never typed into
content.json). Items are addressed by kind and order in the film:
  {"lower_thirds": {"0": {"topic": "THE MATH", "parts": [["I Fired My Trainer", "fired"], ["Saved $1,000 A Month", "saved"]]},
                    "3": {"merge_next": true, ...}, "5": {"drop": "why"}},
   "windows":      {"0": {"heading": "In This Video", "items": ["...", "..."], "reveal": ["why do", "why can"]}},
   "titles":       {"0": {"eyebrow": "PERSONAL TRAINER", "headline": "$400\\nA Month"}},
   "tallies":      [{"from": "phrase", "to": "phrase" | seconds, "value": 400, "frm": 0, "label": "So far"}],
   "pictures":     {"auto_02356": [{"media": "one_clip", "kind": "card", "until": 81.081}], "auto_02382": "drop"},
   "add_pictures": [{"t0": 0.0, "t1": 3.7, "media": "opener", "kind": "bleed", "label_kind": "ai"}]}
`pictures` swaps a recovered picture for a run of pictures (each `dur` s, the last to the beat's end, or to `until`
when it also covers the next beats, which are then "drop"). `add_pictures` adds a picture he does not have.
   "extra_beats":  [{"from": seconds | "phrase", "to": seconds | "phrase", "kind": "bleed" | "card", "media": "key", "label_kind": "real"}],
   "extra_lower_thirds": [{"from": ..., "to": ..., "topic": "...", "parts": [["...", "phrase"]]}]}
A lower third entry may instead carry "fact": {"photo": path, "eyebrow": ["BEFORE", "phrase"], "headline": [["AGE 38", "38"]],
"detail": ["...", "phrase"], "label": "..."}: his corner picture with a tag (Ad 6's "Age: 38" inset) becomes the full-screen
before-card/ (photo + glass fact card). extra_beats adds a picture his master shows that the recovery did not list (two
small photo panels beside Dan); extra_lower_thirds adds a lower third where a replaced lift carried his burned text.
A part's or item's second field is the PHRASE Dan says when it lands (first match inside the graphic's own time
range); without one, parts are spaced evenly. Without a copy entry: topic "KEY POINT", his own words.
"""
import argparse
import json
import os
import re
import shutil
import sys

FPS = 30000 / 1001
_n = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--copy")
    a = ap.parse_args()
    B = os.path.abspath(a.build)
    auto = os.path.join(B, "content_auto.json")
    if not os.path.exists(auto):
        shutil.copy(os.path.join(B, "content.json"), auto)
    C = json.load(open(auto))
    X = json.load(open(a.copy)) if a.copy else {}
    wj = json.load(open(os.path.join(B, C.get("words", "m.whisper.json"))))
    W = [(_n(w["word"]), float(w["start"]), float(w["end"])) for s in wj["segments"] for w in s.get("words", []) if _n(w["word"])]
    dur = float(C["dur"])

    def at(phrase, t0, t1, what):
        """Start of the first place Dan says `phrase` in [t0 - 0.6, t1]."""
        if isinstance(phrase, (int, float)):
            return float(phrase)
        toks = [_n(t) for t in phrase.split() if _n(t)]
        for i in range(len(W)):
            if W[i][1] < t0 - 0.6 or W[i][1] > t1:
                continue
            if [w[0] for w in W[i:i + len(toks)]] == toks:
                return W[i][1]
        raise SystemExit(f"{what}: Dan does not say {phrase!r} between {t0:.2f} and {t1:.2f}")

    def find(phrase, after=0.0):
        toks = [_n(t) for t in phrase.split() if _n(t)]
        for i in range(len(W)):
            if W[i][1] >= after and [w[0] for w in W[i:i + len(toks)]] == toks:
                return W[i][1], W[i + len(toks) - 1][2]
        raise SystemExit(f"Dan does not say {phrase!r} after {after:.2f}")

    say = lambda x, y: " ".join(w for w, s, _ in W if x <= s < y)
    G, report = [], []
    beats, lts, insets = [], [], []
    nw = nt = 0
    src_beats = []
    for b in sorted(C["beats"], key=lambda b: b["t0"]):
        seq = (X.get("pictures") or {}).get(b.get("media"))
        if seq == "drop":                                          # merged into a neighbour's run (its "until")
            continue
        if seq == "drop":                                      # a sliver of his transition lifted as a picture: the talk runs on
            continue
        if not seq:
            src_beats.append(b); continue
        # the copy file replaces one recovered picture by a run of pictures (a clean library original for his lift,
        # his one lift split where he cut): each takes `dur` seconds, the last takes what is left
        t = float(b["t0"])
        for q, r in enumerate(seq):
            t1 = float(r.get("until", b["t1"])) if q == len(seq) - 1 else round(t + float(r["dur"]), 4)
            nb = dict(t0=round(t, 4), t1=t1, kind=r.get("kind", "card"), media=r["media"])
            if q == len(seq) - 1:                                  # his flash on the return belongs to the last of the run
                nb.update({kk: b[kk] for kk in ("flash_after", "his_flash") if kk in b})
                if nb["kind"] == "bleed" and b.get("his_flash"):
                    nb["flash_after"] = True                      # his flash on this return stays when his card becomes a full-screen picture
            for kk in ("label_kind", "caps", "phone", "label_spans", "flash_after"):   # flash_after: a full-bleed swap keeps his flash
                if kk in r:
                    nb[kk] = r[kk]
            src_beats.append(nb); t = t1
    # pictures the editor's master does not have (a new opener over his talking head): explicit times, his audio untouched
    for r in X.get("add_pictures") or []:
        src_beats.append({kk: r[kk] for kk in ("t0", "t1", "kind", "media", "label_kind", "caps", "phone", "his_flash", "flash_after") if kk in r})
    src_beats.sort(key=lambda b: b["t0"])
    for y in X.get("extra_beats") or []:
        t0 = find(y["from"])[0] if isinstance(y["from"], str) else float(y["from"])
        t1 = find(y["to"], t0)[0] if isinstance(y["to"], str) else float(y["to"])
        src_beats.append(dict({kk: v for kk, v in y.items() if kk not in ("from", "to")}, t0=round(t0, 4), t1=round(t1, 4)))
    src_beats.sort(key=lambda b: b["t0"])
    for b in src_beats:
        k = b["kind"]
        if k == "window":
            x = (X.get("windows") or {}).get(str(nw), {})
            gid = f"W{nw + 1:02d}"; nw += 1
            if x.get("drop"):
                report.append(dict(id=gid, dropped=x["drop"], his=[b.get("header")] + b["bullets"])); continue
            t0, t1 = float(b["t0"]), float(b["t1"])
            items = x.get("items") or b["bullets"]
            heading = x.get("heading") or b.get("header") or "KEY POINTS"
            if x.get("reveal"):
                rv = [at(p, t0, t1, gid) for p in x["reveal"]]
            else:
                rv = [round(t0 + 0.5 + i * (t1 - t0 - 1.2) / max(1, len(items)), 3) for i in range(len(items))]
            assert len(rv) == len(items), f"{gid}: one reveal phrase per item"
            rv = [max(t0 + 0.35, r) for r in rv]
            G.append(dict(id=gid, template="side-list", t0=t0, t1=t1, layer="side", text=[heading] + items,
                          config=dict(id=gid, a=t0, b=t1, drift=-6, heading=heading, items=items, reveal=rv),
                          driven_by=[dict(part=f"item {i + 1} lands: {s}", phrase=(x.get("reveal") or [""] * len(items))[i] or "(evenly spaced)", t=round(r, 2))
                                     for i, (s, r) in enumerate(zip(items, rv))]))
            insets.append(dict(kind="hfov", t0=t0, t1=t1, gid=gid))
            report.append(dict(id=gid, his=[b.get("header")] + b["bullets"], ours=[heading] + items, speech=say(t0, t1)))
        elif k in ("title", "stmt"):
            x = (X.get("titles") or {}).get(str(nt), {})
            gid = f"T{nt + 1:02d}"; nt += 1
            his = [b.get("headline"), b.get("sub")] if k == "title" else [" ".join(p for p, _ in b["parts"])]
            if x.get("drop"):
                report.append(dict(id=gid, dropped=x["drop"], his=his)); continue
            eyebrow = x.get("eyebrow")
            headline = x.get("headline") or "\n".join(s for s in his if s)
            rows = x.get("items")                              # glass rows under the headline (a sum, a recap)
            G.append(dict(id=gid, template="softblue:recap" if rows else "softblue:title_card", t0=float(b["t0"]), t1=float(b["t1"]), layer="full",
                          text=[s for s in [eyebrow] + headline.split("\n") + (rows or []) if s],
                          config=dict(eyebrow=eyebrow, headline=headline, **({"items": rows} if rows else {})), driven_by=[]))
            beats.append(dict(t0=b["t0"], t1=b["t1"], kind="hf", gid=gid, caps=False,
                              **{kk: b[kk] for kk in ("flash_after", "his_flash") if kk in b}))
            report.append(dict(id=gid, his=his, ours=[eyebrow, headline], speech=say(b["t0"], b["t1"])))
        elif k == "winmedia":
            beats.append(dict(b, kind="card", phone=True, caps=False))
        else:
            beats.append(dict(b))
    src = sorted(C.get("lower_thirds", []), key=lambda o: o["t0"])
    i = 0
    nl = 0
    while i < len(src):
        it = src[i]
        x = (X.get("lower_thirds") or {}).get(str(i), {})
        t0, t1 = float(it["t0"]), float(it["t1"])
        his = list(it["lines"])
        j = i
        while (X.get("lower_thirds") or {}).get(str(j), {}).get("merge_next") and j + 1 < len(src):
            j += 1; t1 = float(src[j]["t1"]); his += src[j]["lines"]
        i = j + 1
        gid = f"L{nl + 1:02d}"; nl += 1
        if x.get("drop"):
            report.append(dict(id=gid, dropped=x["drop"], his=his)); continue
        if x.get("t1"):
            t1 = at(x["t1"], t0, dur, gid) if isinstance(x["t1"], str) else float(x["t1"])
        if x.get("fact"):
            f = x["fact"]; gid = "F" + gid[1:]
            tt = lambda p: round(max(t0 + 0.25, min(at(p, t0, t1, gid), t1 - 0.5)), 3)
            cfg = dict(id=gid, a=t0, b=t1, photo=f["photo"], eyebrow=[f["eyebrow"][0], tt(f["eyebrow"][1])],
                       headline=[[p, tt(ph)] for p, ph in f["headline"]], push=f.get("push", 1.07), drift=-8)
            if f.get("detail"): cfg["detail"] = [f["detail"][0], tt(f["detail"][1])]
            if f.get("label"): cfg["label"] = f["label"]
            if f.get("count"): cfg["count"] = f["count"]
            if f.get("whole"): cfg["whole"] = True
            txt = [f["eyebrow"][0]] + [p for p, _ in f["headline"]] + ([f["detail"][0]] if f.get("detail") else []) + ([f["label"]] if f.get("label") else [])
            G.append(dict(id=gid, template="before-card", t0=t0, t1=t1, layer="full", text=txt, config=cfg,
                          driven_by=[dict(part=f'"{p}" lands', phrase=ph, t=tt(ph)) for p, ph in [f["eyebrow"]] + f["headline"] + ([f["detail"]] if f.get("detail") else [])]))
            beats.append(dict(t0=t0, t1=t1, kind="hf", gid=gid, caps=False))
            report.append(dict(id=gid, his=his, ours=txt, speech=say(t0, t1)))
            continue
        topic = x.get("topic") or "KEY POINT"
        raw = x.get("parts") or [[" ".join(his)]]
        parts = []
        for q, p in enumerate(raw):
            p = p if isinstance(p, (list, tuple)) else [p]
            t = at(p[1], t0, t1, gid) if len(p) > 1 else t0 + 0.35 + q * max(0.5, (t1 - t0 - 1.0) / max(1, len(raw)))
            parts.append([p[0], round(max(t0 + 0.3, min(t, t1 - 0.5)), 3)])
        G.append(dict(id=gid, template="lower-third", t0=t0, t1=t1, layer="overlay", text=[topic] + [p for p, _ in parts],
                      config=dict(id=gid, a=t0, b=t1, drift=-4, topic=topic, parts=parts),
                      driven_by=[dict(part=f'"{p}" rises', phrase=(raw[q][1] if isinstance(raw[q], (list, tuple)) and len(raw[q]) > 1 else "(on entry)"), t=round(t, 2))
                                 for q, (p, t) in enumerate(parts)]))
        lts.append(dict(t0=t0, t1=t1, lines=[topic, " ".join(p for p, _ in parts)], gid=gid))
        report.append(dict(id=gid, his=his, ours=[topic] + [p for p, _ in parts], speech=say(t0, t1)))
    for y in X.get("extra_lower_thirds") or []:
        t0 = find(y["from"])[0] if isinstance(y["from"], str) else float(y["from"])
        t1 = find(y["to"], t0)[0] if isinstance(y["to"], str) else float(y["to"])
        gid = f"L{nl + 1:02d}"; nl += 1
        parts = [[p[0], round(max(t0 + 0.3, min(at(p[1], t0, t1, gid) if len(p) > 1 else t0 + 0.35, t1 - 0.5)), 3)] for p in y["parts"]]
        G.append(dict(id=gid, template="lower-third", t0=t0, t1=t1, layer="overlay", text=[y["topic"]] + [p for p, _ in parts],
                      config=dict(id=gid, a=t0, b=t1, drift=-4, topic=y["topic"], parts=parts),
                      driven_by=[dict(part=f'"{p}" rises', phrase=(y["parts"][q][1] if len(y["parts"][q]) > 1 else "(on entry)"), t=round(t, 2)) for q, (p, t) in enumerate(parts)]))
        lts.append(dict(t0=t0, t1=t1, lines=[y["topic"], " ".join(p for p, _ in parts)], gid=gid))
        report.append(dict(id=gid, his=["(his text was burned into the clip this replaces)"], ours=[y["topic"]] + [p for p, _ in parts], speech=say(t0, t1)))
    lts.sort(key=lambda o: o["t0"])
    for q, y in enumerate(X.get("tallies") or []):
        gid = f"S{q + 1:02d}"
        t0 = find(y["from"], y.get("after", 0.0))[0] if isinstance(y["from"], str) else float(y["from"])
        t1 = find(y["to"], t0)[1] if isinstance(y["to"], str) else float(y["to"])
        cfg = dict(label=y.get("label", "So far"), value=y["value"], frm=y.get("frm", 0), unit=y.get("unit", "/ month"))
        G.append(dict(id=gid, template="tally", t0=t0, t1=t1, layer="overlay", config=cfg, driven_by=[],
                      text=[cfg["label"].upper(), f"${cfg['value']:,} {cfg['unit']}"]))
        insets.append(dict(kind="hfchip", t0=round(t0, 3), t1=round(t1, 3), gid=gid))
        report.append(dict(id=gid, ours=[cfg["label"], cfg["value"]], speech=say(t0, t1)))
    ctas = []
    for q, c in enumerate(sorted(C.get("ctas") or [], key=lambda o: o["t0"])):
        top, big = c.get("top", C.get("cta_top", "Get A FREE AI Image Of Yourself")), c.get("big", C.get("cta_big", "With Abs"))
        gid = f"C{q + 1:02d}"
        ctas.append(dict(c, top=top, big=big, gid=gid))
        # on the sheet too, so the graphic-lock page shows the button (times are the kit's; the last one runs to the end)
        G.append(dict(id=gid, template="cta", t0=float(c["t0"]), t1=float(c["t1"]), layer="overlay", text=[top, big],
                      config=dict(top=top, big=big, hold_out=abs(float(c["t1"]) - dur) < 0.05), driven_by=[]))
        report.append(dict(id=gid, ours=[top, big], speech=say(float(c["t0"]), float(c["t1"]))))
    beats.sort(key=lambda b: b["t0"])
    out = dict(C, source=C.get("source", "") + "; redrawn in Soft Blue Light by master_to_sbl.py", style="softblue", beats=beats,
               lower_thirds=lts, insets=insets, ctas=ctas, auto_cta=False, flash=True, no_caps_kinds=["hf", "cta"],
               deviations=list(C.get("deviations", [])) + [
                   ["graphics", "Every graphic of the editor's master is redrawn in Soft Blue Light with HyperFrames (Dan, 2026-10-01). "
                                "His text screens (text left, Dan right) become the 3A card under a full-frame Dan."],
                   ["transitions", "His white flash on returns is kept (render_sbl.py draws it in Soft Blue white): transitions stay the editor's."]])
    json.dump(out, open(os.path.join(B, "content.json"), "w"), indent=1)
    if X.get("media"):
        # extra media (library originals, cropped lifts) join the recovered map; assets_auto.py keeps the first one
        ap_, keep = os.path.join(B, "assets.py"), os.path.join(B, "assets_auto.py")
        if not os.path.exists(keep):
            shutil.copy(ap_, keep)
        ns = {}
        exec(open(keep).read(), ns)
        media = dict(ns["MEDIA"])
        for kk, v in X["media"].items():
            media[kk] = tuple(v)
        open(ap_, "w").write('#!/usr/bin/env python3\n"""Media map: auto_content.py\'s (assets_auto.py) plus the copy file\'s additions (master_to_sbl.py)."""\n\n'
                             f"MASTER = {ns['MASTER']!r}\n\nMEDIA = {{\n" + "".join(f"    {kk!r}: {v!r},\n" for kk, v in media.items()) + "}\n")
    json.dump(dict(graphics=sorted(G, key=lambda g: g["t0"]), words=dict(list=[dict(w=w["word"].strip(), t0=w["start"], t1=w["end"])
                                                                               for s in wj["segments"] for w in s.get("words", [])]),
                   video=dict(duration=dur)), open(os.path.join(B, "sbl_sheet.json"), "w"), indent=1)
    json.dump(report, open(os.path.join(B, "sbl_report.json"), "w"), indent=1)
    kinds = {}
    for g in G:
        kinds[g["template"]] = kinds.get(g["template"], 0) + 1
    print(f"{len(G)} Soft Blue Light graphics {kinds}; {sum(1 for b in beats if b['kind'] in ('card', 'bleed'))} pictures; {len(ctas)} CTAs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
