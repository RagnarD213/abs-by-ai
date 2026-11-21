# Handoff — re-render 04 invest-health's audio on the approved dereverb

**Created** 2026-09-09 by Claude Code (Opus 5) · **For** a fresh session · **Not executed**

Dan rejected the delivered audio on 2026-09-09: *"absolutely awful… It sounds underwater. We can
never, ever strip audio like this."* He is right, and it now measures.

## Why this is a separate handoff

`Handoffs/handoff-20260909-audio-match-muhammad.md` covers the three **Shorts** batches (spray tan,
Zepbound, supplements). **It does not cover 04.** 04 was gated on 2026-09-03, six days before the
dereverb was re-tuned, so it shipped on the rejected settings and nothing went back for it.

A sweep of every `*.voice_chain.json` under the three delivery trees on 2026-09-09 found **04 is the
only long-form carrying the rejected dereverb.** Nothing else needs this.

## The damage, measured on the delivered file

`audio_gate.py` re-run 2026-09-09 on `FINAL_invest_health.mp4` — **FAIL, 1 row: `artifacts`**

| | 04 as shipped | Muhammad | bound | verdict |
|---|---|---|---|---|
| spectral flux | **0.094** | 0.072 | ≤ his × 1.10 | **1.31× — FAIL** |
| HF swirl | 0.795 | 0.835 | ≤ his × 1.10 | 0.95× — pass |
| early decay | 43 ms | 40 ms | ≤ 80 ms | pass |

Every other row passes. **That single failing number is the sound Dan is describing** — spectral
subtraction makes each frame's gain differ from its neighbour's, so the voice shimmers.

Settings it was built with, from `FINAL_invest_health.voice_chain.json`:

| | shipped (rejected) | approved 2026-09-09 |
|---|---|---|
| `alpha` | **0.62** | 0.30 |
| `d1_ms` | 20 | 22 |
| `d2_ms` | **150** | 70 |
| `floor_db` | **−24.0** | −10.0 |
| `smooth` | 0.30 | 0.45 |
| result | EDT 74.7 → **37.3 ms** | expect ~45–50 ms |

It overshot Muhammad's 40 ms and paid for it in artefacts — the same failure the module README now
carries a STOP note about. **Do not re-tune. The sound is settled**; Dan picked it by ear from a
four-way A/B ("number 3 sounds good"). This is a re-render, not a tuning job.

## ⚠ Check these two things before you start

1. **`common.stash_untreated()` did not exist at 10:03 on 2026-09-09** while
   `voice_chain.py:158` and `dereverb.py:102` both call it — a fresh render would die with
   `AttributeError`. The audio module was being actively edited by another session at that moment
   (`common.py` mtime 10:03:42, `git status` showing `MM` on `dereverb.py` and `voice_chain.py`).
   **Confirm the module is committed and clean, and that `stash_untreated` and `artifacts` both
   import, before running anything:**
   ```bash
   cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
   git status --short .claude/skills/_shared/audio/
   python3 -c "import sys;sys.path.insert(0,'.claude/skills/_shared/audio');import common as C;print(hasattr(C,'stash_untreated'),hasattr(C,'artifacts'))"
   ```
2. **`selftest.sh` is broken** (`A: unbound variable`, and its reference paths predate the 09-08
   editor-deliveries rename). AGENTS.md requires it before a batch. Repair and run it first — this
   is item 1 of the sibling handoff too, so do it once and both jobs unblock.

## Everything is already staged — no re-render of picture, cut or graphics

Work dir `/Volumes/Extreme/_edit_work/invest-health-cutdowns/style/` (verified present 2026-09-09):

| file | what it is |
|---|---|
| `audio/voice_raw.wav` (241 MB) | the **untreated** single-mic voice, frame-locked. Start here. |
| `picture_final.mp4` (1487 MB) | the finished picture, no audio. Mux onto this with `-c:v copy`. |
| `music/organic_flow.mp3` | the house bed |
| `sfx/bed.wav` (321 MB) | 141 graphic-entrance SFX cues |
| `audio/final_mix_v2.wav` | the REJECTED mix — keep for A/B, do not ship |
| `*_PRE_DRIFT*` | rollback copies of the pre-card-drift build |

**The bed sits at −36 dB, not the module default −30.** −30 failed the gate's floor row on this
programme; that lesson is already recorded in the skill. Keep −36.

⚠ **Two corrections to this doc, found the hard way on 2026-09-09 while executing it.**

1. **The SFX track is `sfx/bed_m15.wav`, NOT `sfx/bed.wav`.** `voice_chain.py --extra` mixes at 0 dB,
   so 09-03 pre-attenuated the 141-cue bed by 15 dB (`REBUILD_NOTES.md` line 162). The raw bed sits
   **+23 dB at 3500 Hz** relative to the reference; passing it cost three full renders, failing `tone`
   at 3500 Hz +6.4 dB and inflating `artifacts` on the SFX transients. The voice was never the problem
   — untreated and dereverbed lavs both read +0.3 dB at 3500 Hz.
2. **Do not pass `--video` when `--out` is a `.wav`.** `pic` is then set and ffmpeg tries to mux H.264
   into a WAV container and dies. `--frame-lock` alone supplies the picture duration; mux separately.

Also: `deliver.sh` runs under `set -e`, and its `[ -f "$D/INVEST_HEALTH_v3.mp4" ] && mv ...` lines are
now false, which aborted the script before it copied anything. Each conditional move needs `|| true`.

## Do this

```bash
cd /Volumes/Extreme/_edit_work/invest-health-cutdowns/style
export PATH=/Volumes/Extreme/_edit_work/bin:$PATH
A="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"

# 1. re-mix on the APPROVED dereverb (module defaults — pass no --dereverb override)
python3 "$A/voice_chain.py" --in audio/voice_raw.wav --out audio/final_mix_v3.wav \
  --bed music/organic_flow.mp3 --bed-db -36 --extra sfx/bed_m15.wav \
  --frame-lock picture_final.mp4

# 2. mux (video untouched)
ffmpeg -nostdin -y -v error -i picture_final.mp4 -i audio/final_mix_v3.wav \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest \
  FINAL_invest_health_v3.mp4

# 3. gate the DELIVERED file — the artifacts row must PASS
python3 "$A/audio_gate.py" FINAL_invest_health_v3.mp4 \
  --ab AB_his-vs-ours_invest_health.mp4
```

Then deliver over `claude edited long form content/04 - Why You Should Invest More In Your Health/
FINAL_invest_health.mp4`, keeping the rejected one as `FINAL_invest_health_UNDERWATER.mp4` until Dan
confirms. `deliver.sh` in the work dir already copies the sidecars; update its source filename.
**`FINAL_invest_health_PRE_REBUILD.mp4` is the 53-minute original — do not overwrite it.**

## Verify before you tell Dan it is done

- `audio_gate.py` PASS **including `artifacts`** — flux and swirl both ≤ his × 1.10.
- The picture is byte-identical: `nb_frames` 52,615 and `-c:v copy` in the mux command.
- Duration 1755.687 s, audio within 0.10 s of picture.
- Send a 540p review copy **and** the A/B clip. The 540p is 197 MB, over the 30 MB chat limit — it
  only reaches the desktop app, so also make a ≤30 MB 640×360 copy if Dan is on his phone.

## The rule this cost us

**Never let a gate reward the thing it is supposed to bound.** `edt`, `dryness` and `floor` all
score MORE suppression as better, so they rated the underwater build as an improvement and it
shipped twice. The `artifacts` row is the counterweight. **Never raise `artifact_x` to make a build
pass** — and never strip audio to hit a number Dan has not heard.

## Starter Prompt

> Execute `Handoffs/handoff-20260909-invest-health-audio-rerender.md`. 04 invest-health shipped with
> the dereverb Dan rejected as "underwater" (flux 1.31× Muhammad's, gate FAIL on `artifacts`); the
> approved setting is already locked in `_shared/audio` and everything needed is staged in
> `/Volumes/Extreme/_edit_work/invest-health-cutdowns/style/`. Check the two prerequisites at the top
> first — `common.stash_untreated()` was missing and `selftest.sh` is broken. Re-mix from
> `voice_raw.wav`, mux onto `picture_final.mp4` with `-c:v copy`, gate the delivered file until the
> `artifacts` row passes, then deliver and send Dan a review copy plus the A/B. Do not re-tune the
> dereverb — he picked it by ear.

**Model:** Sonnet 5, standard effort. It is a mechanical re-render against a locked setting; the
judgement was already made. Roughly 30–45 minutes, mostly the mux and the gate. $0.00 AI spend.
