#!/usr/bin/env python3
"""
Load Dan's voice corpus by type and tier.

WHY THIS EXISTS (2026-10-08, Dan Voice P2A): Dan set four types of writing (content, ads, conversion, products), each
measured against its own material. The raw text lives in `voice-corpus/` on the Mac (git-ignored, mirrored to the Drive
folder `1FE1_fv6XhV96w4OQDji51w7Lrz6ZpiOM`), never in this public repo. Every file there has one row in
`voice-corpus/_manifest/*.jsonl`. This module is the one place that reads them, so the stats, the fingerprint and the
bench all agree on what is in a pile and on what is held out.

Usage:
    python3 scripts/voice/corpus.py                 # words per type and tier
    python3 scripts/voice/corpus.py --list content  # every file in a type

A cloud session has no `voice-corpus/` folder: pull it from the Drive folder first, or the piles come back empty.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS = os.path.join(ROOT, "voice-corpus")
TYPES = ["content", "ads", "conversion", "products"]
WORD = re.compile(r"[A-Za-z0-9$%][\w$%'-]*")


def normalize(text):
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return text.replace("\r\n", "\n")


def count_words(text):
    return len(WORD.findall(text))


def manifest():
    """Every manifest row whose file exists and is not a duplicate. Later rows win over earlier ones for a file."""
    rows = {}
    mdir = os.path.join(CORPUS, "_manifest")
    if not os.path.isdir(mdir):
        return []
    for name in sorted(os.listdir(mdir)):
        if not name.endswith(".jsonl"):
            continue
        with open(os.path.join(mdir, name), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                f = row.get("file", "")
                if f.startswith("voice-corpus/"):
                    f = f[len("voice-corpus/"):]
                row["file"] = f
                if row.get("duplicate_of") or not os.path.isfile(os.path.join(CORPUS, f)):
                    continue
                rows[f] = row
    return list(rows.values())


def read(row):
    with open(os.path.join(CORPUS, row["file"]), encoding="utf-8", errors="replace") as fh:
        return normalize(fh.read())


def heldout_index():
    """Held-out passages: [{id, type, file, start, end, words, ...}], character offsets into the normalized file."""
    path = os.path.join(CORPUS, "heldout", "index.json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def read_without_heldout(row, index=None):
    """The file's text with every held-out span cut out. A file flagged heldout in its manifest row returns ''."""
    if row.get("heldout") is True:
        return ""
    text = read(row)
    spans = sorted(((h["start"], h["end"]) for h in (index if index is not None else heldout_index())
                    if h["file"] == row["file"]), reverse=True)
    for s, e in spans:
        text = text[:s] + "\n\n" + text[e:]
    return text


def pile(type_, tier=None, keep_heldout=False, where=None):
    """[(row, text)] for a type, optionally one tier. Held-out spans are removed unless keep_heldout."""
    idx = heldout_index()
    out = []
    for row in manifest():
        if row.get("type") != type_:
            continue
        if tier is not None and row.get("tier") != tier:
            continue
        if where and not where(row):
            continue
        text = read(row) if keep_heldout else read_without_heldout(row, idx)
        if count_words(text):
            out.append((row, text))
    return sorted(out, key=lambda rt: rt[0]["file"])


def pooled(type_, tier=None, **kw):
    return "\n\n".join(t for _, t in pile(type_, tier, **kw))


def folder_text(rel):
    """Pooled text of a corpus subfolder with no manifest (claude-drafts/<type>, other-creator)."""
    base = os.path.join(CORPUS, rel)
    chunks = []
    for root, _, files in os.walk(base):
        for f in sorted(files):
            if f.endswith((".txt", ".md")):
                with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                    chunks.append(normalize(fh.read()))
    return "\n\n".join(chunks)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", metavar="TYPE", help="list every file of one type")
    a = ap.parse_args()
    rows = manifest()
    if not rows:
        sys.exit("no corpus found at voice-corpus/ (it is local only; pull it from the Drive mirror)")
    if a.list:
        for row, text in pile(a.list, keep_heldout=True):
            print(f'{row.get("tier")}\t{count_words(text)}\t{row.get("year")}\t{row.get("mode")}\t{row["file"]}')
        return
    print("| type | tier | files | words | spoken | written |")
    print("|---|---:|---:|---:|---:|---:|")
    for t in TYPES + ["floor"]:
        for tier in (1, 2, 3, 0):
            got = [(r, read(r)) for r in rows if r.get("type") == t and r.get("tier") == tier]
            if not got:
                continue
            w = sum(count_words(x) for _, x in got)
            sp = sum(count_words(x) for r, x in got if r.get("mode") == "spoken")
            print(f"| {t} | {tier} | {len(got)} | {w} | {sp} | {w - sp} |")


if __name__ == "__main__":
    main()
