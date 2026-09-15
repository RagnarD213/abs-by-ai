# Handoff — Ads 6 and 14: vertical, square and ≤0:59 versions (master-queue jobs J15–J18)

**Written 2026-09-15** by the session that reviewed Muhammad's 09-14 batch, at Dan's request: *"Create a second
handoff document to create the square, vertical, and short versions."* Ads 6 and 14 are the two he finalized in that
batch, so they now owe the standard four variants each.

**This doc is a spec, not a second queue.** The single queue is
`Handoffs/handoff-20260913-ad-variants-master-queue.md` — read it first (coverage matrix, firing rules, the BT.601
colour trap, the "when a new ad goes final" rule this doc implements). Ads 6 and 14 are jobs **J15–J18** there.
Ads 7 and 10 already have J10–J13; nothing here changes them.

## The four jobs

| job | build | status |
|---|---|---|
| **J15** | **Ad 6: 9:16 vertical full + ≤0:59 cutdown** | **READY** |
| J16 | Ad 6: 1:1 square full + ≤0:59 cutdown | BLOCKED on Dan approving J15 |
| **J17** | **Ad 14: 9:16 vertical full + ≤0:59 cutdown** | **READY** (see the export note) |
| J18 | Ad 14: 1:1 square full + ≤0:59 cutdown | BLOCKED on Dan approving J17 |

**One build per session, never more than two video builds running anywhere** (`ps -Ao command | grep -E
'ffmpeg|render|qc_style|whisper'` before you start). Vertical first, square second — the square is a re-layout of the
approved vertical (same EDL, beats, captions, audio), and both cutdowns share one `cut_plan.json`.

## The sources

| | Ad 6 | Ad 14 |
|---|---|---|
| title | You're Not Too Old to Get Abs. I'm Proof. | I Watched 400 Workout Videos and Gained Weight |
| editor 16:9 | `Muhammad Ad Videos/you're not too old to get abs i'm proof - ad 6/you're not too old to get abs i'm proof \| muhammad \| 16x9 \| ad 6.mp4` (filed 09-15) | ⚠ not filed yet — "Daniel HQ ad 14 V3.mp4", Drive `1VQuOxzfbmXv_TgO5GgURXrLkkwusU6_k` |
| file | 1920×1080, 29.97, **8,208 frames, 4:33.9**, 363,314,897 bytes, 10.3 Mbps, Drive `1jO-re15wKmdzD6SQsQLHkSbnVXdDUPOI` | 1920×1080, 29.97, **5,924 frames, 3:17.7**, 79,337,649 bytes, **3.0 Mbps** |
| approval | the 09-15 section of Muhammad's batch doc: finalized, no further revisions | same |
| last notes | `revision docs/ad6-revisions-muhammad-round3-9-12-26.md` | `revision docs/ad14-revisions-muhammad-round2-9-12-26.md` |

**Ad 14's export is 3.0 Mbps**, a review-grade encode; every other final is ~10 Mbps. `Handoffs/handoff-20260915-
finalized-ads-6-14-youtube-and-google-ads.md` asks Dan to request the HD export from Muhammad. **Build J17 from the
HD once it exists**; if Dan wants the vertical sooner, build from the 3.0 Mbps file, say so in `notes-vertical.md`,
and expect to rebuild when the HD lands. Do not start J17 on the 3.0 Mbps file without saying that in the report.

## How to build

`/shortad-from-longform` end to end, exactly as J10/J12 describe it. Step 0b's "approved draft" is the editor's HD
itself (Dan approved the delivered cut, so there is no separate draft to diff).

* **Colour: decode as BT.709 from the start.** Muhammad's masters carry no colour tags, ffmpeg defaults to BT.601,
  and every grade fitted through the default decode is wrong (Dan rejected the Ad 3 vertical's colour for exactly
  this; memory `untagged-video-bt601-trap`). Copy the Ad 3 render-10/12 compositor out of `/Volumes/Extreme/_edit_work/ad3-vert/`
  into a fresh `ad6-vert/` / `ad14-vert/` — never work inside another session's build directory, and never start
  from `ad4-vert/` or `ad5-vert/`, whose grades carry the fault. Verify colour against his file decoded as BT.709.
* **Audio: Muhammad's, untouched** (`--verbatim`), the cutdown his mix cut at the seams only. No loudness change,
  never summed to mono (memory `editor-audio-untouched`).
* **Labels.** Every real after picture of Dan in the selected ranges carries **"Real picture of me — not
  AI-generated"** as the same solid black rounded pill as the AI-GENERATED chip — bold upright capitals, not italic,
  no brackets — and **never over his face or his abs** (`AGENTS.md` 09-12; place it by measuring the rendered frame,
  never at a fixed y). AI images keep AI-GENERATED. Muhammad's own version of this chip on his 16:9 is italic, in
  square brackets, on a see-through band — do not copy it. Ad 6's real pictures are at 0:09.5–0:12.4 (the Age: 40
  photo, label beside that tag), 0:19.5–0:22.5 (four photo-shoot stills) and 2:29.5–2:31.2 (the two photo panels);
  Ad 14's are at 0:56 (Age: 40, label beside the tag), 0:57.5, 0:58.5 and 0:59.5. Re-verify each against the
  delivered master before placing anything.
* **Before/after = same person** (`AGENTS.md` 09-12). Both ads use the app recording that uploads a man who is not
  Dan (memory `app-recording-before-after-pair`). Ad 14's closing flow was fixed in round 2 to end on that man's own
  AI after picture (`1gFwcbYiRvoGQz1WJ7oKj-T7dRAM2zRPp`); Ad 6's demo at 2:57 already ends on the recording's own
  after picture. Confirm both in the delivered masters and keep the pairing intact through every cut.
* **Compliance on every delivered file:** `compliance:banned_screen` over every frame (no side-by-side before/after,
  no "Meet the new you", no email-capture screen), plus a watch pass at full resolution.
* **Cutdowns:** the `/shortad-from-longform` cutdown method — hook, problem, the AI demo, the payoff, CTA; seams
  snapped to silence and to HIS picture cuts, never inside a light leak. Prove every seam's picture against the
  master (memory `cutdown-seams-single-source`). Check the closing CTA-pill caption overprint (memory
  `caption-trailing-entry-overprint`) on every file.
* **Gates on the delivered file, at the current `GATE_VERSION`:** `qc.py`, the watch pass, the hair/framing gate,
  `caption_sync_check.py` (re-copy it from the skill's `reference/` — stale forks in old build dirs use colliding
  `/tmp` paths), `audio_gate.py --verbatim` against Muhammad's mix, `_shared/deliver/gate.py`, then the independent
  audit. Expect "does not ship" on the first pass. Never raise a bound to make a file pass.

## Delivery

Into the ad's folder beside the editor's 16:9, under the `editor-deliveries` convention:
`you're not too old to get abs i'm proof | claude | 9x16 | ad 6.mp4`, `… | 9x16 59s | ad 6.mp4`,
`… | 1x1 | ad 6.mp4`, `… | 1x1 59s | ad 6.mp4`, and the same four for
`i watched 400 workout videos and gained weight | … | ad 14.mp4` (create that folder when Ad 14's master is filed).
Plus the `REVIEW 540p` copies, the audio A/B, the `.audio_gate.json` + `.deliver_gate.json` stamps,
`notes-vertical.md` / `notes-square.md` and the `recipe-*/` folder. Send Dan the review copies.

**A variant is done only when Dan approves it.** After approval it goes into Google Ads as one more `videos` entry on
that ad's existing Demand Gen ad groups (`/ad-setup` step 6) — the groups come from
`Handoffs/handoff-20260915-finalized-ads-6-14-youtube-and-google-ads.md`.

## Closing out

Update the job row and the coverage matrix in the master queue each time, and delete this doc, its
`Handoffs/README.md` row and its `AI_COORDINATION.md` line when J15–J18 are all delivered and approved. No dashboard
rows (Dan's 09-08 rule).

## Model and starter prompt

**Fable 5.1, effort high** — same as every other variant job in the queue.

> Execute job J15 in `Handoffs/handoff-20260913-ad-variants-master-queue.md` (spec:
> `Handoffs/handoff-20260915-ads-6-14-variants.md`): build the 9:16 vertical and ≤0:59 cutdown of Muhammad's finalized
> Ad 6 with `/shortad-from-longform`, decoding his master as BT.709 from the start, his audio untouched, the
> "Real picture of me — not AI-generated" chip on every real picture of me and never over my face or abs, the app
> demo's before and after the same person. Every gate at the current gate version, the independent audit, deliver
> into the ad's folder and send me the review copies. Model: Fable 5.1, effort high.

(For Ad 14 the same prompt with **J17** and Ad 14 — but confirm first whether Muhammad's HD export has landed.)
