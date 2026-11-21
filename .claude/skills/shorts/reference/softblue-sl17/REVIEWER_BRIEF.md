# SL-17 independent review brief (Top 1 Percent SFL R1)

You are a fresh, skeptical reviewer. Expect "does not ship" the first time. You did not build this; do not trust the editor.

## What these are
Three vertical Shorts (1080x1920, 29.97 fps) cut from Dan's approved long-form "I'm 41. My Life Is Top 1%. How I Did It."
(RO-26 R5 master, `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Codex Content Videos/Top 1 Percent - RO-26/Top 1 Percent | codex | 16x9 | RO-26.mp4`).
Organic CONTENT, category SFL. Dan's picks (2026-10-20): A starts on "Believe it or not, nutrition made an even bigger impact"
with content added at the end; B starts on "If you're watching this and you want to start working out" with content added at
the end; D as he picked it (reordered: "I strongly believe..." first).

- A: `Short-form video content/top1-short1_nutrition-matters-more-than-your-workouts.mp4`
- B: `Short-form video content/top1-short2_start-with-5-minutes-every-morning.mp4`
- D: `Short-form video content/top1-short3_every-man-should-train-a-martial-art.mp4`
(all under `/Users/danielrose/Documents/Claude/Projects/Abs By AI/`)

Build data per short S in `/Volumes/Extreme/_edit_work/SL-17/build/S/`: `shots.json` (shot table: kind talk/clip/scene, output
frames f0-f1), `timeline.json` (audio pieces and joins), `words.json` / `cues.json` (captions), `hf/manifest.json` (key-point
bars), `gate/plan.json`, `gate/watch/` (CHECKLIST.md, JUDGE_PROMPT.md, sheets, strips), `gate/hair_clearance.json` +
`gate/hair_proof_S.jpg`, `gate/junk_report.json` (where present), `delivered_asr.json`. Plan source: `/Volumes/Extreme/_edit_work/SL-17/plans.py`.

## Standing rules to judge against (Dan's)
- A Short stands alone: no opening on a list number or a reference back to the long-form; one point per Short.
- Framing: steady per shot, land-then-hold; never his head or hair cut (at least 20 px clear on every frame); a real size step
  (or a clip) at every same-camera cut, never a naked jump cut. Never a junk moment (looking away, resetting, a stumble).
- Clips fill the frame unless something essential would be cut (then a card, with a reason); a horizontal clip in a card is never
  cropped shorter in height. No graphic or watermark sliced at a frame edge. B-roll colour sits with the presenter (not darker).
- Every cutaway of Dan shows an ACTION the line is about (never standing around); an exercise shown is shown as real reps.
- AI clip: AI-GENERATED chip on it, clear of faces; the three questions (cause and effect; a stranger with sound off can say what
  it shows; it shows the line). Real moving footage of Dan carries no photo label.
- Captions: word-timed, match what is said (print what he says), never linger past a cut, never cover his face; title band holds
  the whole Short; key-point bars distil (not echo) and never sit over his face.
- Audio: the film's approved mix, cut only (audio gate --verbatim PASS stamps exist); listen for clicks, clipped word starts or
  ends at every join (`timeline.json` joins), and a hole or level jump. In A, the two pieces at output ~23.3-27.9 s are a raw line
  the film dropped ("I meal prep, which costs me about $8 or $9 a meal. That's less than ordering Chipotle."), treated with the
  film's own fixed voice chain (null-tested against the master at 0.9997 correlation): listen hard for any change in tone or room.
- Hard cases already decided by the editor (judge them, do not assume): D's "most men today can't" is captioned "can't" (the
  approved film's validated subtitle; ASR hears "can"); "martial arts skills" likewise.

## What to deliver for your short S
1. Watch-pass judge: give EVERY image in `gate/watch/sheets` and `gate/watch/strips` a verdict per `gate/watch/JUDGE_PROMPT.md`,
   write `gate/findings.json`, then record: `python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/watch.py" --judge <S>/gate/logs/watch_pass.json --findings <S>/gate/findings.json --by "independent reviewer (Claude Opus 5.5)"`.
2. Full review of the delivered file at full resolution (extract your own frames; listen to the audio around every join and the
   first/last 0.5 s; read every caption against the audio). Write `/Volumes/Extreme/_edit_work/SL-17/review/ROUND-1-REVIEW-<S>.md`:
   numbered defects with exact output timecodes and evidence, then `VERDICT: SHIP` or `VERDICT: DOES NOT SHIP`.
Use a private scratch folder `/private/tmp/claude-501/sl17_rev_<S>/` for every frame dump (the Extreme drive is nearly full).
Tools: ffmpeg/ffprobe at `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/`, person mask CLI
`/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shorts/reference/recentre/personmask`, local Whisper (python
`whisper`, models in ~/.cache/whisper). Heavy steps: wrap them in `python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py" run --light --group SL-17 -- <cmd>`.
Never play audio aloud; never modify the delivered files or the build.
