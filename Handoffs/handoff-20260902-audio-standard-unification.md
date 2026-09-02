# Handoff — ONE audio standard for every video skill, so "bad audio" cannot ship again

**Created** 2026-09-02 by Claude Code (Fable 5.1) · **Status: PHASES 1–2 EXECUTED 2026-09-02 (Fable 5.1); Phases 3–4 open**

> **Executed:** `.claude/skills/_shared/audio/` exists (README there), `selftest.sh` is green on all six
> cases, and the four build skills are wired (shims, `audio_source.json` readers, `require_stamp` in every
> QC and deliver script, SKILL.md edits, shorts README index corrected). Two table rows were corrected from
> measurement (TP limit −1.0 on the delivered file; "not crushed" gates speech spread, not LRA) and a comb
> row was added — see the module README. **Still open:** Phase 3 (findassets, revisions, editor-brief,
> youtube-packaging, make-ad, exercisegeneration) and Phase 4 (re-render the Zepbound + supplements Shorts
> through the module; then the memory/AGENTS/handoff clean-up at the bottom).

Supersedes items 3–4 of `handoff-20260902-shoot-audio-standard.md` (promote the gate everywhere,
measure on new shoots). Items 1–2 of that handoff (re-render the Zepbound + supplements Shorts)
become Phase 4 here and run through the new module instead of a hand copy.

## The one-sentence rule

**Every video we render takes the LAV TRACK ONLY, as mono, duplicated to centred stereo, then goes
through ONE shared voice chain and ONE shared gate measured against Muhammad's
`this picture got me abs | muhammad | 16x9.mp4` — and no QC or delivery script in any skill will
pass a file that does not carry that gate's stamp.**

## What is actually wrong today (measured 2026-09-02, not argued)

1. **Nineteen audio scripts across five skills, no shared module.** Six are byte-identical copies,
   three pairs share a filename with different behaviour (`finish_audio.py` in longform-edit is a
   full chain; in shortad-from-longform it is loudnorm only). A fix lands in one and not the others.
2. **The right-channel rule is written in four SKILL.md files and still bypassed by code.** Four
   render scripts pull audio straight off the roll with no channel selection and encode `-ac 2`:
   `shorts/reference/scored-source/render.js:198`, `shorts/reference/full-bleed/render.js:132`,
   `longform-edit/reference/build_graded.py:28`, `longform-edit/reference/build_split.py:39`. Five
   `composite_*.py` scripts `-c:a copy` whatever they are handed. `findassets` cuts raw-roll clips
   for third-party editors with no channel rule at all.
3. **"Right channel" is the wrong rule for the 8/28 shoot.** Those rolls are FOUR mono tracks with
   the lav on `a:1`; `pan=mono|c0=c1` on them takes `a:0` — the far mic, 7.2 ms late and
   polarity-inverted — or renders silence. Only `ad-edit/reference/website-video/base.py` handles it.
   `revisions/reference/chan_align.py` exits "not stereo — nothing to compare" on those files, so the
   review gate reports nothing wrong.
4. **Three separate reference gates, none shared, one not even wired.** `voice_ref_check.py`
   (ad-edit: tone, floor, dryness, L/R), `audiogate.py` (shorts: EDT reverb, shape, floor),
   `qc_style.py check_channels` (longform: SNR, L/R). `shorts/SKILL.md:235` says `audiogate.py` "is
   wired into `qc.js`" — **it is not; no `qc.js` anywhere references it.** shortad's SKILL.md
   describes a mandatory "check 16" that its `qc.py` does not contain.
5. **The reference file moved today and every gate broke.** Dan put the two files into a
   `this picture got me abs/` subfolder at 16:54; `voice_ref_check.py` and `audiogate.py` hardcode
   the old path and now crash with "No such file". The older reference (`Daniel HQ Fitness AD
   Video v3 HD.mp4`, used by the Zepbound and clean-master chains) is not on disk anywhere.
6. **A stale index recommends a broken pipeline.** `shorts/reference/README.md` still says
   `full-bleed/` is "the more complete pipeline" and never mentions `clean-master/`, `zepbound/` or
   `spray-tan/`.

## The standard — Muhammad's file, measured

| what a listener hears | metric (finished file, 20–140 s) | Muhammad | our Ad 2 rev 2 today | gate |
|---|---|---|---|---|
| one voice, not two mics | L/R correlation at lag 0 | +0.993 | +0.992 | ≥ +0.97 |
| a dry room | early decay time after a word (ms to −20 dB) | 40 ms | 45 ms | ≤ 55 ms |
| tone | 10-band speech spectrum vs his | 0 | mean 0.54 / max 1.13 dB | mean ≤ 1.2, max ≤ 2.5 dB |
| clean between words | voice-over-floor per band (80–250 / 250–1k / 1–4k) | 27.6 / 34.7 / 28.0 dB | −0.5 / −0.9 / −1.4 vs his | within 3 dB of his |
| words stop cleanly | level drop 64 ms after a word | 7.4 dB | 7.4 dB | ≥ his − 1.5 |
| loud enough | integrated loudness | −18.2 LUFS | −14.4 LUFS | **−14 ±1** (platform standard; Dan approved the lifted level on the Ad-1 vertical: "probably even better than Muhammad's") |
| not crushed | loudness range / speech spread p90−p10 | 3.5 LU / 5.7 dB | 2.5 LU / 4.6 dB | LRA ≥ 3 LU; compressor OFF by default |
| no clipping on phones | true peak of the delivered AAC | +0.1 dBTP (his; too hot) | −1.5 | ≤ −1.5 dBTP |
| nothing missing | silent seconds; audio length vs video | 0; equal | 0; equal | 0; within 0.10 s |

The first five rows are what Dan has rejected on. The current approved chain (`audio3.py`, website
video rev 2: "you got it nailed") already meets them — **the problem is not the chain, it is that
only one skill uses it and nothing forces the others to.**

## The architecture — `.claude/skills/_shared/audio/`

One directory, imported by every skill the way `_shared/motionlib.py` already is. Per-skill copies
become 3-line shims (the motionlib precedent, 2026-08-24). Numpy only (no scipy on this Mac);
ffmpeg at `Media/video_edit/bin/ffmpeg` with `/Volumes/Extreme/_edit_work/bin/ffmpeg` as fallback.

| file | job | replaces |
|---|---|---|
| `reference/reference.json` + `reference/muhammad_16x9_voice.flac` | the reference, pinned: a mono 48 k FLAC of his audio (~15 MB, committed — it is Dan's own public ad) plus a committed fingerprint (bands, floor, EDT, LUFS, LRA). `resolve_reference()` regenerates the FLAC from the .mp4 wherever it lives, and refuses to run if the fingerprint does not match | 20+ hardcoded paths, two of them pointing at a file that no longer exists |
| `pick_lav.py` | **source-track selection, per file, never assumed.** Probes every audio stream and channel (2-ch stereo AND N mono tracks), cross-correlates all candidates ±20 ms, scores arrival time, post-word decay, floor, clipped samples; writes `audio_source.json` = `{file, ffmpeg map/filter, lav, far, delay_ms, polarity, verdict}` and prints the exact `[0:a:1]` or `pan=mono\|c0=c1` to use. **Exits non-zero on ambiguity** (near-identical channels = real stereo → take mid; one silent = take the live one; else refuse). Every build script reads the JSON; **no script hardcodes `c0=c1` again** | `chan_analyse.py` ×2, `chancheck.py` ×2, `echo_check.py`, `chan_align.py` |
| `voice_chain.py` | the approved chain, one implementation: mono lav in → highpass → **dereverb if measured EDT > 55 ms** (spray-tan `dereverb.py`, `alpha=0.62 d1=20 d2=150 floor=-24 smooth=0.30`) → per-roll EQ **fitted** to the reference (voicefit lineage, smooth 9-band, never a copied curve) → downward expander → compressor OFF (`--comp` ≤ 1.5:1 opt-in) → `pan=stereo\|c0=c0\|c1=c0` → optional bed ≤ −30 dB ducked + SFX → **measured gain + `alimiter` (never `loudnorm`, which goes dynamic)** with the limiter delay measured by xcorr → −14 LUFS, TP −2.5 in PCM so the AAC lands ≤ −1.5. Length-preserving, so pictures stay frame-locked; `--frame-lock segments.json` for the already-rendered-video case | `audio3.py`, `audio.py`/`audio2.py` ×2, `audio5.py`, `audio_modern.py`, `finish_audio.py` ×2, `audio_final.py`, `finishaudio.py` ×3, `voicechain.py` ×2, `build_audio.py`, `build_audio_singlemic.py`, `build_voice_singlemic.py` |
| `dereverb.py` | moved, unchanged (de-interleaved stereo read kept) | `spray-tan/dereverb.py` |
| `audio_gate.py` | **the one gate**: all nine rows of the table above, on the exact delivered file, against the pinned reference. Writes `<file>.audio_gate.json` with the file's sha256 + every number + PASS/FAIL. `--synthetic` skips the four reference-tone rows for AI-voice videos (make-ad, exercise demos) and keeps loudness/TP/silence/length. `--ab out.mp4` writes his three sentences then ours | `voice_ref_check.py`, `audiogate.py`, `qc_style.py check_channels`, the loose −22…−10 LUFS window in `qc.js` |
| `require_stamp.py` (+ `requireStamp()` in `qclib.js`) | one function every QC and every `deliver.*` calls: the stamp exists, its sha256 matches this file, verdict PASS, reference fingerprint matches. **No stamp = QC FAIL = not deliverable** | nothing — this is the missing enforcement |
| `selftest.sh` | run before any batch: gate PASSES on the reference itself; gate **FAILS** on a synthetic L+R-summed comb render of Ad 2; `pick_lav` picks `a:1` on an 8/28 roll and `c1` on an 8/3 roll; a double-`pan` chain is detected as silence | nothing |

## Per-skill changes

| skill | SKILL.md | code | QC / delivery |
|---|---|---|---|
| **ad-edit** | Step 0.4 + 0.5 collapse into one "Step 0.4 — AUDIO: `_shared/audio`" block; lessons 28/32/33/74/76 keep their history, point at the module | `base.py`, `tight*.py`, `env_full.py` read `audio_source.json`; `audio3.py` → shim; delete `rev1/audio.py`, `rev1/audio2.py` (identical copies) | `qc.py`/`qc5.py` call `require_stamp`; `deliver.sh` refuses without stamp + A/B clip |
| **longform-edit** | Step 0.4, Step 2.5 row 1, Step 5.6, Step 7.6 → module; the per-roll recipe stays as the explanation of what `pick_lav` does | **`build_graded.py` and `build_split.py` are where the three 8/3 longforms shipped comb-filtered** — first stage now maps from `audio_source.json`; every `composite_*.py` asserts the input carries a stamp or refuses; `finish_audio.py`, `audio_final.py`, `build_*_singlemic.py`, `chan_analyse.py` → shims | `qc_style.py` check_channels → `require_stamp`; `cutdown_final_gate.py`, `qc_generic.py`, `qc_investhealth*.py` likewise; `deliver.sh` |
| **shorts** | Steps 0.6 and 0.8 → module; **correct the false "wired into qc.js" claim**; the double-`pan` trap becomes a `selftest` case; rewrite `reference/README.md` index (clean-master/zepbound/spray-tan current; scored-source + full-bleed **DO NOT USE for audio**) | `render.js` (clean-master, zepbound, spray-tan): audio pull filter comes from `audio_source.json` of the SOURCE MASTER, and the master must itself carry a stamp — a short cut from an unstamped master fails; `finishaudio.py` ×3 → shim; `scored-source`/`full-bleed` `render.js` get the same pull or a hard `throw` | `qc.js` ×5: `requireStamp()`; `deliver.js` |
| **shortad-from-longform** | Step 4 keeps Dan's approved "reference's own mix" path (loudnorm → limiter) **but that output goes through the gate too**; add the missing check 16 | `build_audio.py`, `finish_audio.py`, `chan_analyse.py`, `a2/edl_verify.py` → module | `qc.py` gains check 16 (length/silence) + `require_stamp` |
| **findassets** | new Step: any clip cut WITH audio runs `pick_lav` on the roll and is delivered as lav-mono → centred stereo, never `-c:a copy`; a `pick_lav` line goes into `DELIVERED_CLIPS.md` per clip | — | `audio_gate --synthetic` (L/R corr, silence, length) before upload |
| **revisions** | "Audio first" runs `pick_lav --analyse` + `audio_gate` on the editor's file so the doc quotes the same numbers we hold ourselves to; handles 4-track files | `echo_check.py`, `chan_align.py` → shims | — |
| **editor-brief** | the audio paragraph is generated from `pick_lav` on that shoot's rolls (2-ch vs 4-track wording), and the spec says "must pass `_shared/audio/audio_gate.py` against the reference"; the brief links the A/B clip | — | — |
| **youtube-packaging** | one line → `/shorts` + gate; delete stray `SKILL 2.md` | — | — |
| **make-ad**, **exercisegeneration** | one line: final mux runs `audio_gate --synthetic` (loudness, TP, silence, length). No camera audio, lowest priority | — | — |
| **video-use** (external plugin) | longform-edit uses it for transcripts only; add: never let it render audio — its cuts bypass the module | — | — |

## Execution order

**Phase 1 — the module (one session, Fable high).** Build `_shared/audio/` from the approved code
(`audio3.py` chain, `voice_ref_check.py` + `audiogate.py` merged, spray-tan `dereverb.py`, the
`chan_analyse` lag-search generalised to N tracks). Pin the reference. `selftest.sh` green.
Acceptance: gate PASSES Muhammad's file and Ad 2 rev 2 (`Muhammad Ad Videos/this picture got me
abs/…claude | 9x16.mp4`, which passes today: mean 0.54 dB, EDT 45 ms, corr +0.992), and **FAILS**
a deliberately summed-both-mics render of the same cut.

**Phase 2 — wire the four build skills (same or next session).** Shims, `audio_source.json`
readers, `require_stamp` in every QC and delivery script, SKILL.md edits. Acceptance: run each
skill's QC on its last delivered file — the website video rev 2 and Ad 2 pass; a file with the
stamp deleted fails; `scored-source/render.js` output fails.

**Phase 3 — the three human-facing skills** (findassets, revisions, editor-brief) + the two
synthetic ones. Small edits.

**Phase 4 — re-render what is already wrong**, through the module, not by hand: the Zepbound
(`zep-short1..8`) and supplements (`supp-short1..8`) Shorts and, if Dan wants, longforms 01–05
(audio-only re-mux, `-c:v copy`). This is the old handoff's job 2; it closes when every file
carries a PASS stamp. ⚠ Cap at two concurrent renders.

Then: memory `shoot-audio-two-mics` → rewrite as "the lav track, found by `pick_lav`, never a
channel number"; one standing line in `AGENTS.md`; delete the old audio handoff; check off both
dashboard tasks.

## Non-negotiables to encode (so it never happens again)

1. **Selection is measured per file, never assumed** — `pick_lav` output or no render.
2. **One chain, one gate, one reference** — a skill that needs something different extends the
   module with a flag; it never writes a new chain.
3. **The gate measures the delivered file and stamps it; QC and delivery refuse an unstamped file.**
   This is the piece every previous fix lacked: the rule existed, nothing enforced it.
4. **The reference is pinned by fingerprint**, so moving or renaming the .mp4 cannot break a gate
   silently again (it broke today).
5. **An A/B clip (his three sentences, then ours) ships with every review copy.**
6. **A metric Dan rejects on that the gate cannot see becomes a new row in the gate** — the reverb
   lesson, stated as a rule.

## Starter prompt

> Execute `Handoffs/handoff-20260902-audio-standard-unification.md`, Phase 1 then Phase 2. Build
> `.claude/skills/_shared/audio/` from the approved chain in
> `ad-edit/reference/website-video/audio3.py`, merge `ad-edit/reference/voice_ref_check.py` and
> `shorts/reference/spray-tan/audiogate.py` into one `audio_gate.py`, generalise the channel
> lag-search into `pick_lav.py` that handles both 2-channel rolls and the 8/28 four-mono-track rolls,
> and pin the reference by fingerprint. `selftest.sh` must pass Muhammad's file and Ad 2 rev 2 and
> FAIL a summed-both-mics render before you touch any skill. Then convert every per-skill audio
> script to a shim and add `require_stamp` to every QC and delivery script. Do not re-render any
> delivered video in this session.

**Recommended runner:** Fable 5.1, high effort. Phases 1–2 in one session (~3 hours of tool time,
$0 AI spend); Phases 3–4 in a second.
