#!/usr/bin/env python3
"""
The sample bank: whole real passages of Dan's, and a picker that hands a writer the right few.

WHY THIS EXISTS (2026-10-10, Dan Voice P2B): the Phase A bench showed that a guide full of rules makes Claude write
tidier, not more like Dan (judges caught it 90% of the time and named "too clean" in 93% of right calls). The research
says whole passages chosen by format and length, never by topic, teach a voice better than a description of it. So the
writer gets 3 to 5 whole real passages first and writes "the next piece in this set".

Each bank passage also has a twin in `voice/contrast/`: the same content written cold by Claude from a neutral brief.
The pair shows the gap between how Claude says a thing and how Dan said it. Those pairs are the source of the rules in
the guide (the gap list, `contrast` below) and can be shown to the writer as worked examples.

    python3 scripts/voice/bank.py pick --type content --format video --words 300 -n 5     # what a writer loads
    python3 scripts/voice/bank.py pick --type ads --format ad-own --words 220 --pairs     # with Claude's cold twin
    python3 scripts/voice/bank.py list                                                    # what is in the bank
    python3 scripts/voice/bank.py build                                                   # local only, see below
    python3 scripts/voice/bank.py contrast                                                # local only: the gap list

Types and formats:
    content      video (Abs By AI, off the cuff) | video-business (2020-21 channel) | podcast | short
    ads          ad-own (he reads it) | ad-client (another presenter reads it: structure, not voice)
    conversion   sales-script (written) | sales-video (transcript of him reading his own script)
    products     book | book-business | lesson (course video transcript)

`pick` and `list` read only the repo copy (`.claude/skills/_shared/voice/bank/`), so they work in a cloud session.
`build` and `contrast` need `voice-corpus/` and the `claude` command line. `build` never takes text from the hold-out
set and the result is checked by `heldout_guard.py`.

Dashes: his 2007 book and a few scripts were typeset with en and em dashes. New copy never has one (hard rule), so the
bank shows them the way he types them himself, as a double hyphen.
"""
import argparse
import hashlib
import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus  # noqa: E402
import heldout_guard  # noqa: E402

ROOT = corpus.ROOT
BANK = os.path.join(ROOT, ".claude", "skills", "_shared", "voice", "bank")
CONTRAST = os.path.join(ROOT, ".claude", "skills", "_shared", "voice", "contrast")
WORK = os.path.join(corpus.CORPUS, "bank")
SEED = 20261010
MOVES = ["hook", "story", "mechanism", "explanation", "instruction", "proof", "offer", "close"]
FORMATS = {"content": ["video", "video-business", "podcast", "short"], "ads": ["ad-own", "ad-client"],
           "conversion": ["sales-script", "sales-video"], "products": ["book", "book-business", "lesson"]}
# how many passages of each format the bank holds (a thin format gives what it has)
QUOTA = {"video": 18, "video-business": 8, "podcast": 4, "short": 6, "ad-own": 12, "ad-client": 8,
         "sales-script": 12, "sales-video": 6, "book": 10, "book-business": 3, "lesson": 7}
FORMAT_NOTE = {
    "video": "a YouTube video, Dan talking to camera off the cuff (transcript)",
    "video-business": "a 2020-21 YouTube video for business owners, Dan talking off the cuff (transcript)",
    "podcast": "Dan as the guest on a podcast, off the cuff (transcript)",
    "short": "a complete YouTube Short he wrote for himself",
    "ad-own": "an ad script he wrote and reads himself",
    "ad-client": "an ad script he wrote for a client's presenter",
    "sales-script": "a sales video script or sales letter he wrote",
    "sales-video": "a sales video, Dan reading his own script (transcript)",
    "book": "a passage from his book",
    "book-business": "a passage from his business book",
    "lesson": "a lesson from his paid course, Dan talking to customers (transcript)",
}


def dashes(text):
    """En and em dashes the way he types them himself."""
    text = re.sub(r"(?<=\d)[–—](?=\d)", "-", text)
    return re.sub(r"[ \t]*[–—][ \t]*", " -- ", text)


def format_of(row):
    t, f = row.get("type"), row["file"]
    if t == "content":
        if row.get("format") == "short":
            return "short"
        return "podcast" if "/tlab/" in f else ("video-business" if "/old-channel/" in f else "video")
    if t == "ads":
        return "ad-own" if row.get("tier") == 1 else "ad-client"
    if t == "conversion":
        return "sales-video" if row.get("mode") == "spoken" else "sales-script"
    if "/blackbelt/" in f:
        return "lesson"
    return "book" if "/sgm/" in f else "book-business"


def bench_format(item):
    """The bank format for a bench hold-out item."""
    if item["bucket"] == "content-short":
        return "short"
    row = {"type": item["type"], "file": item["file"], "tier": item.get("tier"), "mode": item.get("mode")}
    return format_of(row)


# ---------------------------------------------------------------- read the repo copy

def parse(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    meta["words"] = int(meta.get("words", 0))
    meta["text"] = m.group(2).strip()
    return meta


def load(type_=None):
    out = []
    for t in ([type_] if type_ else corpus.TYPES):
        d = os.path.join(BANK, t)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if re.match(r"\d+\.md$", f):
                it = parse(os.path.join(d, f))
                twin = os.path.join(CONTRAST, t, f)
                if os.path.isfile(twin):
                    tw = parse(twin)
                    it["brief"], it["claude"] = split_twin(tw["text"])
                out.append(it)
    return out


def split_twin(text):
    m = re.search(r"## The content, as a neutral brief\n(.*?)\n## Claude, cold, from that brief\n(.*)", text, re.S)
    return (m.group(1).strip(), m.group(2).strip()) if m else ("", "")


def pick(type_, fmt=None, words=300, n=5, seed="", position=None, not_file=None, need_twin=False):
    """n bank passages for a piece of this type, format and length. Same format first, then the nearest length; the
    seed rotates the choice, so two drafts of the same thing see different passages. Never chosen by topic."""
    items = [i for i in load(type_) if i.get("file") != not_file and (not need_twin or i.get("claude"))]
    rng = random.Random(f"{SEED}-{type_}-{fmt}-{seed}")
    same = [i for i in items if i["format"] == fmt]
    if fmt in ("ad-own",):
        rest = [i for i in items if i["format"] != fmt]  # client ads teach structure: only as a fill
    else:
        mode = same[0]["mode"] if same else None
        rest = sorted((i for i in items if i["format"] != fmt), key=lambda i: i["mode"] != mode)

    def choose(pool_, k):
        if len(pool_) <= k:
            return list(pool_)
        # nearest length first, with a random half so the set rotates
        near = sorted(pool_, key=lambda i: abs(i["words"] - words))[:max(k * 2, k + 2)]
        got = []
        if position:
            pos = [i for i in near if i.get("position") == position]
            rng.shuffle(pos)
            got = pos[:max(1, k // 2)]
        left = [i for i in near if i not in got]
        rng.shuffle(left)
        return got + left[:k - len(got)]
    got = choose(same, n)
    if len(got) < n:
        got += choose(rest, n - len(got))
    # the closest in format and length goes last: the writer continues from it
    got.sort(key=lambda i: (i["format"] == fmt, -abs(i["words"] - words)))
    return got


def show(items, pairs=False):
    out = []
    for n, i in enumerate(items, 1):
        head = f'<piece n="{n}" what="{FORMAT_NOTE[i["format"]]}" source="{i["title"]} ({i["year"]})" move="{i["move"]}">'
        if pairs and i.get("claude"):
            out.append(f'{head}\n<brief>\n{i["brief"]}\n</brief>\n<how_an_ai_wrote_it>\n{i["claude"]}\n'
                       f'</how_an_ai_wrote_it>\n<what_dan_really_wrote>\n{i["text"]}\n</what_dan_really_wrote>\n</piece>')
        else:
            out.append(f'{head}\n{i["text"]}\n</piece>')
    return "\n\n".join(out)


# ---------------------------------------------------------------- build (local)

BRIEF_EXTRA = ('\n\nAdd one more field to the JSON: "move": the one word from this list that best names what the passage '
               'is doing: ' + ", ".join(MOVES) + ".")


EXPLICIT = re.compile(r"\b(cock|pussy|clit\w*|cum|cumming|orgasm\w*|anal|blowjob\w*|fuck(ed|ing)? (a|her|the) |penis|vagina\w*|"
                      r"nipple\w*|erection\w*|masturbat\w*|oral sex|threesome\w*)\b", re.I)  # the repo is public


def edge_window(text, spoken, rng, which, taken):
    """A window that starts at the first unit (opening) or ends at the last one (close)."""
    import bench
    us = bench.units(text, spoken)
    target = rng.randint(200, 380)
    order = us if which == "opening" else us[::-1]
    words, got = 0, []
    for s, e in order:
        got.append((s, e))
        words += corpus.count_words(text[s:e])
        if words >= target:
            break
    if not 150 <= words <= 480:
        return None
    s, e = min(g[0] for g in got), max(g[1] for g in got)
    if any(s < te and ts < e for ts, te in taken):
        return None
    return s, e, which


def candidates():
    import bench
    rng = random.Random(SEED)
    with open(heldout_guard.SHINGLES, encoding="utf-8") as fh:
        hashes = json.load(fh)["hashes"]
    held_files = {h["file"] for h in corpus.heldout_index()}
    by = {}
    for t in corpus.TYPES:
        for row, text in corpus.pile(t):
            if row.get("tier") not in (1, 2) or row.get("confidence") == "low" or row["file"].endswith("-raw.txt"):
                continue
            if row.get("authorship") == "dan-typed-lines-only":
                continue
            if t == "content" and row.get("tier") != 1:
                continue
            if t == "conversion" and row.get("tier") != 1:
                continue
            if t == "products" and row.get("topic") == "explicit-technique":
                continue
            by.setdefault(format_of(row), []).append((row, text))
    out = []
    for fmt, rows in by.items():
        rng.shuffle(rows)
        # files with no hold-out passage first, newest first for his own ads and videos, proven spend first for clients
        rows.sort(key=lambda rt: (rt[0]["file"] in held_files, -(rt[0].get("spend") or 0) if fmt == "ad-client" else 0,
                                  -(rt[0].get("year") or 0) if fmt in ("video", "ad-own") else 0))
        want = int(QUOTA[fmt] * 1.4) + 1
        taken, passes = {}, 0
        positions = ["opening", "middle", "close", "middle"]
        while want > 0 and passes < 3:
            passes += 1
            for row, text in rows:
                if want <= 0:
                    break
                spoken = row.get("mode") == "spoken"
                # steer toward a mix of openings, middles and closes
                want_pos = positions[len(out) % 4] if passes == 1 else "middle"
                w = edge_window(text, spoken, rng, want_pos, taken.get(row["file"], ())) \
                    if want_pos != "middle" and corpus.count_words(text) > 600 else None
                w = w or bench.window(text, spoken, rng, lo=150, hi=480, taken=taken.get(row["file"], ()),
                                      whole_if_short=fmt in ("short", "ad-own", "ad-client"))
                if not w or (w[2] == "whole" and row["file"] in taken):
                    continue
                s, e, pos = w
                if heldout_guard.scan_text(text[s:e], hashes) or (fmt == "book" and EXPLICIT.search(text[s:e])):
                    continue
                taken.setdefault(row["file"], []).append((s, e))
                body = dashes(bench.for_judging(text[s:e], spoken))
                item = {"type": row["type"], "format": fmt, "file": row["file"], "title": row.get("title") or "",
                        "year": row.get("year"), "mode": row.get("mode"), "tier": row.get("tier"), "position": pos,
                        "words": corpus.count_words(body), "text": body, "bucket": "", "kind": bench.kind_of(row)}
                item["key"] = hashlib.sha1((row["file"] + str(s)).encode()).hexdigest()[:10]
                out.append(item)
                want -= 1
    return out


def cmd_build(a):
    import bench
    os.makedirs(WORK, exist_ok=True)
    cpath = os.path.join(WORK, "candidates.json")
    if os.path.isfile(cpath) and not a.repick:
        with open(cpath, encoding="utf-8") as fh:
            cands = json.load(fh)
    else:
        cands = candidates()
        with open(cpath, "w", encoding="utf-8") as fh:
            json.dump(cands, fh, indent=1)
    print(f"{len(cands)} candidates", file=sys.stderr)

    def brief(c):
        path = os.path.join(WORK, "briefs", c["key"] + ".json")

        def make():
            prompt = bench.BRIEF_PROMPT.format(kind=c["kind"], passage=c["text"]) + BRIEF_EXTRA
            best = None
            for _ in range(3):
                d = bench.parse_json(bench.claude_call(prompt, bench.BRIEF_SYS, bench.WRITER_MODEL))
                leaks = bench.five_gram_leaks(d.get("brief", ""), c["text"])
                d["leaks"] = len(leaks)
                if best is None or d["leaks"] < best["leaks"]:
                    best = d
                if not leaks:
                    break
                prompt += "\n\nYour last brief reused these runs of words from the passage. Reword them: " + "; ".join(leaks[:8])
            return json.dumps(best, indent=1)
        return c["key"], json.loads(bench.cached(path, make))
    briefs = dict(bench.pool(brief, cands))
    keep, count = [], {}
    for c in cands:
        b = briefs.get(c["key"])
        if not b or not b.get("usable") or not b.get("brief") or count.get(c["format"], 0) >= QUOTA[c["format"]]:
            continue
        count[c["format"]] = count.get(c["format"], 0) + 1
        c["brief"] = b["brief"]
        c["move"] = b.get("move") if b.get("move") in MOVES else "explanation"
        keep.append(c)

    def cold(c):
        path = os.path.join(WORK, "cold", c["key"] + ".txt")
        prompt = bench.writer_prompt({"files": []}, c)
        return c["key"], bench.cached(path, lambda: bench.claude_call(prompt, "You are a writer.", bench.WRITER_MODEL))
    colds = dict(bench.pool(cold, keep))
    # publish: the repo copy
    for d in (BANK, CONTRAST):
        for t in corpus.TYPES:
            os.makedirs(os.path.join(d, t), exist_ok=True)
            for f in os.listdir(os.path.join(d, t)):
                if re.match(r"\d+\.md$", f):
                    os.remove(os.path.join(d, t, f))
    nums = {}
    for c in sorted(keep, key=lambda c: (c["type"], FORMATS[c["type"]].index(c["format"]), c["file"])):
        if c["key"] not in colds:
            continue
        nums[c["type"]] = nums.get(c["type"], 0) + 1
        name = f"{nums[c['type']]:02d}.md"
        meta = "\n".join(f"{k}: {c[k]}" for k in ("type", "format", "move", "position", "words", "mode", "year", "tier",
                                                   "title", "file"))
        with open(os.path.join(BANK, c["type"], name), "w", encoding="utf-8") as fh:
            fh.write(f"---\n{meta}\n---\n{c['text'].strip()}\n")
        spoken = c["mode"] == "spoken"
        cold_text = dashes(bench.for_judging(colds[c["key"]], spoken))
        with open(os.path.join(CONTRAST, c["type"], name), "w", encoding="utf-8") as fh:
            fh.write(f"---\n{meta}\nnote: NOT Dan. The same content as bank/{c['type']}/{name}, written cold by Claude "
                     f"from the brief. Kept to show the gap.\n---\n## The content, as a neutral brief\n{c['brief'].strip()}\n\n"
                     f"## Claude, cold, from that brief\n{cold_text.strip()}\n")
    print("bank:", {t: nums.get(t, 0) for t in corpus.TYPES}, "| by format:", count)


def cmd_list(a):
    items = load(a.type)
    by = {}
    for i in items:
        by.setdefault((i["type"], i["format"]), []).append(i)
    for (t, f), its in sorted(by.items()):
        moves = {}
        for i in its:
            moves[i["move"]] = moves.get(i["move"], 0) + 1
        print(f"{t:11s} {f:15s} {len(its):3d} passages, {sum(i['words'] for i in its):6d} words  "
              + ", ".join(f"{m} {n}" for m, n in sorted(moves.items(), key=lambda kv: -kv[1])))


def cmd_pick(a):
    items = pick(a.type, a.format, a.words, a.n, seed=a.seed, position=a.position, need_twin=a.pairs)
    print(show(items, pairs=a.pairs))


# ---------------------------------------------------------------- contrast: the gap list (local)

GAP_SYS = "You are an expert editor comparing two writers. You answer with JSON only."
GAP_PROMPT = """Below are {n} pairs. In each pair the SAME content was written twice: once by Dan Rose (the real one: {what}) and once by an AI assistant working cold from a neutral brief of the content.

List the recurring differences between how the AI says things and how Dan says them. I want what the AI does that Dan does not, and what Dan does that the AI does not: word choice, small everyday words, how sentences start and join, repeats, sentence length and its spread, paragraphing, punctuation and typing habits, how blunt or hedged a claim is, where the instruction sits relative to the caveat, how a list is said, how a piece opens and ends.

Rules:
- Only differences that show in at least 3 pairs. Count the pairs honestly.
- Each one concrete enough to check in a draft. No vague words like "more natural" or "more authentic".
- Give one short example from each side (10 words at most each), copied exactly.
- Rank by how many pairs show it.

Answer with JSON only: {{"gaps": [{{"gap": "one sentence: the AI does X where Dan does Y", "pairs": how many of the {n} pairs show it, "ai_example": "...", "dan_example": "...", "kind": one of "word choice", "small words", "sentence shape", "repeats", "structure", "punctuation", "tone", "openings and endings"}}]}}

{pairs}
"""


def cmd_contrast(a):
    import bench
    import voice_stats
    L = ["# Contrastive extraction: Claude cold against Dan, same content (2026-10-10, Voice P2B step B1)", "",
         "For every passage in the sample bank (`.claude/skills/_shared/voice/bank/`, none of it held out) a fresh Claude",
         "wrote the same content cold from a neutral brief (`voice/contrast/`). This is the gap between the two, by",
         "format: first what a fresh Claude reader found in the pairs, ranked by how many pairs show it, then the",
         "counts. These gap lists, not a description from reading, are the source of the rules in the guide and of the",
         "bands in `scripts/voice/voice_check.py`.", ""]
    allgaps = {}
    for t in corpus.TYPES:
        for fmt in FORMATS[t]:
            items = [i for i in load(t) if i["format"] == fmt and i.get("claude")]
            if len(items) < 3:
                continue
            pairs = "\n\n".join(f"=== PAIR {n} ===\nDAN:\n{i['text']}\n\nAI:\n{i['claude']}" for n, i in enumerate(items, 1))
            path = os.path.join(WORK, "gaps", f"{t}-{fmt}.json")
            raw = bench.cached(path, lambda: bench.claude_call(
                GAP_PROMPT.format(n=len(items), what=FORMAT_NOTE[fmt], pairs=pairs), GAP_SYS, bench.WRITER_MODEL))
            gaps = sorted(bench.parse_json(raw).get("gaps", []), key=lambda g: -int(g.get("pairs", 0)))
            allgaps[f"{t}/{fmt}"] = gaps
            L += [f"## {t}: {fmt} ({len(items)} pairs)", "", "| pairs | kind | the gap | Claude | Dan |", "|---:|---|---|---|---|"]
            for g in gaps:
                cl = lambda s: str(s or "").replace("|", "/").replace("\n", " ")
                L.append(f"| {g.get('pairs')} of {len(items)} | {cl(g.get('kind'))} | {cl(g.get('gap'))} | "
                         f"{cl(g.get('ai_example'))} | {cl(g.get('dan_example'))} |")
            dan = "\n\n".join(i["text"] for i in items)
            ai = "\n\n".join(i["claude"] for i in items)
            md, ma = voice_stats.measure(dan), voice_stats.measure(ai)
            sd, sa = voice_stats.small_words(dan), voice_stats.small_words(ai)
            L += ["", "Counts (per 100 words; small words per 1,000), Dan / Claude: "
                  + "; ".join(f"{k} {md[k]} / {ma[k]}" for k in ("and", "lists3", "questions", "contractions", "sent_mean",
                                                               "sent_sd", "para_words", "punch_pct", "oneline_pct"))
                  + ". Small words furthest apart: "
                  + "; ".join(f"\"{w}\" {sd[w]} / {sa[w]}" for w in sorted(sd, key=lambda w: -abs(sd[w] - sa[w]))[:10]) + ".", ""]
    out = os.path.join(ROOT, "Docs", "voice-bench", "2026-10-10-contrast.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L).replace("—", ", ").replace("–", "-") + "\n")
    with open(os.path.join(WORK, "gaps", "all.json"), "w", encoding="utf-8") as fh:
        json.dump(allgaps, fh, indent=1)
    print("wrote", os.path.relpath(out, ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build"); p.add_argument("--repick", action="store_true"); p.set_defaults(fn=cmd_build)
    p = sub.add_parser("list"); p.add_argument("--type"); p.set_defaults(fn=cmd_list)
    p = sub.add_parser("contrast"); p.set_defaults(fn=cmd_contrast)
    p = sub.add_parser("pick")
    p.add_argument("--type", required=True, choices=corpus.TYPES)
    p.add_argument("--format", help="see the list at the top; default: the type's first format")
    p.add_argument("--words", type=int, default=300)
    p.add_argument("-n", type=int, default=5)
    p.add_argument("--position", choices=["opening", "middle", "close", "whole"])
    p.add_argument("--seed", default="", help="any text; a different seed rotates the choice")
    p.add_argument("--pairs", action="store_true", help="also show the brief and Claude's cold version of each")
    p.set_defaults(fn=cmd_pick)
    a = ap.parse_args()
    if a.cmd == "pick" and not a.format:
        a.format = FORMATS[a.type][0]
    a.fn(a)


if __name__ == "__main__":
    main()
