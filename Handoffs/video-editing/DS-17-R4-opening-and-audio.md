# DS-17 R4 — full-screen jump-rope opening and cleaner audio

**Handoff requested by Dan, 2026-09-17. Recommended: GPT-6 Astra, high effort.**
This continues the reviewed R3, not a new first cut. No R4 edit has been made. Dan requested this handoff so a new task can finish the revisions. The previous task releases ownership here.

## Dan's feedback and scope

Dan called R3 “a good first effort” and requested:

- First approximately **4 seconds: full-screen footage of Dan jumping rope**, chosen for the strongest visible physique/definition and fastest clean skipping, to catch attention. Search the dedicated B-roll shoot, compare it with footage from this video's raw rolls, and use whichever looks better. The broader B-roll library has **not yet been searched**; C1674 is a known candidate, not a proven winner.
- Audio: **“For the audio I think it sounds decent but there is some room for improvement, like you're saying. Make the handoff document. Let's try to clean that audio up more and get it more up to Muhammad standards if that's possible here”**.

Keep the spoken cold open under the new B-roll. Preserve the remaining edit, script, later demonstrations, caption wording/timing and covers unless a necessary transition or verified defect requires adjustment. This is revision feedback, not final approval. No social upload or scheduling.

## Read first

Read `AGENTS.md`, `AI_COORDINATION.md`, `Handoffs/video-editing/00-RULES.md` in full (Codex column), its linked environment table in `Handoffs/handoff-20260914-ad3-square-codex.md`, and the original `DS-17-how-to-jump-rope.md`. Use `$abs-edit-organic` for source selection/audio/colour and `.claude/skills/shorts/SKILL.md` for vertical finishing. Dan's requested full-screen opening overrides the existing header/inset treatment for those first seconds.

Read `.claude/skills/_shared/audio/README.md`, the organic adapter's shared standards/workflow, and the current delivery gate README. Check ownership and the two-build limit before any rendering, transcription or QC. Raw footage is read-only. Git contains docs/scripts only; this repository is public. Use `login:false` for shell calls and narrowly scoped Git status (the workspace has a huge unrelated untracked inventory).

## Baseline and locations

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Working root: `/Volumes/Extreme/_edit_work/ds-17/`.
All paths below without a leading slash are relative to the project root.

- Reviewed master: `Short-form video content/ds-17_how-to-jump-rope.mp4`.
- Phone review: `Short-form video content/ds-17_how-to-jump-rope_REVIEW_540p.mp4` (540×960; AAC identical to master, derivation receipt beside it).
- Rebuild/evidence package: `Short-form video content/ds-17-support/`.
- Notes: `Short-form video content/notes-ds-17.md`.
- Muhammad/current audio comparison: `Short-form video content/ds-17-support/review/audio-AB.mp4` (Muhammad first, ours second).
- Covers: support `covers/instagram/` and `covers/youtube/`, A and B PNGs. Keep these.
- Audio and delivery gate JSON files sit beside the master; both honestly retain FAIL.

R3 is **1080×1920, 30000/1001 fps, 1354 frames, 45.1784667 seconds**.
Master SHA256: `9320c866a2a439247647e3a97ace5e04f82a7d10588cb2018effd94fe4fc36df`.
Freeze this exact R3 master, audio, map, scripts and evidence into `revisions/r3/` before editing; R1/R2 already have revision folders. Work in an isolated R4 copy so the review baseline remains reproducible.

## Opening: footage search and construction

Known raw source directory:
`/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/`.

- **C1670.MP4:** 85.5855 seconds, this short's spoken takes. Stored 3840×2160 with −90° rotation, so native **portrait** after autorotation. Actual audio is **stereo dual mono**, not the original handoff's generic four-track description. Source probe and microphone choice are recorded in the support package.
- **C1674.MP4:** 124.6245 seconds, landscape 3840×2160 jump-rope demonstration footage. Contains two-foot jumps, slow beginner skipping and fast alternating skipping. Existing selections include source ~16.016s (two feet), ~66.900–76s (slow/accelerating) and ~95.996s onward (fast alternating). View moving footage; timestamps alone do not establish the best opening.
- **C1669:** slate/false start according to the original brief.
- Existing small proxies: working-root `review/C1670-source.mp4` and `review/C1674-source.mp4`.
- Shoot script: `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt`, short section lines848–856; section8 lists B-roll. Also inspect footage indexes and dedicated B-roll folders across `/Volumes/Extreme` and owned assets. Do not assume a particular other shoot date before finding it.

Compare short moving excerpts for real muscle definition, flattering light, speed, clean continuous performance and usable full-screen vertical framing. Choose actual fast skipping; do not default to speeding it up or altering Dan's body. Keep face, torso and useful footwork visible. Some C1674 rope arcs already leave the original camera frame; cropping cannot recover absent pixels. Record winning source, in/out, crop and why it beats alternatives.

**Full screen means full-bleed 9:16 action, not the current square demo card under a black header.** Adapt/disable the global header/footer during the opening; captions must remain readable and avoid hiding the action. Real moving footage does not need the real-photo disclosure.

Current opening talking shot lasts **142 frames / 4.7380667 seconds**, source C1670 13.6469667–18.3850333. User requested first4 seconds; ~120 frames is4.004 seconds. Choose a clean boundary near4 seconds and avoid a distracting 0.7-second flash before the next existing shot. Document any necessary transition choice; do not silently extend the request to a long B-roll introduction. Preserve dialogue and overall timing where possible.

## Audio: what failed, what it means, and the next test

R3's exact-file delivery report: **35 PASS, one FAIL (`audio:stamp`), zero NOT MEASURED, three declared N/A**. The underlying audio failure is only the artifact comparison with Muhammad:

| Measure | R3 processed | This recording untreated | Muhammad reference |
|---|---:|---:|---:|
| Spectral flux | 0.0901 | 0.1036 | 0.072 |
| High-frequency swirl | 0.9556 | 0.9613 | 0.835 |

Both artifact bounds are reference ×1.10. These describe changes in the sound spectrum; they are not a diagnosis of audible damage by themselves. The processing improved these numbers versus this source, but not enough to meet the reference comparison. All other audio rows passed (roughly −14.2 LUFS, −2.2 dBTP; no detected clipping/clicks). Gemini found a natural, clear voice, but that does not overrule the gate or Dan's ears.

**We have not established that this is unfixable.** Earlier work stopped at the unresolved quality gate; it did not exhaust safe processing options. Different recording conditions may contribute to the comparison failure, but that is a hypothesis, not a proven explanation. Dan now expressly asks for another improvement attempt.

Current chain: shared `pick_lav.py` identified dual mono; the selected signal uses the mid of the identical channels. Shared `voice_chain.py --no-dereverb`, no music, no compressor. Source/untreated/voice WAVs and chain reports are in the working/support directories. The R1–R3 AAC tracks are identical (`records/all-revisions-audio-identity.json`).

Next task should:

1. Listen to the untreated source, R3 and the pinned Muhammad reference at matched perceived level. Identify the audible gap first: room, background noise, harshness, thinness, inconsistent levels, or another specific issue. Recheck source/mic evidence; do not sum distinct microphones or assume four channels.
2. Run shared audio `zsh selftest.sh` before the batch. Test a small number of meaningful candidates on representative phrases/pauses using the **existing shared voice chain and supported settings**. Include R3 as the control. Test gentle room/noise treatment only when the source and listening justify it. Do not write an unrelated custom chain.
3. Compare by listening as well as gate numbers. Preserve natural consonants/body and dynamics. Reject watery, metallic, pumping or over-suppressed results even if a metric improves. The shared README documents an earlier aggressive dereverb that Dan rejected as “underwater”; do not repeat it.
4. Render the best audible improvement, check duration/latency and caption sync, then re-gate the exact delivered file. Provide a short Muhammad / R3 / proposed comparison so Dan can hear the change. If there is no safe audible improvement, keep R3 as the fallback and explain exactly what was tried and the remaining limitation; do not pretend impossibility was proven.

Never raise a threshold to pass this file, fabricate a PASS, or misuse editor-origin `--reference-mix --verbatim` for our own raw-footage mix. If a shared implementation change is actually necessary, coordinate ownership and run the full quality regression corpus before committing it. Gate changes are not the first remedy.

Dan explicitly authorized **R3 flagged review delivery** (“Yeah send me the copy for review”), recorded in `records/review-delivery-authorization.json`. That was not final approval or blanket permission to suppress future failures. Keep any unresolved R4 failure explicit and follow the applicable review-delivery rule; complete all authorized revision/testing work before raising a remaining delivery boundary.

## Rebuild traps and evidence to preserve

The authoritative map is working-root `edit.json`, mirrored in support and `recipe/edit.frozen.json`. **Do not rerun `recipe/configure.py` over it**: that exploratory script predates final crop/tracking corrections. Read `recipe/README.md` and `PROVENANCE.md`.

- `recipe/build.py` has audio/picture/caption/finish stages. Changing it can invalidate all shot caches. Cache unchanged pictures; audio work does not require rebuilding them.
- `recipe/assets.py` / `assets/title.png` implement the global header. `assets/demo-frame.png` is the existing square-demo footer. Simply substituting a source shot will not make the opening full screen.
- Local source grade `assets/source-grade.cube` uses the8/28 S-Log3 conversion; preserve colour continuity and BT.709/tv handling.
- Wider talking shots are fixed; three tight shots have measured smoothing. Preserve the verified hair geometry (morning hair segmentation once mistook a tree for hair).
- Captions: 50 fixed chunks, Arial86 bold, margins100/140/320. Minimum duration is applied **before** the final clamp to the next cue; otherwise overlaps cause vertical jumps. Style is chunk-onset, not karaoke. Files: `caption-template.ass`, `caption-timing-ctc.json`, `caption-word-map.json`, `recipe/retime_captions.py`.
- R3's50 caption onsets passed a separate whole-word acoustic recomputation within34ms; no word mismatches. Independent full-size visual audit reported no defects, and every one of1354 frames passed the forbidden-screen/black-frame scan. Evidence is under `logs/`, `watch-r3/`, `review/ctc-validation-r3/`.
- `recipe/gate_plan.py` binds actual layout/windows and evidence to the master hash. Update opening layout expectations honestly. Do not reuse old hash-bound approvals for changed media. `recipe/phone_review.py` makes the phone copy with identical AAC and a derivation receipt.

## Finish and next action

**Start by freezing R3, claiming the revision, and finding/viewing the strongest jump-rope candidates.** Then run the bounded audio comparison while preserving R3 as the control. Review the new opening in motion and the opening-to-talking transition, captions and complete final video. Obtain the required independent audit and current exact-file audio/delivery stamps; preserve failures honestly.

Deliver R4 master, phone review, audio comparisons, stamps, notes and reproducible recipe. Send Dan the review through the current task; no public posting. Update only DS-17 in `jobs.json`/`00-MASTER.md` through the queue helper and its own coordination entry. Status remains review/revisions, not finalized until Dan explicitly approves. Never add a dashboard row unless asked. Commit/push only this task's docs/scripts, not private media or other sessions' pending work.

Starter prompt:
> Read `Handoffs/video-editing/DS-17-R4-opening-and-audio.md` and the referenced rules. Continue from the reviewed R3 using `$abs-edit-organic` and `.claude/skills/shorts/SKILL.md`. Find the strongest real jump-rope footage and make the first approximately4 seconds full-screen B-roll. Test a cleaner, natural audio treatment closer to Muhammad, comparing against R3 and preserving it as the fallback. Verify, deliver the revised review and audio comparison, and update the master list. Do not upload or schedule.
