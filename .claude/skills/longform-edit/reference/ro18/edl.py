"""RO-18 edit decision list: source ranges on the VIRTUAL two-roll timeline (C1714 at 0, C1715 at 460.46 s; frames.roll_of) (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/RO-18/round1"
# (id, in, out, text-anchor, why)
PIECES = [
 # ---- C1714
 ("open",  153.64, 190.18, "You don't have belly fat because you lack knowledge ... start saving you time today", "fourth run of the intro (the first three stopped for 'Back to the top' x2 and 'roll that back to the top one more time'); the last complete run"),
 ("w1a",   190.64, 196.16, "Number one is the easiest one ... to start working out,", "then 'but I know you don't think you' (196.98) is abandoned and re-said"),
 ("w1b",   199.38, 201.92, "But I know you still think you don't have the time.", "second copy"),
 ("w1c",   204.58, 210.90, "So here's an app you can install on your phone ... working out becomes easy.", "second copy (202.3 'So here's an app that you can' stopped); onset on the level strip (medium.en folds it into a 1.8 s 'install')", None, 204.50),
 ("w1d",   211.42, 215.24, "It's called Wispr Flow. Wispr Flow is an AI dictation app.", ""),
 ("w1e",   222.72, 232.44, "You hold down a button, you talk ... your prompts to ChatGPT, everything.", "third copy (215.5 and 220.3 stopped); onset from the level strip (folded into a 7.4 s 'whatever')", None, 222.64),
 ("w1f",   236.52, 283.28, "Now I know a lot of you guys are saying, oh Dan, my phone ... between texting, email, and work.", "second copy (233.3 stopped at 'my ha-'); the excuse voice; one continuous read through 'email, and work'"),
 ("w1h",   290.04, 307.96, "For most people I would say it's at least 30 minutes ... use it to work out.", "second copy after a 5 s stop (283.7 'For most people I would say it's at'); onset from the level strip", None, 289.96),
 ("s2a",   308.82, 312.40, "Alright, let's talk about the second way. Work out at home, not a gym.", ""),
 ("s2b",   325.00, 348.22, "Think about everything that goes into going to the gym ... roll out of bed and start.", "second read of the gym paragraph (312.4 read was complete, re-said at once: last clean take)"),
 ("s2c",   349.96, 359.98, "And you don't need a lot of equipment ... on screen right now.", "second 'And you don't' (348.3 'You' stopped)"),
 ("s2d",   370.84, 394.26, "You can get all that stuff for under $100 ... if you can do it seven days a week.", "third copy of the $100 line (360.5 and 366.8 stumbled on 'under'), onset from the level strip; C1714 ends here: its 'But if time is the reason' and meal prep lines were re-read on C1715 after 'Something happened with the script here'", None, 370.76),
 # ---- C1715 (virtual 460.46 + roll time)
 ("s2f",   470.44, 480.90, "But if time is the reason you're not working out ... every day is a habit.", "C1715's read (the last); onset from the level strip (medium.en starts 'But' 0.5 s early)", None, 470.34),
 ("s3a",   481.60, 515.56, "Number three, use a meal prep service ... tracking your calories gets a lot easier too.", "C1715's read: 'two or three hours' (C1714 said 'three to five', then stopped); onset from the level strip ('Number' at 481.46)", None, 481.38),
 ("s3b",   523.32, 547.34, "If you're making decent money ... than cooking yourself.", "second copy after a 4 s stop (516.0 copy stopped at 'own food,'); onset from the level strip (folded into a 3.3 s 'you're')", None, 523.24),
 ("s4a",   548.16, 552.46, "Here's the next one. Buy a robot lawnmower like you're seeing on the screen right now.", ""),
 ("s4b",   558.46, 578.60, "If you have a house with a yard ... to mow your lawn perfectly.", "second copy (552.9 copy re-said at once)"),
 ("s4c",   581.96, 600.00, "You map out your yard one time in the app ... that's a lot of money for a lawn mower", "second 'You map out your' (579.2 said 'your lawn' and stopped)"),
 ("s4d",   612.60, 630.14, "But a lawn mowing service is a hundred to two hundred dollars per visit ... as the robot does.", "third copy (600.4 said 'fifty five to a hundred', 605.9 stopped at 'adds up to over'); onset from the level strip", None, 612.52),
 ("s4e",   636.58, 646.90, "So a robot lawnmower actually costs you nothing additional ... free up hours per week to work out.", "second copy (630.6 stopped at 'mowing the'); onset from the level strip", None, 636.50),
 ("s5a",   647.54, 747.30, "Number five, buy a Tesla or take robotaxis ... about exercise and nutrition for the whole ride.", "one read; the look-away and laptop lines are Dan's own ad-libs (kept, shoot report)"),
 ("s5b",   767.44, 800.52, "You'll be shocked at how much more mental focus ... useless bullshit anyways.", "third copy (747.7 complete but re-said, 760.0 stopped at 'wasting that'), onset from the level strip; runs on into number six", None, 767.36),
 ("s6b",   805.00, 823.12, "You are never going to use it ... Use a paid Claude plan, not the free version.", "second copy (800.8 stopped at 'forget'); onset from the level strip", None, 804.92),
 ("s6c",   827.84, 930.82, "Then run what it writes you through ... nobody at your job has to know how you're doing it.", "second 'Then run' (823.6 stopped at 'AI ro-'); onset from the level strip", None, 827.76),
 ("up1",   953.82, 966.08, "so let's add all of this up ... saves you another 2-4.", "the last 'Alright guys, so let's add' (931.4 and 951.2 stopped); onset from the level strip", None, 953.74),
 ("up2",   972.16, 980.04, "A car that drives for you gives you back up to 7 hours a week ... put together.", "third copy (966.6 stopped, 970.8 'A ca-'); onset from the level strip", None, 971.94),
 ("up3",   997.06, 1003.22, "That's well over 10 hours a week ... every single day.", "after a 17 s pause"),
 ("cta1",  1057.36, 1077.38, "So you're not too busy to get in shape ... with six pack abs for free.", "second run of the close (1003.5 run re-said 'So you don't have to' twice); the last"),
 ("cta2",  1084.06, 1099.40, "Then our AI personal trainer designs you a workout plan ... see you in the next one.", "second 'Then our AI personal trainer' (1077.8 stopped at 'nutritionist,')", None, 1083.98),
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
