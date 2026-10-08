#!/usr/bin/env python3
"""
The voice bench: can a judge tell Dan's real writing from Claude's imitation of it?

WHY THIS EXISTS (2026-10-08, Dan Voice P2A): until now nothing measured whether the voice guide works. Dan's goal is
"nobody ever thinks this is AI", so the test is a blind one. For each held-out passage of real Dan, a fresh Claude
writes the same content from a neutral brief under a named SETUP (what it is allowed to see). Then two judges, a fresh
Claude and Gemini, each get 8 real reference passages of the same type plus the real / generated pair in random order
and must pick the AI one. Chance is 50 percent. The finish line is 60 percent or less. Every change to the guide gets
scored here, and only what moves the number is kept.

Local only: it needs `voice-corpus/` (git-ignored, mirrored to Drive folder `1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`), the
`claude` command line on Dan's subscription, and `GEMINI_API_KEY` in `~/.absbyai-secrets.env`.

Steps (each is resumable; finished calls are cached on disk):
    python3 scripts/voice/bench.py pick                  # choose hold-out candidates (once; do not re-run casually)
    python3 scripts/voice/bench.py briefs                # a content-only brief per candidate, and a usability check
    python3 scripts/voice/bench.py finalize              # lock the set: index, HELD-OUT.md, the guard's hash file
    python3 scripts/voice/bench.py repair                # fix speech-to-text mis-hearings in the spoken passages (once)
    python3 scripts/voice/bench.py run --setup guide     # write, judge, report -> Docs/voice-bench/<date>-guide.md
    python3 scripts/voice/bench.py blind --setup guide   # 20 pairs for Dan's blind page, and the answer key

Setups live in `scripts/voice/bench_setups.json`: a name, the files the writer may read, and the layout of its prompt.
Add one per idea in Phase B and compare reports.

The reports in `Docs/voice-bench/` carry numbers and the judges' reasons only. No held-out text ever goes in the repo.
"""
import argparse
import concurrent.futures as cf
import datetime
import glob
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus  # noqa: E402
import heldout_guard  # noqa: E402
import voice_fingerprint as vf  # noqa: E402
import voice_stats  # noqa: E402

ROOT = corpus.ROOT
HELD = os.path.join(corpus.CORPUS, "heldout")
BENCH = os.path.join(corpus.CORPUS, "bench")
SETUPS = os.path.join(ROOT, "scripts", "voice", "bench_setups.json")
REPORTS = os.path.join(ROOT, "Docs", "voice-bench")
HELD_MD = os.path.join(ROOT, ".claude", "skills", "_shared", "voice", "HELD-OUT.md")

WRITER_MODEL = "claude-opus-5-5"
JUDGE_MODEL = "claude-opus-5-5"
GEMINI_MODEL = "gemini-3.1-pro-preview"
GEMINI_PRICE = (2.0, 12.0)  # dollars per million tokens in / out (output includes thinking); checked 2026-10-08
MIN_TRIALS = 80
SEED = 20261008

# shorts are thin (nine scripts that are wholly Dan's), so 4 are held out, not 6, and long-form carries 12
QUOTA = {"content-long": 12, "content-short": 4, "ads": 10, "conversion": 6, "products": 8}
BLIND_QUOTA = {"content": 8, "ads": 5, "conversion": 3, "products": 4}
CUES = ["vocabulary", "sentence_rhythm", "too_clean_grammar", "safe_generic_content", "over_explaining", "tidy_ending",
        "structure_too_organized", "punctuation_formatting", "missing_small_words_or_filler", "tone_hedged_or_polite",
        "performs_the_voice", "facts_or_specifics", "other"]

IDENTITY = ("Dan Rose is a 41-year-old fitness creator, the face of Abs By AI (absbyai.com). Earlier he co-built Six "
            "Pack Shortcuts and ran a YouTube ad agency, Social Response Marketing.")


# ---------------------------------------------------------------- model calls

def claude_bin():
    env = os.environ.get("VOICE_BENCH_CLAUDE")
    if env:
        return env
    apps = glob.glob(os.path.expanduser(
        "~/Library/Application Support/Claude/claude-code/*/*/claude.app/Contents/MacOS/claude"))
    if apps:  # the desktop app's copy is kept current; the PATH one may be too old for the newest model
        ver = lambda p: [int(x) for x in re.findall(r"\d+", p.split("/claude-code/")[1].split("/")[0])]
        return sorted(apps, key=ver)[-1]
    return "claude"


def claude_call(prompt, system, model):
    """One fresh Claude with no tools, no project rules and no memory. Returns its text."""
    cold = os.path.join(tempfile.gettempdir(), "voice-bench-cold")
    os.makedirs(cold, exist_ok=True)
    cmd = [claude_bin(), "-p", "--model", model, "--system-prompt", system, "--tools", "", "--setting-sources", "",
           "--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence", "--output-format", "json"]
    last = ""
    for _ in range(3):
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cold, timeout=600)
        raw = p.stdout
        try:
            d = json.loads(raw[raw.index("{"):])
            if not d.get("is_error") and d.get("result"):
                return d["result"].strip()
            last = str(d.get("result"))[:300]
        except ValueError:
            last = (raw or p.stderr)[:300]
    raise RuntimeError("claude call failed: " + last)


def secret(name):
    with open(os.path.expanduser("~/.absbyai-secrets.env"), encoding="utf-8") as fh:
        for line in fh:
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError(name + " not in ~/.absbyai-secrets.env")


def gemini_call(prompt):
    """Returns (text, input tokens, output tokens)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2,
                                 "thinkingConfig": {"thinkingLevel": "low"}},
            # his book is a sex and dating guide: without this Gemini returns nothing for some product pairs
            "safetySettings": [{"category": c, "threshold": "BLOCK_NONE"} for c in (
                "HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "HARM_CATEGORY_DANGEROUS_CONTENT")]}
    last = ""
    for _ in range(4):
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json", "x-goog-api-key": secret("GEMINI_API_KEY")})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            if not d.get("candidates"):
                raise RuntimeError("no answer: " + json.dumps(d.get("promptFeedback", d))[:200])
            text = "".join(p.get("text", "") for p in d["candidates"][0]["content"].get("parts", []))
            u = d.get("usageMetadata", {})
            out = u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)
            return text.strip(), u.get("promptTokenCount", 0), out
        except Exception as e:  # rate limit or a blip: try again
            last = str(e)[:300]
    raise RuntimeError("gemini call failed: " + last)


def parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON in reply: " + text[:200])
    return json.loads(m.group(0))


def cached(path, make):
    if os.path.isfile(path) and os.path.getsize(path):
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    val = make()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(val)
    return val


def pool(fn, items, workers=5):
    out = []
    with cf.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(fn, it): it for it in items}
        for i, f in enumerate(cf.as_completed(futs), 1):
            try:
                out.append(f.result())
            except Exception as e:
                print(f"  FAILED {futs[f] if isinstance(futs[f], str) else ''}: {e}", file=sys.stderr)
            if i % 10 == 0 or i == len(futs):
                print(f"  {i}/{len(futs)}", file=sys.stderr)
    return out


# ---------------------------------------------------------------- text windows

SENT = re.compile(r"[^.!?\n]+(?:[.!?]+[\"')\]]*|\n|$)\s*")


def units(text, spoken):
    """[(start, end)] of sentences (spoken) or paragraphs (written)."""
    spans = []
    if spoken:
        for m in SENT.finditer(text):
            if corpus.count_words(m.group(0)):
                spans.append((m.start(), m.end()))
    else:
        for m in re.finditer(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", text):
            if corpus.count_words(m.group(0)):
                spans.append((m.start(), m.end()))
    return spans


def window(text, spoken, rng, lo=150, hi=450, taken=(), banned=None, whole_if_short=False):
    """A run of whole sentences or paragraphs of lo..hi words. Returns (start, end, position) or None."""
    total = corpus.count_words(text)
    us = units(text, spoken)
    if not us:
        return None
    if whole_if_short and total <= hi:
        if total < 110 or (banned and banned(heldout_guard.shingles(text[us[0][0]:us[-1][1]]))):
            return None
        return us[0][0], us[-1][1], "whole"
    for _ in range(60):
        i = rng.randrange(len(us))
        target = rng.randint(max(lo + 40, 220), min(hi - 40, 400))
        j, words = i, 0
        while j < len(us) and words < target:
            words += corpus.count_words(text[us[j][0]:us[j][1]])
            j += 1
        if not lo <= words <= hi:
            continue
        s, e = us[i][0], us[j - 1][1]
        if any(s < te and ts < e for ts, te in taken):
            continue
        if banned and banned(heldout_guard.shingles(text[s:e])):
            continue
        pos = "opening" if i == 0 else ("close" if j == len(us) else "middle")
        return s, e, pos
    return None


def shared_shingles():
    """8-word runs already quoted in the guide and example files: a hold-out passage must not contain one."""
    out = set()
    for f in heldout_guard.files_under(heldout_guard.DEFAULT[0]):
        with open(f, encoding="utf-8", errors="replace") as fh:
            out |= heldout_guard.shingles(fh.read())
    return out


FILLER = re.compile(r"\b(um+|uh+|er+m?|ah+|hmm+|mm+)\b[,.]?\s*", re.I)


def for_judging(text, spoken):
    """The same clean-up for the real and the generated side, so layout and transcript noise are not the tell."""
    text = corpus.normalize(text).strip()
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s+", "", text)          # markdown headings
    text = re.sub(r"(\*\*|__)(.+?)\1", r"\2", text)            # bold
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", text)  # italics
    text = re.sub(r"(?m)^\s*(-{3,}|\*{3,})\s*$", "", text)     # rules
    text = re.sub(r"[ \t]+", " ", text)
    if not spoken:
        return re.sub(r"\n{3,}", "\n\n", text)
    text = FILLER.sub("", text)
    text = re.sub(r"\b(\w+)( \1\b)+", r"\1", text, flags=re.I)  # stutters: "the the"
    text = re.sub(r"\s+", " ", text)
    sents = [m.group(0).strip() for m in SENT.finditer(text) if m.group(0).strip()]
    return "\n\n".join(" ".join(sents[i:i + 4]) for i in range(0, len(sents), 4))


# ---------------------------------------------------------------- pick

def kind_of(row):
    """What the writer is told the piece is. Content context only, no style hints."""
    t, mode, f = row.get("type"), row.get("mode"), row["file"]
    title = row.get("title") or os.path.basename(f)
    if t == "content":
        if "/tlab/" in f:
            return (f"part of Dan's answers as the guest on a podcast interview ({row.get('year')}), speaking off the "
                    "cuff. Write the verbatim transcript of what he says.")
        if row.get("format") == "short":
            return (f'a complete YouTube Short titled "{title}" (under a minute, Dan talking to camera with no '
                    "script). Write the verbatim transcript of what he says.")
        return (f'part of a YouTube video titled "{title}" ({row.get("year")}). Dan is talking to camera from bullet '
                "points, with no script. Write the verbatim transcript of what he says.")
    if t == "ads":
        who = "for himself to read on camera" if row.get("tier") == 1 else \
            f"for a client ({row.get('client', 'a health company')}); another presenter reads it on camera"
        return f'part of a YouTube ad script ("{title}", {row.get("year")}) that Dan wrote {who}.'
    if t == "conversion":
        return f'part of a sales video script or sales letter ("{title}", {row.get("year")}) that Dan wrote.'
    if mode == "spoken":
        return (f'part of a lesson video from Dan\'s paid course ("{title}", {row.get("year")}), him talking to '
                "customers. Write the verbatim transcript of what he says.")
    return f'a passage from Dan\'s book ("{title}", {row.get("year")}).'


def bucket_files():
    """{bucket: [(group, row)]} with the groups in priority order."""
    rows = corpus.manifest()
    is_short = lambda r: r.get("format") == "short"
    b = {k: [] for k in QUOTA}
    for r in rows:
        t, tier, f = r.get("type"), r.get("tier"), r["file"]
        if (r.get("authorship") == "dan-typed-lines-only" and r.get("type") != "conversion") or r.get("heldout_overlap") \
                or r.get("confidence") == "low" or r["file"].endswith("-raw.txt"):
            continue  # loose lines, text shared with a blind-test piece, unsure authorship, raw rolls full of retakes
        if t == "content" and tier == 1:
            if is_short(r):
                b["content-short"].append(("absbyai-short", r))
            else:
                g = "tlab" if "/tlab/" in f else ("old-channel" if "/old-channel/" in f else "absbyai")
                b["content-long"].append((g, r))
        elif t == "ads" and tier in (1, 2):
            b["ads"].append(("heldout" if r.get("heldout") else f"tier{tier}", r))
        elif t == "conversion" and tier == 1:
            b["conversion"].append(("tier1", r))
        elif t == "products":
            if "/sgm/" in f and r.get("topic") != "explicit-technique":
                b["products"].append(("sgm", r))
            elif "/blackbelt/" in f:
                b["products"].append(("blackbelt", r))
            elif tier == 2:
                b["products"].append(("15steps", r))
    return b


# Files to try first, per group (substring of the file name, in order), so each type's hold-out is spread across its
# sources instead of bunching in whatever sorts first. Everything else follows, newest first.
PREFER = {
    "tier1@ads": ["ad1-written", "ad3-written", "book-ad-the-top-5", "book-ad-how-to-start", "shorts-ad-fire-your-trainer",
                  "shorts-ad-top-3-tips", "shorts-ad-ai-took-my-job"],
    "tier1@conversion": ["2019-consulting-sales-video", "2021-black-belt-cart-page", "2026-absbyai-sales-letter",
                         "2019-dr-marketing-website-vsl-script", "2021-black-belt-sales-video-outline",
                         "2020-15-steps-book-sales-page", "2020-used-youtube-advertising", "2026-absbyai-new-start-vsl",
                         "2020-15-steps-launch-video-8", "2021-black-belt-pre-sales"],
    "sgm@products": ["03-my-story", "10a-immersion-mindset", "26-bedroom-mentality", "31-testosterone", "07a-dominance",
                     "05-four-archetypes", "04-four-principles", "32-finding-the-right-girl", "45-final-words"],
    "blackbelt@products": ["ten-pillars-of-great-campaign-management-part-1", "turn-your-youtube-profits", "ltv-and",
                           "targeting-ladder", "modern-branding"],
}


def ordered(rows, group, bucket, rng):
    rows = [r for r in rows if not (r.get("spend") and not r.get("heldout"))]  # the top-spend ads stay as examples
    rng.shuffle(rows)
    if bucket == "ads" and group == "tier2":
        # the oldest, proven client work first (HBI, the top account), then the later clients; 2025 last
        rank = {"HBI": 0, "Spy Briefing": 1, "CPA offers": 2, "Physio Tru": 3}
        rows.sort(key=lambda r: (r.get("confidence") == "medium", (r.get("year") or 0) >= 2025,
                                 rank.get(r.get("client"), 4)))
        mixed, by = [], {}
        for r in rows:
            by.setdefault(r.get("client"), []).append(r)
        while any(by.values()):  # deal in turn so no client fills the set; HBI twice per round
            for c in ["HBI", "Spy Briefing", "HBI", "CPA offers", "Physio Tru"] + [c for c in by if c not in rank]:
                if by.get(c):
                    mixed.append(by[c].pop(0))
        return mixed
    rows.sort(key=lambda r: -(r.get("year") or 0))
    pref = PREFER.get(f"{group}@{bucket}", [])
    first = [r for p in pref for r in rows if p in r["file"]]
    return first + [r for r in rows if r not in first]


# how many of each bucket come from each group (candidates are over-picked by EXTRA to allow for unusable ones)
SPLIT = {"content-long": {"absbyai": 8, "old-channel": 3, "tlab": 1},
         "content-short": {"absbyai-short": 4},
         "ads": {"heldout": 1, "tier1": 4, "tier2": 5},
         "conversion": {"tier1": 6},
         "products": {"sgm": 5, "blackbelt": 2, "15steps": 1}}
EXTRA = 1.5


def cmd_pick(a):
    if os.path.isfile(os.path.join(HELD, "index.json")) and not a.force:
        sys.exit("a locked hold-out set already exists (voice-corpus/heldout/index.json). Re-picking changes every "
                 "later score; pass --force only if you mean it.")
    rng = random.Random(SEED)
    quoted = shared_shingles()
    # ad scripts share closes and whole sections across versions: a passage that also sits in another file is not
    # really held out, so any window with an 8-word run found in a second corpus file is rejected
    where = {}
    for r in corpus.manifest():
        if r.get("tier") in (1, 2, 3):
            for x in heldout_guard.shingles(corpus.read(r)):
                where.setdefault(x, set()).add(r["file"])
    cands = []
    for bucket, pairs in bucket_files().items():
        for group, want in SPLIT[bucket].items():
            rows = ordered([r for g, r in pairs if g == group], group, bucket, rng)
            need = math.ceil(want * EXTRA) if group != "heldout" else 1
            taken = {}
            passes = 0
            while need > 0 and rows and passes < 6:
                passes += 1
                for r in rows:
                    if need <= 0:
                        break
                    text = corpus.read(r)
                    spoken = r.get("mode") == "spoken"
                    here = r["file"]
                    # nothing already quoted in a guide file; at most 15% shared with other corpus files (a stock
                    # call to action is fine, a second copy of the passage is not)
                    banned = lambda sh: bool(sh & quoted) or \
                        sum(1 for x in sh if where.get(x, set()) - {here}) > 0.15 * max(1, len(sh))
                    if r.get("heldout"):
                        banned = None  # the one piece held out since Part 1; its look-alikes are flagged instead
                    w = window(text, spoken, rng, taken=taken.get(r["file"], ()), banned=banned,
                               whole_if_short=(bucket in ("content-short", "ads")))
                    if not w or (w[2] == "whole" and r["file"] in taken):
                        continue
                    s, e, pos = w
                    taken.setdefault(r["file"], []).append((s, e))
                    cands.append({"bucket": bucket, "group": group, "type": r["type"], "file": r["file"], "start": s,
                                  "end": e, "position": pos, "words": corpus.count_words(text[s:e]),
                                  "tier": r.get("tier"), "year": r.get("year"), "mode": r.get("mode"),
                                  "audience": r.get("audience"), "title": r.get("title"), "kind": kind_of(r)})
                    need -= 1
            if need > 0:
                print(f"  thin: {bucket}/{group} is short by {need} candidate(s)", file=sys.stderr)
    for i, c in enumerate(cands):
        c["cid"] = f"c{i:03d}"
    os.makedirs(os.path.join(HELD, "candidates"), exist_ok=True)
    for c in cands:
        row = next(r for r in corpus.manifest() if r["file"] == c["file"])
        with open(os.path.join(HELD, "candidates", c["cid"] + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(corpus.read(row)[c["start"]:c["end"]].strip() + "\n")
    with open(os.path.join(HELD, "candidates.json"), "w", encoding="utf-8") as fh:
        json.dump(cands, fh, indent=1)
    tally = {}
    for c in cands:
        tally[c["bucket"]] = tally.get(c["bucket"], 0) + 1
    print("candidates:", tally)


# ---------------------------------------------------------------- briefs

BRIEF_SYS = "You write neutral content briefs. You answer with JSON only."
BRIEF_PROMPT = """Below is a passage by a writer or speaker. Write a CONTENT-ONLY BRIEF of it for another writer who will never see the passage and must write the same content from your brief alone.

Rules for the brief:
- Your own neutral, plain wording. Never reuse a run of 4 or more words from the passage. No quotations.
- Say nothing about style, tone, rhythm, word choice, humour or swearing. Content only.
- Include every fact, number, name, example, claim, instruction and step, in the order the passage makes them, as 4 to 12 short bullets under the line "Points, in order:".
- Then one line starting "The point:" with what the passage is trying to get across or get the audience to do.
- If the passage addresses a particular audience or is read by a named presenter, say so in one line starting "Who:".

Also decide whether the passage can be used in a writing test. It is NOT usable if it is mostly not prose (a list of links, numbers or headings), contains a second speaker's words, is too garbled to follow, makes no sense without what came before it, or is explicit sexual instruction.

Answer with JSON only: {{"usable": true or false, "reason": "a few words", "brief": "the brief as plain text with line breaks"}}

What the passage is: {kind}

PASSAGE:
{passage}
"""


def five_gram_leaks(brief, passage):
    t = heldout_guard.toks(passage)
    grams = {" ".join(t[i:i + 5]) for i in range(len(t) - 4)}
    b = heldout_guard.toks(brief)
    return [g for g in (" ".join(b[i:i + 5]) for i in range(len(b) - 4)) if g in grams]


def cmd_briefs(a):
    with open(os.path.join(HELD, "candidates.json"), encoding="utf-8") as fh:
        cands = json.load(fh)

    def one(c):
        path = os.path.join(HELD, "candidate-briefs", c["cid"] + ".json")
        with open(os.path.join(HELD, "candidates", c["cid"] + ".txt"), encoding="utf-8") as fh:
            passage = fh.read()

        def make():
            prompt = BRIEF_PROMPT.format(kind=c["kind"], passage=passage)
            best = None
            for attempt in range(3):
                d = parse_json(claude_call(prompt, BRIEF_SYS, WRITER_MODEL))
                leaks = five_gram_leaks(d.get("brief", ""), passage)
                d["leaks"] = len(leaks)
                if best is None or d["leaks"] < best["leaks"]:
                    best = d
                if not leaks:
                    break
                prompt += "\n\nYour last brief reused these runs of words from the passage. Reword them: " + "; ".join(leaks[:8])
            return json.dumps(best, indent=1)
        cached(path, make)
        return c["cid"]

    pool(one, cands)
    ok = 0
    for c in cands:
        with open(os.path.join(HELD, "candidate-briefs", c["cid"] + ".json"), encoding="utf-8") as fh:
            ok += bool(json.load(fh).get("usable"))
    print(f"briefs written: {len(cands)}; usable: {ok}")


# ---------------------------------------------------------------- finalize

def cmd_finalize(a):
    if os.path.isfile(os.path.join(HELD, "index.json")) and not a.force:
        sys.exit("already locked. --force re-locks from the candidates (changes every later score).")
    with open(os.path.join(HELD, "candidates.json"), encoding="utf-8") as fh:
        cands = json.load(fh)
    drop = set((a.drop or "").split(",")) - {""}
    index, short = [], []
    for bucket, quota in QUOTA.items():
        got = []
        split = dict(SPLIT[bucket])
        usable = []
        for c in cands:
            if c["bucket"] != bucket or c["cid"] in drop:
                continue
            with open(os.path.join(HELD, "candidate-briefs", c["cid"] + ".json"), encoding="utf-8") as fh:
                b = json.load(fh)
            if b.get("usable") and b.get("brief"):
                usable.append((c, b))
        for c, b in usable:  # first pass: honour the group split
            if split.get(c["group"], 0) > 0:
                split[c["group"]] -= 1
                got.append((c, b))
        for c, b in usable:  # second pass: fill what a thin group left open
            if len(got) >= quota:
                break
            if (c, b) not in got:
                got.append((c, b))
        got = got[:quota]
        if len(got) < quota:
            short.append(f"{bucket}: {len(got)} of {quota}")
        for n, (c, b) in enumerate(got, 1):
            item = {k: c[k] for k in ("bucket", "group", "type", "file", "start", "end", "position", "words", "tier",
                                      "year", "mode", "audience", "title", "kind")}
            item["id"] = f"{bucket}-{n:02d}"
            item["brief"] = b["brief"]
            item["_cid"] = c["cid"]
            index.append(item)
    os.makedirs(os.path.join(HELD, "passages"), exist_ok=True)
    for item in index:
        with open(os.path.join(HELD, "candidates", item.pop("_cid") + ".txt"), encoding="utf-8") as fh:
            text = fh.read()
        with open(os.path.join(HELD, "passages", item["id"] + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(text)
    with open(os.path.join(HELD, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=1)
    heldout_guard.build()
    write_held_md(index, short)
    print(f"locked {len(index)} passages" + (f"; thin: {', '.join(short)}" if short else ""))


def write_held_md(index, short):
    lines = ["# The hold-out set (locked 2026-10-08)", "",
             "Real passages of Dan's that the voice bench (`scripts/voice/bench.py`) uses as the \"real\" side of every",
             "blind pair. **Never quote, paraphrase closely or summarize any of them in a guide, an example file, a skill,",
             "a prompt or a memory entry.** They are listed by source and position only; the text is in",
             "`voice-corpus/heldout/` on the Mac and in the Drive mirror, never in this repo.",
             "`python3 scripts/voice/heldout_guard.py` fails if a file under `.claude/skills/_shared/` contains an 8-word",
             "run from any of them. Run it after editing any voice file.", "",
             "Whole files flagged held out in the corpus manifest (the HBI \"Five Foods To Avoid\" script) are off limits",
             "from end to end, not only the passage listed here.", ""]
    if short:
        lines += ["Thin spots (fewer passages than planned, because there is not enough pure material yet): "
                  + "; ".join(short) + ".", ""]
    lines += ["| id | type | source file (under `voice-corpus/`) | position | words | tier | year | spoken or written |",
              "|---|---|---|---|---:|---:|---:|---|"]
    for it in index:
        row = next((r for r in corpus.manifest() if r["file"] == it["file"]), None)
        text = corpus.read(row) if row else ""
        before = corpus.count_words(text[:it["start"]])
        lines.append(f"| {it['id']} | {it['type']} | `{it['file']}` | words {before + 1} to {before + it['words']} "
                     f"({it['position']}) | {it['words']} | {it['tier']} | {it['year']} | {it['mode']} |")
    with open(HELD_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------- generate

def load_index():
    with open(os.path.join(HELD, "index.json"), encoding="utf-8") as fh:
        return json.load(fh)


def passage(item, repaired=False):
    """The real passage. `repaired` gives the copy with speech-to-text mis-hearings fixed, where one exists."""
    fixed = os.path.join(HELD, "passages-repaired", item["id"] + ".txt")
    if repaired and os.path.isfile(fixed):
        with open(fixed, encoding="utf-8") as fh:
            return fh.read().strip()
    with open(os.path.join(HELD, "passages", item["id"] + ".txt"), encoding="utf-8") as fh:
        return fh.read().strip()


REPAIR_SYS = "You repair speech-to-text transcripts. You output only the repaired transcript."
REPAIR_PROMPT = """This is a machine transcript of a man speaking ({kind_short}). The machine mis-heard some words and put some full stops and commas in the wrong place.

Fix ONLY these two things:
1. A word or name the machine clearly mis-heard (for example a product name spelled as two unrelated words). Replace it with what he obviously said.
2. Punctuation and capitals that are plainly wrong (a sentence broken in the middle, a missing full stop between two sentences).

Change NOTHING else. Keep every word he said, in the same order: his filler, his repeats, his loose grammar, his run-on sentences, his slang. Do not improve, tidy, shorten or rephrase anything. If you are not sure a word was mis-heard, leave it.

Output only the repaired transcript.

TRANSCRIPT:
{text}
"""


def cmd_repair(a):
    """Speech-to-text errors give the real side away for a reason that has nothing to do with voice. Fix them once."""
    import difflib
    os.makedirs(os.path.join(HELD, "passages-repaired"), exist_ok=True)
    todo = [it for it in load_index() if it["mode"] == "spoken"]

    def one(it):
        path = os.path.join(HELD, "passages-repaired", it["id"] + ".txt")
        raw = passage(it)

        def make():
            out = claude_call(REPAIR_PROMPT.format(kind_short=it["kind"].split(". Write the verbatim")[0][:160], text=raw),
                              REPAIR_SYS, WRITER_MODEL)
            a_, b_ = heldout_guard.toks(raw), heldout_guard.toks(out)
            changed = 1 - difflib.SequenceMatcher(None, a_, b_, autojunk=False).ratio()
            return out if changed <= 0.04 else raw  # more than 4% of words changed is a rewrite: keep the original
        cached(path, make)
        a_, b_ = heldout_guard.toks(raw), heldout_guard.toks(passage(it, True))
        return it["id"], round(100 * (1 - difflib.SequenceMatcher(None, a_, b_, autojunk=False).ratio()), 1)
    for pid, pct_changed in sorted(pool(one, todo)):
        print(f"  {pid}: {pct_changed}% of words changed")


def load_setup(name):
    with open(SETUPS, encoding="utf-8") as fh:
        setups = json.load(fh)
    if name not in setups:
        sys.exit(f"no setup '{name}' in {os.path.relpath(SETUPS, ROOT)}; have: {', '.join(setups)}")
    return setups[name]


def setup_context(setup, item):
    """The files this setup lets the writer read, as one block. `{type}` in a path is the passage's type."""
    parts = []
    for pat in setup.get("files", []):
        for f in sorted(glob.glob(os.path.join(ROOT, pat.replace("{type}", item["type"])))):
            if os.path.basename(f) in ("HELD-OUT.md",):
                continue
            with open(f, encoding="utf-8") as fh:
                body = fh.read()
            if setup.get("sections", {}).get(os.path.basename(f)):
                m = re.search(setup["sections"][os.path.basename(f)], body, re.S)
                body = m.group(0) if m else body
            parts.append(f"<file path=\"{os.path.relpath(f, ROOT)}\">\n{body.strip()}\n</file>")
    return "\n\n".join(parts)


def writer_prompt(setup, item):
    ctx = setup_context(setup, item)
    task = (f"Write the following piece as Dan Rose.\n\n{IDENTITY}\n\nWhat it is: {item['kind']}\n"
            f"Where in the piece: {item['position']}.\nLength: about {item['words']} words (stay within 10 percent).\n\n"
            f"Content brief. Say all of it and add no new facts:\n{item['brief']}\n\n"
            "Output only the piece itself: no title, no notes, no stage directions, no quotation marks around it.")
    if not ctx:
        return task
    lead = setup.get("lead", "Everything you know about how Dan Rose writes and talks is in these files. Read them "
                             "first and write the piece so that people who know him would believe he wrote it.")
    return f"{lead}\n\n{ctx}\n\n---\n\n{task}"


def run_dir(setup_name, date):
    return os.path.join(BENCH, f"{date}-{setup_name}")


def generate(setup_name, date):
    setup = load_setup(setup_name)
    index = load_index()
    d = run_dir(setup_name, date)

    def one(item):
        path = os.path.join(d, "gen", item["id"] + ".txt")
        cached(path, lambda: claude_call(writer_prompt(setup, item), setup.get("system", "You are a writer."),
                                         setup.get("model", WRITER_MODEL)))
        return item["id"]
    print(f"writing {len(index)} pieces under setup '{setup_name}'", file=sys.stderr)
    pool(one, index)
    # the writer must not have been handed held-out text: check what it produced and what it read
    hits = heldout_guard.scan_text
    with open(heldout_guard.SHINGLES, encoding="utf-8") as fh:
        hashes = json.load(fh)["hashes"]
    leaked = [it["id"] for it in index if hits(setup_context(setup, it), hashes)]
    if leaked:
        sys.exit(f"setup '{setup_name}' shows the writer held-out text (via its files) for: {leaked}. Fix the files.")


# ---------------------------------------------------------------- judge

JUDGE_SYS = "You are an expert at telling AI-written text from human-written text. You answer with JSON only."
JUDGE_PROMPT = """You use AI writing tools every day and are very good at spotting AI-written text.

Below are {n} passages that are certainly by Dan Rose. They are all the same kind of piece: {type_note}. Use them to learn how he really writes or talks.

Then come two passages, A and B, covering the same content. One is really his. The other was written by an AI imitating him. {layout_note}

Which one did the AI write?

Answer with JSON only:
{{"ai": "A" or "B", "confidence": a number from 0.5 to 1.0, "cues": [one to three of: {cues}], "why": "one or two sentences naming the specific giveaways; do not quote more than five words in a row from either passage"}}

REFERENCE PASSAGES (all really Dan Rose):
{refs}

PASSAGE A:
{a}

PASSAGE B:
{b}
"""
TYPE_NOTE = {"content": "him talking to an audience off the cuff (videos, shorts, a podcast interview), transcribed",
             "ads": "ad scripts he wrote",
             "conversion": "sales video scripts and sales letters he wrote",
             "products": "what his customers get: passages from his books and transcribed lessons from his course"}
SPOKEN_NOTE = ("His passages are machine transcripts of speech: they can contain a mis-heard word or odd punctuation, "
               "and the AI version was written straight as text. A transcription glitch therefore proves nothing either "
               "way, so do not use mis-heard words, typos or punctuation glitches as evidence. Filler sounds were removed "
               "and paragraph breaks were set the same way in every passage. Judge the word choice, the shape of the "
               "sentences, what gets said and how.")
WRITTEN_NOTE = ("Markdown marks were stripped from both. Otherwise the layout is as each was written. Judge the word "
                "choice, the shape of the sentences, what gets said and how.")


def reference_pool(item):
    """Real windows of the same type that are not held out, same mode first, never from the item's own file."""
    rng = random.Random(f"{SEED}-refs-{item['id']}")
    tiers = [1, 2] if item["type"] in ("ads",) else [1]
    spoken = item["mode"] == "spoken"
    refs = []
    for tier in tiers:
        rows = [(r, t) for r, t in corpus.pile(item["type"], tier) if r["file"] != item["file"]
                and r.get("authorship") != "dan-typed-lines-only"]
        rows.sort(key=lambda rt: (rt[0].get("mode") != item["mode"], rng.random()))
        for r, t in rows:
            w = window(t, r.get("mode") == "spoken", rng, lo=140, hi=340, whole_if_short=True)
            if w:
                refs.append(for_judging(t[w[0]:w[1]], r.get("mode") == "spoken"))
            if len(refs) >= 24:
                break
        if len(refs) >= 24:
            break
    if len(refs) < 8 and item["type"] != "ads":  # a thin type borrows tier 2 rather than run with few references
        for r, t in corpus.pile(item["type"], 2):
            w = window(t, r.get("mode") == "spoken", rng, lo=140, hi=340, whole_if_short=True)
            if w:
                refs.append(for_judging(t[w[0]:w[1]], r.get("mode") == "spoken"))
    return refs


def judge(setup_name, date):
    index = load_index()
    d = run_dir(setup_name, date)
    reps = max(1, math.ceil(MIN_TRIALS / (len(index) * 2)))
    pools = {it["id"]: reference_pool(it) for it in index}
    jobs = [(it, j, r) for it in index for j in ("claude", "gemini") for r in range(reps)]
    print(f"judging: {len(jobs)} trials ({len(index)} passages x 2 judges x {reps})", file=sys.stderr)

    def one(job):
        it, who, rep = job
        path = os.path.join(d, "trials", f"{it['id']}-{who}-{rep}.json")

        def make():
            rng = random.Random(f"{SEED}-{setup_name}-{it['id']}-{who}-{rep}")
            spoken = it["mode"] == "spoken"
            real = for_judging(passage(it, repaired=True), spoken)
            with open(os.path.join(d, "gen", it["id"] + ".txt"), encoding="utf-8") as fh:
                fake = for_judging(fh.read(), spoken)
            refs = rng.sample(pools[it["id"]], min(8, len(pools[it["id"]])))
            ai_is = rng.choice("AB")
            a_, b_ = (fake, real) if ai_is == "A" else (real, fake)
            prompt = JUDGE_PROMPT.format(
                n=len(refs), type_note=TYPE_NOTE[it["type"]], layout_note=SPOKEN_NOTE if spoken else WRITTEN_NOTE,
                cues=", ".join(CUES), refs="\n\n".join(f"[Reference {i}]\n{r}" for i, r in enumerate(refs, 1)),
                a=a_, b=b_)
            tin = tout = 0
            if who == "claude":
                v = parse_json(claude_call(prompt, JUDGE_SYS, JUDGE_MODEL))
            else:
                text, tin, tout = gemini_call(prompt)
                v = parse_json(text)
            pick = str(v.get("ai", "")).strip().upper()[:1]
            return json.dumps({"id": it["id"], "type": it["type"], "bucket": it["bucket"], "judge": who, "rep": rep,
                               "ai_is": ai_is, "picked": pick, "correct": pick == ai_is,
                               "confidence": v.get("confidence"), "cues": [c for c in v.get("cues", []) if c in CUES],
                               "why": v.get("why", ""), "refs": len(refs), "tokens_in": tin, "tokens_out": tout})
        cached(path, make)
        return path
    pool(one, jobs, workers=6)


# ---------------------------------------------------------------- report

def wilson(k, n):
    if not n:
        return (0, 0)
    z, p = 1.96, k / n
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (round(100 * (mid - half)), round(100 * (mid + half)))


def pct(k, n):
    return f"{round(100 * k / n)}%" if n else "n/a"


def report(setup_name, date, luar=True):
    setup = load_setup(setup_name)
    index = load_index()
    d = run_dir(setup_name, date)
    trials = []
    for f in sorted(glob.glob(os.path.join(d, "trials", "*.json"))):
        with open(f, encoding="utf-8") as fh:
            trials.append(json.load(fh))
    with open(heldout_guard.SHINGLES, encoding="utf-8") as fh:
        hashes = json.load(fh)["hashes"]
    n, k = len(trials), sum(t["correct"] for t in trials)
    lo, hi = wilson(k, n)
    L = [f"# Voice bench: setup `{setup_name}`, {date}", "",
         f"{setup.get('about', '')}", "",
         f"Writer: {setup.get('model', WRITER_MODEL)}. Judges: a fresh {JUDGE_MODEL} and {GEMINI_MODEL}, each shown 8 "
         "real reference passages of the same type and one real / generated pair in random order. A judge is \"right\" "
         "when it picks the AI piece. Chance is 50%. The finish line is 60% or less.", "",
         f"**Judges picked the AI piece {k} times out of {n}: {pct(k, n)}** (95% range {lo} to {hi}%).", "",
         "## By type and by judge", "",
         "| | trials | picked the AI | rate |", "|---|---:|---:|---:|"]
    groups = [("content", lambda t: t["type"] == "content"),
              ("  content, long-form", lambda t: t["bucket"] == "content-long"),
              ("  content, shorts", lambda t: t["bucket"] == "content-short"),
              ("ads", lambda t: t["type"] == "ads"), ("conversion", lambda t: t["type"] == "conversion"),
              ("products", lambda t: t["type"] == "products"),
              ("judge: Claude", lambda t: t["judge"] == "claude"), ("judge: Gemini", lambda t: t["judge"] == "gemini")]
    for label, f in groups:
        g = [t for t in trials if f(t)]
        L.append(f"| {label} | {len(g)} | {sum(t['correct'] for t in g)} | {pct(sum(t['correct'] for t in g), len(g))} |")
    both = {}
    for t in trials:
        both.setdefault(t["id"], []).append(t["correct"])
    fooled = sorted(i for i, v in both.items() if not any(v))
    L += ["", f"Passages where every judge was fooled (picked Dan's real one as the AI): {len(fooled)} of {len(both)}"
          + (f" ({', '.join(fooled)})" if fooled else "") + "."]

    L += ["", "## Why the judges said it was AI", "",
          "Cues named in the trials where the judge was right (each trial names one to three).", "",
          "| cue | times named | share of right calls |", "|---|---:|---:|"]
    right = [t for t in trials if t["correct"]]
    tally = {}
    for t in right:
        for c in set(t["cues"]):
            tally[c] = tally.get(c, 0) + 1
    for c, v in sorted(tally.items(), key=lambda kv: -kv[1]):
        L.append(f"| {c.replace('_', ' ')} | {v} | {pct(v, len(right))} |")
    L += ["", "In the judges' words (most confident right calls, one per cue):", ""]
    seen = set()
    for t in sorted(right, key=lambda t: -(t.get("confidence") or 0)):
        cue = (t["cues"] or ["other"])[0]
        why = t.get("why", "").replace("\n", " ").replace("\u2014", ", ").replace("\u2013", ", ").strip()
        if cue in seen or not why or heldout_guard.scan_text(why, hashes):
            continue
        seen.add(cue)
        L.append(f"- **{cue.replace('_', ' ')}** ({t['type']}, {t['judge']}): {why}")
        if len(seen) >= 8:
            break

    # style distances and counts: pooled generated text against pooled real held-out text, per type
    lu = vf.Luar() if luar else None
    L += ["", "## Style distances (pooled per type)", "",
          "Delta: function-word distance from Dan's Tier 1 average, lower is closer. LUAR: style-embedding similarity, "
          "higher is closer. \"Dan's held-out\" is the real side of the pairs, scored the same way: where the generated "
          "side should land, and the fair comparison (same amount of text). The ceiling and floor columns come from "
          "2,500-word samples, so a bigger pooled sample can beat the ceiling. Under 1,500 words a number is noise and "
          "is marked ~. These two are weak instruments at this size: the judges are the score.", "",
          "| type | words | Delta generated | Delta Dan's held-out | Delta ceiling | Delta floor (Claude) | LUAR generated "
          "| LUAR Dan's held-out | LUAR ceiling | LUAR floor (Claude) |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    pooled = {}
    for t in corpus.TYPES:
        items = [it for it in index if it["type"] == t]
        gen = "\n\n".join(open(os.path.join(d, "gen", it["id"] + ".txt"), encoding="utf-8").read() for it in items)
        real = "\n\n".join(passage(it) for it in items)
        pooled[t] = (real, gen)
        if not items:
            continue
        base = vf.baseline(t, lu)
        g, r = vf.score_text(gen, t, lu, base), vf.score_text(real, t, lu, base)
        mark = "~" if g.get("small_sample") else ""
        L.append(f"| {t} | {g['words']} | {mark}{g.get('delta_to_dan', 'n/a')} | {mark}{r.get('delta_to_dan', 'n/a')} | "
                 f"{g.get('delta_ceiling', 'n/a')} | {g.get('delta_floor_claude', 'n/a')} | {mark}{g.get('luar_to_dan', 'n/a')} | "
                 f"{mark}{r.get('luar_to_dan', 'n/a')} | {g.get('luar_ceiling', 'n/a')} | {g.get('luar_floor_claude', 'n/a')} |")
        gaps = g.get("biggest_gaps") or []
        if gaps:
            L.append(f"|  | | function words furthest from Dan ({t}), per 1,000, generated / Dan: "
                     + ", ".join(f"{w} {a_}/{b_}" for w, a_, b_ in gaps[:8]) + " | | | | | | | |")

    L += ["", "## Counts: Dan's held-out passages against the generated ones", "",
          "Per 100 words unless marked. From `scripts/voice/voice_stats.py`.", "",
          "| measure | " + " | ".join(f"{t} Dan | {t} gen" for t in corpus.TYPES if pooled[t][0]) + " |",
          "|---|" + "---:|---:|" * sum(1 for t in corpus.TYPES if pooled[t][0])]
    ms = {t: (voice_stats.measure(pooled[t][0]), voice_stats.measure(pooled[t][1])) for t in corpus.TYPES if pooled[t][0]}
    for col in ["and", "lists3", "questions", "you", "contractions", "swears", "emdash", "sent_mean", "sent_sd", "punch_pct"]:
        L.append(f"| {col} | " + " | ".join(f"{ms[t][0][col]} | {ms[t][1][col]}" for t in ms) + " |")
    sm = {t: (voice_stats.small_words(pooled[t][0]), voice_stats.small_words(pooled[t][1])) for t in ms}
    for w in ["actually", "really", "very", "kind of", "stuff", "things", "going to", "which", "because", "just", "so",
              "you know", "like"]:
        L.append(f"| \"{w}\" per 1,000 | " + " | ".join(f"{sm[t][0][w]} | {sm[t][1][w]}" for t in sm) + " |")

    tin = sum(t.get("tokens_in", 0) for t in trials)
    tout = sum(t.get("tokens_out", 0) for t in trials)
    cost = tin / 1e6 * GEMINI_PRICE[0] + tout / 1e6 * GEMINI_PRICE[1]
    counts = ", ".join(f"{b} {sum(1 for it in index if it['bucket'] == b)}" for b in QUOTA)
    L += ["", "## Run facts", "",
          f"- Hold-out passages: {len(index)} ({counts}).",
          f"- Trials: {n}. Gemini tokens: {tin} in, {tout} out, about ${cost:.2f}. Claude calls ran on the subscription.",
          f"- Setup files: {', '.join('`' + p + '`' for p in setup.get('files', [])) or 'none'}.",
          "- Raw pairs and verdicts: `voice-corpus/bench/" + os.path.basename(d) + "/` (local and Drive mirror only).", ""]
    os.makedirs(REPORTS, exist_ok=True)
    out = os.path.join(REPORTS, f"{date}-{setup_name}.md")
    text = "\n".join(L).replace("| None |", "| n/a |").replace("\u2014", ", ").replace("\u2013", "-")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    summary = {"setup": setup_name, "date": date, "trials": n, "right": k, "rate": round(100 * k / n, 1) if n else None,
               "by_type": {t: pct(sum(x["correct"] for x in trials if x["type"] == t),
                                  sum(1 for x in trials if x["type"] == t)) for t in corpus.TYPES},
               "gemini_cost": round(cost, 2)}
    with open(os.path.join(d, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps(summary))
    print("report:", os.path.relpath(out, ROOT))


def cmd_run(a):
    date = a.date or datetime.date.today().isoformat()
    if not a.report_only:
        generate(a.setup, date)
        judge(a.setup, date)
    report(a.setup, date, luar=not a.no_luar)


# ---------------------------------------------------------------- blind page

def cmd_blind(a):
    date = a.date or datetime.date.today().isoformat()
    d = run_dir(a.setup, date)
    index = load_index()
    rng = random.Random(f"{SEED}-blind")
    pairs, key = [], []
    for t, want in BLIND_QUOTA.items():
        items = [it for it in index if it["type"] == t]
        rng.shuffle(items)
        if t == "content":  # 5 long-form and 3 shorts
            items = [i for i in items if i["bucket"] == "content-long"][:5] + \
                    [i for i in items if i["bucket"] == "content-short"][:3]
        for it in items[:want]:
            spoken = it["mode"] == "spoken"
            real = for_judging(passage(it, repaired=True), spoken)
            with open(os.path.join(d, "gen", it["id"] + ".txt"), encoding="utf-8") as fh:
                fake = for_judging(fh.read(), spoken)
            dan_is = rng.choice("AB")
            pairs.append({"type": t, "what": it["kind"].split(". Write the verbatim")[0].rstrip("."), "spoken": spoken,
                          "a": real if dan_is == "A" else fake, "b": fake if dan_is == "A" else real, "_id": it["id"],
                          "_dan": dan_is})
    rng.shuffle(pairs)
    for n, p in enumerate(pairs, 1):
        p["n"] = n
        key.append({"n": n, "dan_is": p.pop("_dan"), "id": p.pop("_id"), "type": p["type"]})
    with open(os.path.join(d, "blind-pairs.json"), "w", encoding="utf-8") as fh:
        json.dump(pairs, fh, indent=1)
    with open(os.path.join(d, "blind-key.json"), "w", encoding="utf-8") as fh:
        json.dump(key, fh, indent=1)
    with open(os.path.join(ROOT, "scripts", "voice", "blind_page_template.html"), encoding="utf-8") as fh:
        page = fh.read()
    data = json.dumps([{k: p[k] for k in ("n", "what", "a", "b")} for p in pairs], ensure_ascii=False).replace("</", "<\\/")
    with open(os.path.join(d, "blind-page.html"), "w", encoding="utf-8") as fh:
        fh.write(page.replace("/*PAIRS*/[]", data))  # holds held-out text: local only, published as a private page
    print(f"{len(pairs)} pairs -> {os.path.relpath(d, ROOT)}/blind-page.html ; key in blind-key.json (chat only)")
    print("key:", " ".join(f"{k['n']}{k['dan_is']}" for k in key))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick"); p.add_argument("--force", action="store_true"); p.set_defaults(fn=cmd_pick)
    p = sub.add_parser("briefs"); p.set_defaults(fn=cmd_briefs)
    p = sub.add_parser("finalize"); p.add_argument("--force", action="store_true")
    p.add_argument("--drop", help="comma-separated candidate ids to leave out"); p.set_defaults(fn=cmd_finalize)
    p = sub.add_parser("run"); p.add_argument("--setup", required=True); p.add_argument("--date")
    p.add_argument("--report-only", action="store_true"); p.add_argument("--no-luar", action="store_true")
    p.set_defaults(fn=cmd_run)
    p = sub.add_parser("blind"); p.add_argument("--setup", required=True); p.add_argument("--date")
    p.set_defaults(fn=cmd_blind)
    p = sub.add_parser("repair"); p.set_defaults(fn=cmd_repair)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
