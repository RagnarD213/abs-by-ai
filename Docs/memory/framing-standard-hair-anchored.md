---
name: framing-standard-hair-anchored
description: "Dan locked the video framing standard on 2026-09-08 — crops anchored to the measured top of his hair, NEAR/FAR only, never wide, hair never cut; apply to every video going forward"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d7b757da-4a9c-4456-81c6-ff4376367766
  modified: 2026-09-11T19:13:11.645Z
---

On 2026-09-08 Dan approved the website video's rev-4 crops and made them the standard: "The framing and the cropping are all looking good. You nailed it with this one. Let's lock that in and crop all the videos like this going forward."

The standard: every talking-head crop is anchored to the MEASURED TOP OF HIS HAIR (never a skin/hairline detector, which reads 60–90 px too low and cut his hair in three rejected revisions), `y0 = the hold's minimum hair top − 4 % of the crop height` (~43 px of headroom at 1080p), two levels only — NEAR = hair → belly button, FAR = hair → shorts line with the waistband in frame — alternating across visible joins, no wide level, and the delivered frames gated so the hair is never within 20 px of the top edge.

**Why:** rev 3 cut the top of his hair in 23 of 26 holds and he called the video "basically not usable"; rev 2 had 160–260 px of dead headroom; rev 1 used the wide kitchen shot he never wants. Rev 4 measured the hair itself and he approved it on sight.

**How to apply:** since 2026-09-12 the DELIVERED file is graded on this standard by the shared gate's five `framing:` rows (`.claude/skills/_shared/deliver/checks/framing.py`: mediapipe FaceMesh + Apple Vision person segmentation, no plan and no set-specific background; bounds per format in `formats.py`; it writes `<file>.framing_proof.jpg` at native scale — look at it). Proven on the corpus: fails rev 2 / rev 3 / the off-centre Short / the fixed-crop Ad 1 cutdown, passes rev 4–6 and Muhammad's Ad 2. For building the crop: `/ad-edit` Step 3 "FRAMING STANDARD" and lessons 107–109; `website-video/reference/recipe/hairdet.py` + `hairgate.py` remain that recipe's plan-side tools (they depend on the 8/28 door panel and only run there). The 1.85×/1.46× zooms are the 8/28 kitchen set's numbers; re-measure the zooms for a new set, keep the rule. **Editor cuts** (no crop plan, no door panel, e.g. the outdoor pool
shoot): `/revisions` `reference/framing.py` measures it per shot with MediaPipe Pose. Dan reinforced the rule on 2026-09-11 on
Zeeshan's ab wheel follow-along: "Crop in closer by 20-30%", with no excess space above his head or to the sides. Related: [[shorts-production-style]], [[cover-photo-selection]].
