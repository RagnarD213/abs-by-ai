# RO-19 plan-writer brief (one part of a 19 minute film)

Film: "My First Spray Tan", Dan Rose talking to camera in his kitchen doorway five days after his first professional spray tan, long-form YouTube CONTENT (not an ad). He explains why a tan makes you look more defined in photos, what the appointment and aftercare are like, how long it lasts, the pros and cons, who should and should not get one, and how to get the most from it with a photo shoot. The cut is locked. You write the VISUAL PLAN for one stretch of it: lower thirds and cutaway clips, anchored to the words he says. You do not render anything.

## Read first (in this order)
1. `/Volumes/Extreme/_edit_work/ro19/recipe/plan_parts/p00_open.py`: the opening section, written by the lead editor. Your part must match its style and field usage exactly.
2. `/Volumes/Extreme/_edit_work/ro19/recipe/plan.py` (the loader: helper names `stock()`, `br()`, `DAN`, `OTHER`, `NONE`, `AIL` are injected into your file; do not import anything).
3. Your stretch of `/Volumes/Extreme/_edit_work/ro19/cut_transcript.md` (the kept words with film times), (there is no picture_cues file for this film: read your stretch closely and picture each sentence yourself).
4. `/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/VIDEO-RULES.md`: only these sections: "A cutaway shows the thing he is naming", "Capital letters in graphics", "No fat pinching or belly close-ups", "Clip library first", "No repeated stock clip within one video" (in "Video editing feedback"), "On-screen text graphics are KEY POINTS", "Jump rope footage", "A hard-to-picture idea gets a funny AI clip". Use Grep to jump to them; do not read the whole file.

## What to write
One file: `/Volumes/Extreme/_edit_work/ro19/recipe/plan_parts/<your file name>` defining `PART = [ ... ]` in film order, plus a comment block at the top. IDs: lower thirds `G<letter>NN`, clips `C<letter>NN`, with YOUR letter (given in your task), numbered from 01.

### Lower thirds (`kind="lt"`)
`dict(id, kind="lt", start="<first words>", end="<last words>", tail=<s, optional>, topic="UPPERCASE TOPIC", point="Title Case Point.", parts=[["text", "phrase he says"], ...])`
- `start` / `end` are short phrases copied EXACTLY from the cut transcript (4 to 7 words, unique after the previous item). The graphic is on screen from the start phrase's first word to the end phrase's last word plus `tail` (default 0.25 s). Keep each on screen 4 to 10 s.
- `parts` split the point into 1 to 4 pieces IN THE ORDER HE SAYS THEM; each piece appears on the first word of its phrase. Joined, the pieces must spell the point exactly.
- The point DISTILLS what he is saying into one useful line a skimming viewer keeps. It never just repeats his sentence. One line: at most about 46 characters including spaces (the checker tells you if it does not fit).
- Title Case. A FULL CAPS word is rare: at most one lower third in six, only where one word truly carries the punch. Numbers, product names, section labels never take caps.
- `topic` is a 1 to 4 word label: `KEY POINT`, a section label (`AFTERCARE`, `THE FIRST SHOWER`, `CON 1: THE COST`, `WHO SHOULD TAN: 1`), or the subject (`TANNING AT HOME`). Number list items the way he numbers them; check the count against the whole transcript before writing "OF N".
- Every numbered item, every section change and every real takeaway gets one. Aim for one about every 20 to 30 s, and never two at once (leave 0.3 s between them). No lower third while a number he has not said would be implied: prices and percentages on screen must be the ones he says.
- Never write a claim he does not make. No drug brand names in ON-SCREEN text (say "GLP-1" or "weight loss medication"; his spoken words are untouched). No "AbsByAI.com" graphic. No em dashes anywhere, in copy or comments.

### Clips (`kind="clip"`, full-frame cutaway, hard cuts, his voice runs underneath)
`dict(id, kind="clip", start=..., end=..., tail=0.1, src=["B0123@2.0"] or [stock("pexels-<id>-<slug>.mp4", 1.5)], people-fields, note="what it shows, where it is from")`
- people-fields: `**OTHER` (strangers), `**NONE` (no people), `**DAN` (real moving footage of Dan). An AI library clip (ID starting with A) also takes `**AIL`.
- 3 to 9 s each. A clip must be at least as long as its slot from its start offset (the checker pre-flights it): never slow, loop or hold a clip. Two or three short sources in one item are allowed (`src=[a, b]`, the slot is split evenly).
- Pick what he is NAMING in that sentence: the object, the place, the situation. When he tells a little story (standing in his briefs in front of the tanning specialist, the brown water in the first shower, the pool he gave up for the weekend), show that scene, not a stock synonym for one word.
- Order of preference: (1) Dan's own footage in the library, (2) other library clips, (3) Pexels, (4) nothing: leave him on camera with a lower third. Do NOT invent new AI clips; see "AI ideas" below.
- Library: `python3 /Volumes/Extreme/_edit_work/ro19/recipe/clipfind.py "words; more words" 6 --169` (OR search; `;` separates queries). Then LOOK at the preview `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/clip-library/contact/<ID>.jpg` (Read tool) before using any clip: descriptions are sometimes wrong, some clips carry burned-in text or graphics from an older video (reject those), some show a stranger's bare stomach (reject). 16:9 clips only. Start offsets come from what you see on the contact sheet.
- Pexels: `/Volumes/Extreme/_edit_work/ro19/stock/pexels_index.md` lists 10 landscape results for each of 70 search terms (Pexels has NO footage of an actual spray tan being applied: do not go looking for it; sunscreen and sunbathing clips are not a spray tan) as `<id> <slug>`. Choose by slug, download with `curl -sS -L -A "Mozilla/5.0" -o "/Volumes/Extreme/_edit_work/ro19/stock/pexels-<id>-<slug>.mp4" "https://www.pexels.com/download/video/<id>/"`, then make a contact sheet (`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg -nostdin -v error -y -i FILE -vf "fps=1/2,scale=480:-2,tile=6x1" -frames:v 1 SHEET.jpg`, sheets go in `stock/sheets/`) and LOOK at it. Keep only clips you use; delete rejected downloads. If the index has nothing for a beat, leave him on camera and list the beat under "NEEDS A PICTURE" in your comment block. Do not use any other stock site or web image.
- Never the same source twice, and never two clips that look like the same scene or the same actors. No watermarks, no visible brand logos as the subject, no on-screen text in a foreign language. First 30 s rule does not apply to you, but the belly rule does: no shot built around a stomach, no hands on a belly; heavier people are shown whole, clothed, doing something.
- Skip a clip where he is making an eye-contact point or showing his own tan on camera ("as you can see", "if you look at me", "if you were to zoom in here"): the viewer must see HIM there. Aim for cutaways over roughly 30 to 40 % of your stretch, spread out, and no stretch longer than 25 s with neither a clip nor a lower third.
- A lower third may run over a clip, but its text must still make sense over that picture.

### The comment block at the top of your file
`# NEEDS A PICTURE:` beats where a specific picture would help but nothing fit (a product he names, his own gym, his mattress, an app screen), with film time and his words.
`# AI IDEAS:` at most ONE idea for a NEW AI clip in your stretch, one line: film time, his words, the scene. The lead editor already has frames for four and places them himself, so do NOT put any clip on these lines and do not propose them again: (A4) the spray tan appointment itself, in the stretch that starts "let's talk about what the experience is like"; (A3) "you're going to destroy your sheets"; (A2) "You don't need to go full Donald Trump color"; (A1) "Number one, vampires". Leave those sentences free of clips (a lower third is fine).
`# SPECIAL:` anything that needs the lead editor. Already his, leave them free of clips and lower thirds: the before / after photo pairs (the stretch that starts "so on screen right now, I'm going to show you a few pictures" through "investing $50 to $100"), and the closing call to action from "go to absbyai.com" to the end. Real photos of Dan from his pool photo shoot are also the lead editor's: if a line would be best served by one of his real photos, list it under NEEDS A PICTURE.

## Film-specific rules
- Dan's own skin is the subject. Never cover a line where he points at his tan or asks the viewer to judge it.
- People in stock: adults, clothed or in ordinary swimwear, shown whole. No close shots of a stranger's body, no sunburn close-ups of skin damage that would read as medical imagery, nothing that looks like surgery or a medical procedure.
- He names Bryan Johnson (the ASR writes "Brian"): no clip of him and no image of him; a lower third may carry the point without his name, or name him as "Bryan Johnson". He says "Donald Trump color": that sentence is the lead editor's (A2); do not picture any real person.
- He names Claude, ChatGPT and Gemini: a generic phone or laptop chat clip is fine; do not show a competitor's logo as the subject.
- Money he says on screen must be the numbers he says ($80 base, $20 contouring, about $100, about $50 without contouring, $50 to $100 per tan).
- GLP-1 and TRT may be written as he says them (generic terms). No brand names.

## Check your work (required, repeat until clean)
`cd /Volumes/Extreme/_edit_work/ro19 && python3 recipe/resolve_part.py recipe/plan_parts/<your file> <T0> <T1>` must end with `ERRORS: 0`. Read its whole printout: every item's time and length, the cover percentage, the gaps list, the caps count.
Then the copy-fit check: `python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes/from_plan.py" --plan recipe/plan_parts/_resolved_<your file without .py>.json --words words_out.json --shots shots.json --out hf_check/<your letter>` (a dry run: it writes configs only, never pass `--render`). An assertion error names the lower third whose point is too long: shorten it.

## Rules of the road
Write only your part file, your `_resolved_` file, `hf_check/<letter>/`, and stock downloads plus sheets. Touch nothing else in the work dir and nothing in the project repo. No video rendering, no Whisper, no AI generation, no git. Python 3.9; ffmpeg is not on PATH (use the full path above). Keep your final message under 250 words: counts (lower thirds, clips by source type), cover %, the NEEDS A PICTURE and AI IDEAS lists, and anything you could not resolve.

## No source twice across the film (three plan writers work at the same time)
Before you use any Pexels id or library clip id, read every `/Volumes/Extreme/_edit_work/ro19/stock/claims_*.txt` and skip anything listed there. The moment you decide to use one, append its id (the Pexels number, or the library id such as B0192) as one line to `/Volumes/Extreme/_edit_work/ro19/stock/claims_<your letter>.txt`. If you drop it later, remove the line. Check the claims files once more just before you finish.

## Lead editor items inside your stretch
Your task message lists film time ranges that belong to the lead editor. Put no clip and no lower third that overlaps those ranges (leave 0.3 s either side). `resolve_part.py` does not know about them, so check your printout against them yourself.
