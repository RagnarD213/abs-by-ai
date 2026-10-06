---
name: shared-fix-may-not-reach-the-pipeline
description: Fixing a shared module proves nothing until you check the batch pipeline for a fork and for hardcoded parameters in the caller
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4ca5bd1f-f3fb-45ac-8b45-7db227dec7e6
  modified: 2026-09-09T15:38:13.019Z
---

On 2026-09-09 the shared dereverb's defaults were corrected and the spray-tan batch still rendered
the rejected sound. Two independent reasons, both invisible from the shared module: the pipeline
kept a **forked `work/dereverb.py`** at the old settings, and `render.js` called that fork **and**
passed the rejected numbers on the command line. Separately, `finishaudio.py` fitted its own seven
octave bands while the shared gate grades ten, so it reported 0.25–0.30 dB while the gate measured
2.6–4.8 dB — and the batch had shipped with no gate stamp at all.

**Why:** AGENTS.md's "one module, extend with a flag" describes the intent, not the disk. Skills
accumulate local copies during a build, and a copy that was correct when it was made goes stale
silently — nothing errors, the numbers just stay wrong.

**How to apply:** before believing a shared fix has landed in a batch, `find` the project for
same-named forks (`find . -name "<module>*.py"`), grep the caller for hardcoded parameters, and
check that the corrector and the gate measure the *same* metric — a stage that reports a number
the gate does not use is a stage fitting the wrong target. Then re-run `selftest.sh`. Related:
[[gate-the-harm-not-just-the-fix]].
