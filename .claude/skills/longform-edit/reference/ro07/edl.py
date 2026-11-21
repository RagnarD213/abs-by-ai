"""RO-07 "Why You MUST Work Out Every Day" edit decision list (7/8 kitchen rolls C1484 intro takes + C1485 body).
Pieces are anchored on PHRASES in the medium.en word list (words.json, global timeline of mkglobal.py), not on typed
times: (id, roll, first words, last words, roll-local hint, script beat, why). Edges are then snapped to the measured
lav envelope. Optional 8th/9th fields: measured roll-local out / in that override the snap."""
import json, re, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro07"
FPS = 30000/1001
ROLLS = json.load(open(f"{W}/rolls.json"))
WORDS = json.load(open(f"{W}/words.json"))["words"]
THR = -45.0   # indoor lav: room -62..-55 dB, speech median -31 dB (measured on lav.wav)
PIECES = [
 # ---- C1484: three intro takes, then the objections
 ("hook", "C1484", "Today I'm going to show you why you must", "done twice per week.", 54.0,
  "Today I'm going to show you why you must work out every day ... a 5 minute workout done every day produces better results for beginners than a one hour workout done twice per week.",
  "take 3 of 3, the last take: cleanest and most energetic on a Gemini listen (take 1 trails off on 'twice per week', take 2 doubles 'workout')"),
 ("obj1", "C1484", "All right, so I know most of y'all guys", "you can make yourself do it.", 111.0,
  "I know most of y'all are not working out every day ... the answer is no, it will not be overtraining, and yes, you can make yourself do it.",
  "second copy (the first stopped for a plane at 88 s; the 100 s copy stops after two sentences)"),
 ("obj2", "C1484", "The key is you probably would be", "long workouts twice per week.", 143.0,
  "The key is ... if you start off with a short five minute workout every day ... it'll actually be easier than doing long workouts twice per week.", "same take"),
 ("obj3", "C1484", "If you're a beginner, you just have to start", "you can do five minutes every day.", 166.0,
  "If you're a beginner, you just have to start with five minutes per day. No matter who you are ... you can do five minutes every day.",
  "same take; 'So no, it will not be overtraining and yes, you can do it' (163.2 to 166.6) left out: it repeats the answer given 25 s earlier"),
 # ---- C1485: the science objection
 ("sci1", "C1485", "so I know y'all nerds in the comments", "at odds with the scientific research.", 0.0,
  "I know y'all nerds in the comments are saying that's not what the scientific research says. And you're right ...", "only take"),
 ("sci2", "C1485", "essentially what the scientific research says is if you put in", "and get it all done?", 15.0,
  "Essentially what the research says is if you put in two hours of total workout time ... why not just pack it all into one long day every week?",
  "second start (the first stopped at 'if you put out two', found on medium.en)"),
 ("sci3", "C1485", "The reason why you don't want to do that", "so they don't go.", 44.0,
  "The reason why you don't want to do that: training beginners in the real world is totally different ... people skip their workouts.", "only take"),
 ("sci4", "C1485", "In the real world, short daily workouts are better", "than long workouts rarely.", 84.0,
  "In the real world, short daily workouts are better than long workouts rarely.",
  "69.4 to 84.3 left out ('So for all the reasons that I'm about to show you ... an hour long workout twice per week'): it repeats the opening promise, with a slip ('and then driving' for 'than driving')"),
 # ---- reason 1: soreness and dread
 ("r1a", "C1485", "Reason number one, when beginners first start", "when you're going to do the next workout.", 106.0,
  "Reason number one ... It's going to build a sense of dread in your mind.",
  "'Okay, so let me explain why in the real world five minutes at home every day outperforms an hour in the gym twice per week' (98 to 106 s) left out: it repeats the sentence before it"),
 ("r1b", "C1485", "You're going to be like, oh, I don't feel like it.", "that's when I see people start skipping.", 156.0,
  "You're going to be like, oh, I don't feel like it ... that's when I see people start skipping.",
  "after his pause he restated the dread sentence (152.2 to 156.5); the restatement is left out"),
 ("r1c", "C1485", "On the other hand, if you're not working out at all", "any beginner can do in my experience.", 179.0,
  "On the other hand, if you just start doing five minutes at home ... A five minute daily workout is something any beginner can do.", "only take"),
 # ---- reason 2: no decision
 ("r2a", "C1485", "Alright, here's the next reason why", "sometimes you won't.", 242.0,
  "Here's the next reason ... In the real world, things come up ... sometimes you'll make the right decision, sometimes you won't.", "only take"),
 ("r2b", "C1485", "That's why you can't be making a decision. Mike Tyson", "tempting to skip your workouts.", 293.0,
  "That's why you can't be making a decision. Mike Tyson once said ... life is going to punch you in the face.",
  "the second 'That's why you can't be making a decision' (the one that runs on into Mike Tyson)"),
 ("r2c", "C1485", "I experienced this first hand", "You don't want that to happen.", 331.0,
  "I experienced this first hand when I used to work out three days a week ... the day is missed. You don't want that to happen.",
  "312.0 to 331.0 left out ('In addition to this, remember you're going to be tired and sore ... half of the time those decisions will not be right'): it repeats reason 1 and the list of emergencies"),
 ("r2d", "C1485", "So that's another reason why I feel a daily workout is better.", "you will do it no matter what happens.", 352.0,
  "There is no decision. I never decide whether I'm working out or not ... Just start with five minutes.", "only take"),
 # ---- reason 3: mornings
 ("r3a", "C1485", "Here's the third reason why I think", "huge difference in how you feel.", 403.0,
  "Here's the third reason ... the morning is hormonally the optimal time to work out.", "only take"),
 ("r3b", "C1485", "You're gonna lift more, your cardio is gonna be better. And most importantly", "can be unrealistic", 432.0,
  "You're going to lift more ... Everything gets better if you work out in the morning. But if you're working out for an hour and a half ...",
  "second copy of 'You're going to lift more' (his own retake)"),
 ("r3c", "C1485", "Even if you can get it done", "far more realistic to work out in the morning.", 464.0,
  "Even if you can get it done, people have to sleep deprive themselves ... five minutes makes the morning realistic.", "second start"),
 # ---- reason 4: identity
 ("r4", "C1485", "And here's the final reason why a short daily workout outperforms long workouts done a few", "because that's who you are.", 507.0,
  "The final reason: a short daily workout builds your identity ... like brushing your teeth ... because that's who you are.",
  "second start (the first, at 495 s, he stopped after one sentence)"),
 # ---- when to work out
 ("t1", "C1485", "Alright, so hopefully by now you are convinced", "short little five minute workout in.", 566.0,
  "So let's talk about how you get started. First, plan your daily time. The best time is the morning ...",
  "595.4 to 609.0 left out ('Anyone can do this and trust me ... if there is any way you can work out in the morning'): it repeats reason 3"),
 ("t2", "C1485", "So, let's say though, I know some of y'all guys", "help you stay consistent.", 610.0,
  "The second best time is immediately after work ... go straight from your job to the gym.", "only take"),
 ("t3", "C1485", "The absolute worst time to work out is late at night", "second best choice is right after work.", 666.0,
  "The absolute worst time is late at night ... morning if you can, right after work if not.", "only take"),
 # ---- the month by month plan
 ("m1", "C1485", "If you're a beginner, if you're not working out at all right now, I recommend just doing", "workout at home every day.", 724.0,
  "If you're a beginner, I recommend a short 5 minute bodyweight workout at home every day.",
  "'Alright so let's talk about how you get started with this' trimmed: he opened the section before it with the same words"),
 ("m2a", "C1485", "So the reason why I recommend getting started that way", "only a five minute time commitment.", 750.0,
  "The reason: no equipment, and commute time. A five minute workout plus a 20 minute drive each way is a 45 minute commitment.", "only take"),
 ("m2b", "C1485", "And what I'm going to do later in this video", "to get started at home.", 789.5,
  "Later in this video I'm going to show you a 5 minute workout you can do at home.",
  "783.3 to 789.5 left out ('So when you're first starting I recommend starting from home. Just do a simple 5 minute workout'): a restatement"),
 ("m3a", "C1485", "Okay, so let's say you've done that for 30 days", "that I'm about to show you.", 807.0,
  "After 30 days, step up to a 10-minute workout. Double the workout I'm about to show you ...", "only take"),
 ("m3b", "C1485", "or if you wanna take things to the next level", "basic pieces of equipment.", 833.0,
  "Or if you want to take things to the next level, you can buy a few basic pieces of equipment.", "second copy (the first said 'a next level')"),
 ("m4", "C1485", "What I recommend to get started is a kettlebell", "start doing 10-minute workouts.", 869.0,
  "A kettlebell, a yoga mat, an ab wheel, a jump rope and push-up handles ... 30 days in, start doing 10-minute workouts.",
  "fourth and last run of the equipment list, the only one with the push-up handles he was trying to remember"),
 ("m5", "C1485", "Third month, start doing 15 minute workouts", "that same basic equipment.", 895.0,
  "Third month, 15 minute workouts with the same equipment.", "only take"),
 ("m6", "C1485", "At the fourth month, once you've been doing this for 90 days", "quit because you're in habit.", 920.0,
  "At the fourth month, invest in a home gym setup or start going to a commercial gym ... you're not going to quit because you're in the habit.",
  "third and complete version of the fourth-month advice (901.7 and 916.3 are his earlier runs at it)"),
 ("m7", "C1485", "Once you're doing that, just keep stepping your workouts another", "easily and naturally.", 960.5,
  "Keep stepping your workouts up another five minutes: add three more sets.", "second start"),
 ("m8a", "C1485", "just keep stepping it up until you're working out one hour per day. Or for those", "Everything is gonna be different for you.", 988.6,
  "Keep stepping it up until you're working out one hour per day ... every aspect of your life is going to change.", "second copy of the sentence (his retake); the false start 'Or for those...' at 988.3 between the two copies is outside the cut"),
 ("m8b", "C1485", "even before you build up to that point", "it's gonna start getting better.", 1018.5,
  "Even before that, at 20 minutes a day, every aspect of your life is going to change.", "'Eventually when you build up to that' (a trailing fragment) left out"),
 # ---- the workout
 ("w1", "C1485", "When you're first starting working out, I recommend not bothering with counting reps", "counting reps", 1060.5,
  "When you're first starting, I recommend not bothering with counting reps.",
  "'Alright, so let's talk about how you can get started' trimmed (third time he says it); the sentence's own ending was abandoned ('very quickly in a...')"),
 ("w2", "C1485", "lead to you doing the reps too quickly", "done as quickly as possible.", 1071.0,
  "Counting reps can lead to you doing the reps too quickly and without proper form. What I recommend instead is timing your sets.",
  "third run at the sentence (1065 'very quickly in a...' and 1071.8 'Counting reps can you...' abandoned, heard on a medium.en re-listen); in measured on the lav", None, "ONSET:1074.2:1075.0"),
 ("g1", "C1485", "So, there are many different free workout timer apps", "it's a great workout timer.", 1123.0,
  "There are many free workout timer apps. The one I use is Gymboss ...", "second take (shorter; the first adds 'they're not paying me')"),
 ("g2", "C1485", "Okay, once you have your gym boss, you're going to want to set it up", "repeat those rounds four times.", 1159.0,
  "Set it up like this: five 30 second rounds, repeated four times.",
  "second take; 'So two and a half minutes through the circuit ... and then we go through the circuit four times' left out (a pause mid-sentence and the same numbers again)"),
 ("e1a", "C1485", "The first round is going to be bodyweight squats.", "about shoulder width apart.", 1189.0,
  "The first round is bodyweight squats. Feet about shoulder width apart.",
  "'I'm going to show you what each of these rounds is as I show you on screen a video of myself' (an editing note said to camera) left out"),
 ("e1b", "C1485", "make sure your weight is on your heels", "pointed straight forward.", 1202.5,
  "Make sure your weight is on your heels and your toes are pointed straight forward.", "his clean third run at the sentence"),
 ("e1c", "C1485", "Avoid bending down as you do the squat", "as you squat.", 1207.5,
  "Avoid bending down ... squat to a 90 degree angle ... look at the ceiling.", "only take"),
 ("e1d", "C1485", "go down to 90 degrees slowly", "go back up for 30 seconds.", 1221.5,
  "Go down to 90 degrees slowly and then go back up for 30 seconds.", "only take"),
 ("e2a", "C1485", "Okay next you're gonna do 30 seconds of push-ups", "because this one's for beginners.", 1235.0,
  "Next, 30 seconds of push-ups. Today without handles, because this one's for beginners.", "only take"),
 ("e2b", "C1485", "For your push-ups, what you're going to do is you're going to start at the top", "controlled the entire time.", 1253.0,
  "Start at the top of the push-up position ... keep your body flat like a plank.", "second start"),
 ("e2c", "C1485", "If you are not able to do four 30-second rounds", "from the knees position.", 1291.0,
  "If you can't do four 30-second rounds of full push-ups, do them from your knees.", "only take"),
 ("e3a", "C1485", "After this, you're going to do 30 seconds of lunges.", "30 seconds of lunges.", 1308.0, "After this, 30 seconds of lunges.", "only take"),
 ("e3b", "C1485", "For this, what you're going to do, you're going to take your yoga mat and take a big", "spike your knee on the ground.", 1319.0,
  "Take a big step forward almost to the end of the yoga mat ... dip down until your knee almost touches.", "second start"),
 ("e3c", "C1485", "Step back, repeat with the other foot and then keep going", "the whole 30 seconds.", 1346.5,
  "Step back, repeat with the other foot, and keep going for the whole 30 seconds.", "his retake of the line (the last take)"),
 ("e4a", "C1485", "Finally, we have our towel row.", "Slowly with control, extend your arms again.", 1357.0,
  "Finally, the towel row ... hold a lot of tension ... have a friend karate chop your towel ... row it back to your chest, extend again.",
  "only take up to the first complete 'extend your arms again'; his three re-runs of that line (1401 to 1413 s) left out"),
 ("e4b", "C1485", "The entire time you need to make sure to keep that tension", "even when you're tired.", 1414.0,
  "The entire time, keep that tension on the towel, even when you're tired.", "only take"),
 ("e5", "C1485", "And then after that you have 30 seconds of rest", "active recovery.", 1424.0, "Then 30 seconds of rest. Jog in place for an active recovery.", "only take"),
 ("wr1", "C1485", "So, that is your short daily body weight workout.", "that makes five minutes.", 1446.0,
  "That is your short daily bodyweight workout. If you're a beginner, go through the circuit twice: that makes five minutes.", "second start"),
 ("wr2", "C1485", "If you're a little bit more advanced you can do it three or four times.", "three or four times.", 1474.5,
  "If you're a little more advanced, do it three or four times.", "his retake"),
 ("wr3", "C1485", "you can easily scale this simple", "the level that you're at right now.", 1482.0,
  "You can easily scale this simple workout to the level you're at right now.", "second start"),
 ("wr4", "C1485", "Now once again guys if you are new to working out", "than something long inconsistently.", 1492.0,
  "Don't overestimate yourself and don't underestimate a five minute daily workout ... better something short every day than something long inconsistently.", "only take"),
 # ---- outro
 ("out1", "C1485", "All right, so that's it for today's video.", "all the latest content.", 1556.0,
  "That's it for today's video. Like and subscribe with notifications on.", "only take"),
 ("out2", "C1485", "And if you wanna start building the body you've always wanted", "go to absbyai.com.", 1580.0,
  "If you want to start building the body you've always wanted using powerful AI tools, go to absbyai.com.", "second take (the first names three AI products)"),
 ("out3", "C1485", "on absbyai.com, you can generate an image", "make that future self happen.", 1590.0,
  "On absbyai.com you can generate an image of your future self ... it's going to motivate you to do these short daily workouts.", "second start"),
 ("out4", "C1485", "Not only that, but we also have an AI macro tracker", "get the body that you want.", 1618.0,
  "We also have an AI macro tracker, an AI nutritionist and an AI personal trainer.", "second take"),
 ("out5", "C1485", "So go check it out and see how good you would look", "Go to absbyai.com now.", 1630.0, "Go check it out. Go to absbyai.com now.", "only take"),
 ("out6", "C1485", "Thanks for watching guys", "see you in the next video.", 1636.0, "Thanks for watching, and I'll see you in the next video.", "only take"),
]
def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
def find(roll, phrase, after, last=False):
    """index range (i, j) of the phrase's words in WORDS for this roll, first match starting at or after `after` (global s)"""
    toks = [norm(x) for x in phrase.split() if norm(x)]
    idx = [k for k, w in enumerate(WORDS) if w["roll"] == roll and norm(w["word"])]
    for a in range(len(idx)):
        if WORDS[idx[a]]["start"] < after - 0.6: continue
        k = a; ok = True
        for t in toks:
            acc = ""
            while k < len(idx) and len(acc) < len(t):
                acc += norm(WORDS[idx[k]]["word"]); k += 1
            if acc != t: ok = False; break
        if ok: return idx[a], idx[k-1]
    raise ValueError(f"phrase not found: {roll} {phrase!r} after {after:.1f}")
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
def onset(w0, lo):
    """speech onset of the first kept word: Whisper folds a pause into a stretched word, so walk BACK from inside the word
    (its last 0.12 s) while the lav is loud; a dip under 60 ms is a stop consonant, not the edge. Never before `lo`."""
    t = max(w0["start"]+0.05, w0["end"]-0.12) if w0["end"]-w0["start"] > 0.45 else w0["start"]+0.10
    if _db(t) <= THR:
        while t < w0["end"] and _db(t) <= THR: t += 0.01
    quiet = 0.0
    while t > lo:
        if _db(t-0.02) > THR: quiet = 0.0
        else:
            quiet += 0.01
            if quiet >= 0.07: t += quiet; break
        t -= 0.01
    return max(lo, t-0.08)
def offset(w1, hi):
    """end of the last kept word: walk forward from near its end while the lav is loud (soft tails), then 0.12 s of room"""
    t = w1["end"]-0.15
    while t < min(hi, w1["end"]+0.55) and max(_db(t), _db(t+0.02), _db(t+0.04), _db(t+0.06)) > THR: t += 0.01
    return min(hi, max(t+0.12, w1["end"]+0.10))
def pieces():
    out = []
    for row in PIECES:
        pid, roll, p_in, p_out, hint, txt, why = row[:7]; off = ROLLS[roll]["f0"]/FPS
        i0, i1 = find(roll, p_in, hint+off)
        if norm(p_out) and not norm(p_in).endswith(norm(p_out)): j0, j1 = find(roll, p_out, WORDS[i0]["start"])
        else: j1 = i1
        w0, w1 = WORDS[i0], WORDS[j1]
        prev_end = WORDS[i0-1]["end"] if i0 and WORDS[i0-1]["roll"] == roll else off
        prev_dur = (WORDS[i0-1]["end"]-WORDS[i0-1]["start"]) if i0 else 0
        lo = prev_end+0.02 if prev_dur <= 0.8 else w0["start"]-0.45            # rule 4: do not clamp to a stretched previous word
        nxt = WORDS[j1+1]["start"] if j1+1 < len(WORDS) and WORDS[j1+1]["roll"] == roll else (ROLLS[roll]["f0"]+ROLLS[roll]["n"])/FPS
        sa = onset(w0, max(off, lo)); sb = offset(w1, nxt-0.04 if nxt - w1["end"] > 0.10 else nxt+0.25)
        if len(row) > 7 and row[7] is not None: sb = row[7]+off
        if len(row) > 8 and row[8] is not None:
            if isinstance(row[8], str):
                _, a, b = row[8].split(":"); t = float(a)+off
                while t < float(b)+off and not (_db(t) > THR and _db(t+0.02) > THR and _db(t+0.04) > THR): t += 0.01
                sa = t-0.10
            else: sa = row[8]+off
        out.append(dict(id=pid, roll=roll, word_in=round(w0["start"], 3), word_out=round(w1["end"], 3), **{"in": round(sa, 3), "out": round(sb, 3)},
                        local_in=round(sa-off, 3), local_out=round(sb-off, 3), text=txt, why=why,
                        heard=" ".join(w["word"].strip() for w in WORDS[i0:j1+1])))
    return out
if __name__ == "__main__":
    P = pieces(); json.dump(P, open(f"{W}/edl.json", "w"), indent=1)
    json.dump([dict(piece=p["id"], roll=p["roll"], source_in=p["local_in"], source_out=p["local_out"], script_beat=p["text"], why=p["why"]) for p in P],
              open(f"{W}/take_map.json", "w"), indent=1)
    tot = sum(p["out"]-p["in"] for p in P)
    for p in P:
        h = p["heard"].split()
        print(f"{p['id']:5s} {p['roll']} {p['local_in']:8.2f} {p['local_out']:8.2f} {p['out']-p['in']:6.1f}s ({p['word_in']-p['in']:+.2f}/{p['out']-p['word_out']:+.2f})  {' '.join(h[:5])} ... {' '.join(h[-4:])}")
    print("pieces", len(P), "duration", round(tot, 1), "s =", f"{int(tot//60)}:{tot%60:04.1f}")
