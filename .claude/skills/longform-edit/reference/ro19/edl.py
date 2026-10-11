"""RO-19 "My First Spray Tan" edit decision list (8/3 kitchen roll C1512, one 30:42 take off an outline; take picks: Docs/TAKE_SELECTION_C1512_20260924.md).
Pieces are anchored on PHRASES in the medium.en word list (words.json, global timeline of mkglobal.py, with the verified
windows of word_patches.json), not on typed times: (id, roll, first words, last words, roll-local hint, script beat, why).
Edges are then snapped to the measured lav envelope. Optional 8th/9th fields: measured roll-local out / in that override the snap.
The list is written by hand from the roll transcript and the approved take picks."""
import json, re, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro19"
FPS = 30000/1001
ROLLS = json.load(open(f"{W}/rolls.json"))
WORDS = json.load(open(f"{W}/words.json"))["words"]
THR = -43.0   # C1512 lav: room mode -60 dB (quiet pauses -62..-56), speech median -25 dB inside words, word tails reach -43 about 0.1 s after the word (measured on lav.wav)
PIECES = [
 ("intro", "C1512", "I just got my first spray", "you how to do it.", 135.5,
  "I just got my first spray tan. What do y'all guys think? Here on the left ... who it's right for and who it's not right for. And I'm going to show you how to do it.",
  "take 5 of 5 of the opening, the last and clean (Dan approved this pick on 2026-09-24)"),
 ("photos", "C1512", "if you guys want to look", "about that in a second.", 194.0,
  "So, if you guys want to look good in photos ... It's not appropriate for everybody, but I'm about to tell you about that in a second.",
  "only take; the 'All right.' before it is a reset and is left out"),
 ("exp1", "C1512", "Alright, so let me tell", "best places to do it?", 302.0,
  "All right, so let me tell you about my first spray tanning experience ... So I'm like, okay, how can I do that? What's the best places to do it?",
  "only take, up to the restart of the next sentence", None, "ONSET:304.6:306.6"),
 ("exp2", "C1512", "my AI went through all the reviews for spray", "from among those options.", 331.0,
  "My AI went through all the reviews for spray tan studios in my local area ... and then you can choose from among those options.",
  "second start of 'My AI went through all the reviews' (the first stopped at 'for people in my local')"),
 ("cost", "C1512", "So for me, I bought a", "bit of a cheaper studio.", 368.0,
  "So for me, I bought a premium spray tan ... you can get a spray tan for about $50 if you skip the contouring and go to a little bit of a cheaper studio.",
  "only take"),
 ("diy1", "C1512", "Now, there are other options that", "use to do it yourself at home.", 414.2,
  "Now, there are other options that you can do even if you don't want to spend money on a professional spray tan ... There are also tanning wipes that you can use to do it yourself at home.",
  "only take, up to the restart of the next sentence"),
 ("diy2", "C1512", "tanning wipes and tanning sprays that", "wipes can work just fine.", 431.0,
  "Tanning wipes and tanning sprays that you do at home are more appropriate if you just want to look good, say on a date ... Aerosol or do it home wipes can work just fine.",
  "second start of the sentence (the first, 'These type of things are more appropriate if you're', he abandoned)"),
 ("help", "C1512", "if you have someone who can help you apply", "and for the contouring.", 462.5,
  "If you have someone who can help you apply the tan ... if you're strapped for budget. If you have the money, though, I recommend going professional, though, just for full even coverage and for the contouring.",
  "second start (the first, 'If you have someone who can help you do it ... then this', he abandoned): the stumble cut Dan approved on 2026-09-24"),
 ("visit", "C1512", "All right, so if you do", "to skip the spray tan.", 489.0,
  "All right, so if you do do professional, let's talk about what the experience is like ... So it's really not as awkward as you think, and it shouldn't be a reason to skip the spray tan.",
  "only take"),
 ("after1", "C1512", "Okay, so let's talk about the drying", "the rapid drying tan because", 584.4,
  "Okay, so let's talk about the drying time and the aftercare ... I personally recommend the rapid drying tan because",
  "only take, up to the clause he says twice", 608.53),
 ("after2", "C1512", "From what my tanning specialist told", "into bed at night.", 613.2,
  "from what my tanning specialist told me, there's not a huge difference in the longevity of these tans ... get it early in the day and then shower before you get into bed at night.",
  "his retake of 'from what my tanning specialist told me, there's not a huge difference in the longevity' (the first ended 'of it'); found by the plan writer's repeat check"),
 ("shower1", "C1512", "Alright, so let's talk about that first", "the chemical reaction happened.", 638.9,
  "All right, so let's talk about that first shower. In that first shower, you can't use any soap ... before the chemical reaction happened.",
  "only take"),
 ("shower2", "C1512", "now, after this, you can start", "you don't smell that.", 688.0,
  "Now after this, you can start showering normally with soap, but there's still a few guidelines ... And so that way you don't smell bad.",
  "second 'now after this' (he said it twice with a pause)"),
 ("last", "C1512", "Alright so let's talk about how long", "wear off won't is noticeable.", 728.0,
  "So let's talk about how long your spray tan is going to last ... those small patches that wear off won't be as noticeable.",
  "only take"),
 ("water1", "C1512", "Now, here is another downside.", "you're taking care of it.", 791.4,
  "Now, here is another downside. If you go in the water ... a fair example of how it looks like five days in if you're taking care of it.",
  "only take, up to the sentence he says twice"),
 ("water2", "C1512", "In my normal life, I'm in", "this in my normal life.", 837.2,
  "In my normal life, I'm in the water all the time, so I'm not entirely sure it would hold up as good as this in my normal life.",
  "second take of the 'In my normal life' sentence (Dan's earlier note: drop the repeat)"),
 ("pics", "C1512", "Okay so on screen right now", "investing $50 to $100.", 858.6,
  "Okay, so on screen right now, I'm going to show you a few pictures ... if that difference would be worth investing $50 to $100.",
  "only take"),
 ("pros", "C1512", "Okay, so now you see what spray", "goes out in the sun.", 916.8,
  "Okay, so now you see what spray tanning can do. Let's talk about the pros and cons ... and why he takes an umbrella out with him when he goes out in the sun.",
  "only take"),
 ("sun1", "C1512", "sun exposure is one of the most common causes", "many different health conditions.", 975.4,
  "Sun exposure is one of the most common causes of cancer. Skin cancer is one of the most common cancers ... sun damage really increases your risk for many different health conditions.",
  "last take of three (the first two said 'most common forms of cancer / forms of aging' and trailed off)"),
 ("sun2", "C1512", "So even though a natural", "less likely to get cancer.", 1004.6,
  "So even though a natural tan can look healthy, it is not healthy ... and you would be less likely to get cancer.",
  "restart of 'So sun damage, even though.'"),
 ("sun3", "C1512", "in my opinion, that's the most", "money in a spray tan.", 1061.5,
  "In my opinion, that's the most important reason to invest in spray tanning ... then I recommend investing that money in a spray tan.",
  "second 'in my opinion' (said twice)"),
 ("ginger1", "C1512", "Now, here's another reason why you", "If you are super pale.", 1082.1,
  "Now, here's another reason why you might want to spray tan. Maybe you have no choice. If you're a ginger ... you have to get a spray tan if you are super pale.",
  "only take"),
 ("ginger3", "C1512", "now, if you are super pale, just", "won't be as noticeable.", 1117.5,
  "Now, if you are super pale, just keep in mind that you don't need a tan that much ... a little bit of wear off won't be as noticeable.",
  "second start (the first was 'Now, even if you are,')"),
 ("cons", "C1512", "Okay, so let's talk about the cons", "can be a good investment.", 1172.3,
  "So let's talk about the cons of spray tanning. So the most obvious con is the money ... a spray tan can be a good investment.",
  "only take"),
 ("self", "C1512", "Now, like I said before, you", "does come with its own drawbacks.", 1238.0,
  "Now, like I said before, you can self apply at home ... So that is an option, but it does come with its own drawbacks.",
  "only take"),
 ("orange", "C1512", "Another drawback of a spray", "can actually look very natural.", 1255.8,
  "Another drawback of a spray tan is that for certain people, such as myself, who naturally tan very well ... If you go premium, it can actually look very natural.",
  "only take"),
 ("wears", "C1512", "The biggest drawback of the", "another significant drawback.", 1288.3,
  "Now, the biggest drawback of the spray tan, like I mentioned before, is it wears off in about a week ... That's another significant drawback.",
  "only take"),
 ("who1", "C1512", "So who should be spray tanning", "very pale skin right now.", 1323.0,
  "So who should be spray tanning and who should not? Number one, vampires, people out there who are super, super pale ... so much better if you have very pale skin right now.",
  "second take (the first stumbled on 'super paired')"),
 ("who2", "C1512", "if you're strapped for fonts, at least do the tanning wipes or the", "invest in a professional tan.", 1355.0,
  "If you're strapped for funds, at least do the tanning wipes or the tanning spray. So that way you can look acceptable with clothes on. And if you have the money, invest in a professional tanning.",
  "second take (the first stopped at 'So that way the clothes,')"),
 ("poor", "C1512", "People who are poor should not", "invest in the spray tan.", 1372.1,
  "People who are poor should not be getting these professional spray tans ... once you already have the body to show off in photo shoots, then invest in the spray tan.",
  "only take"),
 ("app1", "C1512", "And I would say if your", "in person all the time,", 1404.7,
  "And I would say if your money substantially depends on your appearance, if you're going on camera, if you're an influencer, if you're dealing with clients in person all the time,",
  "first part of the sentence; he re-said its ending", 1416.74),
 ("app2", "C1512", "If you're in an industry like fashion", "because you look better.", 1423.7,
  "If you're in an industry like fashion or hair dressing where your appearance is very important, then I would invest in a spray tan as well. That small investment in the professional tan will pay dividends ...",
  "his retake of the ending ('an industry like fashion ... invest in a spray tan as well')"),
 ("mid1", "C1512", "So let's say you're rich, you're", "a wedding to go to.", 1452.0,
  "So let's say you're rich, you're ripped, you're on camera all the time ... or you have a special occasion like a wedding to go to.",
  "only take"),
 ("mid2", "C1512", "So I would say that's what", "doing it at some times.", 1481.6,
  "So I would say that's what I recommend for most people. Do the spray tan sometimes ... consider at least doing it at some times.",
  "only take (the lone 'So.' before it is left out)"),
 ("max1", "C1512", "Now, if you're at that level", "shoot to get the best effect.", 1514.6,
  "Now, if you're at that level where you can only get a spray tan at some times, then you really want to maximize it ... Fast before you shoot to get the best effect.",
  "only take"),
 ("max2", "C1512", "Finally, before your shoot, spend five", "pictures like a professional.", 1569.2,
  "Before you shoot, spend five to ten minutes maximizing your posing ... make sure you know how to take pictures like a professional.",
  "second start (the first, 'And then finally, before you shoot, just spend five to', he abandoned)"),
 ("wrap", "C1512", "So, for the majority of you", "get your spray tan.", 1583.4,
  "So, for the majority of you guys, that's going to be the way to do it ... big events, weddings, photo shoots, video shoots, get your spray tan.",
  "only take"),
 ("outro", "C1512", "All right, so that's today's video. If you guys", "in the next video.", 1777.0,
  "All right, so that's today's video. If you guys want to take the first step to building your dream body ... Thank you for watching, guys, and I'll see you in the next video.",
  "take 4 of 4 of the close, the last and clean (Dan approved this pick on 2026-09-24); the four earlier attempts are out"),
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
