# Handoff: HyperFrames templates round 2, lower third + before card + 3A side list (2026-09-30)

**Goal.** Turn the three most-used Soft Blue Light graphics into approved HyperFrames templates, each shown to Dan as
old vs new on real footage, so the first full video can be built entirely from approved templates. Samples only:
no film is changed, nothing is published.

**Where we are.** The pilot is approved (Dan, 2026-09-30: *"significantly better than the graphics that we're using...
This is approved."*). The cycle template, its word rules, easing table, reframe method and composite recipe are in
`.claude/skills/_shared/hyperframes/README.md`; read it first, then `Media/hyperframes/README.md` (version 0.8.97
pinned, PATH, commands) and `.claude/skills/_shared/SOFTBLUE.md` + `GRAPHICS-STANDARDS.md`. The pilot build to copy:
`Media/hyperframes/pilot-c1652-spiral/` (`make_scenes.py`, `base/build_base.py`, `composite.py`, `page.py`, `BEATS.md`).
Dan's layout call: diagrams and lists sit in the left-third card beside him; full screen felt "a little bit empty".

**The three samples** (all from RO-16 round 1, cut from roll C1710; plan, stills and word timings in
`/Volumes/Extreme/_edit_work/ro16/round1/` and `recipe/`; do NOT modify anything there, RO-16 is locked):
1. **Lower third, G04** (56.2 s): topic "THE MATH", point "1 lb A Week = 7 MONTHS. All In = 90 DAYS." New: the approved
   Motivation lower third with motion (strip settles, cyan accent draws, topic then point reveal on the words) plus a
   small timeline bar that shrinks from 7 months to 90 days on "all in", both numbers as counters.
2. **Before card, G02** (19.1 s, full-screen): "TWO YEARS AGO / 200 lb at 5'7" / No abs." with the real photo and the
   "Real picture of me." label. New: slow push-in on the photo, a light sweep across the glass, "200" counts up on the
   word, the card drifts a few px while up. Full-screen field scene (opaque MP4, not an overlay) since the photo is the content.
3. **3A side list, G20** (622.5 s): "Your Weekly Check / Down 2+ lb: change NOTHING / Stalled a week: CUT 200 cal".
   New: the 3A card exactly as locked (fill, border, type, numbers), with items landing on their words instead of the
   fixed 0 / 0.25 / 0.50 s, a quiet settle, and the drift. Keep "no typing, no bounce" from the 3A lock.

**Steps.**
1. Board entry; beat sheet for all three, anchored to words in RO-16's word timings, keeping the approved copy exactly.
2. Build each as a template folder under `.claude/skills/_shared/hyperframes/<name>/` from the start (template + `build.py`
   + example config), like `cycle/`. `lint` + `check` clean, `snapshot` inspected before any render.
3. Rebuild the caption-free graded base for each moment from the raw roll with RO-16's locked look (colour C, W2/T2
   crops); verify frame alignment against the round-1 media on untouched frames. Render, composite, check every 10th
   frame for Dan's head and hands against the graphic.
4. One review page in the RO-16 format (old and new side by side per sample, stills, "What I decided", reply box),
   served locally; check every media link returns 200. Stop for Dan.
5. On approval: mark the three templates approved in the README table, update SOFTBLUE.md's HyperFrames section, and
   write the first-full-video handoff (the next video to reach its graphics stage builds all graphics from the templates).

**Spend.** $0 (no generation). Tokens: effort high, never above. Record render times.

**Board.** Add an ACTIVE entry at start; delete this handoff's rows in `Handoffs/README.md` and `AI_COORDINATION.md`
when Dan approves; no dashboard row unless Dan asks.

---

**Starter prompt (Claude Opus 5.5, effort high):**

Read and execute `Handoffs/handoff-20260930-hyperframes-templates-round2.md`. Build three more HyperFrames templates in
Soft Blue Light (the G04 lower third with the 7-months-to-90-days bar, the G02 before card with the 200 count-up, the G20
3A side list), each on the real RO-16 footage without touching RO-16, and show me old vs new on one review page with a
"What I decided" list. Stop for my review.
