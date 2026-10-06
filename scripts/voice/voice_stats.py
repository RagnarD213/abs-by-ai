#!/usr/bin/env python3
"""
Measure how a piece of writing is built, so Dan's voice can be told apart from Claude's by numbers.

WHY THIS EXISTS (2026-10-06, Dan Voice Training P1): Dan's sense is that Claude says "and" too much, stacks
three-item lists and writes tidier, more even sentences than he does. This script turns that into a table.
The baseline numbers live in `.claude/skills/_shared/voice/STATS.md`. Part 2 (the AI-tell checker) builds on it.

Usage:
    python3 scripts/voice/voice_stats.py draft.txt                       # one file
    python3 scripts/voice/voice_stats.py --pile "Dan ads=corpus/hbi_dan" --pile "Claude=corpus/claude"
    python3 scripts/voice/voice_stats.py --json a.txt b.txt              # machine-readable

A pile is a folder (every .txt / .md inside it) or a single file; the pile's text is pooled before measuring.
Plain text in, spoken or reader-facing words only (strip filming cues and links first).

Counts are per 100 words. Definitions:
- and: the word "and" anywhere.
- lists3: three-item lists, "X, Y and Z" or "X, Y, and Z" (also with "or"), each item 1 to 4 words.
- questions: sentences ending in "?".
- you: "you", "your", "you're", "yourself" and friends.
- contractions: words with an apostrophe contraction (don't, you're, I'll, it's, ...).
- swears: a fixed list (fuck, shit, bullshit, damn, hell, ass, crap, bitch, piss).
- emdash: em dashes (and en dashes) per 100 words. Dan does not write them in new copy.
- sent_mean / sent_sd: words per sentence, average and spread. "..." does not end a sentence.
- para_words: words per paragraph (blank-line separated; if a file has no blank lines, each line is a paragraph).
- punch_pct: share of multi-sentence paragraphs whose LAST sentence is 6 words or fewer (the "kicker" ending).
- oneline_pct: share of paragraphs that are a single sentence of 10 words or fewer.
"""
import argparse
import json
import os
import re
import statistics
import sys

SWEARS = re.compile(r"\b(fuck\w*|shit\w*|bullshit|damn\w*|goddamn|hell|ass|asses|asshole\w*|crap\w*|bitch\w*|piss\w*)\b", re.I)
YOU = re.compile(r"\b(you|your|yours|yourself|yourselves|you're|you've|you'll|you'd|y'all)\b", re.I)
CONTRACTION = re.compile(r"\b\w+'(s|t|re|ve|ll|d|m)\b", re.I)
AND = re.compile(r"\band\b", re.I)
ITEM = r"[\w$%'-]+(?: [\w$%'-]+){0,3}"
LIST3 = re.compile(ITEM + r", " + ITEM + r",? (?:and|or) [\w$%'-]+", re.I)
WORD = re.compile(r"[A-Za-z0-9$%][\w$%'-]*")


def normalize(text):
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = text.replace("\r\n", "\n")
    return text


def paragraphs(text):
    if re.search(r"\n\s*\n", text):
        parts = re.split(r"\n\s*\n", text)
    else:
        parts = text.split("\n")
    return [p.strip() for p in parts if WORD.search(p or "")]


def sentences(par):
    par = re.sub(r"\.{3,}|…", " … ", par)  # ellipsis keeps the sentence going
    par = re.sub(r"\s+", " ", par)
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+", par)
    return [s.strip() for s in parts if WORD.search(s)]


def words(s):
    return WORD.findall(s)


def measure(text):
    text = normalize(text)
    paras = paragraphs(text)
    all_words = words(text)
    n = len(all_words) or 1
    sents_by_para = [sentences(p) for p in paras]
    sents = [s for ss in sents_by_para for s in ss]
    lens = [len(words(s)) for s in sents] or [0]
    multi = [ss for ss in sents_by_para if len(ss) >= 2]
    punch = sum(1 for ss in multi if len(words(ss[-1])) <= 6)
    oneline = sum(1 for ss in sents_by_para if len(ss) == 1 and len(words(ss[0])) <= 10)
    per100 = lambda c: round(100.0 * c / n, 2)
    return {
        "words": len(all_words),
        "and": per100(len(AND.findall(text))),
        "lists3": per100(sum(len(LIST3.findall(s)) for s in sents)),
        "questions": per100(sum(1 for s in sents if s.rstrip("\"')]").endswith("?"))),
        "you": per100(len(YOU.findall(text))),
        "contractions": per100(len(CONTRACTION.findall(text))),
        "swears": per100(len(SWEARS.findall(text))),
        "emdash": per100(text.count("\u2014") + text.count("\u2013")),
        "sent_mean": round(statistics.mean(lens), 1),
        "sent_sd": round(statistics.pstdev(lens), 1),
        "para_words": round(statistics.mean([len(words(p)) for p in paras]), 1) if paras else 0,
        "punch_pct": round(100.0 * punch / len(multi), 1) if multi else 0.0,
        "oneline_pct": round(100.0 * oneline / len(paras), 1) if paras else 0.0,
    }


def read_pile(path):
    if os.path.isdir(path):
        chunks = []
        for root, _, files in os.walk(path):
            for f in sorted(files):
                if f.endswith((".txt", ".md")):
                    with open(os.path.join(root, f), encoding="utf-8", errors="replace") as fh:
                        chunks.append(fh.read())
        return "\n\n".join(chunks)
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


COLS = ["words", "and", "lists3", "questions", "you", "contractions", "swears", "emdash",
        "sent_mean", "sent_sd", "para_words", "punch_pct", "oneline_pct"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="text files or folders, each measured on its own")
    ap.add_argument("--pile", action="append", default=[], help='"Label=path" (folder or file), pooled')
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    rows = []
    for spec in a.pile:
        label, _, path = spec.partition("=")
        rows.append((label, measure(read_pile(path))))
    for f in a.files:
        rows.append((os.path.basename(f.rstrip("/")), measure(read_pile(f))))
    if not rows:
        ap.error("give at least one file or --pile")
    if a.json:
        print(json.dumps({k: v for k, v in rows}, indent=2))
        return
    print("| source | " + " | ".join(COLS) + " |")
    print("|---|" + "---:|" * len(COLS))
    for label, m in rows:
        print(f"| {label} | " + " | ".join(str(m[c]) for c in COLS) + " |")


if __name__ == "__main__":
    sys.exit(main())
