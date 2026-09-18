#!/usr/bin/env python3
"""Repeated-footage scan on a word list: stretched words and repeated n-grams.

Dan, website video rev 2 (2026-09-02): "At 32 seconds, I repeat 'I've been out of shape' ... check
more thoroughly for repeated footage in the future." Whisper had stitched the restart into ONE token
(`and` timed 1.75 s), so orphan_scan.py saw no uncovered energy. A stretched word is a hidden restart
until an isolated re-transcription proves otherwise.

  repeat_scan.py <tight_cuts.json | whisper.json> [--stretch 0.7] [--window 25] [--n 4]
Prints every word longer than --stretch seconds and every n-gram that recurs within --window seconds.
Verify each flag by re-transcribing that span alone (ffmpeg -ss t-2 -t 4 ... -> whisper medium.en,
condition_on_previous_text=False, word_timestamps=True).
"""
import json, re, sys
args=sys.argv[1:]; src=args[0]
opt=lambda k,d: float(args[args.index(k)+1]) if k in args else d
STRETCH,WINDOW,N=opt("--stretch",0.7),opt("--window",25),int(opt("--n",4))
d=json.load(open(src))
if "words" in d: W=[(w["t"],w["e"],w["w"]) for w in d["words"]]
else: W=[(w["start"],w["end"],w["word"]) for s in d["segments"] for w in s.get("words",[])]
norm=lambda s: re.sub(r"[^a-z0-9 ]","",s.lower()).strip()
toks=[(t,e,norm(w)) for t,e,w in W if norm(w)]
flags=0
print(f"stretched words (> {STRETCH:.1f} s):")
for t,e,w in toks:
    if e-t>STRETCH: print(f"  {t:8.2f}-{e:8.2f} ({e-t:.2f}s) {w!r}"); flags+=1
print(f"repeated {N}-grams within {WINDOW:.0f} s:")
seen={}
for i in range(len(toks)-N+1):
    g=" ".join(x[2] for x in toks[i:i+N]); t=toks[i][0]
    if g in seen and t-seen[g]<=WINDOW: print(f"  {seen[g]:8.2f} and {t:8.2f}: {g!r}"); flags+=1
    seen[g]=t
print(f"{flags} flag(s) -- each one is a restart until an isolated re-transcription says otherwise")
sys.exit(1 if flags else 0)
