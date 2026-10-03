"""RO-02 edit decision list: source ranges on the 8/14 poolside rolls C1614-C1629 (one lav wav per roll in lav/).
Each piece = one kept run of speech on one roll. Word edges from the roll sidecars (whisper small) and medium.en
re-listens (logs/verify_asr.txt), snapped to the measured voice onset / offset on that roll's lav."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro02"
SHOOT = "/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose"
def src(roll): return f"{SHOOT}/{roll}.MP4"
# (id, roll, in, out, words, why[, out_override, in_override])
PIECES = [
 ("hook",   "C1614", 119.76, 154.18, "If you have belly fat, stop doing ab exercises ... the only ab exercise I recommend for people who have stomach fat.", "fifth and last hook take, clean in one run (takes 1-3 are earlier wordings; take 3 restarts 'the vacuum is unique because'; take 4 stopped after two lines)"),
 ("spot",   "C1617", 3.54, 53.32, "So let's talk about why 90% of y'all guys out there shouldn't be doing any ab exercises ... will not burn fat specifically from your abs.", "second full take, one run (C1615 is a false start; C1616 stops for a car at 'That is what...')"),
 ("ta",     "C1618", 1.86, 36.38, "When you're training your abs ... it's the one when you're sucking in for a vacuum that you're working.", "only take"),
 ("ta2",    "C1618", 41.32, 45.90, "This is the muscle you want to train and that's why you want to do vacuums while you still have belly fat.", "second copy (first stopped at 'vacuums when you...')"),
 ("hist",   "C1618", 67.02, 76.18, "Now, the vacuum has been used in bodybuilding for a long time ... to get a tiny waist.", "only take"),
 ("hist2",  "C1618", 84.32, 114.78, "That is part of the reason why old school bodybuilders like Arnold Schwarzenegger and Frank Zane ... you're the one who's going to benefit the most from this.", "second copy of the Arnold line (first stopped at 'than modern...')"),
 ("why2",   "C1618", 131.32, 136.74, "Now, here's the second reason why I recommend people with belly fat do vacuums every single day.", "only take"),
 ("why2b",  "C1618", 147.76, 166.04, "Doing a vacuum the way that I recommend will train your transverse abdominis ... And that's actually a problem.", "third copy of 'Doing a vacuum' (two stopped); ends before the denial line, which he re-said at the top of the next roll"),
 ("denial", "C1619", 6.74, 35.26, "If you're not looking at your stomach on a daily basis ... exposing their stomach for everybody to see.", "the roll-change pickup of the denial line (C1618's copy at 166.7 dropped so it is said once); out set by hand in the 35.32-35.70 gap before the stopped 'But'", 35.46),
 ("part",   "C1619", 41.72, 55.20, "But that is actually an important part of the vacuum, just as important as the physical component ... why you need to shrink your waist.", "second copy (first stopped after 'part of the vacuum')"),
 ("me",     "C1619", 82.22, 105.68, "So the vacuum was very effective for me in shrinking my waist ... in addition to ab exercises.", "second 'so the vacuum' (first is a false start)"),
 ("clients","C1619", 115.26, 127.70, "I've seen even greater success with my clients with belly fat ... you do vacuums every day.", "second copy (first stopped at 'and to bring the...')"),
 ("types",  "C1620", 2.22, 62.56, "So there are three types of vacuums that you can do ... and that's a problem.", "only take; the leading 'Okay,' dropped"),
 ("adv",    "C1621", 3.18, 21.38, "The standing vacuum also has a few practical advantages ... And it just takes a few minutes.", "only take"),
 ("adv2",   "C1621", 25.68, 30.10, "It's super quick. It's super easy. And this is something realistic for you to add to your routine.", "second copy (first: 'something which is realistic.')"),
 ("aipic",  "C1621", 40.42, 82.56, "Now here's the final reason I love the standing vacuum ... is also gonna change you.", "only take"),
 ("how",    "C1622", 4.30, 19.08, "All right, so let's talk about how to do the vacuum ... If you're doing this at the gym after your workout,", "only take; joins the re-said shirt line ('then' at 19.34 dropped)", 19.20),
 ("shirt",  "C1622", 26.40, 40.20, "You want to pull your shirt up, let that belly fat hang out, and do this with at least your belly fat visible in the mirror ... focusing your mind on the problem.", "second copy (first ended on 'visual')"),
 ("fasted", "C1622", 54.64, 81.06, "Another tip I have is to make sure to do these on an empty stomach ... that powerful psychological effect.", "only take"),
 ("fasted2","C1622", 85.06, 86.88, "So, do your vacuums fasted.", "second copy (first: 'So do it fasted.'); in set by hand before the quiet 'So,' at 84.96", 86.95, 84.88),
 ("steps",  "C1623", 3.28, 25.74, "All right, so you got your shirt off, you're in the mirror ... to suck it in as much as possible.", "second take of the steps (C1622's stopped at 'hands on my waist and consciously...')"),
 ("timer",  "C1623", 26.98, 45.90, "Now, when you're doing this, you want to use a timer ... that full 20 seconds for every set of your vacuums.", "only take"),
 ("breath", "C1624", 6.64, 46.42, "Okay, so here's another issue I see with a lot of beginners ... don't run out of oxygen.", "second take of the breathing point, restart inside it cut (C1623's first try at 61.3 was abandoned for the waterfall)"),
 ("live",   "C1625", 23.90, 29.76, "All right, so now I'll show you what a set of vacuums looks like live. I'm going to time out 20 seconds on my phone timer. Here we go.", "second copy (first said '20 minutes')"),
 ("set",    "C1625", 33.40, 55.60, "[the 20-second set, real time, through his 3, 2, 1 and the timer beeps]", "the 3.6 s of starting the timer and putting the phone down (29.8-33.4) is cut; ends before he bends for the phone", 55.60, 33.40),
 ("routine","C1626", 2.64, 60.96, "All right, so that's it. Let's say you're a beginner ... but that's another option.", "only take"),
 ("takeaway","C1628", 3.62, 49.94, "All right guys, so the big takeaway from today's video ... in your waist and in your mentality.", "second take (C1627 is the first, shorter wording, no vacuum recap)"),
 ("cta",    "C1629", 17.92, 54.52, "All right guys, that's it for today's video ... We're going to focus your plan on these vacuums.", "third and last ending (C1628's two tries were stopped by planes; an 'Alright guys' at 15.2 with a 3 s stop is dropped)"),
 ("cta2",   "C1629", 56.80, 71.04, "That means your waist will get smaller physically ... I'll see you in the next video.", "second copy (first stopped at 'will get...'; found by the medium.en pass on the assembled cut, the roll transcript had merged it)"),
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
