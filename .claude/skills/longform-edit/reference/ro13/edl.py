"""RO-13 edit decision list: source ranges on C1707 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro13"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1707.MP4"
# (id, in, out, text-anchor, why)
PIECES = [
 ("hook",  180.34, 227.40, "Can you drink alcohol and still have six pack abs? ... Number one, it is pure liquid calories.", "hook take 4 of 4 (takes 1-3 each stopped and rolled back; take 4 is the only one that runs on into the body, so the first 47 s has no join)"),
 ("cal",   240.40, 251.86, "Seven calories per gram ... If it has calories, do not drink it.", "third copy (228.0 'as much calorie dense as', 235.5 'as much calories as')"),
 ("worst", 255.02, 268.04, "Alcohol is the worst offender ... alcohol knocks you out faster.", "second copy (252.5 stopped at 'in the at-')"),
 ("asleep",299.30, 301.96, "Falling asleep quickly is not high quality sleep.", "seventh and last copy; he rewrote the script line ('Falling asleep is not sleeping') on camera and settled on this wording"),
 ("wrecks",314.82, 330.98, "Alcohol wrecks your sleep quality and I can see it on my Oura ring ... to say no to anything.", "last copy (five earlier tries: 'sweet bleh', 'every time on my Oura ring')"),
 ("three", 339.04, 381.42, "Number three, it lowers your inhibitions ... when we do consume alcohol.", "second copy (331.6 stopped after 'broken their diet')"),
 ("rules", 383.94, 416.28, "All right, so here are my six rules ... That is an entire day's deficit gone in one evening.", "second 'All right'; keeps the FIRST copy of the deficit line ('an entire day's deficit', the script's wording; the re-said copy at 417.7 says 'an entire week's deficit', and 1,000 calories is a day's deficit, not a week's). Shown to Dan as a decision."),
 ("reason",421.46, 425.74, "The reason why a lot of guys fail ... they only count what they're eating,", "only take"),
 ("but",   431.34, 441.80, "But they don't count the calories in their beers ... feel like tracking.", "second copy (first said 'in the liquor they're drank')"),
 ("app",   450.88, 475.80, "This is the part where the app does the work for you ... it is not sugary.", "second copy (first: 'Photo of your drink, done, and it's in your day')"),
 ("benefit",481.28,524.66, "And drinking bad tasting drinks has a second benefit ... every week, forever.", "third copy (476.4 'And this has an ev-', 478.5 'And it has a second benefit.')"),
 ("nover", 531.40, 546.02, "There is no version of that where you get abs ... the times you noticed.", "second copy (525.3 'no version of you where... you get abs')"),
 ("five",  552.20, 566.24, "Rule number five. Your last drink should be ... it takes from you.", "second 'Rule number five' (546.8 said, then a 4 s stop)"),
 ("annoy", 569.90, 586.28, "This one sounds annoying, but it's the single highest return rule ... Drink water in between too.", "second copy (566.8 'and it is a single')"),
 ("water", 590.54, 604.60, "Not because it cancels anything out, it does not ... Not at the bar.", "second copy of 'Not because' (runs on into 'Because it slows you down')"),
 ("morning",627.50,654.32, "The next morning. You wake up feeling like hell ... an easy answer here.", "third copy, after 'roll it back' (605.0 ran to 'the whole day is gone' then stopped; 621.9 stopped at 'was a wri-')"),
 ("cutting",658.44,672.18, "If you are actively cutting right now ... makes the cut faster.", "second copy (654.7 stopped at 'trying to')"),
 ("maintain",686.58,703.08,"Once you are maintaining ... I follow all the rules on this list.", "third copy (672.8 and 680.0 both stopped before 'abs')"),
 ("thats", 719.18, 758.60, "And that's how I can maintain my abs while still enjoying drinking ... get this habit under control.", "fourth copy (three stopped at 'one or two nights')"),
 ("real",  765.40, 774.32, "Realistically, I probably would not have had the willpower ... if you're struggling.", "second copy (759.3 'if I had not have gone on a')"),
 ("end",   844.78, 864.78, "So, can you drink and still have abs? ... don't miss any of my videos.", "third and last ending (after two 'roll it back'); clean in one run"),
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
