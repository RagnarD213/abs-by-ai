# AS-03 — Ad 5 "Every Diet You've Tried Failed For The Same Reason": 1:1 square full + ≤0:59 square cutdown

**List 3 · ad variant · BLOCKED: AV-04 delivered and Dan approves the round-2 Ad 5 vertical.** Read `00-RULES.md` first.

## What a square is here
A 1080×1080 **re-layout of the approved vertical build**, not a third recovery of the editor's cut. It keeps the vertical's
timeline, EDL, beats, grade, labels, caption timing and audio **bit for bit**, and reuses its `cut_plan.json` for the cutdown.
Only the geometry and the per-beat renderers change. Copy the approved vertical build dir to `_edit_work/AS-03/`.

**Read, in order:** `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` (the square translation rules), `Handoffs/handoff-20260911-square-ad5-muhammad.md`,
`.claude/skills/shortad-from-longform/SKILL.md` [S1] START HERE + `reference/a11_sq_ad1/` (the approved Ad 1 square template),
and `.claude/skills/_shared/framing-motion.md` (steady wider shots, updated 09-16). The Ad 3 square R2.1 (`_edit_work/ad3-sq-r2/`,
uploaded 09-16) is the most recent approved square. Its `notes-square-r2.md` records what Dan rejected in R1.

## This ad's specifics
* The per-ad spec predates round 2. **Take the pictures, labels and demo pairing from the AV-04 (round-2) vertical**, not the round-1 beats it lists.
* Build from the AV-04 build dir (BT.709 re-grade).

## Gates and deliver
Every gate on both delivered files at the current `GATE_VERSION`, the independent audit, then
`Muhammad Ad Videos/every diet you've tried failed for the same reason - ad 5/every diet you've tried failed for the same reason | claude | 1x1 | ad 5.mp4` + `Muhammad Ad Videos/every diet you've tried failed for the same reason - ad 5/every diet you've tried failed for the same reason | claude | 1x1 59s | ad 5.mp4`, REVIEW 540p copies, the audio A/B vs the approved
vertical, stamps, `notes-square.md`, `recipe-square/` into the ad's folder. Send Dan the review copies.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/AS-03-ad5-square.md`: first confirm its blocker is cleared, then build the 1:1 square and ≤0:59 square cutdown of Ad 5 as a re-layout of the approved vertical build with /shortad-from-longform [S1], same timeline, grade, labels and audio, steady wider framing, labels off my face and abs. Every gate, independent audit, deliver, send me the review copies, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table) and `Handoffs/handoff-20260914-ad3-square-codex.md` (the Ad 3 square you built, which Dan shipped: reuse its method), then execute `Handoffs/video-editing/AS-03-ad5-square.md`. Confirm the blocker is cleared first. Deliver, send Dan the review copies, update `00-MASTER.md`.
