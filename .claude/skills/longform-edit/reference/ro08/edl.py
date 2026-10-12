"""RO-08 "Intermittent Fasting: The Best Way To Get Abs" edit decision list (7/8 kitchen roll C1486).
Pieces are anchored on PHRASES in the medium.en word list (words.json, global timeline of mkglobal.py), not on typed
times: (id, roll, first words, last words, roll-local hint, script beat, why). Edges are then snapped to the measured
lav envelope. Optional 8th/9th fields: measured roll-local out / in that override the snap."""
import json, re, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro08"
FPS = 30000/1001
ROLLS = json.load(open(f"{W}/rolls.json"))
WORDS = json.load(open(f"{W}/words.json"))["words"]
THR = -45.0   # indoor lav: room -62..-55 dB, speech median -31 dB (measured on lav.wav)
PIECES = [
 # ---- intro: take 3 of 3 (the last take; a blind delivery listen scored it 10 against 8 and 5)
 ("hook", "C1486", "Today, I want to show you why intermittent fasting", "and I feel better.", 78.5,
  "Today I want to show you why intermittent fasting is the number one most powerful way to get six pack abs. I've been doing it for about 10 years ... easier to get lean, easier to maintain abs, more productive and I feel better.",
  "take 3 of 3: the last take and the best delivery (take 1 goes flat on 'so much easier', take 2 restarts 'In today's video'). Out measured on the lav: 'better' ends at 97.72, the cut sentence's 'It's' starts at 97.96; the snap had run 0.1 s into it (heard on the first-minute review)", 97.90),
 ("promise", "C1486", "In today's video, I'm going to show you why intermittent fasting is the simplest", "and six pack abs.", 101.5,
  "In today's video I'm going to show you why intermittent fasting is the simplest way to get abs, why it's a lot easier than you think, and why it is your path to the body you want.",
  "same take; 'It's really changed so much for me and I'm excited to share it with you today' (97.8 to 101.9) left out: it repeats 'totally changed my life'. In 0.17 s earlier (room tone only, measured) so the film's length and every later time stay as rendered after the hook's out moved", None, 101.87),
 # ---- what it is
 ("def1", "C1486", "Okay, for those of y'all guys who don't know", "and to get lean.", 136.0,
  "For those of y'all who don't know, intermittent fasting is super simple: not eating during a certain part of the day, as a strategy to reduce your calories.", "only take"),
 ("def2", "C1486", "So the most important thing in getting lean", "You fast the first part of the day.", 151.5,
  "The most important thing in getting lean is your nutrition, and the most important factor is calories ... How do you reduce your calories while still enjoying the food you want? You fast the first part of the day.", "only take"),
 ("mine1", "C1486", "What I personally do, and what I think is the simplest", "at the start of my day.", 195.0,
  "What I personally do: skip breakfast and eat a late lunch. I wake up around 9, fast until about 2 PM: a five hour fasting window.", "only take"),
 ("mine2", "C1486", "That's the form of intermittent fasting that's worked best for me.", "that I do every single day.", 217.0,
  "That's the form that's worked best for me ... there are other kinds (long fasts, whole days) ... what's gotten me the best result is a simple, short daily fast.", "only take"),
 ("mine3", "C1486", "All I do, skip breakfast, eat a late lunch", "that's what's kept me lean.", 262.0,
  "All I do: skip breakfast, eat a late lunch, keep my lunch fairly low carb. That's what's gotten me abs.", "only take"),
 # 276.1 to 301.4 left out: a second 'in today's video I'm going to show you' promise with a false start; the intro already made it
 # ---- why 1: simplest
 ("w1a", "C1486", "Alright so let's talk about why intermittent fasting is superior", "to get to work.", 309.8,
  "Why intermittent fasting is superior to reducing calories through the day. Number one: it's the simplest way to reduce your calories ... decisions made under duress.", "only take"),
 ("w1b", "C1486", "Mike Tyson once said", "because life punched them in the face.", 369.0,
  "Mike Tyson once said everybody has a plan until they get punched in the face ... life is going to punch you in the face.", "only take"),
 ("w1c", "C1486", "Intermittent fasting though is a plan you can execute", "you probably couldn't stick to it.", 410.5,
  "Intermittent fasting is a plan you can execute when life punches you in the face.", "only take"),
 # ---- why 2: health
 ("w2a", "C1486", "The second reason why intermittent fasting is superior", "outside of just fat loss.", 442.8,
  "The second reason: intermittent fasting has a lot of health benefits outside of just fat loss.", "only take"),
 ("w2b", "C1486", "and this won't make an immediate difference for how you lose your belly fat", "and makes you younger.", 456.4,
  "This won't make an immediate difference to your abs, but long term ... a process called autophagy ... renews your cells.",
  "his retake of the sentence (the first run, at 452.3, ends 'how your belly fat loses')"),
 # ---- why 3: convenient
 ("w3", "C1486", "Here's the third reason why intermittent fasting is superior", "and that's why I love fasting.", 509.6,
  "The third reason: it's convenient and saves you massive amounts of time in the morning.", "only take"),
 # ---- why 4: productivity
 ("w4a", "C1486", "Another reason why I love fasting is that fasting improves your productivity.", "to the next level.", 559.8,
  "Another reason: fasting improves your productivity ... the donuts and muffins I used to eat for breakfast were destroying my productivity.", "only take"),
 ("w4b", "C1486", "And there's a reason for that. When you eat a heavy breakfast, your body", "type of feeling.", 590.2,
  "There's a reason for that: a heavy breakfast makes your body spend energy on digestion. That's the food coma.", "his retake (the first run, at 583.3, stops after 'to digest')"),
 ("w4c", "C1486", "On the other hand, if you're just drinking your black coffee, not consuming anything", "digesting heavy foods.", 606.0,
  "On the other hand, with just black coffee your energy is higher.", "his retake (the first run says 'not consuming energy')"),
 ("w4d", "C1486", "Now, you can maintain this productivity throughout your entire day", "for your lunch.", 618.7,
  "You can maintain this productivity all day if you eat a salad or a very low carb meal for lunch.", "only take"),
 ("w4e", "C1486", "In my experience, the real problem with eating during your workday", "when they're working.", 629.3,
  "The real problem with eating during your workday is the carbs ... nobody grinds out 12 hour days on donuts and pizza.", "only take"),
 # ---- why 5: your body adapts
 ("w5a", "C1486", "Now, here's the most important reason why I love fasting.", "I might as well just quit.", 671.7,
  "The most important reason. People try fasting, get hungry and quit ... your digestive system adapts just like your muscles do to workouts.", "only take"),
 ("w5b", "C1486", "Nobody does that when it comes to working out", "during my fasting window.", 725.2,
  "Nobody does that with working out ... nutrition works the same way ... 30 days in the hunger was nearly gone, 90 days in it was almost totally gone.", "only take"),
 ("w5c", "C1486", "And that's the biggest mental breakthrough that y'all guys have to make.", "throughout the day.", 782.2,
  "That's the biggest mental breakthrough: your body adapts to intermittent fasting over time.", "second start (the first, at 779.3, stops after 'breakthrough that')"),
 # ---- how to get started
 ("h1a", "C1486", "All right, so let's talk about how you get started with this.", "is drinking black coffee.", 827.3,
  "How you get started: simply skip your breakfast, keep everything else the same. To help with the hunger, drink black coffee.", "only take"),
 ("h1b", "C1486", "What I personally drink is cold brew black coffee.", "keep the hunger away.", 848.8,
  "What I personally drink is cold brew black coffee: less acidic, easier on your stomach.", "second start (the first, at 846.5, stops after 'cold brew')"),
 ("h2a", "C1486", "something you can do easily when you're starting off.", "from the get-go.", 871.5,
  "If you really want to take the fat loss to the next level, you can try adding a GLP-1 ... fasting can become nearly effortless from the get-go.",
  "second take (the first, at 864.9, stops at 'take the...'); Whisper folded the gap into a 3.3 s 'that's', so the in point is measured on the lav", None, "ONSET:871.2:872.2"),
 ("h2b", "C1486", "You don't have to do that though", "to start.", 901.0,
  "You don't have to do that though: many people, myself included, have done fasting without a GLP-1.", "only take"),
 ("h3", "C1486", "Okay, so your first month, nothing is changing for you", "you're defeating the purpose.", 918.5,
  "Your first month: nothing changes except you skip breakfast ... keep the rest of the day truly the same.",
  "'So just make sure to keep everything else in the latter part of the day the same' (944.5 to 948.3) left out: third time he says it in 20 s"),
 ("h4a", "C1486", "All right, so once you've locked in that habit", "until one o'clock.", 952.2,
  "Once you've locked in that habit, step it up: move lunch from noon to 12:30 for about 30 days, then to one o'clock.", "only take"),
 ("h4b", "C1486", "Keep doing that until you're fasting five hours in the morning.", "you eat lunch at noon.", 982.5,
  "Keep doing that until you're fasting five hours in the morning.", "his retake (the first run says 'about five to six hours')"),
 ("h4c", "C1486", "So, that gives you a daily 5 hour fasting window.", "if you really stick to this.", 1000.9,
  "That gives you a daily five hour fasting window: an excellent target for a couple of months.", "only take"),
 ("h5", "C1486", "Now, here's how you take things to the next level.", "eating normally for lunch.", 1016.3,
  "The next level: eat a salad or a low carb meal for lunch.", "only take"),
 ("h6", "C1486", "So that's your game plan. Skip breakfast and start with lunch at your normal time", "to break your fast.", 1042.3,
  "So that's your game plan: skip breakfast, push lunch back gradually to a five hour window, then break your fast with a salad or low carb meal.",
  "second take (the first, at 1034.7, stops at 'as soon as you're not...')"),
 # ---- mistakes
 ("m0", "C1486", "Before you start though, I just wanna go over a few common mistakes", "that I want you to avoid.", 1074.3,
  "Before you start, a few common mistakes to avoid.", "'All right, so that's your simple game plan to get started' (1071.1) trimmed: the sentence before it in the cut is 'So that's your game plan'"),
 ("m1a", "C1486", "the first one is binge eating late at night. And this is something", "reasonably healthy food.", 1086.6,
  "The first one is binge eating late at night ... you still have to eat reasonable portions of reasonably healthy food.", "his retake of the line (the first run, at 1081.0, stops at 'This is one that I felt')"),
 ("m1b", "C1486", "With that being said though, you do have some flexibility", "during your eating window.", 1127.9,
  "With that being said, you do have some flexibility to eat the foods you want: reasonable portions, no milkshakes, but spaghetti or a piece of pizza is fine.",
  "second run of the sentence: the first ('With that being said though, you do have...', 1124.9 to 1127.1) was abandoned and Whisper hid the retake inside a 3.4 s 'some' (found on the lav envelope, confirmed by a medium.en pass on the window alone); words.json is patched in mkglobal.py"),
 ("m2a", "C1486", "The second mistake to avoid is eating within two hours of bedtime.", "extend your fasting window.", 1157.9,
  "The second mistake: eating within two hours of bedtime.", "only take"),
 ("m2b", "C1486", "Let's say if you're sleeping eight hours, you fast two hours at night", "you'll lose more fat.", 1176.2,
  "Eight hours of sleep plus two hours before bed plus five in the morning is a 15 hour fasting window.", "his retake (the first run, at 1172.1, stops at 'eight hours fast')"),
 ("m3a", "C1486", "And here is the number one most important mistake", "are going to be a lot worse.", 1196.7,
  "The number one mistake: do not break your fast with alcohol.", "only take"),
 ("m3b", "C1486", "So no alcohol until 30 minutes after you've broken your fast.", "for obvious reasons.", 1228.8,
  "No alcohol until 30 minutes after you've broken your fast.", "only take"),
 # ---- outro
 ("out1", "C1486", "that today's video, if you all guys want to try intermittent fasting for yourself", "how it goes for you.", 1271.0,
  "That's today's video. Try skipping breakfast, try some of these techniques, let me know in the comments how it goes.", "take 3 of 3, the only one without a restart", None, "ONSET:1271.0:1272.0"),
 ("out2", "C1486", "and if you wanna get started building six pack abs, go to", "Go to absbyai.com now.", 1334.2,
  "If you want to get started building six pack abs, go to absbyai.com ... generate an image of your future self.",
  "take 2: he asked for it ('Do that close one more time'); its own false start at 1330.3 is outside the cut"),
 ("out3", "C1486", "Thanks for watching this video and I'll see you guys next time.", "see you guys next time.", 1378.8, "Thanks for watching.", "his retake"),
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
