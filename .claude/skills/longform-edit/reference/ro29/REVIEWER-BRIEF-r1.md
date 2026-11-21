# Independent check of the RO-29 round 1 review page (before Dan sees it)

You are a fresh, skeptical reviewer. You did not build this. Expect to find problems; report every one with its item ID and time.
Do not fix anything. Write `review/INDEPENDENT-CHECK.md` (findings, most severe first) and `review/INDEPENDENT-CHECK.json`
(`{"findings": [{"id", "t", "severity": "fix|note", "what", "evidence"}], "summary": "<two sentences, plain language>"}`).
Read `/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/VIDEO-RULES.md` first (the head and hair
clearance rule at the top, junk footage, stumbles, B-roll colour, AI clip sense rules, graphics rules, no belly framing).
Run heavy work (ffmpeg decodes of many frames, ASR) through the render queue:
`python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py" run --group RO-29 --label "RO-29 independent check" -- <cmd>`.
ffmpeg/ffprobe: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/`. Never play audio out loud.

## What exists (work dir `/Volumes/Expansion/_edit_work/RO-29/round1/`)
- Video: "Cortisol Belly Is Real, But TikTok Has It Wrong" (organic long-form, 16:9), Dan Rose on a studio set (dark green
  backdrop, two cyan tubes, a desk) reading a script, cut from roll C1772 with the recap and close from retake roll C1773.
  Organic: Dan may SAY Zepbound; on-screen graphics keep brand names out ("Appetite Medication"). Claims Dan says from the script
  are pre-approved; graphics must only print numbers he says.
- `review/first-minute/DRAFT - RO-29 round 1 - first minute.mp4` (1080p) and its 540p copy. The AI slots A1 (0:00 to about 0:07)
  and A2 (about 0:48 to 0:55) show Dan on camera on purpose: AI motion is not generated yet.
- `review/stills/<ID>.jpg` and `review/stills.json` (copy, times, speech before / during / after per item).
- `review/context/<ID>-context - REVIEW 540p.mp4`: each item moving with about 3 s of speech either side (source blocks `review/blocks/*.mp4`).
- `aiframes/<ID>-start.png / -end.png` for A1 to A7 (their action and line: `recipe/page_extra.py`, `AI` list; each already passed
  the frame gate and a frame reviewer, but judge them yourself on the three questions below).
- `review/options/colour-A/B/C*` (colour options), `options/voice/*.mp3` (five voice options), `review/index.html` (the page).
- `plan_resolved.json`, `words_out.json` (every word on the film timeline), `recipe/plan.py` (notes per item), `edl.json` (takes).
- The script Dan read: `script/cortisol.txt`.

## Check, item by item (cite the item ID)
1. **Graphics copy:** spelling, title case, eyebrows (the small line above) in CAPITALS, numbers match what Dan says under it (read
   `during`), no brand names on screen, a graphic distills the point rather than repeating words, nothing over his face. Each part
   lands on its word; a lower third stays readable at least 1.5 s after its last part lands. Fact cards: the number counts up on the
   word and stays readable after; the photo is relevant and not the same scene as a nearby clip.
2. **Clips and photos:** each shows the thing Dan names (open the context clip, not just the still). Readable brand names or logos,
   text burned into stock, a person just looking at a phone, a freeze at a clip's end, black bars, a clip visibly darker or off-colour
   next to the presenter shots, the same stock scene twice, a Dan cutaway that is him just standing (must be an exercise), his hair
   cut by a crop in his pool B-roll. AI library clips carry AI-GENERATED. The TikTok phone cards (P01, P02): the drink is visible,
   the creator's own on-screen text is not mistaken for ours. No belly close-up or fat pinching, above all in the first 30 s.
3. **AI frame pairs (A1 to A7), three questions each:** cause and effect between START and END; with the sound off would a stranger
   say what it shows; does it show the line Dan says under it (and does the joke land). Hands, faces, fingers, text. For A6 (lip
   sync of Dan's excuse voice "I can't divorce my wife just because she stresses me out"): does the slot start on the excuse words,
   not on Dan's own narration?
4. **First minute:** every join frame by frame and moving: jump cuts (same framing either side with a pose jump), presenter flashes
   under 0.5 s between cutaways, hair: Dan's hair must have slight visible room at the top in BOTH wide and tight shots on every
   frame (native-scale frames at the tightest moments), audio pops, clipped first or last syllables, stumbles or half-started words
   inside a kept line, sync.
5. **Whole-film speech:** read `words_out.json` end to end against the script for stumbles, repeated phrases or half words left in
   (one "now I know a lot" restart near 3:39 was already cut; confirm), and missing script lines.
6. **Options section:** the three colour options and five voice options are what the page says (same moment, level matched).
7. **Anything a viewer or Dan would call sloppy.** Be concrete.

Report counts: items checked vs items in `plan_resolved.json`; AI pairs checked; joins in the first minute checked.
Never use an em dash or en dash in what you write.
