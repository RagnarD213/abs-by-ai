# SL-10 independent review brief (Alcohol And Abs SFC R1)

You are a fresh, skeptical reviewer. Expect "does not ship" the first time. You did not build this; do not trust the editor.

## What these are
Four vertical Shorts (1080x1920, 29.97 fps) cut from Dan's approved long-form "Can You Drink Alcohol And Still Have Abs?"
(RO-13 round 2 master, `/Users/danielrose/Projects/Claude/Projects/Abs By AI/claude edited long form content/11 - Can You Drink Alcohol And Still Have Abs/Can You Drink Alcohol And Still Have Abs | claude round 2 | 16x9 | RO-13.mp4`;
its corrected subtitles are the `.srt` beside it). Organic CONTENT cut from a long-form. Picture: the film's raw 4K roll C1707
through the film's grade (Color C LUT + a fitted curve matching the master); audio: the master's own mix, cut only.
Dan's picks (2026-10-29, his words): A "start with 'When you drink alcohol, it should taste bad' ... then go to 'Kill the sugary
mixers' ... eliminate the 'drink water' content at the end"; B without "A real night out..." and "One drinking occasion a week ...
take the edge off", with extra content added at the end; D starts with "Your last drink should be 3 hours before you go to bed",
then the sleep lines, then the rest; E as is.

- A: `Short-form video content/alcohol-short1_your-drinks-should-taste-bad.mp4`
- B: `Short-form video content/alcohol-short2_your-nightly-wine-is-killing-your-abs.mp4`
- D: `Short-form video content/alcohol-short3_stop-drinking-3-hours-before-bed.mp4`
- E: `Short-form video content/alcohol-short4_what-killed-my-urge-to-drink.mp4`
(all under `/Users/danielrose/Projects/Claude/Projects/Abs By AI/`)

Build data per short S in `/Volumes/Expansion/_edit_work/SL-10/build/S/`: `shots.json` (shot table: kind talk/clip, output
frames f0-f1), `timeline.json` (audio pieces and joins), `words.json` / `cues.json` (captions), `hf/manifest.json` (key-point
bars), `gate/plan.json`, `gate/watch/` (CHECKLIST.md, JUDGE_PROMPT.md, sheets, strips), `gate/hair_clearance.json` +
`gate/hair_proof_S.jpg`, `delivered_asr.json`. Plan source: `/Volumes/Expansion/_edit_work/SL-10/plans.py` (pieces, covers with
their grades, bars, caption text).

## Standing rules to judge against (Dan's)
- A Short stands alone: no opening on a list number or a reference back to the long-form; one point per Short; it ends on its own
  point, not a subscribe line.
- Framing: steady per shot, land-then-hold; never his head or hair cut (at least 20 px clear on every frame); a real size step
  (or a clip) at every same-camera cut, never a naked jump cut. Never a junk moment (looking away, resetting, a stumble).
- Clips fill the frame unless something essential would be cut; no graphic or watermark sliced at a frame edge. Every B-roll clip
  is colour corrected (a real grade, true blacks, not milky, not a gamma lift) and sits with the presenter.
- A cutaway shows the thing the line names. AI clip (D's smart-ring hand): AI-GENERATED chip on it, clear of the subject; it must
  make physical sense at playback speed.
- Captions: word-timed, match what is said (print what he says; the film's .srt spellings), never linger past a cut, never cover
  his face; the title band holds the whole Short; key-point bars distil the idea and never sit over his face; line 2 of a bar is
  readable for at least 1.5 s.
- B's fact card (2 GLASSES A NIGHT / 1,700 CALORIES / a week + 7 nights of bad sleep.) is the film's approved graphic rebuilt for
  the vertical: check it is whole, moving, and lands on the words.
- Audio: the film's approved mix, cut only (audio gate --verbatim stamps); listen (by measurement and by Whisper, never aloud) for
  clicks, clipped word starts or ends at every join (`timeline.json` joins), a pause that is too short or too long (his natural
  0.3-0.6 s), a hole or a level jump.

## What to deliver for your short S
1. Watch-pass judge: give EVERY image in `gate/watch/sheets` and `gate/watch/strips` a verdict per `gate/watch/JUDGE_PROMPT.md`,
   write `gate/findings.json`, then record: `python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" --judge <build>/S/gate/logs/watch_pass.json --findings <build>/S/gate/findings.json --by "independent reviewer (Claude Opus 5.5)"`.
2. Full review of the delivered file at full resolution (extract your own frames; check the audio around every join and the
   first/last 0.5 s; read every caption against the audio). Write `/Volumes/Expansion/_edit_work/SL-10/review/ROUND-1-REVIEW-<S>.md`:
   numbered defects with exact output timecodes and evidence, then `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`.
Use a private scratch folder `/private/tmp/claude-501/sl10_rev_<S>/` for every frame dump.
Tools: ffmpeg/ffprobe at `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/`, person mask CLI
`/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask`, local Whisper (python
`whisper`). Heavy steps: wrap them in `python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py" run --light --group SL-10 -- <cmd>`.
Never play audio aloud; never modify the delivered files or the build.

## Re-review (round 1, second pass, 2026-10-29)
Each Short was re-rendered after a first independent review (`review/ROUND-1-REVIEW-<S>.md`). Check that every defect there is
fixed on the NEW file and look for anything the fix broke. Write `review/ROUND-1-REVIEW-<S>-v2.md` (same format, VERDICT line).
Changes made:
- All four: every key-point bar's slot now holds every frame of its render, so the exit fade completes (B r1: bars vanished at ~45 %).
- A: bars rewritten to distil ("Bitter Beats Sweet / Less Sugar Per Glass", "Bad Taste Is / A Built-In Brake"), a third bar on the
  practical half ("Sugary Mixers / Double The Damage"); cocktail clip from 1.0 s (sharp before its focus pull); soda cut moved before "You".
- B: second piece starts at film 163.80 (the 90 ms tail of "evening" is gone); the pause at the join is now ~0.27 s, inside Dan's own
  range in this film (0.22-0.8 s between sentences).
- D: "This one sounds annoying, but it's the single highest return rule on the list." removed (pointed back at the film's list; the
  beer-toast clip now covers that join); opener reframed on the nightstand (4:40 clock, whiskey glass) and lifted; asleep clip from 1.8 s
  and starting on the next caption so "protection rule." no longer runs into it.
- E: the glucose-kit cutaway is gone (no real injection-pen clip exists); a red-wine pour covers "Taking Zepbound massively reduced my
  desire to drink alcohol", a beer toast covers "Now when I go out, I have one or two,"; he stays on camera for the recommendation.
  Bars rewritten to distil ("Then: Blowout Nights / Every Single Week", "Zepbound Killed The Urge, / Not Willpower").
The delivery gate runs after your judgement (it needs the judged watch log); its absence is not a defect for this pass.
