# Re-centring an off-centre 9:16 crop

Built 2026-08-27 after Dan caught `v2-short3_supplements-3-percent` off-centre on the day it
posted. Root cause and thresholds are in Step 5 of `SKILL.md`; this folder is the tooling.

Paths at the top of each script point at
`YouTube Long Form Video Content/<slug>/` and a session scratchpad — fix those first.

```
swiftc -O -o personmask personmask.swift     # once; Apple Vision person segmentation
python3 collect.py v2 v3                     # sample source frames for every talk shot
./personmask OUTDIR FRAMES/*.png             # masks
python3 audit.py v2 v3 v6                    # per-shot + per-short offset / cut-off verdicts
python3 ab_multi.py v2 sheet.png SHOT ...    # shipped vs proposed, 5 frames across each shot
python3 apply_crops.py v2 D E I J            # write crops.json (backs up .pre-recentre)
node render.js D                             # re-render, in the build folder
python3 verify_recut.py                      # frame/duration/audio parity vs the shipped file
```

`override_<build>.json` (`{"SHOT": 0.527}`) forces a hand-picked value for a shot where the
automatic anchor is wrong — needed on every V6 shot but one.

**`audit.py` is a shortlist, not a verdict.** It over-fires on handheld and outdoor
footage. Nothing changes until `ab_multi.py` has been looked at.
