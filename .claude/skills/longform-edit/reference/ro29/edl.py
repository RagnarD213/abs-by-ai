"""RO-29 edit decision list: source ranges on rolls C1772 + C1773 (virtual timeline) (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Expansion/_edit_work/RO-29/round1"
# Virtual source timeline: C1772 at 0, C1773 (recap retake) at 380.38 s (frames.OFF). (id, in, out, text, why[, out_override, in_override])
PIECES = [
 ("open",  14.88,  41.14, "Cortisol belly is real ... That part is true.", "second start of the hook (9.30 stopped at 'like the cortisol...'); the 2.7 s slate 'This video is...' dropped"),
 ("yale",  47.84,  89.10, "In a Yale study, women with more belly fat ... whose cortisol stayed calm.", "second read of the Yale line (41.7 read complete, re-said at once: last clean take); runs on through 'What TikTok gets wrong' and the second Yale study"),
 ("calm",  96.06, 114.62, "On a calm day, they ate the same and they went for more sweets. ... you will gain fat.", "the re-said 'On a calm day' (89.6 read: '...and then went for'; the retake matches the script's 'And they went for more sweets')"),
 ("cocktail", 126.86, 186.24, "Stress does not directly lead to belly fat ... The second thing is to train every day.", "second read of 'Stress does not directly lead' (115.1 read, re-said after 8.7 s); one read through the cocktail, supplements, fix 1 and the 'train every day' line"),
 ("train", 193.18, 198.94, "Training is one of the best ways there is to burn off stress. I work out first thing in the morning seven days a week.", "third start (186.9 'Training is one of the best ways to...' stopped; Gemini restart listen; small.en on the region puts the final 'Training' at 193.18)"),
 ("morning", 209.14, 217.56, "When I started working out first thing in the morning ... fewer calories.", "second read of 'When I started working out' (199.3 read complete, re-said after 5 s)"),
 ("late",  221.40, 279.40, "I also did a lot less late night eating ... cut them off until they change.", "second start of 'I also did a lot less' (217.6 stopped at 'than wh-'; Gemini restart listen + level strip: 10 ms levels: the final read starts 221.02); one read through fixes 3, 4 and most of 5", 279.66, 220.96),
 ("late2", 281.66, 299.22, "Now I know a lot of you guys are saying ... you are gonna die many years earlier.", "second start of 'Now I know a lot' (279.88 'now I know a lot' stopped; assembled-ASR check; level strip: voice from 281.66)", None, 281.54),
 ("worth", 302.92, 319.58, "Is it worth killing yourself for this marriage ... stressful person or job in your life.", "one read (3.7 s pause before it closed by the cut)"),
 ("tolerance", 327.70, 335.46, "You'll find that if you have zero tolerance ... who refuse to change.", "fourth start (320.1 'You'll find you have zero', 321.7 'You'll find that y-' stopped; Gemini restart listen)"),
 ("sixth", 338.16, 350.88, "And here's the sixth thing. Don't use stress as an excuse ... hit your calories.", "second 'And here's the sixth thing' (335.5 read re-said at once)"),
 ("routine", 354.04, 359.50, "You should have a routine where you're eating nearly the same thing every day, regardless of whether you feel great or terrible.", "second start (351.4 stopped at 'where eating nearly...')"),
 ("discipline", 362.25, 373.82, "Even if you do everything you can to reduce stress ... when you can't avoid it.", "second start (360.3 'Even if you do reduce...' stopped; onset from the level strip)"),
 ("recap", 384.74, 411.50, "So, let's review the six things ... no matter how you feel.", "C1773 recap retake, one read"),
 ("outro", 428.94, 439.74, "Pick the one you're worst at ... as soon as they're published.", "C1773 second ending (the 412.1 read ended with Dan's 'Roll that back a little')"),
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
