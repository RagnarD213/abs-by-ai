# Follow-up 2: B-roll and existing AI clips from our library

Dan: "Now that our B-roll library is done, go through it and these videos again and look for opportunities to add
B-roll and existing AI clips we already have."

For YOUR video only, scan the clip library thoroughly for clips that would improve it, and write the additions as doc
items. Library: `cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI" && python3 .claude/skills/_shared/cliplib/clip_library.py find "<query>"`
(run many queries: one per spoken line / idea in the transcript, with and without `--aspect 9x16`, and with `--rolls`;
read `.claude/skills/_shared/cliplib/README.md` first for the fields and other commands such as listing everything).
LOOK at the preview `Media/clip-library/contact/<ID>.jpg` of every candidate before proposing it.

Where to add:
- Stretches of plain camera scene longer than about 6-8 s where a line names something we have a clip of.
- Lines where his stock / AI clip could be replaced by OUR real footage of Dan or one of our approved AI clips that
  matches the literal words better (if your section already has an item on that span, say so in "replaces_item").
- The opening: if a library AI clip literally shows the video's subject, propose it as a 2-3 s opener (calibration rule 44).
Rules:
- The clip must match the LITERAL words under it (lesson 9). No padding: do not cover a strong on-camera line, the
  closing call to action, or a beat that already has a correct picture. Aim for the 2-5 best additions, zero is allowed.
- Only clips that have a Drive link / id in the library (report any great local-only clip separately under
  "Assets to upload" with its path; do not use it in an item).
- No clip twice in one video, and do not reuse a clip already used elsewhere in your section. AI clips get the
  AI-GENERATED label; real moving footage of Dan gets no label. Never the app's stick-figure animations. The
  successful prospect is white or Asian, 30-50, lean with abs; never one person's before against another's after.
- Prefer vertical 9:16 clips; a horizontal clip is cropped to vertical full screen unless that cuts off something
  critical, then the centre square.
- Timing: give the exact span in the current cut (from the word timestamps in `work/<NAME>/cut16k.json`) and the
  source range to use from the clip ("Use 0:02 - 0:05 from this clip"), verified on the clip's contact sheet or by
  extracting frames from the local file. "Accelerate footage to fit duration" where it is longer than the slot.

Write `/Volumes/Extreme/_edit_work/revisions-20261001/muhammad/out/<NAME>.broll.md`: ONLY the new bullet items, in the
exact dialect of your section's TIMESTAMPED REVISIONS list (a `- 0:12.3 - 0:15.0` line, then 4-space sub-bullets: one
sentence saying what the line is and that it is plain camera scene (or what is wrong with the current clip), the action
in **bold** ("**Insert this clip here, full screen.**"), the link as `https://drive.google.com/file/d/<id>/view` on its
own sub-bullet, the source range, and the label instruction if it is AI). Dan's voice, first person, no em dashes, no
other editor's name, no mention of a library or of Claude ("this clip" is enough). If nothing qualifies, write the
single line `NONE`. Also append a "## B-roll pass" block to your `.summary.md` listing each proposed clip ID, why, what
you rejected and why, and any "Assets to upload". Reply with the path, the count, and the clip IDs used.
