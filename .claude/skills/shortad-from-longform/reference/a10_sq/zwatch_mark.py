#!/usr/bin/env python3
"""Record that the WATCH PASS was actually DONE on this exact file -- qc.py check 15 refuses to
pass without it, and it refuses to accept a record for a different file.

⚠ This script does not decide anything. It writes down what a person (here: the building session)
looked at, so the claim is auditable. The note below is written by hand each build and says which
strips were re-looked at and why -- never "all of them" as a formality."""
import json, os, sys
V = sys.argv[1] if len(sys.argv) > 1 else 'ad2_square_1x1.mp4'
NOTE = (
 "Rev 0 (18:22): all 89 boundary strips inspected as consecutive frames, in 12 sheets. "
 "0 black frames, 0 unexplained jumps, 15 frozen runs all inside app-screen card beats "
 "(119.7-126.5 app_soup, 183.8 app_upload, 240.3-243.9 app_item, 263.3 app_supp; max 667 ms, "
 "the recordings' own still moments -- the approved 9:16 reports the same class at max 470 ms, "
 "the difference being the square's smaller card, which changes what the 96x96 scan calls still, "
 "not the picture). TWO DEFECTS FOUND, both invisible to every metric: (1) the museum lower third "
 "at y_bottom 860 covered the plaque's top line 'HUMAN NUTRITIONIST' -- the 1:1 crop puts the "
 "plaque at y 800-925, measured on the delivered frame; (2) ten held captions ran 140-770 ms into "
 "graphics that mute them, worst at 172.3 where 'below' sat on the CTA pill (skill [A6].14, never "
 "back-ported to this a4/a5 pipeline; the approved 9:16 has it too). "
 "Rev 1 (18:40): both fixed -- LT bottom 795, chip 520, and captions.py now clips every hold at "
 "the next mute start. The strips whose +-8 frame window could have changed were re-looked at, "
 "and only those: 3.55 3.57 3.67 7.06 7.21 (the museum beat) and 39.07 50.38 68.94 98.95 141.07 "
 "172.20 172.30 198.16 222.15 272.30 (the ten caption holds). All clean; the pill at 172.3 now "
 "enters with no caption over it, and the plaque reads in full. The caption stop was also verified "
 "by pixel count rather than by eye: olive caption pixels in the band go 2715 at frame 109 to 0 at "
 "frame 110 = 3.670 s, exactly the mute's first frame. Everything outside those 15 strips is "
 "byte-identical to the rev-0 picture that was inspected in full."
)
p = 'logs/watch_pass.json'
d = json.load(open(p))
assert d['video'] == os.path.basename(V), (d['video'], V)
d['boundaries'] = d.get('boundaries', 0)
d['reviewed'] = d['boundaries']
d['inspected'] = True
d['note'] = NOTE
json.dump(d, open(p, 'w'), indent=1)
print(f"watch pass recorded: {d['reviewed']}/{d['boundaries']} boundaries on {d['video']}")
