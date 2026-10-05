---
name: vsl-edit
description: Edit or revise Abs By AI website video sales letters from filmed footage using detailed asset approval rounds before a full render. Use for website VSLs with a sales story, proof, product demonstration, offer and CTA. Organic teaching videos, paid ads and speed or aspect changes to an approved master use their own workflows.
---

## Shared HyperFrames graphics (2026-10-03)

For every new build or graphics revision, read the project's [shared HyperFrames method](../../../../.claude/skills/_shared/hyperframes/README.md). Lower thirds, before/fact cards, 3A side lists and cycles use that folder through `from_plan.py`, the shared `composite.py` and `checks.py`, pinned to **hyperframes 0.8.97**. Do not copy or fork its templates. `orglib` and `modern_graphics` panels are superseded for those four kinds; historical recipes remain reproduction records.

Cut first, map the finished words, and store graphics as data in `plan_resolved.json`. Resolve graphic in/out and every part from spoken phrases, never hand-picked whole seconds. Use the maintained Codex integration `scripts/video/hyperframes_graphics.py` for build, per-frame composition and verification. The RO-10 recipe in `.claude/skills/longform-edit/reference/ro10/` is the framing/build reference. New-video adapters copied from older recipes must replace their old panel path with this integration before rendering.

Record each graphic's template, generated config, text and `driven_by` words in the edit sheet, then run the shared sheet validator. Vertical and square adaptations redraw the same configs with shared `vertical.py` / `square.py`. Kinds without an approved template stay on `softblue.py`; new templates need their own graphic-lock approval. Preserve approved videos, source-specific picture/audio, captions and delivery gates. Check actual composite frames for arms, face and colour before presenting them.


# Edit an Abs By AI website VSL

Use the WV-01 website video process: develop the sales presentation in small, reviewable rounds; get Dan's approval for material creative assets; render the complete film only after those choices are locked. The number of rounds follows the work. A long VSL can justify many rounds, while a revision reuses everything already approved.

## Start with the brief and standing rules

1. Read the project's [video rules](../../../../.claude/skills/_shared/VIDEO-RULES.md), [pre-render approval workflow](../../../../.claude/skills/_shared/PRE-RENDER-APPROVAL.md), [graphics standard](../../../../.claude/skills/_shared/GRAPHICS-STANDARDS.md), [cut and junk-footage QC](../../../../.claude/skills/_shared/CUT-CONTINUITY-QC.md), and [edit queue rules](../../../../Handoffs/video-editing/00-RULES.md). Read the job brief, latest handoff, decisions file and existing source map before changing a revision.
2. Confirm the page, audience, offer, recorded CTA, requested versions and deliverables. Build a speech-to-scene map that carries the viewer from the desired result through personal connection, mechanism, visible proof and product use to the offer and next step. Use the [reusable VSL structure](../../../../Handoffs/video-editing/WV-01-EDIT-PLAN-20260924.md#11-reusable-vsl-template-for-future-website-videos) as a planning reference, not a fixed script or runtime. Keep the video promise, on-screen offer and page CTA aligned.
3. For a revision, list the exact requested changes and the shots, graphics, audio, timing and subtitles they affect. Record the approved elements to preserve. Check the hashes of locked assets before reusing them. Work in a new round directory; never overwrite a reviewed round or apply an earlier cut twice.

## Approval rounds before the full render

Use one focused round per session, with a decisions file and handoff. The VSL-specific rule is explicit approval of material assets and integrated scenes before the full render. Do not impose a fixed count of rounds or Dan decisions on a website VSL. Group routine checks and clear choices so review stays manageable, but let Dan decide the opening, consequential graphics and copy, product demonstrations, proof clips, AI motion, offer treatment and CTA when these are new or changed. Keep approved assets locked unless he reopens them.

1. **Look and opening.** Show comparable frames and moving samples for source-specific color, crop and audio. Confirm the opening concept and treatment. Reuse a locked look for a revision unless Dan asks to change it.
2. **Graphics.** Use the approved Soft Blue Light system. Show each new or changed graphic as a still on its real graded frame, with exact text, output time and speech before, during and after it. Check phone readability and clearance over the full shot. After the still is approved, show its moving entrance, reveal and exit in context. Reuse unchanged graphic components.
3. **Footage and demonstrations.** Show the exact trim and crop of each material photo, stock clip, app demonstration and proof scene within surrounding narration. For every new AI motion clip, approve its intended action and start and end frames before generating motion, then review the finished motion in context. Track generation costs across rounds.
4. **Integrated opening and close.** Show the finished first minute with approved audio, graphics and clips, plus any separately affected offer or CTA tail. Revisions should show only changed sections and joins. A labelled placeholder may appear in an opening review where the shared rules permit it; it never authorizes a complete placeholder film.
5. **Full-film authorization.** Confirm that all required choices are locked and Dan has approved moving to the complete render. Preserve requested deferrals between versions. A full render is the final assembly step, not an early draft used to discover the visual style.

Every review packet states what is locked, what changed, what Dan needs to decide, and the precise files being reviewed. Record his words, approval scope, file paths and hashes. Close each round with a concise handoff and ready-to-paste next prompt; stop while awaiting a decision rather than polling.

## Full candidate and delivery

Build from the locked components. Inspect the entire picture and audio in order, every native cut and repaired join, source junk, graphic timing, phone readability, subtitles, offer wording and the complete final CTA. Run the current audio and website delivery gates on the exact file to be delivered. Obtain one independent full-candidate review. Fix confirmed defects and rerun checks affected by a change. Report any remaining gate failure as a failure even if Dan accepts the creative choice.

Deliver the full master, a phone-friendly review copy, subtitle sidecar, recipe or source map, decision record, checks and known exceptions. Record provider costs. Mark a video finalized only after Dan approves the complete candidate. Uploading, website installation and publishing are separate tasks; leave any paused dispatcher paused unless Dan directs otherwise.

## Standard 9:16 centering (Dan, 2026-10-03)

For every vertical talking-head build, read the shared section **Vertical talking head: land on him, then hold** in `.claude/skills/_shared/framing-motion.md` in the Abs By AI project. Use its shared `.claude/skills/_shared/cut/landing.py`, never a private smoother.

1. Split at every picture cut, punch-in and return from graphics. Never smooth across cuts.
2. Land exactly on his measured head centre on the first frame. Measure the actual cut frame.
3. Hold while he is within 3.3% of crop width of centre.
4. Outside it, follow only to the band edge, eased over 0.75 seconds, capped at 28% of crop width per second.
5. Takes wandering less than 6.6% of crop width keep one first-frame-anchored centre.
6. Never recenter the exit.

Call `landing.vertical_track(n, raw_head_x, picture_segments, crop_width, fps)`. This uses `landing.track` with scaled 170/608 speed, 40/608 fixed range, 20/608 tolerance and k=3. Report total crop travel, p90 pan speed, time moving, and median/maximum head distance from centre via `landing.motion_stats`. Inspect actual cut landings and head clearance at the original frame rate. These instructions supersede any continuous vertical recentering or unconditional fixed vertical take in older recipes. Square rules, static horizontal framing and the delivery gate remain unchanged. Approved videos stay untouched.
