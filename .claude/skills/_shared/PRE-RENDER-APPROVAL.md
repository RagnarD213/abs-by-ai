# The round method: approve in small steps, render the full video last

**Dan, 2026-09-28, the standard for EVERY video skill** (filmed ads, organic long-form, website VSLs, Shorts, AI ads, aspect-ratio
adaptations): *"the reason why Codex is making way better videos than you is that it's taking a way more stepwise approach. Rather
than trying to one-shot it and edit the video all in one, there are many small rounds of approval. I want you to copy this approach
going forward."* It replaces the 2026-09-26 "first 30 seconds" version of this page and every "one shot" instruction in any skill.

The model is Codex's WV-01 website video: its first one-shot attempt was rejected; eleven small rounds then produced the film Dan
locked (study: `/Volumes/Extreme/_edit_work/ro05-fable/CODEX_METHOD_STUDY.md`). Claude's RO-05 salad recut was built in one shot,
passed four reviews, and was still rejected on sight for its intro, graphics and grade (2026-09-28).

## The approval order

Each step is its own round unless the items are ready together. Nothing later starts rendering before the items it depends on are locked.

1. **Look.** Colour, crop/framing and audio, on one page. Colour: 2-3 grades on the same source moments (stills and a short moving
   sample), measured numbers beside each. Crop: numbered wide/tight stills at one moment with their crop values. Audio: natural vs one
   subtle, level-matched alternative. Each is locked separately. A revision reuses the locked look unless Dan asks to change it.
2. **Graphic style.** Soft Blue Light is locked for all videos ([GRAPHICS-STANDARDS.md](GRAPHICS-STANDARDS.md), [SOFTBLUE.md](SOFTBLUE.md)).
   Do not invent another style. Only if Dan asks for a new style: 3 directions, each built from the same 5-6 real components.
3. **Every graphic, as a still screenshot first.** One screenshot per graphic, in timeline order, rendered on the real graded frame it
   will sit on, with: its ID (G01, G02...), output time range, the exact copy, and the speech before, under and after it. Dan edits the
   text and approves or rejects each one. Only approved stills become moving previews (entrance, reveal, exit), shown in context with
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
- **Show only what changed or is still pending.** Locked items appear as a record list, never as a question. Batches shrink as locks
  build up (about 40 items early, 3-7 late). A one-variable question (a crop, a transparency) gets its own tiny page so it can be
  answered the same day. Send a small frame page early and keep working on everything that does not depend on it.
- **Choices are 2-3 options at most**, on the same frame or the same narration.
- **Present it like Codex:** one review page (copy `wv01-edit/round11/index.html` or `ro01/revision4/index.html`), a header stating what
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
