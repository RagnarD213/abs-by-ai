"""RO-14 edit decision list: source ranges on C1708 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/RO-14/round1"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1708.MP4"
# (id, in, out, text-anchor, why)
PIECES = [
 ("open1",   147.74, 170.92, "You are eating healthy ... reasons you are eating them in the first place,", "third run of the opening (27.7 and 90.5 were stopped for a prompter scroll: 'Roll it back to the top'); 144.7 'You are eating healthy' abandoned and re-said at once. Every take says FIVE hidden reasons; the video gives four. Cutting 'five' was tested and rejected (blind listen 2/10, 'jarring splice'); a pickup is on the 10/17 list"),
 ("open2",   174.58, 204.70, "And some of those five are going to make you angry ... It was invisible to me too.", "second 'And some of those five' (171.2 said it once, then re-said it)"),
 ("open3",   209.42, 219.00, "I was 200 pounds at 5'7 ... So let me show it to you.", "second 'I was 200 pounds' (205.2 said 'and I would told you with', stopped); onset measured on the level strip (medium.en folds the restart into a 4 s 'told')", None, 209.34),
 ("open4",   224.34, 228.29, "There are four leaks. Almost everybody watching this has at least two of them.", "second copy (219.3 copy re-said at once)"),
 ("leak1a",  245.37, 262.81, "Leak number one ... That excuse is dead now.", "after a 15 s stop (he drank water)"),
 ("leak1b",  269.25, 277.41, "With AI, you take a photo of your plate ... There is no longer any reason not to know.", "second 'With AI' (263.4 copy re-said at once)"),
 ("leak2a",  279.61, 291.05, "Leak number two. Weekend blowouts ... erases all of it.", "second 'Leak number two' (278.0 re-said)"),
 ("leak2b",  294.81, 348.27, "This is why Monday to Friday dieters ... the bites of your kids food,", "second 'This is why Monday to Friday' (291.5 stopped at 'Friday's')"),
 ("leak4b",  353.10, 399.15, "The three chicken nuggets ... nobody else will say out loud.", "second 'the three chicken nuggets' (348.7 stopped at 'over the trash because'); onset from the level strip (medium.en folds it into a 4.7 s 'can')", None, 353.02),
 ("r1a",     405.99, 409.61, "Reason number one, you have a fat girlfriend or a fat wife.", "second copy (399.9 copy stopped at 'If your partner')"),
 ("r1b",     413.23, 447.67, "If your partner is not dedicated to fitness herself ... does not take care of her health.", "second 'If your partner' (410.2 stopped at 'fitness her-')", None, 413.04),
 ("r1c",     473.16, 481.21, "You will be less attracted to her ... instead of living.", "second copy after 'Roll this back a little bit' (447.97 copy ad-libbed 'and your own' and 'sooner than you think'); the script wording", None, 473.06),
 ("r1d",     483.68, 544.11, "And since she's the single biggest influence ... or another GLP-1.", "second 'And since she's the' (481.7 stopped)", None, 483.58),
 ("r3b",     547.28, 601.05, "If you have plateaued for months ... because it is not.", "second 'If you have plateaued for months' (544.6 stopped, 1.2 s pause)", None, 547.20),
 ("r4b",     615.13, 681.35, "It's not going to melt your belly ... like it is part of your diet, because it is.", "third 'It is not going to melt your belly' (601.1 and 604.9 stopped at 'What')"),
 ("s5b",     686.11, 708.93, "Pick a bedtime and defend it ... 100 hours or more of fitness content.", "second 'Pick a bedtime' (681.9 copy re-said at once)"),
 ("s5c",     712.50, 735.43, "Your problem is that nothing in your day is measured ... then you will actually be able to fix it.", "second 'Your problem is' (709.4 said 'nothing in this day is,'); the FIRST '30 days of honest tracking' (736.0 re-said it as 'you will be actually able to fix it')", None, 712.42),
 ("s5d",     741.69, 743.23, "Do this honestly for 30 days.", "between the dropped second '30 days' line and a doubled 'If'"),
 ("s5e",     743.84, 754.93, "If the trend line is not moving ... the leak is on the list I just gave you.", "second 'If' (743.5 'If If')", None, 743.66),
 ("cta",     811.31, 829.73, "The tracking part is the part everybody quits on ... so you don't miss the next video.", "third CTA (755.3 dropped 'part'; 780.0 stumbled on 'gives you'); last clean take", None, 811.18),
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
