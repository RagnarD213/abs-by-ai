# Independent check of the RO-15 round 1 review page (before Dan sees it)

You are a fresh, skeptical reviewer. You did not build this. Expect to find problems; report every one with its item ID and time.
Do not fix anything. Write `review/INDEPENDENT-CHECK.md` (findings, most severe first) and `review/INDEPENDENT-CHECK.json`
(`{"findings": [{"id", "t", "severity": "fix|note", "what", "evidence"}], "summary": "<two sentences, plain language>"}`).
Read `/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/VIDEO-RULES.md` first (the head and hair
clearance rule, junk footage, stumbles, B-roll colour, AI clip sense rules, graphics rules, no belly framing).
Run heavy work (ffmpeg decodes of many frames, ASR) through the render queue:
`python3 "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/renderq/renderq.py" run --group RO-15 --label "RO-15 independent check" -- <cmd>`.
ffmpeg/ffprobe: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/`. Never play audio out loud.

## What exists (work dir `/Volumes/Extreme/_edit_work/RO-15/round1/`)
- Video: "Sleep Better With Glycine" (organic long-form, 16:9, about 5:23), Dan Rose on the 9/23 studio set (green mottled backdrop,
  a light tube on the left, a plant and a bulb on the right) reading a script, cut from one roll, C1709. Claims Dan says from the
  script are pre-approved; graphics must only print numbers he says.
- `review/first-minute/DRAFT - RO-15 round 1 - first minute.mp4` (1080p, the only review copy by rule). AI slots (A1 to A8) show Dan
  on camera on purpose: AI motion is not generated yet.
- `review/stills/<ID>.jpg` and `review/stills.json` (copy, times, speech before / during / after per item).
- `review/context/<ID>-context.mp4`: each item moving with about 3 s of speech either side (AI slots show the X1 start frame as a
  labelled placeholder).
- `review/aiframes/<ID>/X1.jpg` (and X2.jpg): blind AI start frames for A1 to A8 (A6 has only X1). END frames do not exist yet, by design.
  Their action and line: `recipe/page_extra.py`, `AI` list. A frame reviewer already checked them (`aiframes/start-frames-review.md`).
  Never try to work out which model made which.
- `review/options/colour-*` (three colour options), `options/voice/*.mp3` (five voice options, ranked blind), `review/index.html` (the page).
- `plan_resolved.json`, `words_out.json` (every word on the film timeline), `recipe/plan.py` (notes per item), `edl.json` (takes),
  `listen/listen_*.txt` (a verbatim listen of the whole roll marking every restart).
- The script Dan read: `script/glycine.txt`.

## Check, item by item (cite the item ID)
1. **Graphics copy:** spelling, title case, eyebrows (the small line above) in CAPITALS, numbers match what Dan says under it (read
   `during`), a graphic distills the point rather than repeating words, nothing over his face. Each part
   lands on its word; a lower third stays readable at least 1.5 s after its last part lands.
2. **Clips and photos:** each shows the thing Dan names (open the context clip, not just the still). Readable brand names or logos,
   text burned into stock, a person just looking at a phone, a freeze at a clip's end, black bars, a clip visibly darker or off-colour
   next to the presenter shots , the same stock scene twice, a Dan cutaway that is him just standing. No belly close-up or fat pinching, above all in the first 30 s.
   C01 is Dan's own supplement stack (library B0002); P01 is the real app's AI Supplement Audit in a phone beside Dan: no before/after
   screen, no email-capture screen.
3. **AI start frames (A1 to A8):** with the sound off would a stranger say what it shows; does it show the line Dan says under it (and
   does the joke land); is the described action sensible from this frame; no belly framing.
4. **First minute:** every join frame by frame and moving: jump cuts (same framing either side with a pose jump), presenter flashes
   under 0.5 s between cutaways, hair: slight visible room at the top in BOTH wide and tight shots on every frame (native-scale frames at
   the tightest moments), audio pops, clipped first or last syllables, stumbles or half-started words inside a kept line, sync.
5. **Whole-film speech:** read `words_out.json` end to end against the script for stumbles, repeated phrases or half words left in
   (restarts "So wh-", "Now I want you to keep this", "If you rarely", "and now I'm usually in the se-", "I've found that factors" x2,
   "Once you have the major thing-", "But if your numbers go up, you've-" were cut; confirm none is left), and missing script lines.
   Dan's ad-lib "or if you just have a thick build like I do" is kept on purpose (it is a decision on the page).
6. **Options section:** the three colour options and five voice options are what the page says (same moment, level matched).
7. **Side cards (L01 to L05)**: open each context clip and say whether Dan's arms or hands ever touch or pass under the card, and whether
   each card edge sits on a picture cut (a card that starts or ends mid-shot over the same framing is a jump cut).
8. **Anything a viewer or Dan would call sloppy.** Be concrete.

Report counts: items checked vs items in `plan_resolved.json`; AI frames checked; joins in the first minute checked.
Never use an em dash or en dash in what you write.
