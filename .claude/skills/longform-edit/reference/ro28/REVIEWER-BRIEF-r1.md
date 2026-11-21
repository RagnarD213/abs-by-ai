# Independent check of the RO-28 round 1 review page (before Dan sees it)

You are a fresh, skeptical reviewer. You did not build this. Expect to find problems; report every one with its item ID and time.
Do not fix anything. Write `review/INDEPENDENT-CHECK.md` (findings, most severe first) and `review/INDEPENDENT-CHECK.json`
(`{"findings": [{"id", "t", "severity": "fix|note", "what", "evidence"}], "summary": "<two sentences, plain language>"}`).
Read `/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/VIDEO-RULES.md` first (the head and hair
clearance rule at the top, junk footage, stumbles, B-roll colour, AI clip sense rules, graphics rules, no belly framing).

## What exists (work dir `/Volumes/Expansion/_edit_work/ro28/round1/`)
- Video: "Why Zepbound Improves Your Health Even If You're Ripped" (organic long-form, 16:9), Dan Rose on a studio set (dark green
  backdrop, two cyan tubes, a desk) reading a script, cut from one roll (C1771). Organic: Dan may SAY Zepbound; on-screen graphics
  keep brand names out. Claims Dan says from the script are pre-approved; graphics must only print numbers he says.
- `review/first-minute/DRAFT - RO-28 round 1 - first minute.mp4` (1080p). The AI slots A1 (0:00 to 0:04) and A2 (about 0:39 to 0:45)
  show Dan on camera on purpose: AI motion is not generated yet. Its 540p copy sits beside it.
- `review/stills/<ID>.jpg` and `review/stills.json` (copy, times, speech before / during / after per item).
- `review/context/<ID>-context - REVIEW 540p.mp4`: each item moving with about 3 s of speech either side (the source blocks are
  `review/blocks/*.mp4`, 1080p).
- `review/aiframes/<ID>-start.png / -end.png` for A1, A2, A3, A5, A6, A7, A8 (their action and line: `recipe/page_extra.py`, `AI` list).
- `review/options/colour-A/B/C*` (colour options), `options/voice/*.mp3` (voice options), `review/index.html` (the page).
- `plan_resolved.json`, `words_out.json` (every word on the film timeline), `recipe/plan.py` (notes per item), `edl.json` (takes).
- The script Dan read: `script/shootdoc.txt`, section "FILMING SCRIPT: Why Zepbound Improves Your Health Even If You're Ripped".

## Check, item by item (cite the item ID)
1. **Graphics copy:** spelling, title case, the numbers match what Dan says under it (read `during`), no brand names (Zepbound,
   Mounjaro, Ozempic) on screen, a graphic distills the point rather than repeating words, nothing over his face. Each part lands on
   its word; a lower third stays readable long enough after its last part lands. Fact cards: the number counts up on the word, the
   photo shows something relevant and is not the same scene as a nearby clip.
2. **Clips and photos:** each shows the thing Dan names (open the context clip, not just the still). Readable brand names or logos,
   text burned into stock, a person just looking at a phone, a freeze at a clip's end, black bars, a clip visibly darker or off-colour
   next to the presenter shots, the same stock scene twice, a Dan cutaway that is him just standing (must be an exercise), his hair
   cut by a crop in his pool B-roll. AI library clips carry AI-GENERATED. No belly close-up or fat pinching, above all in the first 30 s.
3. **AI frame pairs (A1, A2, A3, A5, A6, A7, A8), three questions each:** cause and effect between START and END; with the sound off
   would a stranger say what it shows; does it show the line Dan says under it (and does the joke land). Hands, faces, fingers, text.
4. **First minute:** every join frame by frame and moving: jump cuts (same framing either side with a pose jump), presenter flashes
   under 0.5 s between cutaways, hair: Dan's hair must have slight visible room at the top in BOTH the wide and tight shots on every
   frame (look at native-scale frames at the tightest moments, not a contact sheet), audio pops, clipped first or last syllables,
   stumbles or half-started words inside a kept line, sync.
5. **Options section:** the three colour options and four voice options are what the page says (same moment, level matched).
6. **Anything a viewer or Dan would call sloppy.** Be concrete.

Report counts: items checked vs items in `plan_resolved.json`; AI pairs checked; joins in the first minute checked.
Never use an em dash or en dash in what you write.
