"""The background planner for a green-screen reaction / commentary film (README "The rules"): proposes one background
per stretch of presenter picture, changing only on cuts, from what is being said.

  python3 planner.py FACTS.json OUT_PLAN.json [--overrides OVR.json]

FACTS.json (written by the film's recipe, every time on the FINAL film timeline, seconds):
  "shots":      [{"t0", "t1", "framing": "W"|"T"}]   every presenter shot (picture cuts are shot edges)
  "inserts":    [{"t0", "t1", "kind": "clip"|"photo"|"card"|"broll"|"intro", "person"?}]   full-screen items (no Dan)
  "people":     {"<name>": {"clip": {"src", "windows": [[a, b]], "after": [[a, b]]},     muted footage of them
                            "photos": [...], "pairs": [{"photos": [b, a], "years": [..], "credits": [..]}],
                            "stat": "42 lb, Ozempic", "big": ["-42 LB", "OZEMPIC"]}}
  "sections":   [{"t0", "t1", "person"}]                 who he is talking about
  "numbers":    [{"t", "lines": ["2.5 MG", "OR LESS"], "person"?}]     a number he says (word start)
  "transformations": [{"t0", "t1", "person"}]            where he talks about how someone's body changed
  "side_cards": [{"t0", "t1"}]                           left-third cards over Dan (keep the background calm)
  "lower_thirds": [{"t0", "t1"}]                         a number said under a lower third is not repeated as big type
  "everyone":   [photo, ...]                             the pool for the walls and cards after the intro
Writes {"segments": [...]} in the plan format gsbg.make_background reads. Every choice carries a "why".
"""
import json, sys

MIN, MAX = 8.0, 20.0


def group_shots(shots, t0, t1):
    """Shots inside one presenter span -> segments of whole shots, about MIN..MAX seconds each."""
    sh = [dict(s, t0=max(s["t0"], t0), t1=min(s["t1"], t1)) for s in shots if min(s["t1"], t1) - max(s["t0"], t0) > 0.1]
    segs, cur = [], []
    for s in sh:
        if cur:
            L = cur[-1]["t1"] - cur[0]["t0"]
            if L >= MIN or (L + s["t1"] - s["t0"] > MAX and L >= MIN * 0.6):
                segs.append(cur); cur = []
        cur.append(s)
    if cur:
        if segs and cur[-1]["t1"] - cur[0]["t0"] < MIN * 0.6 and segs[-1][-1]["t1"] - segs[-1][0]["t0"] + cur[-1]["t1"] - cur[0]["t0"] <= MAX:
            segs[-1] += cur                                  # a short tail joins the segment before it
        else:
            segs.append(cur)
    return [(g[0]["t0"], g[-1]["t1"]) for g in segs]


def overlap(a0, a1, b0, b1):
    return max(0.0, min(a1, b1) - max(a0, b0))


def plan(F):
    inserts = sorted(F["inserts"], key=lambda x: x["t0"])
    end = max(s["t1"] for s in F["shots"])
    spans, t = [], 0.0                                       # presenter spans between full-screen inserts
    for ins in inserts:
        if ins["t0"] - t > 0.05: spans.append((t, ins["t0"], ins))
        t = max(t, ins["t1"])
    if end - t > 0.05: spans.append((t, end, None))
    people = F["people"]; used_photos, used_pairs, used_win = set(), {}, {}
    prev_ins = {round(s[0], 2): None for s in spans}
    for ins in inserts: prev_ins[round(ins["t1"], 2)] = ins
    out, prev = [], None
    after_intro = 0

    def who(a, b):
        best = max(F["sections"], key=lambda s: overlap(a, b, s["t0"], s["t1"]), default=None)
        return best["person"] if best and overlap(a, b, best["t0"], best["t1"]) > 0 else None

    def next_photos(pool, n):
        fresh = [p for p in pool if p not in used_photos]
        pick = (fresh + [p for p in pool if p in used_photos])[:n]
        used_photos.update(pick); return pick

    def clip_window(p, after=False):
        c = people[p]["clip"]; wins = c.get("after") if after and c.get("after") else c["windows"]
        k = used_win.get(p, 0); used_win[p] = k + 1
        rot = wins[k % len(wins):] + wins[:k % len(wins)]
        return dict(src=c["src"], windows=rot, **{x: c[x] for x in ("zoom", "focus", "out_focus") if x in c})

    for a, b, ins_end in [(s[0], s[1], prev_ins.get(round(s[0], 2))) for s in spans]:
        for k, (s0, s1) in enumerate(group_shots(F["shots"], a, b)):
            p = who(s0, s1); P = people.get(p, {}) if p else {}
            lts = F.get("lower_thirds", [])
            nums = [n for n in F.get("numbers", []) if s0 <= n["t"] < s1
                    and not any(l["t0"] - 0.3 <= n["t"] <= l["t1"] for l in lts)]     # a lower third already shows that number
            trans = [x for x in F.get("transformations", []) if overlap(s0, s1, x["t0"], x["t1"]) > 1.0]
            card = [x for x in F.get("side_cards", []) if overlap(s0, s1, x["t0"], x["t1"]) > 0.2]
            first_after = k == 0 and ins_end is not None
            cand, why = [], {}
            if s1 - s0 < 2.5:
                cand.append("soft"); why["soft"] = "a stretch under 2.5 s between full-screen items: a calm background, no new idea"
            if card:
                cand.append("soft"); why["soft"] = "a left-third card is up: calm background, Dan to the side"
            if first_after and ins_end["kind"] == "intro" or (after_intro and after_intro < 2 and not first_after):
                cand += ["cards", "wall"]; why["cards"] = why["wall"] = "right after the intro (Dan: floating cards or the photo wall)"
            if first_after and ins_end["kind"] == "clip" and P.get("clip"):
                cand.append("corner"); why["corner"] = f"right after {p}'s clip: it keeps rolling, Dan reacts from the corner"
            if nums:
                cand.append("bigtype"); why["bigtype"] = f"he says the number ({' / '.join(nums[0]['lines'])})"
            if trans and P.get("pairs"):
                cand.append("panel"); why["panel"] = f"he talks about {p}'s transformation: before and after with the numbers"
            if P.get("clip"):
                cand += ["side", "set", "soft"]; why["side"] = f"{p}'s clip behind, Dan to the side (Dan: occasionally)"
                why["set"] = why["soft"] = "commentary: the studio set, or their clip softened behind him"
            cand += ["set", "soft", "wall", "cards"]
            for x in ("set", "soft", "wall", "cards"): why.setdefault(x, "commentary")
            recent = [o["type"] for o in out[-2:]]
            typ = next((c for c in cand if c != prev and c not in recent[-1:]), cand[0])
            if typ == "side" and "side" in [o["type"] for o in out[-4:]]:     # side is occasional
                typ = next((c for c in cand if c not in ("side", prev)), typ)
            seg = dict(id=f"BG{len(out) + 1:02d}", t0=round(s0, 4), t1=round(s1, 4), type=typ, person=p, why=why.get(typ, ""))
            if card and typ == "soft":                          # the left-third card needs Dan to the side (the 3A card's fixed
                seg["placement"] = "right"                       # presenter position), not centre under it (RO-24 R4 graphics check)
            if typ in ("corner", "side"):
                seg["clip"] = clip_window(p, after=typ == "corner" and first_after)
            elif typ == "soft":
                if P.get("clip"): seg["clip"] = clip_window(p)
                else: seg["photos"] = next_photos(P.get("photos") or F["everyone"], 1)
            elif typ == "set":
                seg["chip_on_tv"] = True                  # Dan 2026-10-30: the AI label goes on the TV, not on the whole scene
                if P.get("clip") and (len(out) % 2 == 0 or not P.get("pairs")): seg["clip"] = clip_window(p)
                else: seg["photos"] = next_photos([x for pr in P.get("pairs", []) for x in pr["photos"]] or F["everyone"], 2)
            elif typ in ("wall", "cards"):
                pool = F["everyone"] if (first_after or after_intro) else (P.get("photos") or F["everyone"])
                seg["photos"] = next_photos(pool, 24 if typ == "wall" else 6)
            elif typ == "panel":
                pairs = P["pairs"]; i = used_pairs.get(p, 0); used_pairs[p] = i + 1
                seg.update(pair=pairs[i % len(pairs)], name=p, stat=P["stat"])
            elif typ == "bigtype":
                seg["lines"] = nums[0]["lines"]
            out.append(seg); prev = typ
            if ins_end is not None and ins_end["kind"] == "intro" and k == 0: after_intro = 1
            elif after_intro: after_intro += 1
    return dict(segments=out)


def main():
    F = json.load(open(sys.argv[1])); P = plan(F)
    if "--overrides" in sys.argv:
        ovr = json.load(open(sys.argv[sys.argv.index("--overrides") + 1]))
        for s in P["segments"]:
            if s["id"] in ovr: s.update(ovr[s["id"]]); s["why"] = s.get("why", "") + " (editor's override)"
    json.dump(P, open(sys.argv[2], "w"), indent=1)
    for s in P["segments"]:
        print(f"{s['id']} {s['t0']:8.2f}-{s['t1']:8.2f} ({s['t1'] - s['t0']:5.1f}s) {s['type']:8s} {s.get('person') or '':16s} {s['why']}")


if __name__ == "__main__":
    main()
