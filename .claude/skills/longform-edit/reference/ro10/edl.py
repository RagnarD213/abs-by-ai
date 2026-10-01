"""RO-10 edit decision list: source ranges on C1704 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro10"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1704.MP4"
# (id, in, out, text-anchor, why)
PIECES = [
 ("hook",  114.44, 145.10, "If you're struggling to lose weight ... so you can lose your belly fat.", "take 3 of 3, the only one without a restart (take 1 restarted 'You're gonna be surprised', take 2 'what kind of day'); no plane rumble in its gaps (20-120 Hz matches the post-plane retake)"),
 ("haub",  170.34, 190.66, "In 2010, a nutrition professor at Kansas State ... eating less calories.", "only take"),
 ("stan1", 199.30, 207.82, "Here's the second one. In 2018, Stanford ... for a full year.", "second copy (first stopped at 'or a low-' 198.8)", 207.97),
 ("stan2", 211.96, 229.84, "Both groups lost about the same amount of weight ... the same rate.", "second copy of 'Both groups' (first said 'wheat', Gemini listen)"),
 ("barely",236.12, 264.22, "Now I know a lot of you guys are saying, but Dan ... how to fix that.", "second copy (first stopped at 'and I can-' 235.5)"),
 ("w1a",   264.96, 279.36, "Number one, take Zepbound ... so you eat fewer calories.", "only take; out extended over the 's' tail (-49 dB to 279.46)", 279.50),
 ("w1b",   289.02, 294.44, "In a big clinical trial, people on the highest dose of Zepbound lost about 20% of their body weight.", "third attempt, the only complete one (280.0 'In the big clinical trial,' abandoned; 282.3 copy re-said)"),
 ("w1c",   294.88, 298.30, "I take a low dose myself, about 1.5 milligrams per week,", "first attempt up to 'per week,' (keeps his dose); it then stalls on 'was that it-'", 298.33),
 ("w1d",   303.86, 331.02, "and the biggest change was that I stopped thinking about food all day ... in the description.", "retake from 'and' (after its 0.3 s pause), continuous", None, 303.80),
 ("w2a",   332.18, 334.84, "Alright, here's the second one. Know your number.", "only take"),
 ("w2b",   340.10, 367.34, "Telling someone to eat less doesn't mean anything ... your average for the week.", "retake (first stopped at 'doesn't know how' 338.4); onset measured on the envelope", None, 340.02),
 ("w2c",   392.36, 420.86, "If the average isn't dropping, lower your number a little and keep going ... nobody stuck with it.", "third copy of the line (371.1 and 387.3 re-said after a drink of water), continuous into Number 3"),
 ("w3b",   426.54, 456.68, "With AI you just take a picture of your plate ... fewer hours in the day to eat,", "second copy (first 421.3 'you get the calories and the protein.' re-said)", 456.76),
 ("w4b",   467.32, 479.30, "And when you've got fewer hours to eat, you eat less calories without really trying ... dinner in the evening.", "third copy (457.0 and 461.5 re-said)"),
 ("w4c",   488.12, 556.30, "And here's why I love this ... your mornings get so much easier.", "second copy (first 480.0 re-said), continuous through Number 5"),
 ("w5b",   564.26, 581.28, "Drinking black coffee alone is powerful ... Researchers at Penn State tested this.", "second copy (557.1 'Drinking black coffee is...' + throat clear removed)"),
 ("w6b",   588.46, 637.20, "They gave people a big, low calorie salad before their meal ... carb snacks do the opposite.", "second copy (581.7 stopped at 'as much of the main'), continuous into Number 7"),
 ("w7b",   651.18, 686.68, "Chips, crackers, and granola bars are designed in a lab ... stop drinking liquid calories.", "third copy (637.9 'and gr-' abandoned; 644.6 said 'so that way you')"),
 ("w8a",   692.10, 738.82, "I've talked about this before on the channel ... zero calorie drinks.", "second copy of the channel line (687.2 re-said); in set before the \"I\" (snap stopped in the I-ve dip)", 738.92, 691.97),
 ("w8b",   748.58, 784.06, "For a lot of you guys, this one change is enough ... far, far easier.", "second copy of the line (739.2 re-said after a 5 s pause), continuous through the wrap"),
 ("end",   802.78, 814.04, "Now, calories are the most important thing ... don't miss that next video.", "retake after 'roll it back' (784.9 copy re-said)"),
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
