"""RO-03 (The Vacuum, workout only) edit decision list: source ranges on the 8/14 poolside rolls C1624-C1629 (one lav wav per roll in lav/).
Each piece = one kept run of speech on one roll. Word edges from the roll sidecars (whisper small) and medium.en
re-listens (logs/verify_asr.txt), snapped to the measured voice onset / offset on that roll's lav."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro03"
SHOOT = "/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose"
def src(roll): return f"{SHOOT}/{roll}.MP4"
# (id, roll, in, out, words, why[, out_override, in_override])
PIECES = [
 ("intro",  "C1625", 23.70, 29.72, "All right. So now I'll show you what a set of vacuums looks like live. I'm going to time out 20 seconds on my phone timer. Here we go.", "second copy (first said '20 minutes'); the same piece RO-02 used", 29.80),
 ("set1",   "C1625", 33.40, 55.60, "[set 1: the 20-second hold, real time, to the phone timer's beep at 55.08]", "the only filmed hold; RO-02's exact in and out", 55.60, 33.40),
 ("rest1",  "C1626", 27.98, 52.44, "When you're resting in between these vacuums, it's important that you take deep belly breaths ... First thing in the morning is my recommended time ... even if you don't do intermittent fasting.", "only take; his own advice for the rest between sets"),
 ("set2",   "C1625", 29.95, 55.60, "[he starts the phone timer and puts it down, then set 2: the same filmed hold]", "the hold is repeated (one hold was filmed); this time it opens on him starting the timer; in set so the rest is 30.0 s", 55.60, 29.95),
 ("rest2",  "C1624", 18.50, 46.42, "So you actually want to be able to breathe as you're doing these vacuums ... make sure to keep breathing as you're doing the vacuum and don't run out of oxygen.", "second take of the breathing point (the one RO-02 used), from 'So you actually want to be able to breathe'"),
 ("set3",   "C1625", 33.85, 56.30, "[set 3: the same filmed hold, held 0.7 s longer on his release]", "the hold is repeated; ends as he lets go, before he bends for the phone; in set so the rest is 30.0 s", 56.30, 33.85),
 ("outro",  "C1626", 2.64, 18.30, "All right, so that's it. Let's say you're a beginner ... That alone is going to make a big difference for you, just that one set.", "only take; stops before the two-set and three-set lines, which say a minute of rest"),
 ("cta",    "C1629", 4.68, 11.70, "So go to absbyai.com now, see yourself with abs and take that first step. Thanks for watching the video guys and I'll see you next time.", "the short pickup ending at the top of the roll, clean in one run", 12.30),
]
FPS = 30000/1001; SR = 48000
_L = {}
def lav(roll):
    if roll not in _L:
        wv = wave.open(f"{W}/lav/{roll}.wav"); _L[roll] = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    return _L[roll]
_T = {}
def thr(roll):
    """Voice threshold for this roll: its room floor (10th percentile of 20 ms frames) + 10 dB, never under -52."""
    if roll not in _T:
        a = lav(roll); n = len(a)//960; e = 20*np.log10(np.sqrt((a[:n*960].reshape(n, 960)**2).mean(1))+1e-9)
        _T[roll] = max(-52.0, float(np.percentile(e, 10))+10.0)
    return _T[roll]
def _db(roll, t, n=0.02):
    a = lav(roll)[int(t*SR):int((t+n)*SR)]
    return 20*np.log10(np.sqrt(np.mean(a*a))+1e-9) if len(a) else -120
def snap(roll, tin, tout):
    th = thr(roll); t = tin+0.15
    if _db(roll, t) <= th:
        while t < tin+0.40 and _db(roll, t) <= th: t += 0.01
    while t > tin-0.45 and _db(roll, t-0.02) > th: t -= 0.01
    a = max(0, t-0.08)
    t = tout-0.15
    while t < tout+0.50 and max(_db(roll, t), _db(roll, t+0.02), _db(roll, t+0.04), _db(roll, t+0.06)) > th: t += 0.01
    return round(a, 3), round(t+0.12, 3)
def pieces():
    out = []
    for row in PIECES:
        pid, roll, a, b, txt, why = row[:6]
        sa, sb = snap(roll, a, b)
        if len(row) > 6 and row[6] is not None: sb = row[6]
        if len(row) > 7 and row[7] is not None: sa = row[7]
        out.append(dict(id=pid, roll=roll, word_in=a, word_out=b, **{"in": sa, "out": sb}, text=txt, why=why))
    return out
if __name__ == "__main__":
    P = pieces(); json.dump(P, open(f"{W}/edl.json", "w"), indent=1)
    tot = sum(p["out"]-p["in"] for p in P)
    for p in P: print(f"{p['id']:8s} {p['roll']} {p['in']:8.3f} {p['out']:8.3f}  ({p['word_in']-p['in']:+.2f}/{p['out']-p['word_out']:+.2f}) thr {thr(p['roll']):.1f}")
    print("pieces", len(P), "duration", round(tot, 1), "s =", f"{int(tot//60)}:{tot%60:04.1f}")
