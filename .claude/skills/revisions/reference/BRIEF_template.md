# Reviewer brief — TEMPLATE (copy to the batch work dir, fill the <…> fields, keep everything else)
# Batch: <editor>, cuts delivered <date>

You are writing ONE revision-round document section for Dan Rose (Abs By AI) in Dan's own voice, per the
`/revisions` skill: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/revisions/SKILL.md`.
READ THAT FILE FIRST, in full — the "Calibration from Dan's edits" section (rules 1–21) and the standing rules
are the spec. The doc goes to the editor exactly as written; Dan does not re-review. Never mention Claude, AI
review, or "measurements we ran" as a third party — everything is "I checked / I measured". American spelling.

Editor: **Muhammad Arsalan** (Upwork, batch of 12 ads). Round numbers are per editor per ad:
- `ad3_v4` = AD 3 ROUND 4 (his 4th cut; rounds 1–3 in the doc). `ad5_v3` = AD 5 ROUND 3. `ad6_v2` = AD 6 ROUND 2.
  `ad7_v2` = AD 7 ROUND 2. For these, the previous round's section IS your checklist: score every item DONE /
  PARTLY / NOT DONE, open the section by crediting what landed ("keep all of that"), then list only what is
  still wrong + anything new the change introduced. A round ≥ 3 says explicitly that this list ends the job.
  `framediff.txt` in the work dir (when present) is the OLD vs NEW picture diff: UNCHANGED stretches mean the
  picture there is byte-for-byte the previous delivery, so every previous timecode there is still valid.
- `ad9_v1`, `ad10_v1`, `ad13_v1`, `ad14_v1` = FIRST cuts of AD 9 / 10 / 13 / 14 (round 1 — no round number in
  the H2, matching the AD 6 / AD 7 / AD 8 sections). Open by crediting what already works, then the fixes.

## What Dan told him on 2026-09-08 (in the Upwork room) — the standing rules he has now been given
"The most significant issues are the audio corrections, and the standing rule for showing the after picture
only for the AI generated fitness goal clip. Once we establish standing rules for those issues, we should have
much more minimal revisions going forward." So on every cut, the two things to check FIRST: (a) audio at
−14 LUFS with a limiter at −1 dBTP, one mic, tone like Ad 1; (b) the app demo / goal-image moments end on the
AFTER (goal) picture ALONE — never the "Meet the new you" before+after reveal, never a dissolve/slide/arrow
between a before and an after, never before straight into after (camera scene between). If he applied the
standing rules on a NEW ad without being told, say so and credit it.

## What already exists for your video (do not redo)
Work dir: `/Volumes/Extreme/_edit_work/<WORKDIR>/work/<NAME>/`
- `probe.json` ffprobe; `transcript.txt` (Whisper small, `m:ss.s - m:ss.s  text`); `<NAME>.json` segment json
- `gate.txt` = `_shared/audio/audio_gate.py` against Muhammad's pinned Ad 1 reference (the rows Dan rejects on);
  `lav.txt` = `pick_lav.py --analyse`; `peaks.txt` = per-second true-peak scan + clipped samples + L/R corr;
  `silence.txt` (silencedetect −35 dB, 0.25 s) for dead air; `scenes.txt` (picture-change timestamps, 0.30)
  + `scenes_summary.txt`; `luma.txt` mean brightness; `AB_ref-vs-<NAME>.mp4` A/B clip; `framediff.txt` (round ≥ 2).
- `frames/f%05d.jpg` at 2 fps, 320 px wide; `sheet_NN.jpg` contact sheets, 60 tiles each with yellow timecodes
  (tile index i → t = i/2 s). LOOK AT EVERY SHEET with the Read tool. Zoom by extracting a full-res frame:
  `"/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg" -ss <sec> -i <video> -frames:v 1 -q:v 2 out.png`
  (single frames only — do NOT run whisper or any full-length ffmpeg pass; the machine is capped at two builds and
  the batch pipeline is using both slots). Transcribe every text panel at full res (calibration rule 1) and check
  letter spacing / weight / size against neighbouring chips (rule 20). Check every insert's EXIT frame (rule 2).
Videos: `/Volumes/Extreme/_edit_work/<WORKDIR>/dl/<NAME>.mp4`.
Previous deliveries of the same ad (for round ≥ 2): `/Volumes/Extreme/_edit_work/revisions-0908/dl/<ad>_v<n>.mp4`
with their prep in `/Volumes/Extreme/_edit_work/revisions-0908/work/<ad>_v<n>/` (gate.txt, transcript, sheets) and
the section we wrote in `/Volumes/Extreme/_edit_work/revisions-0908/out/<ad>_v<n>.md` (+ `.summary.md`).
Scripts doc (plain text export of "AD SCRIPTS TO EDIT (Ads 2–15) — Muhammad batch", with the asset Drive links
under each cue): `/Volumes/Extreme/_edit_work/<WORKDIR>/docs/scripts_ads2-15_fixed.txt`
(AD 3 lines 134–205, AD 5 272–348, AD 6 349–443, AD 7 444–521, AD 9 607–671, AD 10 672–752, AD 13 753–830,
AD 14 831–907). Read your ad's script in full, including the "Ad N note" line at the end — it names the assets,
the load-bearing facts (ages 38 → abs at 40, "one daughter", "around" on every price in Ad 13, "400" only in the
title of Ad 14, no ChatGPT/OpenAI logo or UI in Ad 9, the slightly-enhanced before picture in Ad 10) and the
compliance traps. A script cue that asks for a split screen, a whip pan between the two pictures, or the app's
"Meet the new you" reveal is WRONG — the standing rule wins and the doc says so (lesson 31).
Muhammad's doc AS DAN SENT IT (all previous rounds, with Dan's edits — the register to match):
`/Volumes/Extreme/_edit_work/<WORKDIR>/docs/muhammad_doc_0909.txt`. Sections: AD 2 (Dan's own notes, lines
3–34 — "Remove this clip, use camera scene", "Replace with 0:00 - 0:05 from this clip"), AD 3 r1 35–128, AD 3 r2
129–184, AD 4 185–266, AD 5 r1 267–386, AD 3 r3 387–417, AD 4 r2 418–451, AD 5 r2 452–486, AD 6 487–571,
AD 7 572–674, AD 8 675–end. For a round ≥ 2 cut, your checklist is the LAST section for that ad in this file
(not our markdown — Dan edited before sending).

## Hard rules (from the skill; violations are the items)
- Compliance: NO before+after in one frame (side-by-side, arrow two-panel, app "Meet the new you" reveal); NO
  before imagery cut straight into after imagery (camera scene between); NO belly-fat grab/pinch/zoom; NO email
  capture form on screen; no celebrity likeness / magazine logo / competitor logo or UI in a paid ad.
- "*AI Generated" label on every AI visual for its full duration, upper LEFT, ~50% larger on full-frame clips;
  REAL photos (the photo-shoot stills, the raw before picture) never get one.
- Audio: one mic (no comb, no two-mic pair), room ≤ 80 ms, −14 ±1 LUFS, true peak ≤ −1.0 dBTP, no clipping.
  Quote gate FAIL rows with numbers in editor words. Name the hot seconds from peaks.txt and say whether they are
  voice or SFX (lesson 30). Write the fix as an ordered recipe: limiter at −1 dBTP first, then lift to −14 through
  it (lesson 38 — he "fixed" Ad 5's clipping by dropping the mix to −29.7 LUFS).
- Casting: aspirational figure = white or Asian man 30–50 in shape; antagonists cast as the caricature; new clips
  are "stock footage or an AI clip"; body judgements only when verified at full res and it is the reason.
- Every insert has an exit; text centred in its panel; Title Capitalization; no header rewording on taste;
  no padding items; one before beat per section; no bullet list of negatives; video holds ~2 s after last word.
- Real app screens only; end on the after picture alone.
- Graphics budget (calibration pass 2, rules 12–16): about TWO added text chips per ad, each stating an outcome
  or benefit in Dan's positive voice — never a restatement of the spoken line, a question, or a list of
  negatives. No new bullet builds unless it replaces something wrong. No app screen as a gap fill. No panel or
  device copied from another ad in the batch (check the AD 3–8 sections for what already exists). No item may
  cross-reference another item, and no item counts in the prose ("four things are left"). A truncated lower
  third is a chip, not a defect. When in doubt on a single strong graphic idea, include it — Dan's rule is that a
  graphic is easy for the editor to remove.
- Rule 17/19: check the hero asset against the LITERAL script claim (Ad 9: the "ChatGPT attempt" image must be
  DAN'S face crudely pasted on a generic ripped body, no ChatGPT branding; Ad 10: skip-stopper before is the
  slightly-enhanced version, after is the real trees / hands-on-hips shoot photo; Ad 13: the running tally is
  editor-built text — transcribe every number and every "around"; Ad 14: "400" appears only in the on-screen
  title). "Got the abs" proof = two real pool-shoot after photos, the same two as the previous ads.


## Pass-3 rules (Dan's edits 2026-09-10 — these override anything above that conflicts)
- ROUND ≥ 2 AUDIO: an item ONLY if level is outside −14 ±1 LUFS, or true peak ≥ 0 dBTP with clipped samples, or the
  mic/room is wrong. Tone, artifacts and a −0.7/−0.8 ceiling are NOT a round. If the level and peaks are right and
  nothing else is wrong, the section is the H2, then a bold line `APPROVED - FINALIZED - READY FOR HIGH QUALITY EXPORT`,
  then the credit paragraph. No THROUGHOUT, no items.
- NO end-hold item unless the button or picture cuts off BEFORE the last word ends.
- STANDING RULE blocks: every item that violates a standing rule ends with a bold sub-bullet in the CANONICAL wording
  from the skill's "Standing rules to check" list (paste verbatim), repeated in every ad it applies to.
- BOLD THE KEY CHANGE in every item: one diagnostic sentence, then the action in **bold**, then timing. Short.
- App/phone demo: the one-line block ("The real app recording is the right thing here, keep it. But it ends on the
  Generating screen and never pays off … end on that recording's own after picture alone … Small AI-GENERATED tag") +
  the recording link + the goal-image STANDING RULE. Identity-check the before picture inside every phone/app clip
  against Dan's real before picture; if it is not Dan, one line + the before-picture link (`02_BEFORE-PICTURE_dan-200lb.png`,
  `11Qb559-mqga9FznIpC8tgxLLfz1BUKQX`). ⚠ The only real app recording that exists (`example generation video.MP4` =
  `09_CLIP_app-generate-future-self.mp4`) uploads a STRANGER — there is no recording of Dan's own upload, so never write "use
  this recording of my own upload"; the fix is always the before-picture swap inside the clip (lesson 40).
- After-photo beats: "Show TWO pictures here, images below" with two empty `- ` sub-bullets for Dan to fill; do not
  pick stills; never the same pair as an earlier beat in the same ad. No item about WHICH real after photo.
- Logo in frame: "Take the logo out." + `STANDING RULE: Do not use logos of other companies in our ads. Names of other
  companies are OK` + "camera scene". Do not design a replacement title.
- No chip fills on round 1 unless a 15 s+ stretch is empty and the chip states a benefit; never replace the editor's
  own skip-stopper chips. Adjacency inside/beside an approved AI asset is not an item. A bullet build mid-build is not a
  composition defect.

## Output (write these files, nothing else)
1. `/Volumes/Extreme/_edit_work/<WORKDIR>/out/<NAME>.md` — the doc section, in the exact dialect
   `md_to_docs_clipboard.py` parses: `## ` H2 title line, plain paragraphs, `- ` bullets with 4-space nesting,
   `**\*\*HEADER\*\***` for THROUGHOUT headers, links as `<https://…>`. Model it on
   `/Volumes/Extreme/_edit_work/revisions-0908/out/ad8_v1.md` (round 1) and `ad3_v3.md` (round 3).
   H2 forms: `## AD 3 — ROUND 4 (Stop Paying Human Trainers! Use AI Instead)`, `## AD 5 — ROUND 3 (…)`,
   `## AD 6 — ROUND 2 (…)`, `## AD 7 — ROUND 2 (…)`, `## AD 9 — I Tried to Get Abs With ChatGPT. Here's What Happened.`,
   `## AD 10 — My Dad Bod at 38. My Dad Bod at 40.`, `## AD 13 — I Added Up What Getting Abs Was Supposed to Cost`,
   `## AD 14 — I Watched 400 Workout Videos and Gained Weight`.
   Open with what he fixed / what works ("keep all of this"), then THROUGHOUT, then TIMESTAMPED REVISIONS in play
   order, then "Everything else, keep." Every item states the exact replacement (exact text, exact Drive link from
   the scripts doc or the asset library in the skill, or exact source timecodes).
2. `/Volumes/Extreme/_edit_work/<WORKDIR>/out/<NAME>.summary.md` — for Dan's chat report: 5–10 lines:
   scorecard vs last round (DONE / PARTLY / NOT DONE counts, for round ≥ 2), the 3 biggest findings with numbers,
   the item count, anything that needs Dan's call (kept OUT of the doc), and a one-paragraph paste-ready Upwork
   message from Dan to Muhammad saying the round is in the same doc
   (`https://docs.google.com/document/d/1L2XJKLFrRJHKlcL4Iii70iFvZeiNNeplxYQw2aeAJ_A/edit`) — short, warm, specific
   about the 2–3 things that matter most, and (for a round ≥ 3) explicit that the list ends the job.
Before writing file 1, run the self-check in workflow step 7 of the skill and delete any item that fails it.
Return in your final message: the path of both files, the item count, and the three biggest findings.

## Asset links (the plain-text scripts export lost most of the embedded images — use these)
The standard Ad 1 set, already linked in previous sections (copy the exact links from
`/Volumes/Extreme/_edit_work/revisions-0908/out/ad8_v1.md` and `ad7_v1.md`): raw before picture
`1LF0vG8oVtwjLl7wPucj_mMowrEju_BfV`… (see those files), the two fat-dad photos, the four photo-shoot stills
(red shorts / towel / flag / trees), the goal image `1-8QAfoeAIt52fswKhFvg6ep1i4iqLGGu`, the AI warning picture
`https://absbyai.com/ad-assets/ai_warning_heavier.png`, real app screens (trainer assessment
`1wFsyT9eKeUVzDcF0L7bbAPn5DSAVdRIs`, workout day `11AS0LYjs-LfUPuhhVqGdAtiN1sjkJ02j`), reference-ad folder
`10veL4yDYVaaDh1q_2VKJObfa-YpGEW_A`, benefit/dad AI clips folder `1bO1mZAk0ii9c-m45-YhSYmuYq_qPIpvm`. If an ad
needs an asset that exists nowhere (e.g. Ad 9's bad-AI attempt image if he did not build one), give DIRECTIONS
for it as "stock footage or an AI clip / AI image, with the label" — do not invent a link.
