# The round method: approve in small steps, render the full video last

**Dan, 2026-09-28, the standard for EVERY video skill** (filmed ads, organic long-form, website VSLs, Shorts, AI ads, aspect-ratio
adaptations): *"the reason why Codex is making way better videos than you is that it's taking a way more stepwise approach. Rather
than trying to one-shot it and edit the video all in one, there are many small rounds of approval. I want you to copy this approach
going forward."* It replaces the 2026-09-26 "first 30 seconds" version of this page and every "one shot" instruction in any skill.

The model is Codex's WV-01 website video: its first one-shot attempt was rejected; eleven small rounds then produced the film Dan
locked (study: `/Volumes/Extreme/_edit_work/ro05-fable/CODEX_METHOD_STUDY.md`). Claude's RO-05 salad recut was built in one shot,
passed four reviews, and was still rejected on sight for its intro, graphics and grade (2026-09-28).

## Decision budget for organic and other non-VSL videos (Dan, 2026-09-29)

**Round 1 always shows every graphic, stock item and clip (Dan, 2026-10-08).** *"Let's always do graphics review for all
videos in the first round, graphics stock and clips review."* The first round's page carries all of them for his look,
each on its real frame; later rounds show only what changed and stay lighter than the VSL cadence. The budget below
still governs how many QUESTIONS he is asked; it no longer lets an item be locked without being shown in round 1.
Full rule: VIDEO-RULES.md, "Round 1 always reviews every graphic, stock item and clip".

**For these formats, this overrides every "Dan approves each item" line below.** RO-05 round 3 put about 50 items in front of him (every graphic
and clip, one by one). Dan: *"This is way too complicated... I can't be approving this much stuff per video... Just go with what
you think is best for most of this and reduce it to 10 to 15 decisions max. Only for things that legitimately need my decision."*

**Website VSL exception (Dan, 2026-09-29):** use `$vsl-edit` for the deeper WV-01 approval cadence. Dan wants extensive
approval of material VSL assets before the complete render. Do not force a 10 to 15 decision or round cap on a VSL;
group routine checks, reuse locked approvals, and take as many focused rounds as the film needs. The budget below
continues to guide organic videos and other formats.

- Claude still builds and checks everything in steps (stills, moving previews, first minute), but **Claude approves what it checked**:
  sync, face/hair clearance, copy against the speech, the standing rules. Those are not questions for Dan.
- Ask Dan only what Claude genuinely cannot call: taste choices between close options he has strong views on (grade, the opening,
  a new look), facts only he knows, and anything that changes something he already locked. **At most 10 to 15 decisions per video, in
  total, not per round.** Fewer is better; zero is fine.
- Every packet opens with a short "what I decided" list (one line each) so he can overrule while watching, never item-by-item forms.
- Dan still sees the first minute and the finished film; his notes there are the check on Claude's calls.

**Organic path (Dan, 2026-09-29):** use `$long-form-content-edit` with GPT-6 Sol throughout. Reuse the approved studio
framing, color, audio and graphic family after a source-specific check. Build still and motion checks internally for
every new graphic and clip, but group only material new choices into one early look-and-assets packet. Show the
finished first minute next, then the complete film after all assets are locked. Keep the AI start/end-frame approval
gate before new motion. Revisions reuse locked work and need only the affected previews.

## The review page: one layout, and a "What I decided" list on every packet (Dan, 2026-09-30)

**Also copy every review video of 45 seconds or longer to the project folder `Videos to Review/` for VLC, and delete the copies when Dan finalizes the video (Dan, 2026-10-08): VIDEO-RULES.md, first section.**

Dan, on the RO-16 round 1 page: *"I like this 'What I Decided' section. Let's make this the standard way to do things going
forward... so I can look over your decisions just in case I need to revise any of them"* and *"the first minute is right on
top, the AI opener frames are below that, and all graphics and clips are in order. That makes it significantly faster for me
to review than looking at all this in the browser panel one at a time."* Every approval packet, Claude or Codex, uses this page:

1. **Header:** one line on the video, then what is already locked (reused approvals), then **"Your decisions (N)"**: the few
   genuine questions, numbered, 2-3 options each, recommendation first.
2. **The first minute** (or the current finished section) in one lazy player at the top, with the 1080p master and audio A/B links.
3. **AI opener / new AI clip frames** directly below: START and END side by side, the action, duration and cost under each pair.
4. **"What I decided (overrule anything)":** one line per call Claude/Codex made without asking: take choices and restarts cut,
   numbers used on screen, rejected assets and why, reviewer findings fixed, spend so far. Plain language, no jargon.
5. **All graphics and clips, in timeline order, three per row:** each a still on its real graded frame, with its ID, output time
   range, exact copy, source, and a collapsible speech before / during / after.
   **Every moving graphic gets a "Play it moving, in context" button** (Dan, 2026-09-30, on the RO-10 round 1 page: *"I really
   like what you did with the review page, with the 'Play it moving in context' button. Let's lock that into the skill."*).
   The button loads that graphic with about 3 s of speech either side into ONE shared player docked above the grid
   (`preload="none"`; never one player per card). Name the clips `context/<ID>-context - REVIEW 540p.mp4`. A collapsible beat
   sheet (film time, word, what moves) sits under each graphic whose parts land on words.
6. **One reply box** with the decision lines pre-filled and a Copy button.

**The player floats at the side and every video can be scrubbed (Dan, 2026-10-02, Ad 13 round 2).** *"Fully utilize the
huge amount of space I have on the screen, put the video in a kind of floating panel to the side, and then put all the
other stuff in the middle"* and *"I'm not able to click around to go backwards and forwards, which is essential."* On a
wide screen the shared context player is a fixed panel at the right; the page scrolls in the middle and playing an item
never jumps the page or covers it. Serve the page with `.claude/skills/_shared/review_server.py PORT [DIR]`, never
`python3 -m http.server`: the built-in server ignores byte ranges, so a click on a video's timeline does nothing.
On macOS this command now installs a persistent login service and returns after checking it. Require the
"Managed review ready" result; do not leave delivery dependent on a chat terminal. The server restarts after a crash
and at login. It caches the linked page assets locally so the editing drive can be disconnected. Run the command
again after page or video changes to refresh the published cache. Before sending, seek in one player and confirm the time moves.
Long review files also go in `Videos to Review/` under the shared rule above. Layout reference: `kit9x16/sbl_page.py`.

Reference build: `/Volumes/Extreme/_edit_work/ro16/round1/index.html`, generator `.claude/skills/longform-edit/reference/ro16/page.py`.
With the context player and beat sheets: `/Volumes/Extreme/_edit_work/ro10/round1/index.html`, generator `.claude/skills/longform-edit/reference/ro10/page.py` + `review_media.py` (start from this one).
Dan reviews it in Chrome, so every media link must resolve over a local server (check each `src`/`href` returns 200 before sending).

## The approval order

Each step is its own round unless the items are ready together. Nothing later starts rendering before the items it depends on are locked.

1. **Look.** Colour, crop/framing and audio, on one page. Colour: 2-3 grades on the same source moments (stills and a short moving
   sample), measured numbers beside each. Crop: numbered wide/tight stills at one moment with their crop values. Audio: natural vs one
   subtle, level-matched alternative. Each is locked separately. A revision reuses the locked look unless Dan asks to change it.
2. **Graphic style.** Soft Blue Light is locked for all videos ([GRAPHICS-STANDARDS.md](GRAPHICS-STANDARDS.md), [SOFTBLUE.md](SOFTBLUE.md)).
   Do not invent another style. Only if Dan asks for a new style: 3 directions, each built from the same 5-6 real components.
3. **Every graphic, as a still screenshot first.** One screenshot per graphic, in timeline order, rendered on the real graded frame it
   will sit on, with: its ID (G01, G02...), output time range, the exact copy, and the speech before, under and after it. Claude checks and
   locks each one. Dan sees material new VSL graphics and the selected organic graphics that need his judgment. Only locked stills become moving previews (entrance, reveal, exit), shown in context with
   about 5 s of narration either side. A style approval never approves an individual graphic.
4. **Every clip.** Stock, existing B-roll, photos and app demos: the exact moving trim and crop, in context (about 5 s either side),
   plus the isolated source when useful. AI clips have three gates: the concept (text only when Dan asks for ideas; offer 2-3 opener
   concepts), then START and END frames with the action, duration and cost, then the finished motion in context. Never generate motion
   before its frames are approved; never ask twice about unchanged approved frames. Records: [ASSET-APPROVAL.md](ASSET-APPROVAL.md).
5. **The first minute.** Export the first 60 seconds finished (approved look, intro, graphics and clips in place; anything still pending
   is a clearly labelled placeholder). This is what Dan is pickiest about. For a video under two minutes, the first 30 seconds.
6. **The full video**, only when nothing is pending. Build from the locked components, rebuild only affected joins, then the exact-file
   gates, the watch pass and one independent complete-candidate review, then deliver.

## How a round works

- **One round is one session.** It starts from the previous round's handoff, reads the decisions file, and re-hashes every locked file
  (record expected vs actual) before touching anything. It builds in a new `roundN/` folder and never overwrites a reviewed round.
- **Show only what changed or is still pending.** Locked items appear as a record list, never as a question. Stay inside the decision
  budget above (10 to 15 per video in total); items Claude checked are listed as decided, not asked. A one-variable question (a crop, a transparency) gets its own tiny page so it can be
  answered the same day. Send a small frame page early and keep working on everything that does not depend on it.
- **Choices are 2-3 options at most**, on the same frame or the same narration.
- **Present it on the standard review page** (layout and order: "The review page" section above, Dan 2026-09-30; older references: `wv01-edit/round11/index.html`, `ro01/revision4/index.html`), a header stating what
  is locked, one button per item ID feeding a single lazy player (`preload="none"`; several players crash the browser), one section per
  item with its still, copy, times and before/during/after speech, and a decision control (Approve / Changes requested / Remove) that
  saves a JSON file. Name clips `<ID>-context.mp4` with a matching `.jpg` poster; frames `frames/<ID>-start.png` and `-end.png`; drafts
  `DRAFT - <job> round N - first minute.mp4` plus a `REVIEW 540p` copy.
- **Record every decision** when Dan replies, in `round(N+1)-plan/decisions.json`: per item its ID, path, sha256, verdict (approved /
  approved-with-notes / rejected), Dan's exact words, scope (for example "frames only", "text approved, timing pending") and next action,
  plus `motion_authorized` and `new_frames_before_motion` lists. A locked item is never reopened unless Dan reopens it.
- **Close every round with a handoff** (`Handoffs/handoff-YYYYMMDD-<job>-roundN-<topic>.md`): scope; files to read; locks with hashes
  and Dan's words; each requested change anchored to heard words and output times; exact authorizations per AI item; cuts already
  applied (so none is applied twice); gate status stated honestly; a cost ledger (known, unknown, cap); the recommended model and effort;
  the exact next action; a ready-to-paste starter prompt. Then stop. No session stays alive polling for Dan's answer.

## Forbidden

A full film, or a full placeholder film, before every graphic and clip is locked. Re-asking about locked items. Motion before frame
approval. Changing a locked file in place. Applying a pause cut twice. Stretching or holding a clip to fill a slot. Relaxing a gate or
claiming a gate PASS from creative approval. Graphics that only echo the speech (VIDEO-RULES "KEY POINTS"). One useful point belongs in
a compact `KEY POINT:` lower third, not a large empty card; larger layouts need a real list, study, comparison or diagram.

## Editing checks before any packet

Review pauses, resets, false starts, stray words and awkward joins against the source and the finished audio; remove confirmed junk
without clipping syllables. Inspect the words on both sides of each edit. Read the whole take map against the roll transcripts: take
maps drop lines of reasoning. Check every handheld piece's first and last second and every mid-line camera move for junk with no audio
signature. If timing changes, regenerate the time maps, graphic timing, subtitles and chapters. Approval of a look survives a clean cut;
exact-file stamps do not. Transcribe every music bed before use and require zero words.

**Check a side card over every piece it spans before proposing it, not only on its still.** A 3A left card that was clear on
its approved still covered Dan in RO-05 round 3 (2026-09-29): handheld kitchen takes swing to products, punch in, and he walks
to the left edge, so no fixed `shift_presenter` clears him. Sample about 8 frames per piece with the person mask and measure the
head's left edge against the card edge (x752). If any piece fails, propose one Motivation lower third per item, on as he names it,
beside the card option. Recipe: `/Volumes/Extreme/_edit_work/ro05-fable/round3/recipe/build_r3.py shifts`.

## Queue and records

`placeholders.json` keeps its schema for clip identities and approval fingerprints; the opening, graphics and broader creative
decisions live in the round's `decisions.json` / work packet. The queue's `frames_approved` state is frame approval only. Park using
the supported queue states; keep a paused dispatcher paused. Once locked, the final assembly still needs every exact-file check, the
full picture/audio review and one independent reviewer. Creative approval does not authorize publishing.
