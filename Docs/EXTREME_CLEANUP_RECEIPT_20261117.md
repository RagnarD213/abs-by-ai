# Extreme drive cleanup receipt, 2026-11-17

Handoff: `Handoffs/handoff-20261117-clear-extreme-drive.md`. Done from the M6 with commands on the M2.

## Result

| | Free space on the Extreme |
|---|---|
| Before (morning of 2026-11-17) | 28 GB |
| After (8:30 PM Central) | 850 GB |

**The 1 TB target was not reached (150 GB short).** The 8/28 or 9/23 raw-shoot clear handoffs (229 GB and 195 GB, see below) each close the gap by themselves.

The jobs listed below total 632.7 GB removed from the Extreme. Free space rose by 822 GB, so about 190 GB of the gain came from other sessions' deletions during the day that I did not make and cannot itemize.

## Blocker fixed

`jobarchive.py` stopped every night on `review reference evidence incomplete: ... AbsByAI Reviews/9717/manifest.json`, a review whose folder no longer exists. A review with no folder is now treated as retired (commit `ab99f13`). I also added a Dan-approved explicit mode: `run --approved "<jobs>" --keep-file JOB:path` moves only the named jobs, skips the idle and reference guards for them, and removes the source only after the Seagate copy is re-read in full by SHA-256. Selftest passes (16 tests locally, OK on the M2). The new code is installed at `~/.absbyai-jobarchive/jobarchive.py` on the M2. The nightly LaunchAgent (`com.absbyai.jobarchive`) is unchanged and still loaded.

## Safety check that paid off

The first attempt on **ro01** stopped twice: "last removal check changed", then "verify failed: file set or bytes differ; source kept". The Seagate copy of `RO01_MASTER_R2.mp4` was corrupted (same size, different bytes, SHA-256 `9a6a1504...` against the recorded `6d515335...`). This is the same Seagate corruption pattern as Nov 1 to 3. The source was kept both times. I re-copied that file from the Extreme, confirmed its SHA-256 matched the manifest, and re-ran the move. It then verified all 6,110 files and removed the source.

## Jobs moved (Seagate copy re-read by SHA-256, then the Extreme copy removed)

Each job's per-file SHA-256 receipt is `.jobarchive-manifest.json` inside its Seagate folder, plus one line in `/Volumes/Expansion/_finished_edit_jobs/index.jsonl`. Restore any job with `jobarchive.py restore JOB`. These moves relied on the Seagate copy alone, as the explicit mode allows. No second copy exists. Seagate path is `/Volumes/Expansion/_finished_edit_jobs/m2-Extreme/<JOB>`.

| Job | Files verified | GB |
|---|---|---|
| website-video-828 | 4,195 | 27.9 |
| ro01 | 6,110 | 18.2 |
| sl03 | 7,672 | 16.8 |
| ro08 | 8,332 | 15.7 |
| ro10 | 1,006 | 23.8 |
| ro16 | 607 | 26.3 |
| ra04 | 3,691 | 7.8 |
| RO-25 | 9,676 | 6.0 |
| ra07 | 2,639 | 6.8 |
| RO-17 | 7,198 | 44.1 |
| ro17 | 19 | 0.7 |
| SL-19 | 693 | 1.9 |
| sl09 | 26,171 | 41.1 |
| SL-15 | 2,498 | 5.6 |
| RO-14 | 26,913 | 47.2 |
| sl06 | 9,015 | 29.7 |
| SL-17 | 1,131 | 4.2 |
| sl08 | 6,542 | 14.8 |
| SL-16 | 3,081 | 7.6 |
| ro27 | 7,362 | 14.4 |
| SL-11 | 9,288 | 11.6 |
| RO-30 | 5,163 | 6.1 |
| DS-42 | 9,550 | 105.3 |
| DS-38 | 9,140 | 149.1 |

(The index also shows DS-108 at 63.0 GB, but that was the M6's internal copy moved by its own nightly job, not the Extreme.)

Small files that other things still point to were written back in place after removal (they survived, checked):
- DS-38: `r3/analysis/independent-off` (125 files)
- RO-14: `round2/veo/A2-flow-t1.mp4`
- ra04: `round2/frames` (240 files)
- ra07: `r1_chain_b.sh`

Clip-library catalog `source_path` values that name a moved folder are provenance only. The permanent library copies (`Abs By AI - Video Asset Library`) were checked and were not touched.

## Kept on the Extreme, and why

Active or recent work (changed in the last two weeks, or in production, review or setup):
- WV-03 (109.7 GB, active), SRM-goldenroots-jointvigor (188 GB, Joint Vigor), DS-106 (125.5), DS-107 (108.2), DS-108 (105.4), DS-109 (150.3), DS-30, DS-50, DS-51, SL-36, FLOWCLIPS, REALDEMOS-B02, B03, B08, B09 and the `*-setup` folders: all changed within days or have setup/waitlist work open on the board.
- RO-15 (63.9, waitlisted Dec 23), RO-32 (24.8, queued Jan 29), SL-12, SL-13, DS-77, DS-34-r2-keycache (33.8): recent, with setup or release pending.

Referenced by a skill, script or standing rule:
- `kit9x16` (115.9, shared 9:16 reference kit), RO-22 (46.6, technical hold, checkpoint in `RO-22/setup/RESUME.md`), RO-23 (48.3, queued Nov 22), wv01-edit (47.7), DS-40-codex (74.7), SHOOT-20261023 (40.4), abwheel, ad1-8-14, ad2-vert-v2, ad3-vert, ads234-8-14 (66.9 together), plus about 30 small folders under 7 GB each.

Raw shoot folders at the drive root were not touched:
- 8/28 (229 GB) and 9/23 (195 GB): both already verified on the Seagate and Google Drive. Their clear handoffs are gated on the edits that still need them: `Handoffs/handoff-20261117-clear-828-shoot-from-extreme.md` and `Handoffs/handoff-20261117-clear-923-shoot-from-extreme.md`.
- 11/13 (262 GB), 10/15 (224 GB), 10/23 (88 GB): still have open jobs, so they stay.

## Next 150 GB if Dan wants 1 TB before the shoot clears

Candidates I did not move without a named approval: DS-40-codex (74.7 GB, long since published), the five ad folders (66.9 GB, since no new Abs By AI ads are planned) and wv01-edit (47.7 GB). All three are referenced by rules or skills, so each needs a look at what points at it first.

## Housekeeping

The three SanDisk installer files named in the handoff (step 6) were not on the drive root, so nothing was deleted there.
