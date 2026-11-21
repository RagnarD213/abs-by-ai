#!/usr/bin/env python3
"""Word-timed burned captions for one aspect, rendered as PNG STATES (not libass).

Usage: s07_captions.py 9x16|16x9

Style: the approved Ad 1 / Ad 3 vertical treatment -- heavy sans, white, heavy black shadow,
the current word lit in the verticals' lime. Geometry from the approved vertical recipe
(`recipe-vertical/captions.py`): CAP_Y 1400 on 1080x1920, band 1385-1495.

ROUND 2, R1: CAPTIONS RUN FROM THE FIRST WORD TO THE LAST, over every beat including the photo
cards and the phone recording. Round 1 suppressed them under every card, so the whole hook -- "This
picture got me abs. And it's not even real!" -- was never on screen and only 12.6 s of the first
30 s carried a caption (D2), and lines restarted mid-sentence with words missing (D9). The cards
were relaid so the caption band is CLEAR (A.CARD_RECT stops above it and the band is J2AD field),
which is what makes running them everywhere legal rather than a collision.

Each state is exported for the delivery gate's evidence contract v2: the actual PNG the compositor
drew, its rect and its word.
"""
import hashlib, json, os, subprocess, sys
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra04")
import ra01lib as L
from ra01lib import Aspect, LIME
from PIL import Image, ImageDraw, ImageFilter
from motionlib import font, text_size

KEY = sys.argv[1]
A = Aspect(KEY)
OUT = f"cap_{KEY}"; os.makedirs(OUT, exist_ok=True)
B = json.load(open("beats.json"))
WORDS = json.load(open("words_aligned.json"))["words"]
TOTAL = B["total"]
FD = L.FD
snapf = lambda t: round(round(t/FD)*FD, 6)
F = font(A.CAP_SIZE, "ExtraBold")
GROUP_MAX = 22
MIN_STATE = 2*FD

# R1: nothing is muted. The ONE exception is the end card, which is the only full-screen card left
# and carries its own "Tap the button below" and URL: the last line's HOLD is clipped to its
# in-point so two calls to action never share a frame. No word loses its caption -- the last word
# ends 0.3 s before the end card starts.
MUTE = []          # RA-04: no end card; captions run to the last word

# ⚠ D9 / R1: SENTENCE BOUNDARIES COME FROM THE SCRIPT, NOT FROM WHISPER. Whisper ran two of the
# script's sentences together -- "...got me abs and it's not even real." and "...was 200 pounds and
# this is what I look like today." -- so a caption line began mid-sentence with a lowercase "and".
# Each pair below is (last word of a sentence, first word of the next) as the script writes them;
# the period is restored and the next word capitalised. A pair that is already punctuated is left
# alone, and a pair that is not in this cut fails loudly rather than silently.
SENTENCE_BREAKS = [("goal", "and")]
import re as _re
_n = lambda s: _re.sub(r"[^a-z0-9']", "", s.lower())
cur = 0
for a, b in SENTENCE_BREAKS:
    for i in range(cur, len(WORDS)-1):
        if _n(WORDS[i]["w"]) == a and _n(WORDS[i+1]["w"]) == b:
            if not WORDS[i]["w"].strip().endswith((".", "?", "!")):
                WORDS[i]["w"] = WORDS[i]["w"].strip().rstrip(",") + "."
                print(f"  sentence break restored from the script: {a!r} -> {b!r}")
            cur = i+1
            break
    else:
        raise SystemExit(f"script sentence break {a!r}->{b!r} is not in this cut")

# ⚠ D9: EVERY SENTENCE STARTS WITH A CAPITAL. Round 1 printed "it inspired me to" and "it gave me
# a" because Whisper had heard those words mid-sentence in the untrimmed roll. Casing is decided
# here, from the punctuation of the PREVIOUS word, not from whatever Whisper wrote.
for i, w in enumerate(WORDS):
    starts = (i == 0) or WORDS[i-1]["w"].strip().endswith((".", "?", "!"))
    if starts and w["w"][:1].islower():
        w["w"] = w["w"][:1].upper() + w["w"][1:]

gs, cur = [], []
for w in WORDS:
    if cur and cur[-1]["w"].rstrip().endswith((".", "?", "!")):
        gs.append(cur); cur = [w]; continue
    cand = cur + [w]
    if len(" ".join(x["w"].strip() for x in cand)) > GROUP_MAX and cur:
        gs.append(cur); cur = [w]
    elif cur and w["t"] - cur[-1]["e"] > 0.55:
        gs.append(cur); cur = [w]
    else:
        cur = cand
if cur: gs.append(cur)

# state schedule, frame-snapped: the LAST word of a line holds until the next line or 0.7 s,
# and never past a card (ad-edit: a held caption must not run onto the next graphic).
states = []
for gi, g in enumerate(gs):
    nxt = gs[gi+1][0]["t"] if gi+1 < len(gs) else TOTAL
    # ⚠ NO BLANK BETWEEN LINES. `stop - 0.06` left a TWO-FRAME hole at every one of the 52 line
    # changes -- measured on the round-2 picture at f43-44, between "This picture got me" and
    # "abs." It reads as a flicker on every line, and R1 says a caption is never dropped. The last
    # word of a line now holds until the next line STARTS. The 0.06 s stand-off is kept only against
    # the end card, the one graphic a caption must not touch.
    mute = [a for a, _ in MUTE if a > g[0]["t"]]
    stop = min([m - 0.06 for m in mute] + [nxt, TOTAL])
    txt = " ".join(x["w"].strip() for x in g)
    for k, w in enumerate(g):
        a = snapf(w["t"])
        if k < len(g)-1:
            b = snapf(g[k+1]["t"])
        else:
            b = snapf(min(w["e"] + 0.70, stop))
        b = max(b, snapf(a + MIN_STATE))
        if k < len(g)-1:
            b = min(b, snapf(g[k+1]["t"]))
        states.append({"name": f"cap{len(states):04d}", "word": w["w"].strip(),
                       "line": txt, "k": k, "beat": [a, max(b, snapf(a+MIN_STATE))]})
# no state may run into the next
for i in range(len(states)-1):
    if states[i]["beat"][1] > states[i+1]["beat"][0]:
        states[i]["beat"][1] = states[i+1]["beat"][0]
states = [s for s in states if s["beat"][1] - s["beat"][0] >= FD*0.9]

os.makedirs(f"{OUT}/png", exist_ok=True)
# ROUND 2 (RA-15): in the cardboard nutritionist clip the fallen cutout's face lies at the right end of the caption band (y 1380-1550), the
# clip's punchline. Every line that STARTS inside that card is lifted whole onto the table (never a lift mid-line). 9:16 only.
_bc = {c["name"]: c["beat"] for c in json.load(open("beats.json"))["cards"]}
LIFTS = [(_bc["cutout"][0] - 0.02, _bc["cutout"][1], 1215)] if KEY == "9x16" and "cutout" in _bc else []
for s in states:
    if s["k"] == 0: _cur = s["beat"][0]
    s["line_t0"] = _cur
for s in states:
    s["cap_y"] = next((y for a0, b0, y in LIFTS if a0 <= s["line_t0"] < b0), A.CAP_Y)
# ROUND 3, 16:9: the lower thirds sit at the bottom of the frame (approved 16:9 box, top ~840) over the caption band (930-1040), so a
# line that is on screen at any moment a lower third is up is lifted WHOLE above the strip (standing rule 2026-09-02: captions never
# overlap a graphic; lift, never mid-line). The lift is measured from the rendered strip's box (hf16/manifest.json) and the ink's own
# height incl. the 9 px shadow blur, with 24 px to spare.
if KEY == "16x9":
    _man = json.load(open("hf16/manifest.json"))
    _ink_h = sum(F.getmetrics()) + 12          # cap_y is the top of the ascent box; the ink and its blur end by ascent+descent+12
    _lts = [(m["a"], m["b"], m["box"][1]) for m in _man if m["template"] == "lower-third"]
    _lines = {}
    for s in states: _lines.setdefault(s["line_t0"], []).append(s)
    _cards = [tuple(c["beat"]) for c in B["cards"]]
    for t0, ss in _lines.items():
        a1, b1 = ss[0]["beat"][0], ss[-1]["beat"][1]
        hit = [(a0, b0, top) for a0, b0, top in _lts if a1 < b0 and b1 > a0 - 0.02]
        if not hit: continue
        if any(ca <= a1 < cb for ca, cb in _cards):
            # the line STARTS in a card (it sits on the field under the card) and runs into a strip: not lifted; its held state ends on
            # the strip's first frame (RA-14 round 3 lesson 5: clip at the hand-over, never lift mid-line)
            la = min(a0 for a0, _, _ in hit)
            assert all(s["beat"][0] < la for s in ss), ("a word starts under the strip", t0)
            for s in ss: s["beat"][1] = min(s["beat"][1], snapf(la))
            continue
        y = min(top for *_, top in hit) - 30 - _ink_h      # 30: the gate measured 19 px at 24 (min 20)
        for s in ss: s["cap_y"] = y
        # a lifted line that runs on into a card stops on the card's first frame (the card's picture sits where the lift puts it)
        for ca, cb in _cards:
            if a1 < ca < b1:
                assert all(s["beat"][0] < ca for s in ss), ("a word starts inside the card", t0)
                for s in ss: s["beat"][1] = min(s["beat"][1], snapf(ca))
    print("16:9 lifts:", sorted({(round(t0, 2), ss[0]["cap_y"]) for t0, ss in _lines.items() if ss[0]["cap_y"] != A.CAP_Y}))
for s in states:
    BASE = s["cap_y"] + F.getmetrics()[0]
    words = s["line"].split(" ")
    h = hashlib.md5(f"{s['line']}|{s['k']}|{s['cap_y']}|{KEY}".encode()).hexdigest()[:10]
    p = f"{OUT}/png/{h}.png"
    if not os.path.exists(p):
        im = Image.new("RGBA", A.size, (0, 0, 0, 0))
        tw = F.getlength(s["line"])
        x = int((A.VW - tw)//2)
        sh = Image.new("RGBA", A.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x, BASE), s["line"], font=F, fill=(0, 0, 0, 245), anchor="ls")
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(9)))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
        d = ImageDraw.Draw(im); cx = float(x)
        for j, ww in enumerate(words):
            d.text((int(cx), BASE), ww, font=F, fill=(LIME if j == s["k"] else (255, 255, 255)) + (255,),
                   anchor="ls")
            cx += F.getlength(ww + " ")
        im.save(p)
    s["image"] = os.path.abspath(p)
    s["rect"] = [0, 0, A.VW, A.VH]

blank = f"{OUT}/png/_blank.png"
if not os.path.exists(blank): Image.new("RGBA", A.size, (0, 0, 0, 0)).save(blank)
# ⚠ ONE ENTRY PER OUTPUT FRAME. Writing per-state durations and letting the concat demuxer resample
# put five states one frame away from where the plan said they were, and the delivery gate -- which
# samples each state at its beat midpoint -- could not find them in the delivered pixels. A list
# with exactly TOTALF entries maps 1:1 onto the timeline and cannot drift.
TOTALF = int(round(TOTAL/FD))
frame_state = [None]*TOTALF
for si, st in enumerate(states):
    f0 = int(round(st["beat"][0]/FD)); f1 = int(round(st["beat"][1]/FD))
    f0 = max(0, min(TOTALF-1, f0)); f1 = max(f0+1, min(TOTALF, f1))
    for f in range(f0, f1): frame_state[f] = si
    st["beat"] = [round(f0*FD, 6), round(f1*FD, 6)]      # the beat IS the rendered frame span
# ROUND 4 (RA-04): the concat demuxer's 6-decimal duration (0.033367 > 1001/30000) put every state change ONE FRAME LATE (a frame-
# by-frame match of captions.mov against the list: 217 of 217 changes late), so a lifted 16:9 caption overlapped a card's first frame.
# One symlink per output frame, read as an image sequence at exactly 30000/1001, maps frame n to state n.
import shutil
SEQ = f"{OUT}/seq"; shutil.rmtree(SEQ, ignore_errors=True); os.makedirs(SEQ)
for i in range(TOTALF):
    os.symlink(states[frame_state[i]]["image"] if frame_state[i] is not None else os.path.abspath(blank), f"{SEQ}/{i:05d}.png")
subprocess.run([L.FF, "-nostdin", "-v", "error", "-y", "-framerate", "30000/1001", "-i", f"{SEQ}/%05d.png", "-frames:v", str(TOTALF),
                "-c:v", "qtrle", "-pix_fmt", "argb", f"{OUT}/captions.mov"], check=True)
# an SRT sidecar describing the LINES (what captions:card_collision and captions:within_runtime read)
def ts(x):
    h = int(x//3600); m = int(x % 3600//60); s = x - h*3600 - m*60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
lines, i = [], 1
idx = 0
for g in gs:
    n = len([w for w in g])
    grp = [st for st in states if st["line"] == " ".join(x["w"].strip() for x in g)]
    seg = states[idx:idx+len(g)]
    seg = [x for x in seg if x["line"] == " ".join(y["w"].strip() for y in g)]
    if not seg:
        continue
    idx += len(seg)
    lines.append(f"{i}\n{ts(seg[0]['beat'][0])} --> {ts(seg[-1]['beat'][1])}\n"
                 f"{seg[0]['line']}\n"); i += 1
open(f"{OUT}/captions.srt", "w").write("\n".join(lines))
kept = len(states)
json.dump({"states": states, "groups": len(gs), "words_total": len(WORDS), "captioned": kept,
           "cap_y": A.CAP_Y, "font_px": A.CAP_SIZE},
          open(f"{OUT}/caption_states.json", "w"), indent=1)
uncaptioned = len(WORDS) - sum(len(g) for g in gs)
assert uncaptioned == 0, f"{uncaptioned} words have no caption — R1 requires every word captioned"
print(f"{KEY}: {len(WORDS)} words, {kept} captioned states in {len(gs)} lines, "
      f"0 suppressed (R1: captions run over every beat)")
print(f"  -> {OUT}/captions.mov  +  captions.srt  +  caption_states.json")
