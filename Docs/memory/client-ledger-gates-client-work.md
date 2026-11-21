---
name: client-ledger-gates-client-work
description: "11-19 client work: every client instruction itemized in his exact words in CLIENT-LEDGER.json the turn it arrives; client_ledger.py gate must pass before build, review, Dan's page and any send"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c4cd1986-547c-4ffe-aced-696764bb1f6c
  modified: 2026-11-19T18:39:48.040Z
---

For any client job (SRM agency, Upwork, client VSL), every instruction the client writes (brief, feedback doc, message, picks) and every promise we send back goes into `CLIENT-LEDGER.json` in the job folder, in the source's exact words, the same turn it arrives. Run `.claude/skills/client-vsl/tools/client_ledger.py gate <job> --stage plan|build|review|deliver`; a failing gate stops the work. Method: `.claude/skills/client-vsl/reference/CLIENT-LEDGER.md`.

**Why:** On the Joint Vigor VSL (client Eric, Upwork), his detailed feedback doc on the trial lead (11-09, plus a reference he added 11-10) was promised three times and never built into the full film sent 11-18. Dan, 2026-11-19: "a catastrophic, potentially job-ending and upward career-ending mistake"; "I want to improve our client video editing skills so that we never miss critical feedback like this again." Traced causes: the notes lived only in his Google Doc; each round was planned in a fresh chat from the previous handoff plus his newest message, and each handoff dropped something; the round structure only carried answers to our own A/B questions; the trial lead was labelled "approved by Eric" when he had only paid the $5 milestone and Dan had approved it; six independent reviews and Dan's review page compared the film with our plan, never with his doc.

**How to apply:**
- At the start of every round and every new chat on a client job, read the client's thread yourself to the newest message and fetch his linked docs again (he edits them). Never plan from a handoff's summary alone.
- Never write "approved by the client" without his quoted words. A paid milestone, Dan's approval, "sounds good" and silence are not approval. Trial or sample footage is our draft; his feedback on it is the build list.
- Notes that need no option still get an owner: show them back to him on the next review page and put them in every brief.
- The independent reviewer and Dan's review page get the client's own notes, each with its film time.
- The delivery message answers his notes one by one. Nothing is sent before `gate --stage deliver` passes.
- Only the client's own written words can drop one of his notes.

Related: [[no-next-round-until-review-finished]], [[model-proven-funnels-exactly]], [[do-the-next-step-and-contact-support]].
