"""RO-28 edit decision list: source ranges on roll C1771 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Expansion/_edit_work/ro28/round1"
# (id, in, out, text-anchor, why)
PIECES = [
 ("open1", 109.38, 117.12, "I think every man should take Zepbound, even if you're already ripped. ... longevity drug.", "third run of the intro (runs 1 and 2 stopped for 'Roll it back'); its 'It's already proven' (117.4) is re-said at once as 'It's obviously proven'"),
 ("open2", 120.70, 142.84, "It's obviously proven to help you lose fat ... only for people who are fat.", "the re-said 'It's obviously proven' (script wording); onset from the level strip (medium.en folded it into a stretched 'which')", None, 120.60),
 ("dr",    143.58, 178.08, "Now, I'm not a doctor ... rest of my life. Let me show you why.", "one read"),
 ("recap", 178.66, 190.02, "First, let's do a quick recap ... In one of the biggest diabetes studies ever done,", "one read up to 'ever done,'; its 'people with prediabetes ... 58% by losing weight' is re-said at 199.6", 190.22),
 ("dpp",   199.62, 232.72, "People with pre-diabetes ... 58%. And in a Swedish study ... overweight or obese. That is seven out of 10 people.", "the re-said DPP line runs on through the Swedish study, reason 1 and the CDC line; then 'That is seven out of 10 people' (one read); first read; the ad-lib after it ('And even if you're not technically overweight...') is dropped: he went back and re-read from 'That's seven out of ten'"),
 ("guys",  248.72, 258.18, "A lot of guys think they're at a normal weight ... ideal weight.", "third start of the line (245.2 stopped at 'think that,'); his re-said 'that's seven out of 10 people' (246.8) is not used twice"),
 ("belly", 263.74, 304.60, "and many men who aren't technically overweight ... type 2 diabetes by 94%.", "second start (261.6 stopped at 'aren't over-'); runs through Reason 2 and the 94% line", 305.5),
 ("ninety9", 309.00, 331.74, "Nearly 99% of the people who stayed on it stayed diabetes free. Next is sleep apnea ... December 2024.", "second 'Nearly 99%' (305.9 stopped at 'stayed')"),
 ("hf1",   336.82, 341.90, "then there's heart failure. In people with obesity and a type of heart failure where the heart gets stiff,", "second start (332.6 stopped at 'obesity,')", 342.04),
 ("hf2",   349.70, 371.34, "tirzepatide cut the risk of dying from heart failure or getting worse by 38%. ... heart related death.", "second read of the tirzepatide clause (342.3 read stopped before '38%')"),
 ("excuse", 380.70, 386.92, "Now, I know a lot of you guys are saying, Oh Dan, those studies are done on people who are fat or sick. And that's true.", "third start (372.0 and 378.4 stopped)"),
 ("research", 391.26, 398.24, "Most of the research on weight loss medication ... But here's what convinced me.", "second 'Most of the research' (387.5 stopped at 'has been in')", 398.45),
 ("select", 405.86, 433.98, "In the Big Heart Study on semaglutide ... ask your doctor about Zepbound first.", "second read of the SELECT line (398.8 read complete but re-said at once: last clean take)", 434.15),
 ("dose",  443.30, 530.54, "And even if you don't, I would still talk to your doctor ... then I go up to 2.5 milligrams.", "second 'And even if you don't' (434.4 read ended 'I would start on that dose regardless of that'); one read through 'Why for life', the cheating section and the dose; the ad-lib 'That is (the) standard starting dose...' (530.8, 535.3) is dropped: off-script, both reads awkward, and the later 'instead of the standard 2.5' carries it", 530.66),
 ("month", 540.16, 563.04, "But, I've been on 1.5mg for a month now ... Zepbound costs me about $400 a month.", "one read"),
 ("close", 567.90, 581.34, "Now for the benefits I showed you ... why I think you should too.", "second start (563.0 stopped at 'prevention of heart')"),
 ("outro", 601.80, 610.22, "Thank you for watching guys ... as soon as they're published.", "the last outro (582 read: Dan asked to roll it back; 599.3 stopped at 'If you wa-')"),
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
