"""RO-15 edit decision list: source ranges on C1709 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/RO-15/round1"
# (id, in, out, text-anchor, why)
PIECES = [
 ("open",  134.44, 200.72, "This amino acid helped me sleep ... blood vessels in your hands and your feet.", "fourth and last run of the intro (the first three ended in 'Back to the top' x2 and 'Back to the top one more time'); runs straight on into the body"),
 ("cool",  202.30, 225.60, "So what that does is it lets more blood flow ... less sleepy the next day.", "second 'So what that does' (201.3 stopped at 'So wh-'); onset from the level strip", None, 202.30),
 ("persp", 229.20, 281.50, "Now I want to keep this in perspective ... Glycine could help with that.", "second 'Now I want to keep this' (226.3 said 'Now I want you to keep this' and stopped); onset from the level strip", 281.62, 229.10),
 ("cold",  294.20, 366.44, "If you rarely get hot at night ... that's worth it in my opinion.", "second 'If you rarely' (281.9 stopped, then a throat clear and a drink of water); onset from the level strip", None, 294.12),
 ("score", 373.20, 390.82, "My average sleep score before glycine ... it's not a cure-all.", "second copy (366.9 copy stopped at 'and now I'm usually in the se-'); onset from the level strip", None, 373.12),
 ("factors", 410.84, 435.44, "I've found that factors like what time I go to bed ... about 5% of your results.", "third copy (391.4 stopped at 'factors', 393.9 stopped before 'than glycine', then 'Roll that back a little bit'); out at 436.10 (independent check: 0.17 s between sentences ran 'results' into 'Once')", 436.10, 410.76),
 ("major", 439.54, 470.18, "Once you have the major things handled ... stop taking it.", "second 'Once you have the major' (436.4 stopped at 'thing-'); onset from the level strip; in at 439.30 for a sentence pause; out at 470.36 keeps his breath and ends in the quiet after it (re-check: 0.18 s pause at the join, raw 0.40)", 470.36, 439.30),
 ("numbers", 472.92, 494.04, "But if your numbers go up ... go to absbyai.com.", "second 'But if your numbers go up' (470.4 stopped at 'you've-'); in at 472.865, after a lip smack at 472.81-472.86 (re-check), 15 ms before the onset; runs on into the close", None, 472.865),
 ("member", 545.70, 559.92, "When you become a member ... see you in the next video.", "third and last run of the AI supplement audit lines (520.9 run re-said 'And it designs you', then 'One more time'); the last clean run", None, 545.62),
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
