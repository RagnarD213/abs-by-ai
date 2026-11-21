"""RO-37 round 2 background plan: the locked green-screen template's rules (greenscreen-bg/README "The rules") applied to
this film's facts. This is a how-to film with no other people, so "their clip" is Dan's own October 23 gym footage.

  1. the background changes only on a picture cut, about every 8-20 s (whole shots; a short tail joins the one before)
  2. a side list is up -> the moving Soft Blue field, Dan right (Dan's approved test: "the how this looks graphic")
     right after the opening montage -> 6 cards (gym stills), then 3 wall
     right after one of his gym clips played full screen -> 2 corner (that clip keeps rolling, Dan small, lower right)
     he says a number no lower third shows -> 7 big type
     otherwise 1 soft (a gym clip blurred and navy behind him) or, now and then, 2b side (the clip sharp, Dan right)
  3. never the same type twice in a row; side at most once in four
  the pool close-up (no cutout) only at r2.CLOSEUPS (Dan: "sparingly"). Not used: 4 panel (no before/after in this film),
  8 set (needs a set plate; this film has enough backgrounds without it).
  python3 plan_bg.py  ->  round2/bg_plan.json (+ prints every segment and its why)"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
FPS = r2.FPS; t = lambda f: f / FPS
MIN, MAX = 8.0, 20.0

# numbers he says (big type), each [phrase, search window, lines]
NUMBERS = [("more than 20 years", (8, 14), ["20+ YEARS", "IN THE GYM"]),
           ("15 minutes is easy", (68, 76), ["15 MINUTES", "IS EASY"]),
           ("five minutes", (122, 128), ["5 MINUTES", "THAT'S FINE"]),
           ("it takes about 15 minutes", (166, 176), ["15 MINUTES", "WHOLE WORKOUT"]),
           ("only about 15 minutes", (258, 266), ["STILL 15 MIN", "NO EXTRA TIME"]),
           ("two hour workout on his first", (318, 328), ["2 HOURS", "GONE IN 3 WEEKS"]),
           ("lifting for 20 years", (355, 362), ["20 YEARS", "NO DEADLIFTS"])]
# background footage: his own clips (graded with the round 1 tune method), by what he talks about; the rest rotate
TOPIC = [(("bike",), "B0566"), (("leg press",), "B0620"), (("chest press",), "B0678"), (("cable row", "rows"), "B0648"),
         (("pull down", "pulldown"), "B0688"), (("shoulder press",), "B0682"), (("crunch",), "B0574"),
         (("walk between", "walk around"), "B0710"), (("seat",), "B0624")]
GENERAL = ["B0665", "B0673", "B0723", "B0631", "B0699", "B0626", "B0651", "B0655", "B0669", "B0637", "B0579", "B0611", "B0720"]
LONGER = {"B0691": "B0624", "B0583": "B0574", "B0575": "B0566", "B0623": "B0620", "B0681": "B0678", "B0693": "B0682"}
DUR = {}   # filled from bgclips/index.json (clip seconds)


def numbers():
    out = []
    for ph, (lo, hi), lines in NUMBERS:
        tt = r2.word_t(ph, lo, hi)
        dig = next((w for w in r2.WORDS if tt <= w["t0"] <= tt + 3 and any(c.isdigit() for c in w["w"])
                    or w["w"].lower().strip(".,") in ("five", "two", "ten")), None)
        out.append(dict(t=tt, t_num=dig["t0"] if dig else tt, lines=lines))
    return out


def group(shots):
    segs, cur = [], []
    for s in shots:
        if cur:
            L = t(cur[-1]["out_f1"] - cur[0]["out_f0"])
            if L >= MIN or (L + t(s["out_f1"] - s["out_f0"]) > MAX and L >= MIN * 0.6): segs.append(cur); cur = []
        cur.append(s)
    if cur:
        if segs and t(cur[-1]["out_f1"] - cur[0]["out_f0"]) < MIN * 0.6 and t(segs[-1][-1]["out_f1"] - segs[-1][0]["out_f0"] + cur[-1]["out_f1"] - cur[0]["out_f0"]) <= MAX:
            segs[-1] += cur
        else: segs.append(cur)
    return segs


def main():
    global DUR
    DUR = json.load(open(f"{r2.W2}/bgclips/index.json"))
    shots = r2.shots2(); nums = numbers()
    lt_win = [(r["t0"] - 0.3, r["t1"] + 2.0) for r in r2.LTS]
    used_clip = {}; out = []; prev = None
    # walk the film: covered shots are full-screen inserts; list / close-up shots are their own segments
    runs, cur, last_ins = [], [], None
    def flush():
        nonlocal cur
        if cur: runs.append(("plain", cur, last_ins)); cur = []
    i = 0
    while i < len(shots):
        s = shots[i]
        if s["covered"]:
            flush(); last_ins = s["covered"]; i += 1; continue
        if s["l3"] or s["closeup"]:
            flush(); kind = "list" if s["l3"] else "closeup"; g = [s]
            while i + 1 < len(shots) and not shots[i + 1]["covered"] and (shots[i + 1]["l3"] == s["l3"] if s["l3"] else shots[i + 1]["closeup"]):
                i += 1; g.append(shots[i])
            runs.append((kind, g, last_ins)); last_ins = kind; i += 1; continue
        if cur and last_ins and cur[-1]["out_f1"] != s["out_f0"]: flush()
        cur.append(s); i += 1
        if i < len(shots) and shots[i]["covered"]: flush()
    flush()
    after_intro = 0; quarter = []
    def pick_clip(s0, s1, avoid=()):
        text = r2.speech(s0, s1).lower()
        for keys, cid in TOPIC:
            if any(k in text for k in keys) and cid not in avoid and used_clip.get(cid, 0) < 2: return cid
        pool = sorted(GENERAL, key=lambda c: (used_clip.get(c, 0), GENERAL.index(c)))
        return next(c for c in pool if c not in avoid)
    def windows(cid, dur_needed, start=None):
        d = DUR[cid]; a = 0.4 if start is None else start
        if start is None and used_clip.get(cid, 0): a = min(max(0.4, d - dur_needed - 0.4), d / 2)
        return [[round(a, 2), round(d - 0.3, 2)]] + ([[0.4, round(d - 0.3, 2)]] if d - 0.3 - a < dur_needed else [])
    for kind, g, ins in runs:
        if kind in ("list", "closeup"):
            s0, s1 = t(g[0]["out_f0"]), t(g[-1]["out_f1"])
            seg = dict(t0=round(s0, 4), t1=round(s1, 4), type=kind, why="a side list is up: the moving field, Dan right (your approved test layout)"
                       if kind == "list" else "the full-frame pool close-up, used rarely")
            out.append(seg); prev = kind; continue
        first_ins = ins
        for k, gg in enumerate(group(g)):
            s0, s1 = t(gg[0]["out_f0"]), t(gg[-1]["out_f1"]); dur = s1 - s0
            fi = first_ins if k == 0 else None
            cand, why = [], {}
            has_num = [n for n in nums if s0 <= n["t"] < s1 - 1.0 and not any(a <= n["t"] <= b for a, b in lt_win)]
            if fi and fi.startswith("C01") or (after_intro == 1 and k > 0):
                cand += ["cards", "wall"]; why["cards"] = why["wall"] = "right after the opening montage (template: floating cards, then the photo wall)"
            if fi and fi.startswith("C") and not fi.startswith("C01"):
                cand.append("corner"); why["corner"] = f"right after his {fi} gym clip: it keeps rolling, Dan talks from the corner"
            if has_num:
                cand.append("bigtype"); why["bigtype"] = f"he says the number ({' / '.join(has_num[0]['lines'])})"
            if dur < 2.5:
                cand.insert(0, "soft"); why["soft"] = "under 2.5 s between full-screen items: a calm background"
            # commentary: soft, alternating with side (at most one in four), the photo wall or the cards (the template's
            # "8 or 1" alternation; this film has no set plate, so the gym-still wall and cards take the set's turn)
            recent = [o["type"] for o in out[-3:]]
            alt = "side" if "side" not in recent else ("wall" if [o["type"] for o in out if o["type"] in ("wall", "cards")][-1:] == ["cards"] else "cards")
            why.setdefault("side", "his gym clip sharp behind him, Dan to the side (template: now and then)")
            why.setdefault("wall", "commentary: a wall of stills from his gym footage scrolling behind him")
            why.setdefault("cards", "commentary: stills from his gym footage drifting as cards around him")
            why.setdefault("soft", "commentary: his gym footage softened behind him")
            cand += ["soft", alt]
            typ = next((c for c in cand if c != prev), alt)
            seg = dict(t0=round(s0, 4), t1=round(s1, 4), type=typ, why=why.get(typ, "commentary"))
            if typ in ("soft", "side"):
                cid = pick_clip(s0, s1, avoid=[o.get("clip", {}).get("id") for o in out[-2:]]); used_clip[cid] = used_clip.get(cid, 0) + 1
                seg["clip"] = dict(id=cid, src=f"bgclips/{cid}.mp4", windows=windows(cid, dur))
                if typ == "side": seg["clip"].update(zoom=1.22, focus=[0.5, 0.45], out_focus=[0.36, 0.45])
            elif typ == "corner":
                it = next(r for r in r2.CLIPS if r["id"] == fi); cid, a = it["src"].split("@")[0], float(it["src"].split("@")[1])
                cont = a + (it["t1"] - it["t0"])                     # the clip keeps rolling from where its insert ended
                if DUR.get(cid, 0) - cont < min(dur, 6.0): cid, cont = LONGER.get(cid, cid), 0.4
                seg["clip"] = dict(id=cid, src=f"bgclips/{cid}.mp4", windows=windows(cid, dur, start=cont))
                seg["why"] += f" (footage: {cid} from {cont:.1f} s)"
            elif typ == "bigtype":
                n = has_num[0]; seg["lines"] = n["lines"]; seg["max_w"] = 680; seg["line_times"] = [round(max(s0 + 0.15, n["t_num"]), 3), round(max(s0 + 0.4, n["t_num"] + 0.45), 3)]
                nums.remove(n)
            elif typ in ("cards", "wall"):
                seg["photos"] = None                                 # dealt by photos.py from the gym stills pool
            out.append(seg); prev = typ
            if fi and fi.startswith("C01") and k == 0: after_intro = 1
            elif after_intro: after_intro += 1
    for n, s in enumerate(out): s["id"] = f"BG{n + 1:02d}"
    # deal the gym stills to cards (6) and wall (up to 24), least used first
    pool = json.load(open(f"{r2.W2}/photos/index.json")); used = {}
    for s in out:
        if s["type"] in ("cards", "wall"):
            n = 6 if s["type"] == "cards" else 24
            pick = sorted(pool, key=lambda p: (used.get(p, 0), pool.index(p)))[:n]
            for p in pick: used[p] = used.get(p, 0) + 1
            s["photos"] = [f"photos/{p}" for p in pick]
    ovr = f"{r2.W2}/bg_overrides.json"
    if os.path.exists(ovr):
        O = json.load(open(ovr))
        for s in out:
            if s["id"] in O: s.update(O[s["id"]]); s["why"] += " (editor's override)"
    json.dump(dict(segments=out), open(f"{r2.W2}/bg_plan.json", "w"), indent=1)
    for s in out:
        extra = s.get("clip", {}).get("id") or " / ".join(s.get("lines") or []) or ""
        print(f"{s['id']} {s['t0']:7.2f}-{s['t1']:7.2f} ({s['t1'] - s['t0']:4.1f}s) {s['type']:8s} {extra:24s} {s['why']}")


if __name__ == "__main__":
    main()
