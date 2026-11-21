#!/usr/bin/env python3
"""
The 80% rule for an assembled take: how many sentences of the result are Dan's own, as he said them?

WHY THIS EXISTS (2026-10-10, Dan Voice P2B step B9): for the pieces that matter most (sales videos and letters,
personal posts) Dan records a take and Claude only orders and cuts it. Research on this is clear: text a person wrote
and AI arranged reads as human, text AI wrote and a person edited does not. This script keeps the editor honest.

    python3 scripts/voice/assemble_check.py take.txt assembled.txt

A sentence counts as his when it matches a sentence in the take almost word for word (filler removed, case and
punctuation ignored, 90% of the words the same). Anything inside [+ ... +] is Claude's addition and never counts.
Exit code 1 when under 80%, or when an unmarked sentence is not in the take.
"""
import difflib
import re
import sys

FILLER = re.compile(r"\b(um+|uh+|er+m?|ah+|hmm+|mm+|you know|i mean|like)\b", re.I)


def sentences(text):
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+|\n+", text)
    return [p.strip() for p in parts if re.search(r"\w", p)]


def norm(s):
    return re.findall(r"[a-z0-9']+", FILLER.sub(" ", s.lower()))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    take = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    out = open(sys.argv[2], encoding="utf-8", errors="replace").read()
    added = re.findall(r"\[\+(.*?)\+\]", out, re.S)
    body = re.sub(r"\[\+.*?\+\]", " ", out, flags=re.S)
    src = [norm(s) for s in sentences(take)]
    joined = " ".join(w for s in src for w in s)
    his, not_his = 0, []
    for s in sentences(body):
        n = norm(s)
        if len(n) < 3:
            his += 1
            continue
        best = max((difflib.SequenceMatcher(None, n, t, autojunk=False).ratio() for t in src), default=0)
        if best >= 0.9 or " ".join(n) in joined:  # the same sentence, or a clean cut out of a longer one
            his += 1
        else:
            not_his.append(s)
    marked = sum(len(sentences(a)) for a in added)
    total = his + len(not_his) + marked
    share = 100.0 * his / total if total else 0.0
    print(f"{his} of {total} sentences are his as said ({share:.0f}%); {marked} marked additions; "
          f"{len(not_his)} unmarked sentences not found in the take.")
    for s in not_his:
        print("  NOT IN THE TAKE (mark it [+ +] or put his sentence back):", s[:140])
    return 1 if share < 80 or not_his else 0


if __name__ == "__main__":
    sys.exit(main())
