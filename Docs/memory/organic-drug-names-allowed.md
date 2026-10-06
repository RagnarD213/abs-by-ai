---
name: organic-drug-names-allowed
description: "Dan 2026-09-30: organic videos may say and subtitle Zepbound, tirzepatide, GLP-1; the no-brand-name rule is for ads only"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 9f946bc2-2e17-400e-84c8-5d92b39c9af2
  modified: 2026-09-30T21:57:31.415Z
---

Organic content videos may say and subtitle Zepbound, tirzepatide, GLP-1 and other drug names. Dan (2026-09-30, on RO-12): "I plan to make a lot of organic videos where the entire topic of the video is Zepbound. Organic videos can say Zepbound, Tirzepatide, GLP-1, or any of those." The "weight loss medication only, never a brand name" rule stays for ADS.

**Why:** many planned organic videos are about Zepbound itself; the ad rule was leaking into organic through the delivery gate (`compliance:drug_names`, `srt:shape` banned spelling on `longform`).

**How to apply:** never rewrite or bleep drug names in organic speech or subtitles. Until the gate is changed (corpus + GATE_VERSION bump, planned in the RO-12 round-2 handoff), report those two rows as the known mismatch. On-screen graphics on organic videos: not yet ruled, keep brand names out until Dan says so. Also: never tell viewers to "empty the entire vial" (non-standard doses don't). Rule text: `.claude/skills/_shared/VIDEO-RULES.md`. Related: [[ad-copy-no-unbelievable-claims]], [[ads-never-organic]].
