CONTENT (SFC). Codex revisions recovery results, 2026-10-05.

# Outcome

Partial recovery. Tooling and a training writing sample delivered. Full review-method reliability and Claude parity are NOT established. Independent fresh blind passes: 0. Keep Claude Opus 5.5 high as the editorial default. No long-form substitution claim.

[Test revision Google Doc](https://docs.google.com/document/d/1sHfkjXSm7N_26PFp0b1QNp0cY1IjrPXZ0ZEImqf84xY/edit). Its title says TEST ONLY and it lives in a separate test folder. This verifies writing and native Doc output on an exposed case; it is not a passing production review. No editor messages. No sent Docs changed.

# What changed

The repository revisions skill remains authoritative. Its only editorial-file addition is a short link to implementation support. The installed Codex adapter is unchanged. No calibration, later-round rule or audio/delivery threshold was relaxed.

- Fixed `reference/framing.py`: preserve portrait, landscape, square, sample aspect ratio and rotation metadata instead of stretching everything to landscape. Preserve proof-thumbnail shape. Empty decodes and runs with no assessable subject raise an error.
- Added `reference/review_record.py`: check declared runtime coverage, join/AI/text inventories, evidence files, source hash and unresolved judgments. Freeze notes and private summary before revealing a benchmark. Reject exposed blind cases and overwrite attempts. It explicitly cannot judge whether a reviewer actually inspected the evidence or whether the editorial decisions are correct.
- Added focused geometry and evidence-record tests, plus `reference/REVIEW_EVIDENCE.md` next to the authoritative skill. Support is scoped to execution and receipts, not a second review manual.

# Known-case regression

Muhammad, DS-11 Why You Must Weigh Yourself Daily V2, round 2. Archived October 2 file, not verified as the newest Drive export. Duration 47.4474 seconds, 1080x1920, 29.97 fps, 19,692,661 bytes, approximately 3.32 Mbps.

SHA256: `764381578f902a06f36c29a5a0af8ab600d03f57bf0db9da9719eaefd1be5d23`.

| Required action | Recovery evidence | Remaining limit |
|---|---|---|
| Presenter cuts at 5.1, 7.6, 18.7, 35.6, 40.9 | Native frames and strips show position changes with similar composition; all five included in training sample | Full moving/audio context and complete actual-join inventory remain unfinished; 5.1 is subtle |
| Scale edges at 10.1-16.1 | Native edge crop shows thin grid strips on both sides | No claim that every insert edge has had an exhaustive native pass |
| AI ending at 33.6-34.8 | Native frames show mouth opening and gaze turning away after a closed-mouth/downward state | Full source-skill playback, consecutive ending frames and region pass are incomplete |
| Late key point | Absent at 39.6/40.85; empty panel entering at 41.0; text begins later. Local transcript starts the phrase at 39.58 | External audio estimate differs by about 0.3 seconds; no direct Codex listening claimed |

The sample uses exact repairs, bold actions and Dan's required standing-rule wording. It does not reopen the accepted graph, demand a questionable scale decimal change, or turn detector candidates into editor items. No title/hair claim added. Round-2 audio restraint retained: -13.30 LUFS, -0.90 dBTP, zero clipped samples, 51 ms room. The full audio gate still reports FAIL; that has not been relabeled PASS.

# Audiovisual method test

Codex received overview stills, targeted native frames/crops, local transcript and numerical audio reports. It did not directly watch continuous motion or listen to the file. Two external video attempts and one audio-only attempt were recorded:

1. Gemini 3.1 Pro preview, full original video, requested 24 fps: request timed out after 180 seconds. No answer or usage receipt. Billing unknown; $1.50 budget reserve retained.
2. Gemini 3.8 Flash, full original video, requested 24 fps: completed with 76,738 input tokens, 4,873 answer tokens and 1,080 thought tokens. Cost estimate from returned usage: $0.079877. Its chronological account covered the runtime, but it identified none of the eight required repairs (five joins and three other corrections). It missed the borders, described the changing AI face as static and did not diagnose the late graphic. Its only issue was tiny graph labels, which are accepted prior work. This supporting review FAILED. Its clean result cannot clear the cut.
3. Gemini 3.8 Flash, complete extracted audio-only WAV: completed, usage explicitly contains 1,187 AUDIO tokens. Estimated cost $0.009344. It supplied a full interval account and speech timing, but inferred a visual punch-in and a treated booth from audio alone. Those claims are discarded. No new editor demand is based on this answer.

Recorded successful-call total: $0.089221. The timed-out call's actual cost remains unknown. Stated batch estimate was $3 with a $5 approval threshold; no further generation runs planned.

The actual coverage record remains incomplete. Its validator exits 1 and refuses a blind freeze. Required unresolved work includes full native AI ending/region inspection, every actual join in moving/audio context, and all full-resolution text panels. The new receipt tool exposes this failure; it does not repair editorial perception by itself.

# Fresh benchmark discovery

Metadata-only Drive searches and local review filenames located the September 26, September 29, October 1 and October 2 Muhammad shorts reviews. Their relevant answers appear in required calibration/reference material or in the original failed test. The entire October 2 batch was exposed previously. None was called fresh. No current answer from an eligible new case was opened because no eligible pair was identified.

An asynchronous request to Dan asks for another delivered short, editor, round and matching Claude revision Doc. This is missing benchmark input, not a request for permission. Use at least two consecutive genuinely unseen passes before recommending routine substitution. Preserve necessary previous-round instructions, but seal the current answer until notes, private summary and complete coverage are frozen.

# Verification

- Geometry: 2 tests passed, including five real decoded shape/orientation fixtures and invalid-input failure.
- Evidence record: 9 tests passed, including coverage gaps, changed source, missing AI ending, unresolved judgment, missing proof, exposed benchmark and no-overwrite freeze.
- Shared audio self-test: PASS.
- Watch scan: 4 tests PASS. Existing excerpt fixture path was a flattened symlink; created a 30-second scratch fixture from the real approved source and supplied it to the tests without editing the shared fixture.
- Optional broad corpus: initial normal run blocked by the existing fixture path. A later corpus-only run was stopped after roughly 12 minutes while testing unrelated long-form exports. Partial log retained, including existing gaps and pending checks. No full corpus PASS claimed. Shared audio/delivery gate code was not changed.
- Doc: public reader permission; anonymous Markdown readback; exact text match against source HTML; H2 title; 11 native bullets, 7 nested bullets, 10 bold spans; visual first and final portions inspected; zero em or en dashes. No replacement asset links needed because actions reuse the cut's footage and graphic.
- Code committed as `4cc41ec`, pushed through merge `87057cf`. The later descendant `ed8459c` reached SUCCESS on all three Railway services. Live site returned HTTP 200. Final report/sample push is also checked after delivery; receipts remain in scratch. No app behavior changed and no native retest trigger.

# Files and exact next action

Evidence: `/Volumes/Extreme/_edit_work/codex-revisions-recovery-20261005/`. Includes requests, responses, usage ledger, native frames, manifests, rejected coverage record, test logs, comparison and Doc-verification receipt. No media committed.

Sample Markdown: `revision docs/TEST-ds11-recovery-muhammad-round2-10-5-26.md`. Separate private summary and unsent message example: same basename with `.summary.md`.

Next: obtain an eligible delivered short/reference pair, establish trustworthy complete motion review that detects the known defects without hints, then perform and freeze a fresh review before opening its Claude answer. Do not treat this report, the sample or the external model's clean answer as evidence that parity has been achieved.
