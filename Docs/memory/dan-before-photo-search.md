---
name: dan-before-photo-search
description: "Exhaustive search for a \"before\" photo of Dan at ~200 lbs — what exists, what doesn't, and the best candidates"
metadata: 
  node_type: memory
  type: project
  originSessionId: b011a067-567b-428f-b6b0-df0e2af8defc
  modified: 2026-08-06T19:53:47.146Z
---

Searched 2026-08-06 for the heaviest/worst-looking shirtless photo of Dan to use as an ad "before" image (he's 179 lbs now, started ~200).

**Sources searched (exhaustive):** Photos library — all 1,441 photos of Dan dated pre-2026, pulled via the Photos SQLite face index (`ZPERSON.ZFULLNAME = 'Daniel Rose'`, Z_PK 2, 1,647 face detections); the 2022 PhoneRescue export at `~/Documents/PhoneRescue-Export-2022-05-24` (616 camera photos + 1,526 message attachments).

**Key finding — his heaviest era is 2022–2024, NOT earlier.** In 2020–2021 he had a visible six-pack (library indices 0121, 0131). 2019–2021 is ruled out as a "before" source. Photo counts by year: 2020=156, 2021=145, 2022=208, 2023=121, 2024=298, 2025=244.

**Sample-bias caveat that matters:** Dan avoided the camera shirtless at his heaviest, and the library confirms it — **no photo exists of him at his genuine heaviest with his shirt off.** The best candidates are all from mid-2024 when he was already training. If a search "fails" to find something heavier, that's the reason; don't keep re-searching.

**Best candidates (exported to `before-photo-candidates/` in the project):**
- **A — library idx 0740, 2024-07-02** (⛔ Dan 2026-09-30: NEVER use as a before picture, see [[standard-before-picture]]), standing front-on in a bathroom, arms down, NOT flexing. Best composition by far, and matches what the transform pipeline handles best (full torso, front-on, arms down).
- **X — idx 0745, same day, minutes apart, flexing.** The A/X pair is the strongest creative angle: same body, same light, same day, radically different read.
- B — patio deck chair (phone export `cand_0230`); C — idx 0732, 2024-05-20 pool; D — idx 0425, 2022-06-21 (only a 480px thumbnail survives — too small to use); E — 2024-08-24 beach cabana (full-res original is local).

**Message attachments were a dead end** — 1,526 images, overwhelmingly memes/screenshots; the ~10 shirtless shots of Dan are all Belize/cruise 2022 and show him athletic.

**Technical notes worth keeping:** 910 of 1,216 originals are iCloud-only (Optimize Mac Storage), so scanning must use `resources/derivatives/<X>/<UUID>_1_105_c.jpeg` (1024px, full coverage) rather than `originals/`. Reading the library at all needs Full Disk Access granted to **Claude** (`/Applications/Claude.app`) — granted 2026-08-06, took effect with no restart. See [[photo-edit-recipe]] and [[repo-is-public]] (don't commit personal photos).
