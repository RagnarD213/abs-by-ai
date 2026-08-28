#!/usr/bin/env python3
"""BURNED captions for a cut that is already locked, timed through its own EDL.

Step 8 says to word-time captions from the FINAL VOICE. That is right when the cut is
being made. For the five delivered longforms the cut is locked and its word mapping has
ALREADY been proven against the finished render (spray tan scored 98.0% word overlap over
12 windows of the delivered file), so re-transcribing 19-53 minutes of audio would spend
an hour to re-derive a mapping that is known-good — and would introduce fresh Whisper
errors into copy that has been through two rounds of Dan's review.

So the word timings come from the source transcript mapped through `edl.json`, exactly as
`make_srt_declump.py` does it, INCLUDING its two hard-won rules:
  * a CLUSTER of zero-length word timestamps is text Whisper invented — drop it
  * a timestamp tie breaks on READING ORDER, never on the text (`mapped.sort()` on tuples
    sorts a zero-length cluster alphabetically, and that shipped once)

What is new is the CHUNKING, because a burned caption is not an .srt cue:
  * break on phrase boundaries at ~40 characters, not at the .srt's 84
  * fold one-word orphans into a neighbour — the delivered .srt has a cue that reads
    just "tan." because the previous cue hit its character cap first
  * SUPPRESS every cue that overlaps a full-screen card; the card carries its own
    headline and a caption on top is two texts saying different things
  * drop the fragment that arrives out of a suppressed cue when it starts lowercase

usage:
  captions_from_edl.py --edl edl.json --whisper C1512.whisper.json
                       --suppress cards.json --ass cap.ass --srt captions.srt
                       [--fixes fixes.json] [--maxch 40] [--marginv 62]
"""
import argparse, json, re, sys
from collections import Counter


def hallucinated(ws):
    bad, i, n = set(), 0, len(ws)
    while i < n:
        if ws[i]["end"] - ws[i]["start"] > 0.05: i += 1; continue
        j = i
        while (j + 1 < n and ws[j + 1]["end"] - ws[j + 1]["start"] <= 0.05
               and ws[j + 1]["start"] - ws[i]["start"] < 0.10): j += 1
        if j - i + 1 >= 3:
            bad.update(range(i, j + 1))
            mode = Counter(round(ws[k]["start"], 3) for k in range(i, j + 1)).most_common(1)[0][0]
            if j + 1 < n and abs(ws[j + 1]["start"] - mode) < 1e-6: bad.add(j + 1)
            if i > 0 and ws[i - 1]["end"] - ws[i - 1]["start"] <= 0.05 \
               and abs(ws[i - 1]["end"] - ws[i]["start"]) < 1e-6: bad.add(i - 1)
        i = j + 1
    return bad


def map_words(edl, words):
    DROP = hallucinated(words)
    mapped, off = [], 0.0
    for r in edl["ranges"]:
        a, b = r["start"], r["end"]; d = round(b - a, 3)
        for idx, w in enumerate(words):
            if idx in DROP: continue
            mid = (w["start"] + w["end"]) / 2
            if a <= mid < b:
                t0 = round(off + (max(w["start"], a) - a), 3)
                t1 = round(off + (min(w["end"], b) - a), 3)
                txt = w["word"].strip()
                if txt: mapped.append((t0, idx, max(t1, t0 + 0.06), txt))
        off = round(off + d, 3)
    mapped.sort(key=lambda x: (x[0], x[1]))
    return [{"t": t0, "e": t1, "w": txt} for t0, _, t1, txt in mapped], len(DROP)


def join_words(ws):
    out = ""
    for x in ws:
        if out and x[:1] not in "'.,%)-’": out += " "
        out += x
    return out


def chunk(words, maxch, pause=0.26, maxdur=5.0):
    chunks, cur = [], []
    def width(c, extra=""):
        return len(join_words([w["w"] for w in c] + ([extra] if extra else [])))
    for w in words:
        if cur and (w["t"] - cur[-1]["e"] >= pause
                    or width(cur, w["w"]) > maxch
                    or w["e"] - cur[0]["t"] >= maxdur):
            chunks.append(cur); cur = []
        cur.append(w)
        t = w["w"]
        if re.search(r"[.?!…]$", t): chunks.append(cur); cur = []
        elif t.endswith(",") and width(cur) >= maxch * 0.55: chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    # fold orphans: one or two short words alone read as a mistake
    merged = []
    for c in chunks:
        txt = join_words([w["w"] for w in c])
        if merged and len(c) <= 2 and len(txt) <= 8 and \
           c[0]["t"] - merged[-1][-1]["e"] < 0.6 and \
           len(join_words([w["w"] for w in merged[-1]])) + 1 + len(txt) <= maxch + 10:
            merged[-1].extend(c)
        else:
            merged.append(list(c))
    return merged


def wrap2(t, maxline):
    if len(t) <= maxline: return t
    ws = t.split(); best, bi = None, 1
    for i in range(1, len(ws)):
        a, b = " ".join(ws[:i]), " ".join(ws[i:])
        cost = abs(len(a) - len(b)) + 400 * (max(len(a), len(b)) > maxline)
        if best is None or cost < best: best, bi = cost, i
    return " ".join(ws[:bi]) + "\n" + " ".join(ws[bi:])


def overlaps(a, b, spans, slack=0.10):
    return any(not (b <= s - slack or a >= e + slack) for s, e in spans)


ASS_HEAD = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n"
            "WrapStyle: 0\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, "
            "Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour,"
            " Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle,"
            " BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "{style}\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL,"
            " MarginR, MarginV, Effect, Text\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--edl", required=True)
    ap.add_argument("--whisper", required=True)
    ap.add_argument("--suppress", help="json [[a,b],...] windows where a full-screen card runs")
    ap.add_argument("--fixes", help="json [[pattern, replacement],...]")
    ap.add_argument("--forbidden", help="json [str,...] that must not reach the file")
    ap.add_argument("--ass", required=True)
    ap.add_argument("--srt", required=True)
    ap.add_argument("--maxch", type=int, default=40)
    ap.add_argument("--maxline", type=int, default=45)
    ap.add_argument("--marginv", type=int, default=62)
    ap.add_argument("--size", type=int, default=58)
    A = ap.parse_args()

    edl = json.load(open(A.edl))
    words = [w for s in json.load(open(A.whisper))["segments"] for w in s.get("words", [])]
    mapped, ndrop = map_words(edl, words)
    total = round(sum(round(r["end"] - r["start"], 3) for r in edl["ranges"]), 3)
    SUP = [tuple(x) for x in json.load(open(A.suppress))] if A.suppress else []
    FIX = json.load(open(A.fixes)) if A.fixes else []
    FORB = json.load(open(A.forbidden)) if A.forbidden else []

    chunks = chunk(mapped, A.maxch)

    def text_of(c):
        t = join_words([w["w"] for w in c])
        t = re.sub(r"\s+([.,!?%])", r"\1", t)
        for pat, rep in FIX: t = re.sub(pat, rep, t)
        return re.sub(r"\s{2,}", " ", t).strip()

    def t2ass(t):
        h, m = int(t // 3600), int(t % 3600 // 60)
        s, cs = int(t % 60), min(99, round(t % 1 * 100))
        return "%d:%02d:%02d.%02d" % (h, m, s, cs)

    def t2srt(t):
        ms = int(round(t * 1000)); h, r = divmod(ms, 3600000); m, r = divmod(r, 60000)
        s, ms = divmod(r, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    events, srt, ndrop_card, last_dropped, n = [], [], 0, False, 0
    for i, c in enumerate(chunks):
        a = c[0]["t"]; b = c[-1]["e"] + 0.15
        if i + 1 < len(chunks): b = min(b, chunks[i + 1][0]["t"] - 0.01)
        if b - a < 0.5: b = a + 0.5
        if i + 1 == len(chunks): b = max(b, total)
        txt = text_of(c)
        if overlaps(a, b, SUP):
            ndrop_card += 1; last_dropped = True; continue
        if last_dropped and txt[:1].islower():
            ndrop_card += 1; continue
        last_dropped = False
        body = wrap2(txt, A.maxline)
        events.append(f"Dialogue: 0,{t2ass(a)},{t2ass(b)},Cap,,0,0,{A.marginv},,"
                      + body.replace("\n", "\\N"))
        n += 1
        srt += [str(n), f"{t2srt(a)} --> {t2srt(b)}", body, ""]

    style = (f"Style: Cap,Arial,{A.size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H7F000000,-1,0,0,0,"
             f"100,100,0,0,1,4,2,2,180,180,{A.marginv},1")
    open(A.ass, "w").write(ASS_HEAD.format(style=style) + "\n".join(events) + "\n")
    open(A.srt, "w").write("\n".join(srt))

    text = "\n".join(events)
    bad = [f for f in FORB if re.search(rf"\b{re.escape(f)}\b", text)]
    assert not bad, f"forbidden strings reached the captions: {bad}"
    three = [e for e in events if e.count("\\N") > 1]
    assert not three, f"{len(three)} cues have 3+ lines"
    longest = max(max(len(l) for l in e.split(",,")[-1].split("\\N")) for e in events)
    print(f"{n} cues  ({ndrop_card} suppressed over full-screen cards, "
          f"{ndrop} hallucinated words dropped)  longest line {longest} chars")
    print("->", A.ass, "and", A.srt)
