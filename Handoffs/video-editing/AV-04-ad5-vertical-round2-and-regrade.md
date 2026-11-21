# AV-04 — Ad 5 "Every Diet You've Tried Failed For The Same Reason": vertical round-2 revisions + re-grade

**List 3 · ad variant · READY · replaces J4.** Read `00-RULES.md` first. Unblocks AS-03 (Ad 5 square).

## What exists
* 16:9 (Muhammad): filed. The long-form went public 09-16 (`bwfSQopZy1w`).
* 9:16 full + 59s delivered (`… | claude | 9x16 | ad 5.mp4`, `… | 9x16 59s | ad 5.mp4`), build `/Volumes/Extreme/_edit_work/ad5-vert/`.
  **Not approved:** Dan wrote round-2 revisions, and the grade has the BT.601 fault.

## Build
**The full spec is `Handoffs/handoff-20260912-ad5-vertical-revisions-round2.md`.** Execute it. Dan's two asks:
1. The app demo ends on **the same man's** after picture: `13_AFTER_ai-generated_app-demo-man.jpg`, no spend.
2. The real-picture label on every real picture of Dan, larger, off his abs and face. ⚠ `g5.real_chip` is shared with
   Ad 4, so don't break AV-03.

**Plus the colour fix the spec predates:** in the same re-render, re-fit the grade with the Ad 3 render-10 tools (BT.709
decode, as in AV-03 step 1) and verify against Muhammad's file decoded as BT.709. Rebuild both the full length and the 59s.
Work in a copy (`_edit_work/AV-04/`).

## Deliver
Replace the two Ad 5 vertical files (move the old ones to an `old versions/` subfolder in the ad folder, never delete them)
+ review copies + stamps + an updated `notes-vertical.md`. Send Dan the review copies.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AV-04-ad5-vertical-round2-and-regrade.md` (full spec in `Handoffs/handoff-20260912-ad5-vertical-revisions-round2.md`): same-man app-demo ending, real-picture labels off my face and abs, and re-fit the grade with BT.709 decoding in the same re-render, full + 59s. Every gate, audit, deliver, send me review copies, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/AV-04-ad5-vertical-round2-and-regrade.md` and the round-2 spec it links, using `.claude/skills/shortad-from-longform/SKILL.md` as the method. Deliver, send Dan review copies, update `00-MASTER.md`.
