#!/usr/bin/env python3
"""
Check a draft written as Dan: hard rules, then how far its numbers sit from his. Detect only: it never rewrites.

WHY THIS EXISTS (2026-10-10, Dan Voice P2B step B6): the Phase A bench showed rules with no numbers overshoot. "Fewer
ands" produced 1.76 per 100 against his 2.82, and Claude's sentence lengths were less than half as varied as his. So
every rate here is a BAND, a floor and a ceiling, fitted on his own text cut into draft-sized pieces, and each measure
is weighted by how well it actually separates his text from Claude's. A measure that does not separate the two is
dropped. The bands live in `scripts/voice/voice_bands.json` (numbers only), so this runs in a cloud session.

    python3 scripts/voice/voice_check.py draft.txt --type content --format video
    python3 scripts/voice/voice_check.py draft.txt --type ads --format ad-own --json
    python3 scripts/voice/voice_check.py --hard draft.txt        # hard rules only (what the hook runs); - reads stdin
    python3 scripts/voice/voice_check.py --fit                   # local only: refit the bands from voice-corpus/

Formats: see `scripts/voice/bank.py`. Exit code: 1 on a hard fail, 2 when the score is over the format's line, else 0.

Reading the result:
- HARD FAIL: an em or en dash, or a phrase Dan has cut from drafts. Fix before anything else.
- SCORE: 0 to 100, the weighted share of measures outside his band. The line for each format is the score that 80%
  of his own pieces stay under. Over the line means "reads like Claude by the numbers", not "is bad".
- Each flagged measure shows the draft's number and his band, and says which side it is off. A measure off on the far
  side from Claude is an OVERSHOOT: the draft is performing the voice. Do not push a number past his band.
- LINES: sentences to look at (hedges, formal words, "not X but Y", kicker endings, tidy triads, an even run).
A pass is not proof it sounds like him. The bench (`bench.py`) is the test; this is the tripwire.
"""
import argparse
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voice_stats  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BANDS = os.path.join(HERE, "voice_bands.json")
CHUNK = 300

# Phrases Dan cut from Claude drafts or ruled out (sources: DAN-VOICE.md section 8, voice/dan-edits-2026-10-06.md,
# scriptfromoutline WHAT DAN CHANGED, memory entries). A hit is a hard fail.
HARD_PHRASES = [
    r"let'?s be honest", r"here(?:'s| is) the uncomfortable truth", r"honest answer\.", r"this is that video",
    r"quote[ ,-]+unquote", r"\bmy wife\b", r"today we(?:'re| are) talking about", r"to be fair,",
    r"i know how that sounds",
]
HARD_RE = [re.compile(p, re.I) for p in HARD_PHRASES]
DASH = re.compile(r"[—–]")

HEDGE = re.compile(r"\b(maybe|might|perhaps|probably|somewhat|a bit|a little bit|tend to|tends to|can be|may|often|"
                   r"usually|typically|generally|in most cases|i think|i'd say|sort of)\b", re.I)
FORMAL = re.compile(r"\b(several|however|therefore|additionally|furthermore|moreover|ensure|utili[sz]e\w*|significant\w*|"
                    r"crucial|ultimately|essential\w*|numerous|approximately|regarding|prior to|in order to|as well as|"
                    r"individuals?|consume|consuming|purchase\w*|obtain\w*|require[sd]?|achieve\w*|maintain\w*|"
                    r"effective\w*|properly|genuinely|simply put|worth noting|keep in mind|straightforward|"
                    r"incredibly|completely|entirely|specifically|particularly|exactly)\b", re.I)
NOT_X_BUT_Y = re.compile(r"\b(not just|isn't just|aren't just|not only|it's not about|it isn't about|"
                         r"(?:isn't|aren't|wasn't|not) [^.?!]{3,40}[,.] (?:it's|it is|they're|that's|but)\b)", re.I)
START_CONJ = re.compile(r"^(and|so|but|now|because|or|then|also|plus)\b", re.I)
CAPS = re.compile(r"\b[A-Z]{3,}\b")
ACRONYM = {"AI", "USA", "CPA", "ROI", "LTV", "VSL", "FAQ", "HBI", "SEO", "CEO", "DVD", "GLP", "PM", "AM", "MG", "TV",
           "YOU", "USD", "PDF", "CTA", "RPM", "LLC", "IRS", "MMA", "UFC", "BJJ", "DNA", "FDA", "CTR", "CPM", "CPV"}


def features(text):
    """Every measure for one piece. Rates are per 100 words unless the name ends in _k (per 1,000) or _pct."""
    text = voice_stats.normalize(text)
    m = voice_stats.measure(text)
    n = m["words"] or 1
    out = {k: m[k] for k in ("and", "lists3", "questions", "you", "contractions", "sent_mean", "sent_sd", "para_words",
                             "punch_pct", "oneline_pct")}
    for w, v in voice_stats.small_words(text).items():
        out["w:" + w] = v
    sents = [s for p in voice_stats.paragraphs(text) for s in voice_stats.sentences(p)]
    lens = [len(voice_stats.words(s)) for s in sents] or [0]
    ns = len(sents) or 1
    k = lambda c: round(1000.0 * c / n, 2)
    out["sent_long_pct"] = round(100.0 * sum(1 for x in lens if x >= 30) / ns, 1)
    out["sent_short_pct"] = round(100.0 * sum(1 for x in lens if x <= 5) / ns, 1)
    out["sent_max"] = max(lens)
    out["start_conj_pct"] = round(100.0 * sum(1 for s in sents if START_CONJ.match(s.lstrip("\"'( "))) / ns, 1)
    heads = [" ".join(w.lower() for w in voice_stats.words(s)[:2]) for s in sents]
    out["start_repeat_pct"] = round(100.0 * sum(1 for i, h in enumerate(heads) if h and h in heads[max(0, i - 2):i]) / ns, 1)
    toks = [w.lower() for w in voice_stats.words(text)]
    grams = {}
    for i in range(len(toks) - 2):
        g = " ".join(toks[i:i + 3])
        grams[g] = grams.get(g, 0) + 1
    out["repeat3"] = round(100.0 * sum(c for c in grams.values() if c >= 2) / n, 2)
    first = toks[:150]
    out["variety150"] = round(100.0 * len(set(first)) / len(first), 1) if len(first) >= 120 else None
    out["word_len"] = round(sum(len(t) for t in toks) / n, 2)
    out["long_word_pct"] = round(100.0 * sum(1 for t in toks if len(t) >= 9) / n, 2)
    out["ly_k"] = k(sum(1 for t in toks if t.endswith("ly") and len(t) > 4))
    out["i"] = round(100.0 * sum(1 for t in toks if t in ("i", "i'm", "i've", "i'll", "i'd", "my", "me")) / n, 2)
    out["comma"] = round(100.0 * text.count(",") / n, 2)
    out["colon_k"] = k(len(re.findall(r":(?!\d)", text)))
    out["semicolon_k"] = k(text.count(";"))
    out["ellipsis_k"] = k(len(re.findall(r"\.{2,}|…", text)))
    out["dash_aside_k"] = k(len(re.findall(r" --? ", text)))
    out["hyphen_word_k"] = k(len(re.findall(r"\b[A-Za-z]+-[A-Za-z]+\b", text)))
    out["exclaim_k"] = k(text.count("!"))
    out["paren_k"] = k(text.count("("))
    out["caps_k"] = k(sum(1 for c in CAPS.findall(text) if c not in ACRONYM))
    out["hedge_k"] = k(len(HEDGE.findall(text)))
    out["formal_k"] = k(len(FORMAL.findall(text)))
    out["notxbuty_k"] = k(len(NOT_X_BUT_Y.findall(text)))
    return out


def hard_fails(text):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if DASH.search(line):
            out.append((i, "em or en dash", line.strip()[:110]))
        for rx in HARD_RE:
            hit = rx.search(line)
            if hit:
                out.append((i, f'phrase Dan cuts: "{hit.group(0)}"', line.strip()[:110]))
    return out


def lines_to_look_at(text, limit=14):
    """Sentences a reviser should look at, most telling first."""
    out = []
    paras = voice_stats.paragraphs(voice_stats.normalize(text))
    sents = [(pi, s) for pi, p in enumerate(paras) for s in voice_stats.sentences(p)]
    for pi, p in enumerate(paras):
        ss = voice_stats.sentences(p)
        if len(ss) >= 2 and len(voice_stats.words(ss[-1])) <= 6:
            out.append(("kicker ending (a short punch closing a paragraph)", ss[-1]))
    for _, s in sents:
        if NOT_X_BUT_Y.search(s):
            out.append(('"not X but Y" turn', s))
        if voice_stats.LIST3.search(s) and not re.search(r"\d", s):
            out.append(("three-item list: does he need all three, or does it only sound nice?", s))
        f = FORMAL.findall(s)
        if f:
            out.append((f"formal or neat word ({', '.join(sorted(set(x.lower() for x in f)))}): what is the plain word?", s))
        h = HEDGE.findall(s)
        if len(h) >= 2 or (h and re.match(r"\s*(maybe|perhaps|i think)", s, re.I)):
            out.append((f"hedged ({', '.join(sorted(set(x.lower() for x in h)))}): say it straight", s))
    lens = [len(voice_stats.words(s)) for _, s in sents]
    for i in range(len(lens) - 4):
        run = lens[i:i + 5]
        if max(run) - min(run) <= 5 and min(run) >= 7:
            out.append((f"five sentences in a row of nearly the same length ({', '.join(map(str, run))} words)", sents[i][1]))
            break
    seen, uniq = set(), []
    for why, s in out:
        if (why[:12], s) not in seen:
            seen.add((why[:12], s))
            uniq.append((why, s if len(s) <= 150 else s[:147] + "..."))
    return uniq[:limit]


def load_bands():
    with open(BANDS, encoding="utf-8") as fh:
        return json.load(fh)


def band_for(type_, fmt, bands=None):
    bands = bands or load_bands()
    return bands["formats"].get(f"{type_}/{fmt}") or bands["formats"].get(f"{type_}/*")


def score(text, type_, fmt, bands=None):
    b = band_for(type_, fmt, bands)
    f = features(text)
    words = voice_stats.measure(text)["words"]
    flags, total, hit = [], 0.0, 0.0
    for name, spec in b["measures"].items():
        v = f.get(name)
        if v is None:
            continue
        total += spec["weight"]
        lo, hi = spec["lo"], spec["hi"]
        if lo <= v <= hi:
            continue
        side = "high" if v > hi else "low"
        claude_side = side == spec["claude_side"]
        w = spec["weight"] * (1.0 if claude_side else 0.5)
        hit += w
        flags.append({"measure": name, "draft": v, "lo": lo, "hi": hi, "side": side, "weight": round(w, 2),
                      "overshoot": not claude_side, "dan_median": spec["median"]})
    flags.sort(key=lambda x: -x["weight"])
    return {"type": type_, "format": fmt, "words": words, "score": round(100.0 * hit / total, 1) if total else 0.0,
            "line": b["line"], "claude_typical": b.get("claude_median_score"), "flags": flags,
            "short": words < 120}


LABEL = {"and": '"and" per 100 words', "lists3": "three-item lists per 100 words", "sent_sd": "spread of sentence lengths",
         "sent_mean": "average sentence length", "sent_max": "longest sentence, words",
         "sent_long_pct": "% of sentences of 30+ words", "sent_short_pct": "% of sentences of 5 words or fewer",
         "start_conj_pct": "% of sentences starting And/So/But/Now/Because", "repeat3": "repeated 3-word runs per 100 words",
         "start_repeat_pct": "% of sentences opening like one of the two before", "variety150": "% distinct words in the first 150",
         "punch_pct": "% of paragraphs ending on a 6-word punch", "oneline_pct": "% one-line paragraphs",
         "para_words": "words per paragraph", "formal_k": "formal or neat words per 1,000", "hedge_k": "hedges per 1,000",
         "notxbuty_k": '"not X but Y" turns per 1,000', "ly_k": "-ly words per 1,000", "long_word_pct": "% words of 9+ letters",
         "word_len": "letters per word", "comma": "commas per 100 words", "colon_k": "colons per 1,000",
         "semicolon_k": "semicolons per 1,000", "ellipsis_k": "ellipses per 1,000", "dash_aside_k": "hyphen asides per 1,000",
         "hyphen_word_k": "hyphenated words per 1,000", "exclaim_k": "exclamation marks per 1,000", "caps_k": "CAPS words per 1,000",
         "paren_k": "brackets per 1,000", "i": "I / my / me per 100 words", "you": "you / your per 100 words",
         "contractions": "contractions per 100 words", "questions": "questions per 100 words"}


def label(name):
    return f'"{name[2:]}" per 1,000 words' if name.startswith("w:") else LABEL.get(name, name)


def report(text, type_, fmt):
    r = score(text, type_, fmt)
    hard = hard_fails(text)
    L = []
    if hard:
        L.append(f"HARD FAIL ({len(hard)}):")
        L += [f"  line {i}: {why}: {line}" for i, why, line in hard]
    verdict = "over the line: reads like Claude by the numbers" if r["score"] > r["line"] else "inside his range"
    L.append(f"SCORE {r['score']} ({verdict}; the line for {type_}/{fmt} is {r['line']}, Claude's cold drafts sit around "
             f"{r['claude_typical']}). {r['words']} words." + (" Under 120 words: the numbers are noise." if r["short"] else ""))
    if r["flags"]:
        L.append("OUTSIDE HIS BAND (heaviest first):")
        for f in r["flags"][:12]:
            where = "above" if f["side"] == "high" else "below"
            tag = " OVERSHOOT, performing the voice: pull back" if f["overshoot"] else ""
            L.append(f"  {label(f['measure'])}: {f['draft']} is {where} his band {f['lo']} to {f['hi']} "
                     f"(his typical {f['dan_median']}).{tag}")
    look = lines_to_look_at(text)
    if look:
        L.append("LINES TO LOOK AT:")
        L += [f"  [{why}] {s}" for why, s in look]
    return r, hard, "\n".join(L)


# ---------------------------------------------------------------- fit (local)

def pctl(xs, p):
    xs = sorted(xs)
    if not xs:
        return 0.0
    i = (len(xs) - 1) * p
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def auc(a, b):
    """Chance that a value from a is above a value from b (ties count half)."""
    if not a or not b:
        return 0.5
    wins = sum((x > y) + 0.5 * (x == y) for x in a for y in b)
    return wins / (len(a) * len(b))


def cut(text, spoken):
    """Draft-sized pieces of whole sentences (spoken) or paragraphs (written), in the form a judge sees."""
    import bench
    import bank
    us = bench.units(text, spoken)
    out, start, words = [], None, 0
    for s, e in us:
        if start is None:
            start = s
        words += voice_stats.measure(text[s:e])["words"]
        if words >= CHUNK:
            out.append(bank.dashes(bench.for_judging(text[start:e], spoken)))
            start, words = None, 0
    return out


def cmd_fit():
    import bank
    import corpus
    formats = {}
    for t in corpus.TYPES:
        dan, claude = {}, {}
        for row, text in corpus.pile(t):
            if row.get("tier") not in (1, 2) or row.get("confidence") == "low" or row["file"].endswith("-raw.txt") \
                    or row.get("authorship") == "dan-typed-lines-only" or (t in ("content", "conversion") and row.get("tier") != 1):
                continue
            dan.setdefault(bank.format_of(row), []).extend(cut(text, row.get("mode") == "spoken"))
        for it in bank.load(t):
            if it.get("claude"):
                claude.setdefault(it["format"], []).append(it["claude"])
        drafts = []  # Claude's own scripts for this type (tier 0): the same writer in real use
        for row in corpus.manifest():
            if row.get("type") == t and row.get("tier") == 0 and "claude" in (row.get("authorship") or "claude"):
                drafts += cut(corpus.read(row), row.get("mode") == "spoken")
        for fmt in bank.FORMATS[t]:
            d = dan.get(fmt, [])
            c = claude.get(fmt, [])
            if len(d) < 12 or len(c) < 4:
                continue
            # Claude's real-use drafts are scripts: they count for written formats and for shorts, not for transcripts
            if fmt in ("short", "ad-own", "sales-script"):
                c = c + drafts[:40]
            fd, fc = [features(x) for x in d], [features(x) for x in c]
            measures = {}
            for name in fd[0]:
                a = [f[name] for f in fd if f.get(name) is not None]
                b = [f[name] for f in fc if f.get(name) is not None]
                if len(a) < 10 or len(b) < 4:
                    continue
                sep = auc(b, a)  # above 0.5: Claude runs higher than Dan
                if abs(sep - 0.5) < 0.15:
                    continue  # does not separate the two: not a rule
                lo, hi = pctl(a, 0.10), pctl(a, 0.90)
                if lo == hi == 0 and sep < 0.5:
                    continue
                measures[name] = {"lo": round(lo, 2), "hi": round(hi, 2), "median": round(statistics.median(a), 2),
                                  "claude_median": round(statistics.median(b), 2), "auc": round(sep, 2),
                                  "weight": round(2 * abs(sep - 0.5), 2), "claude_side": "high" if sep > 0.5 else "low"}
            entry = {"measures": measures, "line": 0, "dan_pieces": len(d), "claude_pieces": len(c)}
            tmp = {"formats": {f"{t}/{fmt}": entry}}
            ds = [score(x, t, fmt, tmp)["score"] for x in d]
            cs = [score(x, t, fmt, tmp)["score"] for x in c]
            entry["line"] = round(pctl(ds, 0.80), 1)
            entry["dan_median_score"] = round(statistics.median(ds), 1)
            entry["claude_median_score"] = round(statistics.median(cs), 1)
            entry["claude_caught_pct"] = round(100.0 * sum(1 for x in cs if x > entry["line"]) / len(cs))
            formats[f"{t}/{fmt}"] = entry
        # a fallback for the type: its biggest fitted format
        got = [k for k in formats if k.startswith(t + "/")]
        if got:
            formats[f"{t}/*"] = formats[max(got, key=lambda k: formats[k]["dan_pieces"])]
    with open(BANDS, "w", encoding="utf-8") as fh:
        json.dump({"fitted": "2026-10-10", "chunk_words": CHUNK,
                   "about": "Bands (10th to 90th percentile of Dan's own 300-word pieces) for every measure that separates "
                            "his text from Claude's. Numbers only, no text. Refit with voice_check.py --fit.",
                   "formats": formats}, fh, indent=1)
    for k, e in formats.items():
        if k.endswith("/*"):
            continue
        top = sorted(e["measures"].items(), key=lambda kv: -kv[1]["weight"])[:10]
        print(f"{k}: {e['dan_pieces']} Dan pieces, {e['claude_pieces']} Claude; line {e['line']}; Claude median "
              f"{e['claude_median_score']}; Claude over the line {e['claude_caught_pct']}%")
        print("   " + "; ".join(f"{n} {m['claude_median']}/{m['median']} ({m['auc']})" for n, m in top))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="the draft, or - for stdin")
    ap.add_argument("--type", choices=["content", "ads", "conversion", "products"])
    ap.add_argument("--format")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--hard", action="store_true", help="hard rules only")
    ap.add_argument("--fit", action="store_true")
    a = ap.parse_args()
    if a.fit:
        return cmd_fit()
    if not a.file:
        ap.error("give a draft file (or - for stdin)")
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8", errors="replace").read()
    if a.hard:
        hard = hard_fails(text)
        for i, why, line in hard:
            print(f"line {i}: {why}: {line}")
        print(f"voice_check: {'HARD FAIL, ' + str(len(hard)) + ' hit(s)' if hard else 'hard rules OK'}")
        return 1 if hard else 0
    if not a.type:
        ap.error("--type is needed for the score (or use --hard)")
    import bank
    fmt = a.format or bank.FORMATS[a.type][0]
    r, hard, text_report = report(text, a.type, fmt)
    if a.json:
        print(json.dumps({"hard": hard, **r, "lines": lines_to_look_at(text)}, indent=1))
    else:
        print(text_report)
    return 1 if hard else (2 if r["score"] > r["line"] else 0)


if __name__ == "__main__":
    sys.exit(main())
