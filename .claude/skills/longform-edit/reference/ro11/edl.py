"""RO-11 edit decision list: source ranges on C1705 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro11"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1705.MP4"
# (id, in, out, text-anchor, why)
PIECES = [
 ("hook",  117.46, 198.28, "You can still gain fat ... I'll link to it in the description.", "hook take 3 of 3 (all three clean; the last runs straight into Number one with no stop); in set 0.14 s before the measured onset (118.24)", None, 118.10),
 ("sleep2",202.30, 245.68, "Get seven to eight hours ... two of the other factors in this video.", "second copy (first said 'and your art' 200.8)"),
 ("alc2",  262.58, 281.10, "I made a whole video on whether you can drink alcohol ... So let me keep it real with you.", "fourth copy of the line, the only clean one (246.3 'whole factor', 248.6 stopped, 251.2 ended on 'too' then re-said, 258.3 'still drink alcohol and have abs')"),
 ("horm",  289.30, 313.64, "For most of you guys, hormones aren't the main reason ... without changing their diet at all.", "second copy (first ended 'let me explain the difference' 287.5)"),
 ("cort",  318.12, 328.56, "The second one is cortisol ... in your belly specifically.", "second copy (identical first copy 314.2 re-said)"),
 ("test",  334.94, 341.38, "So if you think you might have low testosterone ... instead of just guessing.", "second copy (first stopped at 'you'll know you' 334.3)"),
 ("warn",  345.68, 375.36, "And I want to warn you about something ... the next factor is timing.", "second copy (first stopped at 'The normal range' 344.7)"),
 ("time",  381.52, 426.46, "What time you eat makes a difference ... stronger than most people realize.", "second copy (identical first copy 376.0 re-said)"),
 ("ill",   432.59, 564.50, "Researchers at the University of Illinois ... not in the way that you might expect.", "second copy (first stopped at 'obese adults' 430.8), continuous through Number five"),
 ("card1", 586.77, 614.22, "A lot of guys are doing cardio ... nobody told them to change their diet.", "second copy, after a 17 s pause and throat clear (first copy 565.0 stopped after 'leaner')"),
 ("card2", 621.00, 636.10, "The group doing the most cardio ... it came from eating more.", "second copy (first stopped at '1,700' 618.2)"),
 ("card3", 639.90, 650.20, "Nine out of ten people in that group ... you earned a treat.", "second copy (first stopped at 'made up for' 638.9)"),
 ("card4", 652.52, 713.94, "So if you're not tracking your calories ... the fat they gained was wildly different.", "second copy of 'So if you're not' (650.8 'So you're not tracking'); keeps the FIRST 'but the fat they gained was wildly different' because it is one unbroken sentence with 'Everybody got the same extra food,' (the re-said copy at 715.7 would need a cut with no pause)"),
 ("neat1", 718.26, 726.22, "One person gained less than a pound ... the same extra calories.", "only take"),
 ("neat2", 730.78, 747.50, "So, what was the difference? ... when you're dieting.", "second copy (first said 'how much they moved.' 729.9, re-said with 'around during the day')"),
 ("neat3", 751.32, 807.78, "When you cut your calories, your body quietly ... Lift weights, and keep your steps up.", "second copy (first stopped at 'your body has qu-' 750.4), continuous through the wrap"),
 ("end",   841.52, 854.82, "Do those seven things ... subscribe for more videos like this one.", "the retake after 'roll it back' (says 'the FIRST video on calories'; the 808.0 copy needed three tries at that line); in after the lip click at 841.54", None, 841.60),
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
