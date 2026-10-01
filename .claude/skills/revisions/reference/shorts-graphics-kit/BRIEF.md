# Reviewer brief: Muhammad, dedicated SHORTS delivered 2026-09-30 / 10-01

You are writing ONE revision document section for Dan Rose (Abs By AI) in Dan's own voice, per the `/revisions`
skill: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/revisions/SKILL.md`. READ THAT FILE
FIRST, in full. The calibration passes (rules 1-48, ESPECIALLY pass 7, rules 44-48, which was written on this same
editor's first shorts) and the standing rules are the spec. Then read
`.claude/skills/_shared/CUT-CONTINUITY-QC.md` (same repo) and the "Short-form footage fills the vertical frame",
"Hair never leaves the frame", "On-screen text graphics are KEY POINTS", "Label Dan's real pictures" and "Lock the
graphic style before editing" sections of `.claude/skills/_shared/VIDEO-RULES.md`.

The doc goes to the editor as written; Dan's goal is to change nothing. Write as Dan, first person ("I"). Never
mention Claude, a review, a gate, a script or tool as an actor. American spelling. **NO EM DASHES and no en dashes
anywhere** (rewrite with a comma, colon, parentheses or two sentences; a hyphen in a compound or a range like
"0:10 - 0:14" is fine). Never name another editor (no "Zeeshan", "Waleed"; say "my other videos"). Never write
anything about Dan's swearing. No compliance / legal / policy commentary beyond the standing rules below.

## What these videos are
ORGANIC dedicated Shorts (vertical 1080x1920, 45-66 s), filmed 8/28 as shorts, edited by Muhammad Arsalan from raw
footage. They are NOT ads, so:
- Calibration rule 48 applies: where the script cues before and after pictures "full frame, sequential", there is NO
  before/after adjacency item. A picture beat of Dan gets "images below" with empty sub-bullets for Dan to fill; do
  not pick his photos for him.
- Drug names: organic videos MAY say and caption "Zepbound". Never write an item about the spoken or captioned word.
  If an on-screen GRAPHIC (chip, title bar) shows the brand name, do not write a doc item; put one line in the
  summary under "For Dan's call".
- Labels still apply: AI-GENERATED on every AI image or AI clip for its full duration; "Real picture of me, not
  AI-generated" on real physique photos of Dan (never on moving footage). No label over a face or abs.

## Where this editor stands (read before writing)
- Dan's live doc for the previous shorts round, exactly as he sent it (he edited ours):
  `/Volumes/Extreme/_edit_work/revisions-20261001/muhammad/doc_0929_live.txt` (DS-05 and DS-06, V1). Our copies:
  `docs/our_md_0929.md`, `docs/our_md_0926.md`; the 9-26 live doc: `doc_0926_live.txt`. MATCH THE REGISTER AND FORMAT
  of doc_0929_live.txt / our_md_0929.md. What Dan changed in the 9-29 doc: (a) a bodybuilder picture became "Use a
  picture of a man with a lean, ripped, natural looking physique similar to Kinobody" instead of "take the picture
  out"; (b) he replaced two "show me start and end frames for a new AI clip" items with ONE existing clip he
  already had ("Insert this clip here" + link + "accelerate footage to fit duration"). Lesson: before directing a
  new AI clip, look for an existing clip (see Clip library below) and link it; a wrong picture gets a better
  picture, not removal.
- The standing asks he has already been given on shorts (so on a FIRST cut of a new video, check whether he applied
  them unprompted, and credit it if he did): audio at -14 LUFS with limiter at -1 dBTP and not over-compressed;
  framing cropped in tight (bottom of frame around mid-thigh, small space above the hair, never full body with
  shoes in frame; the "Getting Abs" short is the framing and color reference:
  `/Volumes/Extreme/_edit_work/revisions-20260926/dl/getting_abs.mp4`); wide / tight alternation at every cut
  between takes (no same-framing jump cuts); pictures and clips fill the whole vertical screen, not a small card on
  a dark background; no empty screens; AI clips shown as start and end frames first; key points as
  "KEY POINT: ..." top graphic over camera scene, not full-screen cards.
- GRAPHIC STYLE IS NOT LOCKED YET for shorts (the four top-graphic variations asked for on Getting Abs have not been
  delivered or picked, as far as the record shows). So per rule 46: NO cosmetic items about his title bar or chip
  styling; any item that ADDS or changes a graphic ends with the sub-bullet "Wait until the graphic style is locked
  before making this." If his graphics in this cut look like a NEW style compared with the 9-29 cuts (compare
  against `/Volumes/Extreme/_edit_work/revisions-20260929/work/ds05/sheets/`), say so in the summary.
  Wrong WORDS in a graphic or caption (typo, wrong word vs the script) are still items.

## Your video
`NAME` and round are given in your task prompt. Paths (W = `/Volumes/Extreme/_edit_work/revisions-20261001/muhammad`):
- Video: `W/dl/<NAME>.mp4`. Script: `W/docs/script_<dsNN>.txt` (bracketed cues are the picture plan; read every one).
- Prep already done in `W/work/<NAME>/`: `pick_lav.txt`, `audio_gate.txt` (rows vs his Ad 1 reference; ignore the
  "do no harm NOT MEASURED" row, it cannot be measured on an editor's file), `ebur.txt` (integrated LUFS / true
  peak at the end), `silence.txt` (silencedetect -40 dB, 0.3 s), `scenes.txt`, `luma.txt`,
  `sheets/sheet_NN.jpg` (2 fps contact sheets, 8x6 tiles with yellow timecodes; LOOK AT EVERY SHEET),
  `cut16k.json` (Whisper small, word timestamps), `framing.txt` + `framing_sheet.jpg` (per-shot looseness),
  `gateframing.txt` / `gateframing.json` (hair-top pixels; lesson 57: quote these, never framing.py alone),
  and for round 2 cuts `framediff.txt` (old vs new mean luma difference per second; a MAP of where he worked, never
  proof by itself, lesson 45).
- Round 2 only: the previous cut is `/Volumes/Extreme/_edit_work/revisions-20260929/dl/ds05.mp4` or `ds06.mp4`, prep
  in `/Volumes/Extreme/_edit_work/revisions-20260929/work/ds05|ds06/`. Your checklist is that video's section in
  `doc_0929_live.txt`. Score every item DONE / PARTLY / NOT DONE on full-resolution frames, open by crediting what
  landed, then list only what is still wrong plus anything the changes introduced. Round 2 audio is an item only if
  the level is outside -14 +/-1 LUFS, or true peak >= 0 with clipping, or the mic/room is wrong (rule 22). If
  nothing is left, the section is the H2 plus a bold `FINALIZED - APPROVED - NEEDS HQ EXPORT FOR UPLOAD` line plus a
  credit paragraph (Dan sets the final wording; state bitrate and size in the summary).
- ffmpeg / ffprobe: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg` (not on
  PATH). Full-res frame: `ffmpeg -v error -ss <sec> -i <video> -frames:v 1 -q:v 2 out.jpg`. Strips of consecutive
  frames: `-ss <t> -t 0.5 -vf "scale=360:-1,tile=8x2"`. Put your scratch files in `W/work/<NAME>/scratch/`.
  Short extractions only: NO whisper, NO full-length encodes (the machine is capped at two builds).

## What to check, in this order
1. Audio (round 1: level, peaks, compression "not crushed" row, one mic, room; quote numbers in editor words with the
   audio STANDING RULE; if it already lands at -14 +/-1 with peaks under 0 and is not crushed, credit it, no item).
2. Script match: every line present, no leftover words from another take, no dead air over 0.3 s; burned caption
   words transcribed at full resolution against the script (wrong words are items with the exact fix).
3. Framing of every camera shot against the reference short (crop-in item with a number if loose; hair never out of
   the top of frame; quote gateframing hair-top numbers).
4. Every cut between takes: same-framing presenter jump = item with the timecodes; inspect native consecutive frames
   at each join (CUT-CONTINUITY-QC), not the 2 fps sheet. Junk (stray words, lip smacks you can see in the
   transcript, long pauses) = item.
5. Every script cue: is the right picture / clip on the right line, does it fill the vertical screen, does it exit
   on time, is it labeled correctly, is the casting right (successful prospect = white or Asian man 30-50, lean with
   abs, not a bodybuilder; before = American average with a small belly), no repeated stock clip, no empty screens.
   A script cue the footage for which "DOES NOT EXIST / needs filming" was the editor's to fill with stock or AI:
   judge what he used.
6. Every AI shot: the step 3b artifact pass at full resolution with the false-positive protocol. AI clips he shows
   as start/end-frame placeholders: judge the frames and either approve them in the doc ("the start and end frames
   are good, go ahead and generate it") or say what to change; list in the summary which you approved on Dan's
   behalf so he can overrule.
7. Text graphics: transcribe every chip; echo of the spoken words = replace with a "KEY POINT: ..." (Title
   Capitalization, punch words in FULL CAPS), about two added key points per video at most, each a benefit or the
   most memorable line; plus the wait-for-lock sub-bullet.
8. AI opener (rule 44): consider it; propose three concepts only when the on-camera cold open is weak or the script
   cues a picture open. The script's own "[COLD OPEN ... tight on Dan]" cue means a strong on-camera open can stay.
9. AbsByAI.com mark where the script cues it. End: item only if picture or sound cuts before the last word ends.
10. Color against Getting Abs (blacks, flatness): item only if clearly washed out or off, measured on matched frames.

## Clip library and assets (link existing assets; never invent a link)
- Search first: `cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI" && python3 .claude/skills/_shared/cliplib/clip_library.py find "<what the beat needs>" --aspect 9x16` (also try without --aspect, and `--rolls`).
  Previews: `Media/clip-library/contact/<ID>.jpg`. If a library clip fits and the hit lists a Drive link or id, link
  it. If it only exists locally, do NOT upload anything yourself: name the local path and clip ID in the SUMMARY
  under "Assets to upload" and write the doc item with the placeholder text `[LINK: <clip ID>]` on its own
  sub-bullet; the lead session will upload and fill the link.
- Already on Drive: dating app clip (used in DS-05) `1g9wt3_MuggGK5DPVZhst_CgTBMQzqG9L`; Dan's 200 lb before picture
  `11Qb559-mqga9FznIpC8tgxLLfz1BUKQX`; goal image `1-8QAfoeAIt52fswKhFvg6ep1i4iqLGGu` (AI); real app screen
  recording of a generation `1fwRGtoHh4oTlwfQZ0gItY3Oj7DZPkN6P` (use 0:03 - 0:26, cut before its side by side
  ending; the man in it is not Dan); real app screens: trainer assessment `1wFsyT9eKeUVzDcF0L7bbAPn5DSAVdRIs`,
  workout day `11AS0LYjs-LfUPuhhVqGdAtiN1sjkJ02j`; reference-ad folder `10veL4yDYVaaDh1q_2VKJObfa-YpGEW_A`; "AI clips
  for Muhammad" folder `1bO1mZAk0ii9c-m45-YhSYmuYq_qPIpvm`. Exercise demos: `https://absbyai.com/exercise-demos/<id>.mp4`.
  Never direct or show the app's stick-figure exercise animations.
- A new clip is always "stock footage or an AI clip"; if AI: "show me the start and end frames first, in vertical
  9:16, I pick before you generate" + AI-GENERATED label.

## Output (write exactly these two files)
1. `W/out/<NAME>.md`: the doc section, same dialect as `docs/our_md_0929.md`: `## ` H2 = the video title in caps
   plus his file version, e.g. `## WHY HAVING ABS BEATS BEING A FAT MILLIONAIRE - V2` or
   `## TOP 3 WAYS TO USE AI TO GET ABS - V1`; a credit paragraph; `**\*\*THROUGHOUT VIDEO\*\***` with
   `- **HEADER**` bullets and 4-space nested sub-bullets; `**\*\*TIMESTAMPED REVISIONS\*\***` in play order; links as
   bare URLs `https://drive.google.com/file/d/<id>/view`. Every item: one diagnostic sentence, the action in
   **bold**, the timing; canonical STANDING RULE lines verbatim as the last sub-bullet where a standing rule is
   broken. Items self-contained, no cross-references, no counts. Then run the skill's step 7 self-check and delete
   whatever fails it. Check the file for em dashes and en dashes and make the count 0.
2. `W/out/<NAME>.summary.md`: 8-15 lines for the lead: file facts (duration, bitrate, LUFS / true peak), for round 2
   the DONE / PARTLY / NOT DONE scorecard, the three biggest findings with numbers, item count, "AI CLIPS FLAGGED,
   watch before forwarding" block (CONFIRMED / POSSIBLE per shot, or "none"), frames you approved on Dan's behalf,
   "Assets to upload" (if any), "For Dan's call" (things kept out of the doc), and two or three sentences in Dan's
   voice the lead can fold into ONE combined message to Muhammad (specific praise first, then the one or two things
   that matter most). No em dashes.
Final message back: both paths, the item count, the three biggest findings, and anything you could not verify.
