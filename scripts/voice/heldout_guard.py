#!/usr/bin/env python3
"""
Fail if any guide, example or skill file quotes a held-out passage.

WHY THIS EXISTS (2026-10-08, Dan Voice P2A): the voice bench asks judges to tell Dan's real writing from Claude's
imitation of it. The real passages it uses (the hold-out set, listed in `.claude/skills/_shared/voice/HELD-OUT.md`) must
never be shown to the writer, or the test proves nothing. This script is the lock: it fails when a file under
`.claude/skills/_shared/` (or any other path you pass) contains an 8-word run from a held-out passage.

The passages themselves are not in this public repo. What is here is `scripts/voice/heldout_shingles.json`: a short hash
of every 8-word run in them. That is enough to detect a quote and useless for reading the text, and it means the guard
runs in a cloud session too.

Usage:
    python3 scripts/voice/heldout_guard.py                 # check .claude/skills/_shared/ ; exit 1 on a hit
    python3 scripts/voice/heldout_guard.py path1 path2     # check other files or folders as well
    python3 scripts/voice/heldout_guard.py --build         # rebuild the hash file from voice-corpus/heldout/ (local)
"""
import argparse
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHINGLES = os.path.join(ROOT, "scripts", "voice", "heldout_shingles.json")
HELDOUT = os.path.join(ROOT, "voice-corpus", "heldout")
DEFAULT = [os.path.join(ROOT, ".claude", "skills", "_shared")]
RUN = 8
TOKEN = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def toks(text):
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    return TOKEN.findall(text.lower())


def h(words):
    return hashlib.sha1(" ".join(words).encode("utf-8")).hexdigest()[:12]


def shingles(text):
    t = toks(text)
    return {h(t[i:i + RUN]) for i in range(len(t) - RUN + 1)}


def build():
    with open(os.path.join(HELDOUT, "index.json"), encoding="utf-8") as fh:
        index = json.load(fh)
    out = {}
    for item in index:
        with open(os.path.join(HELDOUT, "passages", item["id"] + ".txt"), encoding="utf-8") as fh:
            for s in shingles(fh.read()):
                out[s] = item["id"]
    with open(SHINGLES, "w", encoding="utf-8") as fh:
        json.dump({"run": RUN, "passages": len(index), "hashes": out}, fh, separators=(",", ":"), sort_keys=True)
    print(f"wrote {len(out)} hashes from {len(index)} passages to {os.path.relpath(SHINGLES, ROOT)}")


def scan_text(text, hashes):
    """[(passage id, the 8 words)] for every held-out run found in text."""
    t = toks(text)
    hits = []
    for i in range(len(t) - RUN + 1):
        pid = hashes.get(h(t[i:i + RUN]))
        if pid:
            hits.append((pid, " ".join(t[i:i + RUN])))
    return hits


def files_under(path):
    if os.path.isfile(path):
        yield path
        return
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith((".md", ".txt", ".py", ".json", ".html")) and "heldout_shingles" not in f:
                yield os.path.join(root, f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    if a.build:
        build()
        return 0
    if not os.path.isfile(SHINGLES):
        print("heldout_guard: no hash file yet (scripts/voice/heldout_shingles.json); nothing to check")
        return 0
    with open(SHINGLES, encoding="utf-8") as fh:
        hashes = json.load(fh)["hashes"]
    bad = 0
    for base in DEFAULT + [os.path.abspath(p) for p in a.paths]:
        for f in files_under(base):
            with open(f, encoding="utf-8", errors="replace") as fh:
                hits = scan_text(fh.read(), hashes)
            if hits:
                bad += 1
                pid, words = hits[0]
                print(f"HELD-OUT TEXT in {os.path.relpath(f, ROOT)}: {len(hits)} run(s), first from {pid}: \"{words}\"")
    if bad:
        print(f"heldout_guard: FAIL, {bad} file(s) quote the hold-out set. Remove the quote; never edit the hash file.")
        return 1
    print(f"heldout_guard: OK, no held-out text ({len(hashes)} hashes checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
