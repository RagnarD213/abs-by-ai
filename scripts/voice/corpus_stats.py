#!/usr/bin/env python3
"""
Print the per-type baseline tables for `.claude/skills/_shared/voice/STATS.md`.

WHY THIS EXISTS (2026-10-08, Dan Voice P2A): Dan set four types of writing, and a baseline for a type comes only from
that type's Tier 1 (material that is really him). This prints, as markdown, the counts (`voice_stats.py`), the small
everyday words per 1,000, and the two style distances with their ceiling and floor (`voice_fingerprint.py`), each from
the corpus with the hold-out set cut out. Paste the output into STATS.md when the corpus changes.

Usage:  python3 scripts/voice/corpus_stats.py [--no-luar]
Local only (needs `voice-corpus/`).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus  # noqa: E402
import voice_fingerprint as vf  # noqa: E402
import voice_stats as vs  # noqa: E402

sub = lambda t, key: "\n\n".join(x for r, x in corpus.pile(t, 1) if key in r["file"])
PILES = [
    ("CONTENT Tier 1 (all)", lambda: corpus.pooled("content", 1)),
    ("  Abs By AI off the cuff, 2026", lambda: sub("content", "/absbyai/")),
    ("  shorts he wrote, 2026", lambda: sub("content", "/absbyai-shorts/")),
    ("  old channel solo, 2020-21", lambda: sub("content", "/old-channel/")),
    ("  Travel Like a Boss, 2020", lambda: sub("content", "/tlab/")),
    ("content Tier 2 (podcast half, outlines)", lambda: corpus.pooled("content", 2)),
    ("content Tier 3 (Six Pack Shortcuts)", lambda: corpus.pooled("content", 3)),
    ("Claude content drafts", lambda: corpus.folder_text("claude-drafts/content")),
    ("Dan reading Claude scripts", lambda: corpus.folder_text("claude-drafts/content-as-read")),
    ("Other fitness creators", lambda: corpus.folder_text("other-creator")),
    ("ADS Tier 1 (own ads)", lambda: corpus.pooled("ads", 1)),
    ("ads Tier 2 (for other presenters)", lambda: corpus.pooled("ads", 2)),
    ("Claude ad drafts", lambda: corpus.folder_text("claude-drafts/ads")),
    ("CONVERSION Tier 1", lambda: corpus.pooled("conversion", 1)),
    ("conversion Tier 2 (Fujiyama)", lambda: corpus.pooled("conversion", 2)),
    ("Claude conversion drafts", lambda: corpus.folder_text("claude-drafts/conversion")),
    ("PRODUCTS Tier 1 (all)", lambda: corpus.pooled("products", 1)),
    ("  The Sex God Method, 2007", lambda: sub("products", "/sgm/")),
    ("  Black Belt course videos, 2021", lambda: sub("products", "/blackbelt/")),
    ("products Tier 2 (15 Steps)", lambda: corpus.pooled("products", 2)),
]
SMALL = ["actually", "really", "very", "kind of", "stuff", "things", "going to", "gonna", "which", "because", "just",
         "so", "pretty", "a lot", "you know", "basically", "like", "now", "right"]


def main():
    texts = [(label, fn()) for label, fn in PILES]
    texts = [(label, t) for label, t in texts if corpus.count_words(t)]
    print("| pile | " + " | ".join(vs.COLS) + " |")
    print("|---|" + "---:|" * len(vs.COLS))
    for label, t in texts:
        m = vs.measure(t)
        print(f"| {label.strip() if label.startswith('  ') else label} | " + " | ".join(str(m[c]) for c in vs.COLS) + " |")
    print()
    print("| per 1,000 words | " + " | ".join(SMALL) + " |")
    print("|---|" + "---:|" * len(SMALL))
    for label, t in texts:
        m = vs.small_words(t)
        print(f"| {label.strip()} | " + " | ".join(str(m[w]) for w in SMALL) + " |")
    print()
    luar = None if "--no-luar" in sys.argv else vf.Luar()
    cols = ["type", "dan_words", "dan_samples", "delta_ceiling_dan_vs_dan", "delta_floor_claude",
            "delta_floor_other_creator", "luar_ceiling_dan_vs_dan", "luar_floor_claude", "luar_floor_other"]
    print("| " + " | ".join(cols) + " |")
    print("|---|" + "---:|" * (len(cols) - 1))
    for t in corpus.TYPES:
        r = vf.baseline(t, luar)[0]
        print("| " + " | ".join(str(r.get(c, "n/a")) for c in cols) + " |")


if __name__ == "__main__":
    main()
