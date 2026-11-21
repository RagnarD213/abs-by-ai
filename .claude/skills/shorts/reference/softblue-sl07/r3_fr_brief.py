import sys, json
k, fr, line = sys.argv[1], sys.argv[2], sys.argv[3]
a, b = fr.split(":"); W = "/Volumes/Extreme/_edit_work/sl07"; CC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck/clipcheck.py"
print(f"""Fresh frame-reviewer task: one AI motion take used in a vertical Short (it is shown cropped to 9:16 in the Short; judge the take itself).
TAKE: `{W}/clips/{k}.mp4`, the used range is frames {a} to {b} (both ends included).
SPEC: `{W}/clips/specs/{k}.spec.json`
GATE EVIDENCE (clipcheck PASSed on this range): `{W}/clips/clipcheck/{k}.f{a}-{b}.clipcheck.jpg` and sampled frames in `{W}/clips/clipcheck/{k}.f{a}-{b}.frames/`
THE SPOKEN LINE IT PLAYS UNDER: "{line}"
Do your standard A to I measurement on the sampled frames (decode more frames yourself into a scratch folder `{W}/r3/fr_scratch_{k}/` if needed), and answer
the three sense questions, one line each: (1) does everything obey cause and effect (nothing vanishes, appears, melts or changes by itself)?
(2) with the sound off, would a stranger say what it shows? (3) does it show the line being said?
Write `{W}/clips/clipcheck/{k}.f{a}-{b}.review.md` ending with a last line `VERDICT: PASS` or `VERDICT: FAIL`, then record it:
`python3 "{CC}" "{W}/clips/{k}.mp4" --frames {fr} --review "{W}/clips/clipcheck/{k}.f{a}-{b}.review.md"` and confirm
`python3 "{CC}" "{W}/clips/{k}.mp4" --frames {fr} --verify` exits 0 (if your verdict is PASS). Reply with the verdict and the three answers.""")
