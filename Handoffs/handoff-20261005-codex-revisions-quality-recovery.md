CONTENT (SFC). Repair Codex revision reviews and prove parity with Claude.

# Codex revisions quality recovery

Written: 2026-10-05. Requested by Dan after the first adoption test failed.
Recommended executor: Codex GPT-6 Astra, high effort, continuing the original adoption handoff's specific routing for this capability test. Claude Opus 5.5 high remains the established editorial default until the evidence supports changing it.
Task name: Codex revisions quality recovery. When reviewing a particular editor's cut, follow the source skill's editor naming convention.

## Goal and scope

Make Codex execute the existing revisions skill to Claude's demonstrated standard, then prove that with a fresh blind test and an editor-ready sample. Do the work, not just propose another checklist. Do not message any editor. Do not edit or replace a sent revision Doc, re-render a delivered video, or publish content. The test is private.

Keep `.claude/skills/revisions/SKILL.md` as the single authority. The adapter at `~/.codex/skills/revisions/SKILL.md` must stay thin. Do not copy calibration into it, relax review requirements, or invent new editorial rules to make the test pass. Fix execution and tool support first. Any necessary shared implementation instructions belong beside the authoritative skill, with a short reference from it, not a competing Codex review manual.

## Read first

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

1. Re-read `AGENTS.md` and `AI_COORDINATION.md`; respect concurrent ownership. Victory Dashboard remains paused.
2. Read `.claude/skills/_shared/VIDEO-RULES.md` in full before media work.
3. Read `~/.codex/skills/revisions/SKILL.md`, then the entire repository `.claude/skills/revisions/SKILL.md`, including all calibration passes and required references.
4. Read `.claude/skills/_shared/CUT-CONTINUITY-QC.md` and the reference/tool files actually used. Follow the original adoption handoff's memory and asset reading list.
5. Read `Handoffs/handoff-20261005-codex-adopt-revisions-skill.md` and `/Volumes/Extreme/_edit_work/codex-revisions-adoption-20261005/adoption-report.txt`.

Protect the fresh benchmark: choose it before opening any more example revision Docs. The required source skill itself contains historical examples. Any video whose answer appears there is a training example, not an unseen test.

## Completed work: preserve it

- Thin adapter installed and official validator passed. No source review rules changed.
- Google Doc route passed: repository `reference/md_to_docs_clipboard.py` conversion, rclone HTML import with BOTH `--drive-import-formats html --drive-export-formats html`, anyone-with-link access, anonymous Markdown export verification, test Doc trashed.
- rclone is `/Users/danielrose/bin/rclone`; ffmpeg/ffprobe are in `Media/video_edit/bin/`. rclone currently warns of shared-client retirement. If authentication/import fails, investigate and use the documented browser-paste fallback; never expose credentials.
- Original bookkeeping commit: `81c7a3a407cecb402bcd049e36c84dc57ea817ff`. All three Railway services reached SUCCESS; site returned HTTP 200. Do not repeat installation or disposable Doc tests unless your changes require it.
- Evidence directory: `/Volumes/Extreme/_edit_work/codex-revisions-adoption-20261005/`. Includes `cold-findings.txt`, `cold-freeze.json`, `adoption-report.txt`, audio/scan results and crops. Keep media and scratch evidence outside Git.

## What failed

Training video: Muhammad, Why You Must Weigh Yourself Daily V2, round 2, 47.4474 seconds, 1080x1920 at 29.97 fps.
Local source: `/Volumes/Extreme/_edit_work/revisions-20261002/muhammad/dl/ds11_weigh_v2.mp4`.
SHA256: `764381578f902a06f36c29a5a0af8ab600d03f57bf0db9da9719eaefd1be5d23`.
This is an archived October 2 delivery, not a verified current Drive export. Searches did not locate Muhammad's Daniel HQ folder reliably.

Codex relied too much on detected boundaries and overview stills. Full audiovisual playback was not completed. Claude's finished notes do not establish exactly what tools Claude used; compare observable results, not imagined methods.

| Defect | First Codex result | Confirmed reference |
|---|---|---|
| Same-framing presenter cuts | Shared matches at 18.7 and 40.9; incomplete inventory | Also 5.1, 7.6 and 35.6; inspect all actual joins and zoom behavior |
| Thin side borders | Missed | Grid strips beside insert at 10.1-16.1 |
| AI face behavior | Missed | Mouth movement and looking away at 33.6-34.8 |
| Graphic timing | Missed | Key point appears near 41.0, phrase starts near 39.6 |
| Graph numbers | Flagged discrepancies | Visible, but Claude credited graph as fixed; rule 42 governs reopening accepted work |

Other Codex candidates, including additional detector cuts, title/hair overlap and a hard-to-see scale decimal, were not established editor items. Apply the false-positive protocol. Extra findings do not cancel missed defects.
Audio measurements were useful, but the full gate did not pass. Round-2 rule 22 prevented unnecessary new audio demands. `framing.py` stretched portrait input onto a landscape analysis canvas; its crop recommendations were not trustworthy alone. Fix or bypass this distortion with a verified method if still present.

## Work sequence

### 1. Establish an honest, complete inspection method

Inspect available tools and current review scripts before building anything. Find a practical way to cover the entire video, motion and speech timing, audio, every join, full-resolution edges/text, and every AI shot including its ending. Sparse screenshots, a transcript, or an automatic SUCCESS flag cannot stand in for this.

State what the model actually receives. Opening a player or letting it run does not prove the model saw motion or heard audio. If native audiovisual input is unavailable, establish and test a supported alternative that covers the required judgments. Existing authorized Gemini video/audio review may support this, with estimated cost stated first and the standing $5 batch approval threshold respected. Label external review evidence honestly; a Gemini clean result cannot override visible defects. Do not claim direct listening based on waveform measurements.

Make failures impossible to silently mark complete: preserve a compact coverage record of time ranges, actual joins, AI shots, text panels, spoken/graphic timing and unresolved judgments. Do not replace the source skill with a new checklist. Reuse its requirements and existing tooling. Fix meaningful tooling defects with appropriate tests; keep this scoped to reliable reviews, not a new video platform.

If no available method can complete a required judgment, record exactly what is unavailable. Continue independent improvements, but do not declare parity or production readiness.

### 2. Repair the known-case execution

Reinspect DS-11 using the complete method. Recover and independently verify the missed defects with precise evidence. Also apply the source skill's restraint to unsupported or previously accepted issues. This is a training/regression case, not a blind pass, because its findings are known. Verify the corrected method covers the whole short, not merely the known timestamps.

### 3. Run a genuinely fresh blind comparison

Use a different delivered short with a completed Claude review and verified matching editor, round and video version. The entire October 2 Muhammad shorts document and its summary were opened during the first attempt, not just DS-11. Treat that batch as exposed for this recovery; prefer another delivery/batch absent from the source skill's examples and the first report.

Identify the cut and reference location from metadata without opening its current answer. Read legitimate previous-round instructions when the source skill requires them. Do not hide the revision history needed to judge a later round. Keep the current-round benchmark sealed until the candidate review is frozen.

Record source ID/path, version, duration and SHA256. Complete the review and source skill's full self-check. Save and hash the proposed editor notes, private summary and coverage record before reading Claude's matching current-round notes. Then fetch the live reference, noting possible later edits, and compare required actions against the exact video.

For each agreement or difference record: timestamp, visible/audible evidence, applicable source rule, whether a required correction was missed, whether Codex added an unsupported demand, and the consequence for the editor. Claude's notes are a benchmark, not automatic truth. Resolve disagreements from the footage and Dan's established rules.

If the test fails, fix the cause and use a new unseen short for the next blind attempt. Rechecking the revealed answer is regression testing only. Prefer two consecutive fresh passes before recommending routine substitution; do not generalize a shorts result to long-form reviews. Respect spend limits and record all attempts, including failures.

### 4. Prove the final writing and document output

For a passing case, produce the source skill's complete editor-ready notes and separate private summary, including its specified status handling and paste-ready message. Do not send the message. Create a clearly named test Google Doc in a test destination, with the required sharing, leaving existing sent Docs untouched. Keep test labeling outside the editor prose. Save the matching Markdown and summary; verify native formatting, exact content, links, nesting and Dan's voice. Run the full calibration self-check and punctuation check. No em dashes or en dashes in new writing.

## Pass criteria and delivery

A pass requires complete evidence coverage, all adjudicated required corrections found, no unsupported revision demands, correct treatment of accepted prior work, and a verified document that follows Dan's format and voice. Matching the number of bullets is not enough. No pass with unresolved audiovisual coverage. State the actual number of independent fresh passes and the scope supported by them.

Deliver a concise report to Dan: what changed in the method, recovered training defects, each fresh test result, false positives and misses, remaining capability limits, costs, and test Doc link. Do not claim Claude parity if the evidence still fails. Preserve detailed receipts outside the always-loaded board.

Commit and push task files under project rules. Shared files must be pushed immediately when edited. In the main checkout use `scripts/git/safe-push.sh -m "message" -- <explicit task files>`, follow its stale-file policy, confirm Railway deployment and live site. Never commit media or unrelated work. Re-read the board before changing your entry and run `scripts/board-check.sh`. Mark this handoff executed with the true outcome when finished; no Victory Dashboard update.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20261005-codex-revisions-quality-recovery.md` and execute it. Fix the incomplete inspection method, verify the known DS-11 misses, then run genuinely fresh blind comparisons against Claude's revisions. Keep the repository revisions skill authoritative and its Codex adapter thin. Do not call a known-answer recheck blind or claim motion/audio coverage without evidence. Deliver the tested method, results, and a verified sample revision Doc in my voice. Do not message any editor or modify sent Docs. Use GPT-6 Astra at high effort.
