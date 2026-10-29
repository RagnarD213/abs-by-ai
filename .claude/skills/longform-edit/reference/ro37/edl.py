"""RO-37 edit decision list: (id, roll, word_in, word_out, text, why[, out_override, in_override]) on the four 10/23 pool rolls;
edges measured on each roll's lav by snap() (ro28 method). Take rule: last clean take of each line (memory take-selection-rule-approved)."""
import json, wave, numpy as np
W = "/Volumes/Expansion/_edit_work/RO-37/round1"
PIECES = [
 ("hook", "C1894", 2.84, 14.06, "If I walked into a gym for the first time today ... more than 20 years.", "second hook take (C1893 14.6 is the first); its 'Alright,' lead-in trimmed"),
 ("why", "C1894", 48.58, 61.72, "So why should you listen to me? ... So rule number one, only work out for 15 minutes.", "second 'why listen' (C1894 14.6 stopped at 'get someone...')"),
 ("fifteen", "C1894", 64.28, 72.96, "That's gonna be it for your workout, just 15 minutes. Not an hour ... way too short.", "ad-lib 'I know you're probably surprised like that' (62.5) dropped"),
 ("most", "C1894", 80.92, 106.32, "Most guys walking into a gym ... So nothing stops you from coming back tomorrow.", "second 'Most guys' read (73.8 read re-said at once); runs through reason 1; out from the level strip (tomorrow ends 106.70)", 106.82),
 ("dread", "C1895", 6.80, 57.70, "Second, you won't dread the next workout ... then 25, and then 30.", "one read; its 'If you try going...' line is re-said at 64.5 with the script ending; onset from the level strip ('Second' starts 6.40, quiet S)", None, 6.33),
 ("failure", "C1895", 64.46, 69.70, "If you try going an hour and a half your first time in ... training beginners.", "second read (58.6 read ends without 'training beginners'); quiet 'If' at 64.80", None, 64.70),
 ("struggle", "C1895", 73.88, 78.20, "Now what if 15 minutes every day becomes a struggle? Maybe you had a terrible day.", "one read up to 'terrible day'; 'Maybe you're just not feeling it' is re-said at 86.4"),
 ("five", "C1895", 86.38, 112.22, "Maybe you're just not feeling it. Then do five minutes ... my first day on the gym.", "second read (80.6 'No matter how bad your day was, always do five minutes' is the off-script first try)"),
 ("bike", "C1895", 137.42, 151.96, "First, get on the bike ... two working sets of 8 to 12 reps.", "second 'First, get on the bike' (113.1 read is the first)"),
 ("rep", "C1895", 154.20, 158.70, "on every rep, take 2 to 3 seconds on the way down and then explode up.", "second 'on every rep' (152.8 stopped); onset from the level strip"),
 ("whole", "C1895", 178.66, 183.88, "That's it. That's your whole workout and it takes about 15 minutes. Then come back tomorrow and do it again.", "second 'That's it' (159.5 read stops at 'whole workout')"),
 ("same", "C1895", 187.88, 231.96, "Now you might be thinking, wait a minute, I'm doing the same exercises every day? ... and then you go home.", "second 'Now you might be thinking' (184.8 stopped at 'I'm going to')"),
 ("boring", "C1895", 238.32, 252.74, "Once these exercises get boring and easy ... Now let's talk about weeks two to four.", "second 'Once these exercises' (233.0 read is the first)"),
 ("weeks", "C1895", 253.48, 255.68, "In weeks two to four I would add a second workout,", "first statement; the ad-lib 'Once you're used to the basic workout I would add in...' (256.4) stops"),
 ("alt", "C1895", 262.58, 271.22, "and I will alternate between the two workouts ... that's what you were already doing.", "joins the re-said 260.3 sentence at 'and I will alternate'"),
 ("wa", "C1895", 275.02, 277.86, "the leg press, the chest press machine and the seated cable rows.", "second list (271.9 read stopped at 'and the'); onset measured"),
 ("wb", "C1895", 278.92, 287.00, "Workout B is lat pulldowns ... Day two you do workout B.", "one read; 'Day three...' is re-said at 304.1"),
 ("day3", "C1895", 304.08, 332.90, "Day three, you do workout A again, and so on ... far more important than", "second 'Day three' read; ends on 'than' before the restart"),
 ("longer", "C1895", 337.40, 342.94, "working out longer. If you can't get yourself to do 15 minutes a day ... an hour every day.", "the re-said ending (334.1-336.95 restart 'working out every day is far more important than' dropped); in after its 'than' (ends 336.95)", None, 337.03),
 ("fail", "C1895", 346.00, 359.42, "So why does this work when most beginners fail? ... every single day.", "second 'So why does this work' (343.9 read flubbed 'work out work')"),
 ("most2", "C1897", 5.62, 19.30, "Here's what most beginners do ... and they quit.", "C1897 re-says 'Here's what most beginners do' (C1895 360.0 is the first)"),
 ("seen", "C1897", 23.00, 24.36, "I've seen this happen over and over again.", "second read (20.2 is the first)"),
 ("guy", "C1897", 32.44, 41.20, "The guy who does a crazy two hour workout ... he's still there.", "third start (25.0 said 'three days a week'; 30.9 stopped at 'crazy three')"),
 ("belly", "C1897", 46.12, 60.40, "That's the guy who ends up losing his belly fat. In my experience, about 80% ... long term.", "second read of the belly-fat line (41.8 read ran into 'in my experience...' and stopped); its 'And' (45.1) hangs 1 s before it, so in at 'that's'", None, 45.95),
 ("machines", "C1897", 61.40, 69.76, "Next, only work out with machines and cables ... later if you want to.", "one read up to 'if you want to'"),
 ("started", "C1897", 72.34, 73.90, "but you don't need them to get started.", "second read (70.5 stopped at 'to get,')"),
 ("deadlift", "C1897", 79.46, 84.28, "I've been lifting for 20 years and I still never do high risk barbell lifts like deadlifts, never.", "second read (74.8 read is shorter, no 'like deadlifts')"),
 ("matters", "C1897", 84.96, 86.70, "Here's why this matters so much when you're new.", "one read"),
 ("injury", "C1897", 89.30, 129.08, "An injury when you're first getting started ... Watch those before you go in.", "second 'An injury' (87.1 stopped at 'when you're new,'); one read on to the how-to videos"),
 ("self", "C1897", 132.10, 152.14, "Next, if you're self-conscious at the gym ... wondering what to do.", "one read"),
 ("plan", "C1897", 154.42, 169.36, "You already have one. It's the plan in this video. Next, walk between your sets ... walk between your sets.", "one read after a 2.3 s pause (cut out)"),
 ("stretch", "C1897", 173.40, 183.92, "Then, stretch after every workout ... doesn't do that much for you.", "second 'Then' (171.5 stopped); onset measured"),
 ("recap", "C1897", 186.70, 196.42, "So here's the whole plan one more time ... and stretch after.", "second 'So here's the whole plan' (184.6 is the first)"),
 ("simple", "C1897", 202.62, 204.84, "That's it. Keep it real simple and keep it real short.", "second 'That's it' (197.2 read ran into 'And don't worry about going hard', re-said at 222.9)"),
 ("close", "C1897", 222.92, 233.24, "Don't worry about going hard. Just worry about showing up ... for all my newest videos.", "last read (205.2 stopped at 'Just worry...')"),
]
FPS = 30000/1001
_L = {}
def lav(r):
    if r not in _L:
        wv = wave.open(f"{W}/lav_{r}.wav"); _L[r] = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    return _L[r]
def rms_db(r, t0, t1, sr=48000):
    a = lav(r)[int(t0*sr):int(t1*sr)]
    return 20*np.log10(np.sqrt(np.mean(a*a))+1e-9) if len(a) else -120
def snap(r, tin, tout, thr=-46.0):
    _db = lambda t: rms_db(r, t, t+0.02)
    t = tin+0.15
    if _db(t) <= thr:
        while t < tin+0.40 and _db(t) <= thr: t += 0.01
    while t > tin-0.45 and _db(t-0.02) > thr: t -= 0.01
    a = max(0, t-0.08)
    t = tout-0.15
    while t < tout+0.50 and max(_db(t), _db(t+0.02), _db(t+0.04), _db(t+0.06)) > thr: t += 0.01
    return round(a, 3), round(t+0.12, 3)
def pieces():
    out = []
    for row in PIECES:
        pid, r, a, b, txt, why = row[:6]
        sa, sb = snap(r, a, b)
        if len(row) > 6 and row[6] is not None: sb = row[6]
        if len(row) > 7 and row[7] is not None: sa = row[7]
        out.append(dict(id=pid, roll=r, word_in=a, word_out=b, **{"in": sa, "out": sb}, text=txt, why=why))
    return out
if __name__ == "__main__":
    P = pieces(); json.dump(P, open(f"{W}/edl.json", "w"), indent=1)
    tot = sum(p["out"]-p["in"] for p in P)
    for p in P: print(f"{p['id']:9s} {p['roll']} {p['in']:8.3f} {p['out']:8.3f}  ({p['word_in']-p['in']:+.2f}/{p['out']-p['word_out']:+.2f})")
    print("pieces", len(P), "duration", round(tot, 1), "s =", f"{int(tot//60)}:{tot%60:04.1f}")
