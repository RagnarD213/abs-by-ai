#!/usr/bin/env python3
"""
Two style distances that do not depend on topic: a function-word fingerprint (Burrows' Delta) and a style embedding
(LUAR). Both answer "how far is this text from Dan?", always against a ceiling and a floor.

WHY THIS EXISTS (2026-10-08, Dan Voice P2A): counting "and" and kickers caught the obvious gaps. These two catch the
ones nobody can name: the mix of small grammar words a person uses without thinking, and the overall style signature.

- Delta: relative frequency of the most common function words (the, of, to, that, just, so, I'm ...), z-scored across
  all the samples being compared, then the mean absolute difference from Dan's average. LOWER is closer to Dan. It is
  written out here in plain Python (same maths as the `faststylometry` package) so it runs in a cloud session with
  nothing installed. Samples are pooled to about 2,500 words; under 1,500 the number is noise and is flagged.
- LUAR (`rrivera1849/LUAR-MUD`): a model trained to recognise authors. Each sample is split into 16 pieces and embedded
  once; the score is the cosine similarity to Dan's average. HIGHER is closer to Dan. Needs
  `pip install torch transformers einops` (local Mac only; it prints "skipped" where they are missing).

Ceiling = Dan against Dan (each of his samples against the average of his other samples).
Floor = Claude's own drafts against Dan, and another fitness creator against Dan.
A draft is doing well when it sits near the ceiling and far from both floors.

Usage:
    python3 scripts/voice/voice_fingerprint.py --baseline                 # ceiling and floor for every type
    python3 scripts/voice/voice_fingerprint.py --type content draft.txt   # one draft against the content baseline
    python3 scripts/voice/voice_fingerprint.py --baseline --no-luar --json
"""
import argparse
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus  # noqa: E402

SAMPLE_WORDS = 2500
MIN_WORDS = 1500
TOP_N = 150

# A fixed list keeps topic words out: only grammar words, pronouns, auxiliaries, common adverbs and spoken glue.
FUNCTION_WORDS = """
a about above across actually after again against all almost also although always am an and another any anyone anything
are aren't around as at back be because been before being below between both but by can can't cannot could couldn't did
didn't do does doesn't doing don't down during each either else enough even ever every everyone everything few for from
further get gets getting go goes going gonna got had hadn't has hasn't have haven't having he he's her here here's hers
herself him himself his how however i i'd i'll i'm i've if in into is isn't it it's its itself just kind least less let
let's like lot many may maybe me might more most much must my myself never no nor not nothing now of off often on once
one only onto or other others our ours ourselves out over own perhaps pretty quite rather really right same shall she
should shouldn't since so some someone something sort still such than that that's the their theirs them themselves then
there there's these they they'd they'll they're they've thing things this those though through thus to too toward under
until up upon us very was wasn't way we we'd we'll we're we've well were weren't what what's whatever when where whether
which while who whom whose why will with within without won't would wouldn't yeah yes yet you you'd you'll you're
you've your yours yourself
""".split()
FW = set(FUNCTION_WORDS)
TOKEN = re.compile(r"[a-z]+(?:'[a-z]+)?")


def tokens(text):
    return TOKEN.findall(corpus.normalize(text).lower())


def chunks(text, size=SAMPLE_WORDS, min_words=MIN_WORDS):
    """Split a pooled text into samples of about `size` words. A short tail joins the sample before it."""
    toks = tokens(text)
    if len(toks) < min_words:
        return [toks] if toks else []
    n = max(1, round(len(toks) / size))
    step = len(toks) / n
    return [toks[int(i * step):int((i + 1) * step)] for i in range(n)]


def profile(toks, vocab):
    n = len(toks) or 1
    counts = {}
    for t in toks:
        if t in FW:
            counts[t] = counts.get(t, 0) + 1
    return [1000.0 * counts.get(w, 0) / n for w in vocab]


def pick_vocab(sample_lists, top_n=TOP_N):
    totals = {}
    for toks in sample_lists:
        for t in toks:
            if t in FW:
                totals[t] = totals.get(t, 0) + 1
    return [w for w, _ in sorted(totals.items(), key=lambda kv: -kv[1])[:top_n]]


class Delta:
    """Fit on labelled piles of samples, then score any sample against a label's average."""

    def __init__(self, piles):
        # piles: {label: [token list, ...]}
        self.piles = {k: v for k, v in piles.items() if v}
        every = [s for v in self.piles.values() for s in v]
        self.vocab = pick_vocab(every)
        raw = [profile(s, self.vocab) for s in every]
        self.mean = [statistics.mean(c) for c in zip(*raw)]
        self.sd = [statistics.pstdev(c) or 1.0 for c in zip(*raw)]
        self.z = {k: [self._z(profile(s, self.vocab)) for s in v] for k, v in self.piles.items()}

    def _z(self, prof):
        return [(x - m) / s for x, m, s in zip(prof, self.mean, self.sd)]

    @staticmethod
    def _centroid(zs):
        return [statistics.mean(c) for c in zip(*zs)]

    @staticmethod
    def _dist(a, b):
        return sum(abs(x - y) for x, y in zip(a, b)) / len(a)

    def to_label(self, toks, label):
        return self._dist(self._z(profile(toks, self.vocab)), self._centroid(self.z[label]))

    def self_distance(self, label):
        """Leave-one-out: each sample against the average of the label's other samples."""
        zs = self.z[label]
        if len(zs) < 2:
            return None
        return statistics.mean(self._dist(z, self._centroid(zs[:i] + zs[i + 1:])) for i, z in enumerate(zs))

    def between(self, a, b):
        """Each sample of `a` against the average of `b`."""
        cb = self._centroid(self.z[b])
        return statistics.mean(self._dist(z, cb) for z in self.z[a])

    def biggest_gaps(self, toks, label, n=12):
        """The function words where a sample sits furthest from the label's average, per 1,000 words."""
        prof = profile(toks, self.vocab)
        cen = [statistics.mean(c) for c in zip(*[profile(s, self.vocab) for s in self.piles[label]])]
        z = self._z(prof)
        zc = self._centroid(self.z[label])
        order = sorted(range(len(self.vocab)), key=lambda i: -abs(z[i] - zc[i]))[:n]
        return [(self.vocab[i], round(prof[i], 1), round(cen[i], 1)) for i in order]


class Luar:
    """Style embedding. `ok` is False when torch / transformers / einops are not installed."""

    def __init__(self):
        self.ok = False
        try:
            import warnings
            warnings.filterwarnings("ignore")
            import torch
            from transformers import AutoModel, AutoTokenizer
            self.torch = torch
            self.tok = AutoTokenizer.from_pretrained("rrivera1849/LUAR-MUD")
            self.model = AutoModel.from_pretrained("rrivera1849/LUAR-MUD", trust_remote_code=True)
            self.model.eval()
            self.ok = True
        except Exception as e:  # missing packages or no network: the caller prints "skipped"
            self.why = str(e).splitlines()[0][:120]

    def embed(self, toks, pieces=16, max_len=256):
        step = max(1, len(toks) // pieces)
        texts = [" ".join(toks[i * step:(i + 1) * step]) for i in range(pieces)]
        texts = [t or "." for t in texts]
        enc = self.tok(texts, max_length=max_len, padding="max_length", truncation=True, return_tensors="pt")
        enc["input_ids"] = enc["input_ids"].reshape(1, pieces, -1)
        enc["attention_mask"] = enc["attention_mask"].reshape(1, pieces, -1)
        with self.torch.no_grad():
            out = self.model(**enc)
        return self.torch.nn.functional.normalize(out[0], dim=0)

    def cos(self, a, b):
        return float(self.torch.dot(a, b))

    def centroid(self, vecs):
        return self.torch.nn.functional.normalize(self.torch.stack(vecs).mean(0), dim=0)


def type_piles(type_):
    """Token samples for one type: Dan's Tier 1, Claude's drafts of that type, the other creators."""
    dan = chunks(corpus.pooled(type_, 1))
    claude = chunks(corpus.folder_text(os.path.join("claude-drafts", type_)))
    other = chunks(corpus.folder_text("other-creator"))
    return {"dan": dan, "claude": claude, "other": other}


def baseline(type_, luar=None):
    piles = type_piles(type_)
    res = {"type": type_, "dan_samples": len(piles["dan"]), "claude_samples": len(piles["claude"]),
           "other_samples": len(piles["other"]), "dan_words": sum(len(s) for s in piles["dan"])}
    if len(piles["dan"]) < 2:
        res["note"] = "under two samples of Tier 1: no ceiling for this type"
        return res, None, piles
    d = Delta(piles)
    res["delta_ceiling_dan_vs_dan"] = round(d.self_distance("dan"), 3)
    if "claude" in d.piles:
        res["delta_floor_claude"] = round(d.between("claude", "dan"), 3)
    if "other" in d.piles:
        res["delta_floor_other_creator"] = round(d.between("other", "dan"), 3)
    if luar is not None and luar.ok:
        dv = [luar.embed(s) for s in piles["dan"]]
        res["luar_ceiling_dan_vs_dan"] = round(statistics.mean(
            luar.cos(v, luar.centroid(dv[:i] + dv[i + 1:])) for i, v in enumerate(dv)), 3)
        cen = luar.centroid(dv)
        for k in ("claude", "other"):
            if piles[k]:
                res[f"luar_floor_{k}"] = round(statistics.mean(luar.cos(luar.embed(s), cen) for s in piles[k]), 3)
        res["_luar_centroid"] = cen
    return res, d, piles


def score_text(text, type_, luar=None, base=None):
    """One draft (or a pooled set of drafts) against a type's baseline."""
    res, d, piles = base if base is not None else baseline(type_, luar)
    toks = tokens(text)
    out = {"type": type_, "words": len(toks), "small_sample": len(toks) < MIN_WORDS}
    if d is None:
        out["note"] = res.get("note")
        return out
    out["delta_to_dan"] = round(d.to_label(toks, "dan"), 3)
    out["delta_ceiling"] = res.get("delta_ceiling_dan_vs_dan")
    out["delta_floor_claude"] = res.get("delta_floor_claude")
    out["biggest_gaps"] = d.biggest_gaps(toks, "dan")
    if luar is not None and luar.ok and "_luar_centroid" in res:
        out["luar_to_dan"] = round(luar.cos(luar.embed(toks), res["_luar_centroid"]), 3)
        out["luar_ceiling"] = res.get("luar_ceiling_dan_vs_dan")
        out["luar_floor_claude"] = res.get("luar_floor_claude")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--type", choices=corpus.TYPES)
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--no-luar", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    luar = None if a.no_luar else Luar()
    if luar is not None and not luar.ok:
        print(f"LUAR skipped: {luar.why}", file=sys.stderr)
    clean = lambda r: {k: v for k, v in r.items() if not k.startswith("_")}
    if a.baseline:
        rows = [clean(baseline(t, luar)[0]) for t in corpus.TYPES]
        if a.json:
            print(json.dumps(rows, indent=2))
            return
        cols = ["type", "dan_words", "dan_samples", "delta_ceiling_dan_vs_dan", "delta_floor_claude",
                "delta_floor_other_creator", "luar_ceiling_dan_vs_dan", "luar_floor_claude", "luar_floor_other"]
        print("| " + " | ".join(cols) + " |")
        print("|---|" + "---:|" * (len(cols) - 1))
        for r in rows:
            print("| " + " | ".join(str(r.get(c, "n/a")) for c in cols) + " |")
        return
    if not a.files or not a.type:
        ap.error("give --baseline, or --type and at least one file")
    base = baseline(a.type, luar)
    for f in a.files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            r = score_text(fh.read(), a.type, luar, base)
        print(json.dumps({os.path.basename(f): r}, indent=2) if a.json else f"{os.path.basename(f)}: {r}")


if __name__ == "__main__":
    main()
