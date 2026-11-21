#!/usr/bin/env python3
"""Phrase lookup on the C1706 Whisper words: at("needles and vials", 168) -> (start, end) source seconds of the phrase
occurrence nearest `near`. Used to anchor every graphic and insert to the words Dan says."""
import json, re, os
P = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1706.roll/words.json"
_w = json.load(open(P)); _w = _w["words"] if isinstance(_w, dict) else _w
WORDS = [dict(w=re.sub(r"[^a-z0-9.]", "", x["word"].lower()).strip("."), s=x["start"], e=x["end"]) for x in _w]
def at(phrase, near, span=25.0):
    toks = [re.sub(r"[^a-z0-9.]", "", t).strip(".") for t in phrase.lower().split()]
    best = None
    for i in range(len(WORDS) - len(toks) + 1):
        if abs(WORDS[i]["s"] - near) > span: continue
        if all(WORDS[i + j]["w"] == toks[j] for j in range(len(toks))):
            d = abs(WORDS[i]["s"] - near)
            if best is None or d < best[0]: best = (d, WORDS[i]["s"], WORDS[i + len(toks) - 1]["e"])
    if best is None: raise KeyError(f"phrase not found: {phrase!r} near {near}")
    return best[1], best[2]
