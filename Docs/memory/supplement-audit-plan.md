---
name: supplement-audit-plan
description: "July 16 2026 plan — Decision Counsel eliminated, replaced by photo-based AI Supplement Audit; handoff in repo, not yet executed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0c0072b3-e2f4-4869-b2c2-ef3bf721d435
---

Decided July 16 2026: [[decision-counsel]] is eliminated as a product and replaced by
the **AI Supplement Audit** — users photograph each supplement label, AI reads them,
pulls existing context (physique photos, trainer/nutrition intakes, logged meals),
asks budget/max-servings/medications/caffeine, and returns a keep/drop table with
monthly savings plus a generic-ingredient recommended stack ("Recommend a Brand"
button per item for specific picks). Members-only with savings-total teaser; the
five-seat Counsel engine and `counsel_sessions` table are reused invisibly.

Full spec: repo `HANDOFF_supplement_audit.md` (rewritten July 16, supersedes the
July 11 text-only version — old version is in that file's git history once committed).
**Not yet executed.** Recommended executor: Opus 4.8 high effort. Ship gates: eval
canaries (St. John's Wort + SSRI, fish oil + warfarin must rate RED).
