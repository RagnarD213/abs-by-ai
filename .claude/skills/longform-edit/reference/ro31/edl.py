"""RO-31 edit decision list: source ranges on roll C1775 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Expansion/_edit_work/RO-31/round1"
# (id, in, out, text, why[, out_override, in_override])
PIECES = [
 ("open",   38.10,  64.96, "You think that you have man boobs ... the same as your belly.", "second read of the hook (6.5 read ended with Dan's 'Roll it back a little bit'); the slate 'this video is how to get rid of man boobs' dropped; one read through the first kind", 65.26),
 ("second", 76.96, 114.40, "The second kind is true gynecomastia ... you will definitely know that it's there.", "third start of 'The second kind is true gynecomastia' (65.8 stopped, 73.8 re-said); one read through the check", 114.62, 76.96),
 ("diag",  116.66, 134.50, "If you want a diagnosis ... spot reduce your belly.", "second start of 'If you want a diagnosis' (114.9 stopped at 'a diag-': found by the assembled transcript, confirmed by a Gemini listen)", None, 116.58),
 ("fastest",149.30, 154.26, "The fastest way I know is Zepbound ... every liquid calorie.", "second read (143.7 stopped at 'with AI and')", 154.36, 149.28),
 ("zep",   160.86, 180.20, "On Zepbound, I went from 192 to about 175 ... change yours too.", "second read (154.9 'On Zepbound ... because I wasn't' stopped); includes your two ad-libbed lines after 'not a doctor'", 180.30, 160.80),
 ("track", 190.12, 194.04, "Then track your calories with an AI app that does it from a photo of your food.", "third read (181.2 said 'an app', 186.3 stopped at 'from a')", 194.12, 190.02),
 ("try",   200.26, 209.80, "Try mine at AbsByAI.com ... sweet coffee and alcohol.", "third start of 'Try ours at' (194.6 and 196.5 dropped)", 209.96, 200.18),
 ("step2", 212.40, 214.53, "The second step is to build your chest.", "second start (210.5 'The second step is' stopped: Gemini listen, level strip)", 214.62, 212.30),
 ("push",  217.68, 237.46, "Push-ups and chest flies build the muscle ... within a few months.", "second start (215.1 'Push-up' stopped: Gemini listen, level strip)", None, 217.60),
 ("gyno",  243.88, 248.26, "Now let's talk about the fix for true gynecomastia. See a doctor first.", "second read (238.4 first read kept the stumble on the word)", 248.30, 243.80),
 ("cause", 252.66, 293.18, "True gynecomastia has a cause ... starting another diet.", "second read of 'has a cause' (248.7 said 'and if you want'); one read to 'another diet', his 'Okay' dropped", 293.22, 252.62),
 ("again", 299.84, 305.10, "But again, I want to remind you ... true gynecomastia.", "second start of 'But again' (293.6 stopped at 'really')", 305.16, 299.76),
 ("assume",307.78, 332.44, "So don't assume the issue is gland tissue ... surgery is the fix.", "second start of 'So don't assume' (305.6 stopped at 'the'); one read through the recap", None, 307.70),
 ("close", 337.66, 349.90, "Either way ... as soon as they're published.", "second read of 'Either way' (333.1 read complete, re-said at once: last clean take)", 350.02, 337.58),
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
