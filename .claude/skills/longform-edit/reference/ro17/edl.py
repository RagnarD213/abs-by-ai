"""RO-17 edit decision list: source ranges on C1713 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/RO-17/round2"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1713.MP4"
# (id, in, out, text-anchor, why)
PIECES = [
 ("open",     54.86, 101.20, "You can get fat eating healthy foods ... than any workout program I ever followed.", "opening take 2 of 2 (take 1 at 8.5 s stopped after 'for years': 'Back to the top one more time'); runs on into the list, so the first 46 s has no join"),
 ("food1",   101.88, 105.86, "Food number one is trail mix. Trail mix has a great reputation.", "first copy; its next sentence ended 'good at you' and was re-said twice"),
 ("nuts",    115.26, 152.42, "It's nuts and fruit ... 65 grams of carbs.", "third copy of 'It's nuts and fruit' (107.6 'good at you', 112.3 stopped after 'hiking')"),
 ("bigmac",  155.54, 162.26, "That's more calories than a Big Mac ... being healthy the whole time.", "second 'Big Mac' (he re-said it at once)"),
 ("average", 173.18, 209.32, "That's how you become the average American ... any of that off.", "second copy (162.8 stopped at 'calories of...', then a throat clear)"),
 ("doing",   215.90, 259.42, "And I was doing this too ... 26 of those grams are sugar.", "second 'And I was doing this too' (209.8 then a 5 s stop)"),
 ("grapes",  263.34, 270.12, "That's about the same as a big bowl of grapes ... fills you up.", "second copy (he re-said it at once)"),
 ("raisins", 275.68, 310.44, "The raisins fit in the palm of your hand ... before you can eat too much of it.", "second copy (270.5 'and you can eat them in just three bites', re-said); script wording"),
 ("coconut", 329.68, 377.48, "And the third one is coconut water ... Just drink water.", "second copy (324.4 stopped at 'sold as the na-'; before it 14 s of coughs and a drink)"),
 ("electro", 380.32, 400.66, "And if you want the electrolytes ... confused by this.", "second copy ('And if you want to get...' at 377.9 abandoned)"),
 ("notsay",  405.88, 420.56, "I'm not saying these foods are bad ... eating fewer calories.", "second copy (401 said 'small amounts for them')"),
 ("budget",  429.52, 442.02, "You only get so many calories a day ... nothing left for dinner.", "second copy (421.0 said 'in a day ... and...' then a 4 s stop)"),
 ("because", 445.00, 459.94, "Just because it says healthy on the bag ... less need to snack.", "second 'Just because' (442.4 stopped at 'it says,')"),
 ("snacking",472.64, 497.84, "In my experience ... try a can out.", "after a 12 s stop (he drank water)"),
 ("surprised",509.48,543.54, "You might be surprised to find you really like them ... nothing else in it.", "third copy of 'You might be surprised' (498.3 'like the taste', 503.5 'surprised you find' + stop); script wording"),
 ("chipotle",549.40, 554.70, "The chicken one is about 180 calories ... about $7.", "second copy (543.5 stopped at 'it costs...'); the spoken price is about $7"),
 ("running", 558.54, 591.84, "If you're out running around ... so much easier.", "third 'If you're' (555.4, 557.5 stopped)"),
 ("addict",  604.14, 614.52, "Carbs and sugar are addictive ... help you lose weight.", "second copy, after a noise check on set ('You hearing that? No? Okay.')"),
 ("wrap",    645.82, 666.56, "Alright guys, those are three healthy foods ... see you in the next video.", "second wrap (615.2 wrap 1 said 'my three' and 'all three of them'; Dan re-read it after a prompter scroll)"),
]
FPS = 30000/1001
_lav = None
def lav():
    global _lav
    if _lav is None:
        wv = wave.open(f"{W}/lav.wav"); _lav = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    return _lav
def rms_db(t0, t1, sr=48000):
    a = lav()[int(t0*sr):int(t1*sr)]
    return 20*np.log10(np.sqrt(np.mean(a*a))+1e-9) if len(a) else -120
def _db(t, n=0.02):
    return rms_db(t, t+n)
def snap(tin, tout, thr=-50.0):
    """Measured edges. in: from 0.15 s after the first word's Whisper start, walk back through voiced 20 ms frames to the
    first quiet one (max 0.45 s back) = onset; keep 0.08 s of room before it. out: from 0.15 s before the last word's
    Whisper end, walk forward through voiced frames to the first 80 ms that stays quiet (max 0.5 s) = offset; keep 0.12 s."""
    t = tin+0.15
    if _db(t) <= thr:                       # Whisper start is late: step forward to the voice first
        while t < tin+0.40 and _db(t) <= thr: t += 0.01
    while t > tin-0.45 and _db(t-0.02) > thr: t -= 0.01
    a = max(0, t-0.08)
    t = tout-0.15
    while t < tout+0.50 and max(_db(t), _db(t+0.02), _db(t+0.04), _db(t+0.06)) > thr: t += 0.01
    b = t+0.12
    return round(a, 3), round(b, 3)
def pieces():
    out = []
    for row in PIECES:
        pid, a, b, txt, why = row[:5]
        sa, sb = snap(a, b)
        if len(row) > 5 and row[5] is not None: sb = row[5]      # measured by hand (energy profile + medium.en)
        if len(row) > 6 and row[6] is not None: sa = row[6]
        out.append(dict(id=pid, word_in=a, word_out=b, **{"in": sa, "out": sb}, text=txt, why=why))
    # never overlap the next piece's source audio
    return out
if __name__ == "__main__":
    P = pieces(); json.dump(P, open(f"{W}/edl.json", "w"), indent=1)
    tot = sum(p["out"]-p["in"] for p in P)
    for p in P: print(f"{p['id']:6s} {p['in']:8.3f} {p['out']:8.3f}  ({p['word_in']-p['in']:+.2f}/{p['out']-p['word_out']:+.2f})")
    print("pieces", len(P), "duration", round(tot, 1), "s =", f"{int(tot//60)}:{tot%60:04.1f}")
