"""RO-06 edit decision list. Pieces are (id, roll, in, out, text, why) with ROLL-LOCAL word times (sidecar words, doubtful
spots re-heard with medium.en, see take_map.json); converted to the global timeline of mkglobal.py and snapped to the
measured envelope by snap(). Optional 7th/8th fields: measured out / in (roll-local) that override the snap."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro06"
FPS = 30000/1001
ROLLS = json.load(open(f"{W}/rolls.json"))
WORDS = json.load(open(f"{W}/words.json"))["words"]
PIECES = [
 ("hook",   "C1559",  42.36,  67.46, "Today I'm going to show you how to create a great home workout setup ... how to put it all together.", "take 4 of 4 in C1559 (and after C1558's single take): the last take, complete and clean on a medium.en re-listen ('limited time to work out, if you don't have time'); takes 2 and 3 were abandoned by Dan, take 1 lacks the COVID line he added"),
 ("exc1",   "C1560",   3.82,   7.16, "I know a lot of you guys you want to lose that belly fat, you want to get in shape.", "take 1's sentence: take 2 says 'you want to lose in shape' (heard on medium.en). 'Alright, so' trimmed: it follows the hook directly"),
 ("exc2",   "C1560",  16.36,  33.94, "but you got all kinds of excuses ... not valid in any way whatsoever.", "take 2, from 'but'"),
 ("exc3",   "C1560",  38.40,  67.90, "You don't need a gym membership to get in shape ... a quick workout whenever you want.", "second copy (first stopped at 'You can do it just with them')"),
 ("amzn",   "C1563",   1.18,  16.36, "Alright, so for all this stuff, it's available on Amazon ... a few pennies on each thing that you buy.", "C1563 is the single clean retake of C1562's three attempts"),
 ("mat",    "C1565",   4.08,  68.26, "The first thing you need to buy is a yoga mat like this ... buy a basic yoga mat.", "C1565 is the retake of C1564 (later, complete, has the price); its opener 'let's talk about what you need to buy' trimmed", None, 3.97),
 ("push1",  "C1566",  39.40, 100.46, "All right, so the next item that you need to buy is push-up handles ... build muscle even when you're athletic.", "second copy (first stopped for the plane at 21.7)"),
 ("push2",  "C1566", 109.96, 115.62, "Once again, don't waste your money on the fancy ones like I did. Buy the cheap basic ones ...", "his own redo of the last two sentences ('I need to do that last part one more time')"),
 ("rope",   "C1567",  11.00,  39.80, "So here's the next thing you need to buy. A jump rope ... that will get the job done.", "only take; in measured (after the slate's 'All right.')", None, 10.94),
 ("wheel",  "C1568",   1.02,  50.86, "All right, next thing that you need is our favorite infomercial gimmick, the ab wheel ... gets the job done.", "only take"),
 ("tot1",   "C1569",  20.74,  32.10, "Okay, so if you are strapped for cash ... then this is what you should get.", "second copy (first stopped by a noise)"),
 ("tot2",   "C1569",  46.14,  65.13, "Yoga mat, $22. Push-up handles, $10. Jump rope, $9. And ab wheel, $17 ... this will get the job done.", "second run of the prices (first said push-up handles $9 and stopped). Round 5 length trim (Dan, option A): 65.7 to 91.4 left out ('I don't care how poor you are ... on the days that you don't work out'), a restatement of the excuses section and of the backup-setup point", 65.34),
 ("kb1",    "C1571",   1.32,  27.66, "All right, so that's the setup for y'all brokeies ... kettlebell deadlift and a variety of other exercises.", "C1571 is the retake of C1570 (which he stopped to back up); out measured (kettlebell set-down noise after the word)", 27.95),
 ("kb2",    "C1570",  15.70,  22.54, "So this kettlebell, you can pick up a 35 pound kettlebell, which will be appropriate for most beginners for about $45.", "C1571 says '$45 for a $35 kettlebell' (heard on medium.en); C1570 has the same line said right; out measured (speech ends 22.82)", 22.98),
 ("kb3",    "C1571",  37.94, 142.22, "If you're a little bit more advanced ... kettlebell swings or another exercise appropriate for that weight.", "continues after the replaced price line"),
 ("kb4",    "C1572",   2.14,  15.84, "So, with the kettlebell, should I spend $100 on a fancy rubber-coated beautiful kettlebell? ... you don't really need that rubber coating.", "only take", 16.04),
 ("kb4b",   "C1572",  30.20,  33.80, "So go basic, go iron, go black, and keep it very cheap.", "only take. Round 5 length trim: 16.1 to 29.9 left out (the yoga mat is enough, slamming the weight, not a super heavy weight): repeats the point just made", None, 30.19),
 ("mb1",    "C1573",   1.90,  77.02, "All right, next thing that you need is a medicine ball ... four pounds or two if you're just getting started.", "only take"),
 ("mb2",    "C1574",   2.22,  26.24, "So the medicine ball is not completely necessary ... a five pound plate or a five pound dumbbell instead.", "only take"),
 ("db1",    "C1575",   1.70,  21.50, "All right, so the next thing that you need to buy is some dumbbells ... useful for a home workout setup.", "only take"),
 ("db2",    "C1575",  32.02,  43.68, "So for the dumbbells it's going to run you about $29 for 25 pound dumbbells ... a little bit less.", "second copy (first stopped to check the price)"),
 ("db3",    "C1576",   1.96, 109.08, "Okay, so let's talk about what weight to buy ... investing in a full rack of dumbbells will be worth it.", "only take; its last 52 s (up to 100 lb, 60 vs 70, his own rack, a restart at 127) left out as repetition: Dan can restore"),
 ("rec1",   "C1577",  30.34,  47.16, "Okay, so that is what you need to buy for the intermediate setup. The kettlebell ... Your medicine ball, about $20 ...", "second copy (first stopped at 21.5). The only place the medicine ball price is said"),
 ("rec2",   "C1577",  66.98,  74.84, "And then finally you have your dumbbells. About $29 for 25 pounds ...", "second copy; the pairs recap after it (75-112 s) repeats db3 and is left out: Dan can restore"),
 ("rec3",   "C1578",   1.70,  29.26, "Okay, so that is my recommended intermediate setup ... even if you have a gym membership.", "only take"),
 ("towel",  "C1579",   0.66,  33.10, "All right, so one last thing I need to mention ... if you don't have these right now", "only take"),
 ("cav1",   "C1580",   1.74,  11.57, "Okay, guys, so that's how you build a basic home workout set up ... before I wrap up the video.", "only take", 11.76),
 ("cav1b",  "C1580",  24.96,  38.86, "However, I don't want you to stay at this level your entire life ... I want you to get a gym membership.", "only take. Round 5 length trim: 11.9 to 24.5 left out ('This is a great way to get started ... a great way for you to begin'): restates the excuses section", None, 24.86),
 ("cav2",   "C1580",  47.35, 141.26, "That means you're going to have to drive a few minutes ... the backup for when I can't make it to the gym.", "third copy of the drive line (39.4 said 'close to by'; 44.9 stopped at 'a few minutes', found by medium.en on the assembled cut)", 141.40),
 ("cav2b",  "C1580", 149.41, 154.08, "Eventually, once you're ready, get that gym membership or build a full gym at your house.", "only take. Round 5 length trim: 141.6 to 149.0 left out ('So I want you guys to get started ... progress beyond that'): restates the two sentences before and after it", None, 149.20),
 ("cta",    "C1581", 122.82, 186.08, "Alright, so that's today's video ... go to absbyai.com. Thank you for watching and I'll see you in the next video.", "take 2 of 3: the latest take with no restart inside it (take 3 restarts twice, take 1 stops for a noise). Round 5: 0.74 s of his end smile held after the last word (the film ended a tenth of a second after it)", 187.0),
]
_lav = None
def lav():
    global _lav
    if _lav is None:
        wv = wave.open(f"{W}/lav.wav"); _lav = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(np.float32)/32768
    return _lav
def rms_db(t0, t1, sr=48000):
    a = lav()[int(t0*sr):int(t1*sr)]
    return 20*np.log10(np.sqrt(np.mean(a*a))+1e-9) if len(a) else -120
def _db(t, n=0.02): return rms_db(t, t+n)
def snap(tin, tout, thr=-42.0):  # outdoor lav: room -58..-48 dB (measured per roll), not the studio -50
    t = tin+0.15
    if _db(t) <= thr:
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
        pid, roll, a, b, txt, why = row[:6]; off = ROLLS[roll]["f0"]/FPS
        sa, sb = snap(a+off, b+off)
        sb = max(sb, b+off+0.18)                                   # a soft tail ('house', 's') sits under the outdoor threshold
        nxt = [w["start"] for w in WORDS if w["roll"] == roll and w["start"] > b+off+0.05]
        if nxt: sb = min(sb, nxt[0]-0.04)                          # never into the next (cut) word
        if len(row) > 6 and row[6] is not None: sb = row[6]+off
        if len(row) > 7 and row[7] is not None: sa = row[7]+off
        end = (ROLLS[roll]["f0"]+ROLLS[roll]["n"])/FPS
        sa = max(sa, off); sb = min(sb, end-1/FPS)
        out.append(dict(id=pid, roll=roll, word_in=round(a+off, 3), word_out=round(b+off, 3), **{"in": round(sa, 3), "out": round(sb, 3)},
                        local_in=round(sa-off, 3), local_out=round(sb-off, 3), text=txt, why=why))
    return out
if __name__ == "__main__":
    P = pieces(); json.dump(P, open(f"{W}/edl.json", "w"), indent=1)
    json.dump([dict(piece=p["id"], roll=p["roll"], source_in=p["local_in"], source_out=p["local_out"], script_beat=p["text"], why=p["why"]) for p in P],
              open(f"{W}/take_map.json", "w"), indent=1)
    tot = sum(p["out"]-p["in"] for p in P)
    for p in P: print(f"{p['id']:6s} {p['roll']} {p['local_in']:8.3f} {p['local_out']:8.3f}  ({p['word_in']-p['in']:+.2f}/{p['out']-p['word_out']:+.2f})")
    print("pieces", len(P), "duration", round(tot, 1), "s =", f"{int(tot//60)}:{tot%60:04.1f}")
