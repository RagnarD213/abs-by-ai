---
name: ai-clip-artifact-giveaways
description: Dan rejects AI clips with giveaways a viewer sees at speed (breath smoke, fogging mirrors, melting hands); small faults of a few frames are acceptable and a slight speed-up can cover them (calibrated 2026-10-08)
metadata:
  type: feedback
---

Dan, 2026-09-14, on the Ad 3 vertical (otherwise approved): at 1:16 the AI story clip shows a man exhaling and the bathroom
mirror fogging with breath smoke — *"a weird AI artifact… things that just give away that this is AI-generated and make it
seem like it's not a real clip."* It had passed five of Muhammad's revision rounds, our rebuild, five audits and a full
watch pass, because it sits in one corner and grows over 1.5 s.

**Why:** an AI-GENERATED label discloses the clip but does not excuse it looking fake; a giveaway breaks the ad's credibility.

**How to apply:** in any review or build that contains AI shots, read each shot as consecutive full-resolution frames (all of
its last 2 s — Kling/Veo image-to-video degrades toward the end), cropping mirrors, mouths, hands, held objects, backgrounds
and screens. The checklist and item wording live in `/revisions` step 3b; the Ad 3 fix is
`Handoffs/handoff-20260914-ad3-ai-smoke-artifact-fix.md`. When generating new AI clips, run the same check before handing
them over. Related: [[untagged-video-bt601-trap]].

**Calibration, Dan 2026-10-08 (RO-11 opener, session "Calories Don't Matter LFC R2").** Claude rejected two Veo takes because,
frame by frame, the fork read as a spoon in the man's mouth for about 10 frames, its head detached from the handle for about
6 frames, and the food reshaped at the cut. Dan, after watching both takes in VLC: *"I think the clip was actually acceptable.
Those small faults that you notice, I don't think they would be noticed by humans. For future clips, if we did want to use the
whole thing, I think small faults like that could be covered by slightly accelerating the clip. I think normally clips like
that would be okay."* (He still chose the shorter clean tail for that video, because it flowed better.)

**How to apply (the last two points are Claude's interpretation):** the frame-by-frame pass finds candidates; the verdict is
made by watching the clip at normal speed as a viewer. A fault that lasts well under half a second and is not visible at
speed is a note in the report, not a rejection and not a reason to pay for another take or stop for approval. A slight
speed-up of the clip is an allowed way to hide such a fault (holding or slowing a clip to fill a slot is still forbidden).
The 09-14 rule above still stands for faults a viewer sees at speed or that grow over a second or more. Rule text:
`_shared/VIDEO-RULES.md`, "AI clip faults: judge at playback speed".

