# Handoff: first full video with every graphic from the HyperFrames templates (2026-09-30)

**Goal.** The next long-form to reach its graphics stage builds every lower third, before / fact card, 3A side list
and cycle diagram from the four approved HyperFrames templates, not from hand-coded `softblue.py` motion. Along the
way, turn the round-2 sample scripts into one reusable graphics pass that any video's plan can call.

**Which video.** Whichever long-form reaches its graphics stage next. Recommended: **RO-10, "Calories: The Reason
You're Not Losing Weight"** (9/23 roll C1704, READY in `Handoffs/video-editing/00-MASTER.md`). It was shot on the same set as
RO-16, so the look (grade C), the W2 / T2 / W4 crops, the reframe-room numbers and the base round trip are already
proven. Check `AI_COORDINATION.md` first: never take a video another session owns. RO-12 and RO-16 already have
their graphics built; do not rebuild them.

**What is approved (Dan, 2026-09-30).** Pilot: *"significantly better than the graphics that we're using."* Round 2:
*"All three approved."* Templates in `.claude/skills/_shared/hyperframes/`:
- `cycle/`: 4-step loop in the left-third card beside Dan.
- `lower-third/`: Motivation lower third. The point comes in parts on the words. Optional counter bar (long way vs short way). A second `_mask` render carries the glass blur.
- `before-card/`: full-screen photo plus glass fact card on the live field. Optional number count-up. The disclosure chip arrives with the photo.
- `side-list/`: the 3A card, exactly as locked, but items land on their words (replaces the fixed 0 / 0.25 / 0.50 s).

Read first: `hyperframes/README.md` (word rules, easing table, reframe, composite, the traps), `_shared/SOFTBLUE.md`,
`_shared/GRAPHICS-STANDARDS.md`, `_shared/PRE-RENDER-APPROVAL.md`, then the round-2 build that proved all of it:
`Media/hyperframes/round2-templates/` (`BEATS.md`, `bases.py`, `composite.py`, `clearance.py`, `page.py`).

**Steps.**
1. Board entry. Edit the chosen video through its skill (`/longform-edit`) up to the graphics stage as normal. The
   plan's graphic copy follows the usual rules (distilled, self-contained, no echo of the speech).
2. Build `.claude/skills/_shared/hyperframes/from_plan.py`. It reads the video's resolved plan (kinds `lt`,
   `scene`/fact, `l3`, cycle) and its mapped word timings, and writes one config per template. The rules:
   - Every time is a word start. A lower third's point is split where Dan says each piece.
   - Items land on the word that starts them. Counters count on the number's word.
   - `a` / `b` are the plan's in and out, snapped to shot boundaries where the card moves Dan.
   - It then runs each template's `build.py --render`.
   - Print a beat sheet like `round2-templates/BEATS.md` for the review page.
3. Generalise `round2-templates/composite.py` into `hyperframes/composite.py`: it composites every overlay into the
   film render in RGB. Keep three rules:
   - Decode the renders as **BT.601** (they are untagged) and the bases as BT.709.
   - For the lower third, blur the base inside the `_mask` alpha (GaussianBlur 14) before laying the content on top.
   - Opaque scenes replace exactly `fr(b) - fr(a)` frames.

   Hook it into the video's render in place of the PIL paint for those four kinds. Every other kind (title, study,
   chart, recap, phone) stays `softblue.py`.
4. Side cards: slide the approved crop left inside the 4K frame only where it has room. On the 9/23 set, W4 has
   520 px of room and W2 has only 144. Otherwise keep the video's existing wall stretch; never zoom in past his
   shoulders. Run `clearance.py`-style checks on every 10th frame: hands and arms clear of the card (round 2
   minimum: 78 px). Also check the lower third never covers his face.
5. Verify before any review:
   - `lint` + `check` 0 errors on every scene, and snapshots inspected.
   - Base against the untouched frames of the video's own draft: 43 dB or better, as in round 2.
   - Card fill measured at 10,38,72 ±2 on a composite frame.
6. One review page in the RO-16 format: first minute on top, then "What I decided", every graphic three per row on
   its real frame with the speech before, during and after, then a reply box. Serve it so it survives the session: a
   `launchctl submit` http.server from a folder under `/Users/Shared/` (background jobs cannot read
   `/Volumes/Extreme`; that is why the round-2 page went down). Check that every media link returns 200. Stop for Dan.
7. After approval, continue the video through its normal gates and delivery. Record in `hyperframes/README.md`
   anything new the templates needed (new config fields, a trap), and mark RO-10 (or the chosen video) as the first
   full-template film.

**Spend.** $0 (no generation). Render time: about 6 to 11 s per second of overlay, plus the lower-third mask pass
(round 2: 60 s for 9.3 s of side list, 99 s for 5.2 s of before card, 83 s + 59 s for 11.6 s of lower third). A
20-minute film with about 25 graphics is roughly 30 to 60 minutes of rendering, so run it in the background.

**Not in scope.** New template kinds (title card, study, chart, recap, phone). If the video needs one, keep
`softblue.py` and note it on the review page as a candidate for the next template round. Codex adoption of the
templates is a later handoff.

**Board.** Add an ACTIVE entry at start; when Dan approves, delete this handoff's rows in `Handoffs/README.md` and
`AI_COORDINATION.md`. No dashboard row unless Dan asks.

---

**Starter prompt (Claude Opus 5.5, effort high):**

Read and execute `Handoffs/handoff-20260930-first-full-video-from-hyperframes-templates.md`. Take the next long-form
that reaches its graphics stage (RO-10 recommended, if no session owns it), build every lower third, before card, 3A
side list and cycle diagram from the approved HyperFrames templates through a new reusable `from_plan.py` and
compositor, verify colour, alignment and clearance, and show me the review page in the RO-16 format with a "What I
decided" list. Stop for my review.
