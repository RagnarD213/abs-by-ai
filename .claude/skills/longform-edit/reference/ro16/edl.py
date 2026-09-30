"""RO-16 edit decision list: source ranges on C1710 (word-level edges from words.json; snapped to silence by snap()).
Each piece = one kept run of speech. Take choices recorded in notes; see ../takes.md for the shared picker's report."""
import json, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro16"
SRC = "/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1710.MP4"
# (id, in, out, text-anchor, why)
PIECES = [
 ("hook",      195.54, 233.12, "If I woke up 30 pounds fatter ... get done in 90 days.", "last full hook take (Dan asked for 'one more time'); shared picker chose it"),
 ("warn",      233.64, 264.12, "I do want to warn you ... get it over with.", "only take"),
 ("s1a",       277.48, 295.12, "Number one ... take care of their family,", "first part of take; its tail is restated at 300.0"),
 ("s1b",       300.00, 304.64, "and then they try to work out ... left over.", "restated clause, the complete copy"),
 ("s1c",       308.02, 321.96, "And there usually isn't any left over. So it never happens. ... around that.", "second copy (first copy 305.2 said alone)"),
 ("s1d",       322.46, 348.78, "Now I know a lot of you guys ... took the time off.", "only take"),
 ("s1e",       363.26, 403.10, "A lot of people don't think like that ... possibly afford", "last copy of the restated sentence, then continuous"),
 ("s2a",       403.68, 438.14, "Alright, here's the second thing ... mostly goes away.", "only take"),
 ("s2b",       444.40, 459.08, "To lose 30 pounds in 90 days ... becomes easy.", "only take"),
 ("s2c",       464.62, 480.78, "The second reason is ... diet too. I take Zepbound myself.", "second copy (false start at 459.6); medium.en hears 'I take Zepbound myself' 479.8-480.8", 480.90),
 ("s2e",       490.15, 500.40, "I went from 192 to 175 in about two months ... in the description.", "third attempt, the only complete one (medium.en: 481 said 181, 486 stalled after 'in', 490.1 clean)", None, 490.07),
 ("s2f",       500.94, 531.82, "If you tried and failed ... from Zepbound.", "only take, ends before the abandoned 'So talk to your doctor... in my'"),
 ("s2g",       536.02, 552.64, "So, talk to your doctor ... the rest of my life.", "complete copy; first take of the last sentence (the retake at 554 has a 3.7 s stall)"),
 ("s3a",       563.78, 571.80, "Number three ... Most guys", "only take; 0.95 s stall after 'Most guys' removed", 571.97),
 ("s3a2",      572.90, 598.66, "do it the opposite way ... even on vacation", "resumes after the stall; ends before the abandoned 'And if all you can do is'", 598.97, 572.84),
 ("s3b",       602.25, 611.98, "and if all you can do at first ... getting skipped.", "clean copy after the stumble 599.0-601.0; starts after a 601.95 mouth click", None, 602.17),
 ("s3c",       612.84, 626.92, "So why first thing in the morning? ... getting skipped.", "only take"),
 ("s3d",       631.78, 640.04, "I work out every morning ... and your sleep.", "second copy of 'I work out every morning'"),
 ("s3e",       646.54, 649.40, "That's why I work out first thing every day and why you should too.", "retake (script wording)"),
 ("s4a",       650.12, 672.28, "Here's the next thing ... But here's the bigger reason.", "only take"),
 ("s4b",       678.72, 709.58, "every meal comes with ... for rich people.", "second copy (first stopped at 'each meal is,')"),
 ("s4c",       713.88, 727.70, "But yet they're spending $15 on a burrito every single day for lunch ... in your city.", "second copy (script wording)"),
 ("s5a",       728.42, 742.04, "Number five ... by guessing.", "only take"),
 ("s5b",       763.40, 793.38, "If you never look at your bank account ... not tracking at all.", "first copy of 'It's not perfect' is fluent"),
 ("s5c",       801.44, 811.38, "And if you're eating the meal prep meals ... adds up your day for you.", "after the restart of 'it's not perfect'", 811.52),
 ("s5d",       816.50, 823.98, "Try ours out or use any other AI calorie tracking app ... losing fat.", "medium.en: first 'Try ours out... any other AI' 811.9-814.0 abandoned + throat clear 814.4-814.9", None, 816.42),
 ("s6a",       824.68, 840.28, "Alright, so once you're tracking ... per day.", "only take"),
 ("s6b",       845.86, 867.52, "That means every meal ... if you let it.", "second copy (first said 'be a large serving of meat')"),
 ("s6c",       874.24, 900.82, "And on Zepbound, this is an even bigger problem ... your muscle.", "second copy (first flubbed)"),
 ("s6d",       906.62, 936.76, "I've gained muscle and strength ... should NOT be carbs.", "second copy, then continuous"),
 ("s7a",       937.46, 956.44, "Number 7 ... if the plan is working.", "up to the stalled 'In one study... lost about'"),
 ("s7b",       962.00, 976.78, "In one study ... any one day.", "complete copy"),
 ("s7c",       982.10, 991.86, "What you want to look at ... wouldn't change anything.", "second copy; ends before the abandoned 'But let's say I stole that for a f-' 992.3-994.0", 991.97),
 ("s7d",       994.70, 1028.36, "But let's say it stalled out for a full week ... in the first place?", "complete copy, continuous into Number 8", None, 994.62),
 ("s8a",       1032.08, 1058.64, "It's because they're not weighing themselves ... 90 days of sacrifice.", "retake of the answer line"),
 ("s8b",       1059.34, 1072.94, "In addition to this ... health benefits.", "only take"),
 ("s8c",       1086.68, 1098.38, "If I ever were to start gaining weight ... belly fat.", "only take"),
 ("wrap",      1098.98, 1116.76, "Alright guys ... see you in the next one.", "first wrap take: fluent and has 'go all in'; the second restarts at 1140; out held to 1117.10 (round-2 review: 0.1 s tail; he smiles to camera until ~1117.15, then starts 'Roll it back')", 1117.10),
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
