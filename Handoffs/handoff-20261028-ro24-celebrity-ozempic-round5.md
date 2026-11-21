**LFC.** Task name: `Celebrity Ozempic LFC R5`. Model: **Claude Opus 5.5, high** (the video started on Claude; Dan's 10-20 rule).

# RO-24 "Reacting To Celebrity Ozempic Transformations": round 5 handoff (written 2026-10-28, round 4 delivered)

## First
- The work drive **Expansion** (`/Volumes/Expansion/_edit_work/RO-24/`) was NOT mounted when this was written. Check it is mounted
  before anything else; if not, tell Dan in one line to plug it in and stop (no production without it).
- Then: `python3 .claude/skills/_shared/editcap/editcap.py acquire RO-24 --title "Celebrity Ozempic LFC R5" --type LFC`.
- Copy Dan's decisions below into `round5/DAN-DECISIONS.md` and his two screenshots from `Handoffs/assets/ro24-r5/` into
  `round5/dan-screenshots/`.

## Read first
`.claude/skills/longform-edit/reference/ro24/round4/README.md` (the round 4 recipe, order and every trap from five independent
reviews), `.claude/skills/_shared/VIDEO-RULES.md` (AI clips sections, green-screen template, drug-name graphics rule updated
2026-10-28), `.claude/skills/_shared/greenscreen-bg/README.md`, `.claude/skills/_shared/framecheck/README.md`,
`.claude/skills/_shared/veo/README.md` and the `flow-veo` agent.

## Dan's reply to round 4 (2026-10-28, verbatim, Wispr)
> Okay, clips A1 through A6 look good. Generate all these.
>
> For A7, I need new start and end frames. I want the guy in the red shirt jumping off on the left side in the foreground, rather
> than on the ramp behind. That doesn't really make sense because it wouldn't be any worse than walking down the stairs, and he
> would land smoothly. I want him to jump so that he jumps the full distance to the bottom, rather than landing on the ramped hill.
>
> A looks good. You can generate that one as is.
>
> Okay, revisions to the video. When I say Amy Schumer later posted a picture with her abs, try to find that picture and include it
> in the video if you can find it.
>
> For the full-screen graphic at 4:02, the newer shot 1, this one in the screenshot here, change it to "Zepbound beats Ozempic in
> studies," and then change the graph labels to Zepbound and Ozempic.
>
> I want to eliminate the rule that we have to not mention weight loss drug names and graphics, because the whole video like this is
> about weight loss drugs. Let's just make that rule apply to videos that aren't entirely about weight loss drugs. We'll avoid that,
> but for once, like this, where the whole thing is about weight loss drugs, we can put weight loss drug names and graphics. For the
> quit-over-stomach-side-effects, it's a little unclear to me. I want two new bar graphs below that, both of them very short, to show
> that only a small amount of people quit: 2.7% for the Zepbound and 5.6% for the Ozempic. Okay, when there's 2:50 remaining in the
> video in this screenshot here with the 7 days a week graphic, there's a slight pause. I want you to remove that and make that
> transition smooth. Everything else looks good. Go ahead and proceed to the next round of edits.

## Read as (the work)
1. **AI motion, approved frames: A1 (two shots), A3, A4, A6, A8.** "A1 through A6" = the four pairs that exist in that range (A2 and
   A5 were dropped in round 3); "A looks good" = A8 (Wispr dropped the 8). Frames: `round4/ai/<ID>/` (`start.png`, `end.png`,
   `spec.json`, gate + reviewer stamps; `gate.py --verify` passes on each). Motion on the Google Flow subscription through the
   background `flow-veo` agent (`_shared/veo/veo.py add`); never paid API unless Dan says rush. Every take: `clipcheck.py` + a fresh
   `frame-reviewer` with the three sense questions and "real footage or AI?"; regenerate slop. Note A6's frames were restructured in
   review (START already holds the heap; END reaches for one more roll) and A1 is two shots joined by a cut. Cut each in where the
   round 4 page says (A1 = option B for 0:00-0:06 in place of the photo montage; A3 2:13.5; A4 3:01; A6 6:47-6:49 over "I out ate
   Ozempic"; A8 7:50) as full-screen inserts with the AI-GENERATED chip; check what each covers (A4 sits on the G04 lower third,
   A8 inside the G12 step-down card: keep both readable).
2. **A7 new frames:** the red-shirt jumper on the LEFT, in the FOREGROUND, jumping the full distance from the top of the stairs to
   the bottom (not onto the sloped lawn); comic heap at the bottom, not an injury. Frame gate + fresh frame-reviewer, then show
   Dan the frames on the round 5 page BEFORE making motion. Round 4 lessons: build END first, START from END; no pasted people.
3. **Amy Schumer abs photo:** find the picture she posted of her abs (2025, Instagram; downloads are pre-authorized) and show it
   where Dan says she "posted pictures of her abs" (round 4 film about 4:13, Amy corner segment BG15), credited on screen.
4. **G06 head-to-head card** (round 4 film 4:32-4:46; Dan's "4:02" is VLC's time remaining; screenshot `G06-at-4m34s.webp`):
   title "Zepbound Beats Ozempic In Studies", bar labels "Zepbound" / "Ozempic"; add below two very short bars for quitting over
   stomach side effects: Zepbound 2.7%, Ozempic 5.6%. Built by round 2's `round2/hf/build_custom.py` (kind `study`); copy into
   round 5 as round 4 did for G12/G14.
5. **Pause at "7 DAYS A WEEK"** (Dan's "2:50 remaining" = round 4 film 5:46; screenshot `7DAYS-at-5m46s.webp`): the gap after
   "...why you should too." (film words: "too." 344.57) before the next line; tighten it like `round4/recipe/retime_r4.py` did for
   Tracy (picture EDL, words, voice wav all shift by the same whole frames) so the transition is smooth.
6. Everything else is approved: keep it.

## State after round 4
Work dir `/Volumes/Expansion/_edit_work/RO-24/round4/` (round 3 media linked). Final film `final/RO24_R4_MASTER.mp4` (sha256
416a73d0ea2d982d..., 8:36.2, one full render), review page `review/` served at http://127.0.0.1:9420/. Recipe scripts in
`round4/recipe/` and copied to `.claude/skills/longform-edit/reference/ro24/round4/`. Fifth independent review SHIP; watch pass 0
defects; delivery gate fails only the known rows (voice A tone/artifacts, celebrity faces read as hair, template headroom/splices,
clip speech in fidelity/restarts, sidecar SRT read as cards/burned). Known notes Dan did not raise: Fat Joe's photo cards at 2:50 reuse
his photos; one faint lip smack at 4:41. Spend so far $0.

## Rules learned in round 4 (do not relearn)
- `assemble_r4.py --reuse` darkens copied frames ~1.65 luma levels per generation: the delivered film must be a full render.
- Run a fresh independent `ra-reviewer` on every new build until SHIP; then a fresh watch judge; then the gate.

## Deliver
Round 5 page (A7 frames first, then the full film with timestamped watch ranges for every change), Videos to Review copy, edit
slot released with `--review`, Edit Queue `delivered`, board entry updated.

## Starter prompt
> Celebrity Ozempic LFC R5. Model: Claude Opus 5.5, high. Rename this task to Celebrity Ozempic LFC R5 at the start. Read
> `Handoffs/handoff-20261028-ro24-celebrity-ozempic-round5.md` and execute round 5 of "Reacting To Celebrity Ozempic
> Transformations" (RO-24) with /longform-edit: check the Expansion drive is mounted first; motion on the Flow subscription for the
> approved AI clips A1, A3, A4, A6, A8 (every take through clipcheck and a fresh frame-reviewer) and cut them in; new A7 frames
> through the frame gate and an independent frame review, shown to Dan before motion; the Amy Schumer abs photo; the G06 card
> changes; remove the pause at the 7 DAYS A WEEK graphic; full render, every gate, independent review, deliver the round 5 page.
