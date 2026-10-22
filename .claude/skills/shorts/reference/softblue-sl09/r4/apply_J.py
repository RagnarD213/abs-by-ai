"""R4: put J1 (opener) and J2 (WHOOP hand) into short 5's plan (run once; both takes passed clipcheck + reviewer)."""
p = "/Volumes/Extreme/_edit_work/sl09/round2/plans.py"; s = open(p).read()
i = s.index(' "J": [dict(id="app"'); j = s.index('\n', i); old = s[i:j]
new = (' "J": [dict(id="j1", a="o0.0", b="o3.70", src=W9 + "sl09_r4/veo/J1-api-t2.mp4", t=0.3, fx=0.5, fy=0.0, eq="curves=all=\'0/0 0.5/0.45 1/0.96\'", ai=[40, 336, 1.6], '
       'note="AI clip J1 (Veo 3.1 Fast, paid take 2 of 2, 4 s, from the start/end frames Dan approved 2026-10-20): a hand on white sheets lifts and tilts so the matte black smart ring on the index finger catches the light; take seconds 0.3-4.0"),'
       '      # R4 (Dan 2026-10-20: "Smart ring close-up ... look good"): replaces the opening phone (R3b: psolo of his Oura recording 7:05.3 at 1.5x). fy 0.0 puts the ring at picture row ~580, in the centre third; grade median 0.51 -> 0.46 (white sheets)')
assert s.count(old) == 1; s = s.replace(old, new)
k = s.index('       dict(id="compare", a="o20.603"')
s = s[:k] + ('       dict(id="j2", a="o16.30", b="o20.603", src=W9 + "sl09_r4/veo/J2-api-t5.mp4", t=0.417, fx=0.5, fy=0.7, eq="curves=all=\'0/0 0.5/0.40 1/0.92\',eq=saturation=1.05", ai=[40, 336, 1.6], '
             'note="AI clip J2, WHOOP version (Veo 3.1 Fast, paid take 5, 6 s, from the approved WHOOP start frame): one hand with the smart ring on the index finger and a WHOOP-style strap, its sensor pod on top of the wrist; the open hand lifts and tilts so ring and pod catch the light, then settles; take seconds 0.42-4.70"),'
             '      # R4: "Just more depends whether you prefer a wrist-based or a finger-based sleep tracker" (16.47-20.43): the hand shows exactly that pair. Dan stays on camera for "Oura Ring and WHOOP are my top two options" (13.80-16.30): four takes could not close the hand into the approved fist without a finger flicking up, and the open-hand take is 6 s. fy 0.7 keeps the pod above the captions (pod rows ~840-1000)\n') + s[k:]
open(p, "w").write(s); print("patched")
