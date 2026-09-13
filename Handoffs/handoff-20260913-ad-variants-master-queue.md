# Ad variants — MASTER QUEUE (vertical, square and ≤0:59 cutdowns for every finalized ad)

**Written 2026-09-13 at Dan's request: "make sure that we don't miss square, vertical, or short-form for any of these
ads, and … have one single thread where I have all the handoff documents that I can fire."** This doc is that single
place. It lists every finalized horizontal ad, what exists for it, and every build still owed, in firing order. The
older per-ad square docs stay on disk as the detailed specs; this doc is the queue that points at them and covers the
three builds nothing else covers (J1–J3).

## How to fire

Paste this into a fresh session, as often as you like. Each run does ONE job and updates this file:

> Open `Handoffs/handoff-20260913-ad-variants-master-queue.md`. Re-check the blockers of every job marked BLOCKED
> against the current state of the ad folders, `AI_COORDINATION.md` and `.claude/skills/editor-deliveries/state.json`,
> and update their status. Then execute the highest job marked **READY**, following its own doc and the rules in
> this file, through every gate, the independent audit and delivery into the ad's folder. Update that job's row and the
> coverage matrix, then stop. If nothing is READY, say what each job is waiting on and stop.
> Model: Fable 5.1, effort high.

Each job also has its own starter prompt below if Dan wants to fire a specific one.

## The standard: every finalized 16:9 ad gets four variants

| variant | file name (`editor-deliveries` convention) |
|---|---|
| 9:16 full length | `<title> \| claude \| 9x16 \| ad N.mp4` |
| 9:16 ≤0:59 cutdown | `<title> \| claude \| 9x16 59s \| ad N.mp4` |
| 1:1 full length | `<title> \| claude \| 1x1 \| ad N.mp4` |
| 1:1 ≤0:59 cutdown | `<title> \| claude \| 1x1 59s \| ad N.mp4` |

Plus the `REVIEW 540p` copies, audio A/B, `.audio_gate.json` + `.deliver_gate.json` stamps, notes and recipe folder,
all beside the editor's 16:9 in `<Editor> Ad Videos/<title> - ad N/`. **A variant is done only when Dan has approved
it** (the verticals rule). After approval it goes through `/ad-setup` step 6 as one more `videos` entry on that ad's
existing Demand Gen ad groups.

Order within an ad: **vertical first, square second.** The square is a re-layout of the approved vertical build (same
EDL, beats, captions, audio). Both cutdowns share one `cut_plan.json`, because vertical and square have the same timeline.

## Coverage matrix — as of 2026-09-13

| ad | editor 16:9 | 9:16 full | 9:16 ≤0:59 | 1:1 full | 1:1 ≤0:59 |
|---|---|---|---|---|---|
| **1** this picture got me abs (Muhammad) | filed | ✅ approved 09-10 (`Iz0u8KHRbyE`) | ❌ **J2** | 🟡 delivered 09-12, Dan reviews | 🟡 delivered 09-12, Dan reviews |
| **1** this picture got me abs (Zeeshan) | filed | 🟡 delivered 09-10, Dan reviews | 🟡 delivered 09-10, Dan reviews | ❌ J9 | ❌ J9 |
| **2** stop wasting money on nutritionists | filed | ✅ approved 09-08 (`7XgHxn59Tsg`) | ❌ **J3** | ✅ approved 09-12 (`hHiPzQKTzrg`) | ❌ **J3** |
| **3** stop paying human trainers | filed ⚠ HD text defect | 🔧 J6 being built by another session | 🔧 J6 | ❌ J7 | ❌ J7 |
| **4** stop wasting money on supplements | filed | 🟡 review copies only, masters held → **J1**; Dan reviews | 🟡 same | ❌ J8 | ❌ J8 |
| **5** every diet you've tried failed | filed | 🟡 delivered, round-2 revisions open → **J4** | 🟡 same | ❌ J5 | ❌ J5 |

**Not final yet, so no variants are owed:** Muhammad's Ads 6, 7, 8, 9, 10, 13, 14, 15 (all in revision rounds as of 09-12;
Ad 7 and Ad 10 HDs came in but carry revisions), and Waleed's Video 1 (= a third Ad 1, round 4 open). Muhammad wrote
on 09-13 18:56Z that he will "send tomorrow"; the next `/editor-deliveries` run files whatever arrives.

## The queue

Only one build per session. **Never more than two video builds running at once across all sessions**
(`ps -Ao command | grep -E 'ffmpeg|render|qc_style|whisper'` first). Never work inside a build directory another session
is actively using. Copy it.

| job | what | status | blocked on |
|---|---|---|---|
| **J1** | Ad 4: put the held 9:16 masters (full + 59s) in the folder | **READY** | — |
| **J2** | Ad 1 (Muhammad): 9:16 ≤0:59 cutdown | **READY** | — |
| **J3** | Ad 2: ≤0:59 cutdown plan → 9:16 59s + 1:1 59s | **READY** | — |
| **J4** | Ad 5: vertical round-2 revisions (full + 59s) | **READY** | — |
| J5 | Ad 5: square full + 59s | BLOCKED | J4 delivered AND Dan approves the revised vertical |
| J6 | Ad 3: vertical full + 59s | IN PROGRESS, owned by the Ad 3 vertical session | that session; Dan's approval |
| J7 | Ad 3: square full + 59s | BLOCKED | J6 approved AND Muhammad's corrected Ad 3 HD passes `hd_vs_draft.py` |
| J8 | Ad 4: square full + 59s | BLOCKED | Dan approves the Ad 4 vertical |
| J9 | Ad 1 (Zeeshan): square full + 59s | BLOCKED | Dan approves the Zeeshan Ad 1 vertical |

Suggested order among the READY jobs: **J1** (minutes), **J4** (Dan is waiting on it and it unblocks J5), **J3** (Ad 2 took
~80% of the campaign's early spend), **J2**.

---

### J1 — Ad 4: deliver the held 9:16 masters

**What exists.** `/Volumes/Extreme/_edit_work/ad4-vert/ad4_vertical_9x16.mp4` (561 MB, 09-11) and
`ad4-vert/cut/ad4_vertical_9x16_59s.mp4` (122 MB, 57.19 s). `qc.py` 18/20 on both, three audits, and audit 3 said
SHIPS. Only the review copies are in `Muhammad Ad Videos/stop wasting money on supplements - ad 4/`. `deliver4.py`
refused the masters for one reason: Muhammad's export peaks at **−0.90 dBTP** against the −1.0 rule, so the verbatim
audio stamp cannot pass. **Dan accepted that audio as-is on 09-11** (*"I think the audio sounded fine"*, recorded in
the Ads 3+4 entry of `AI_COORDINATION.md`).

**Do.**
1. **Never raise a bound to make it pass** (`AGENTS.md`, memory `audio-never-over-strip`). Record Dan's acceptance as an
   explicit, auditable, per-file exception with his words and the date, using whatever declared mechanism the audio
   gate and `_shared/deliver/gate.py` provide (`not_applicable` / a waiver field). If neither has one, add one, run
   `python3 .claude/skills/_shared/qc_corpus/run.py`, and do not commit unless it passes. If that still cannot be done
   cleanly, stop and report. Do not tune the bound.
2. The board warned that `ad4-vert/` carries **stale copies** of `caption_sync_check.py` and `captions.py`. Re-copy both from
   the skill's `reference/` and re-run the caption gate. Check the closing CTA-pill caption overprint ([S1] 22–24,
   memory `caption-trailing-entry-overprint`) on both files. If it is present, fix it with a caption rebuild + mux, not a
   re-render.
3. Re-gate both files at the **current** `GATE_VERSION`, because every stamp older than the current version is invalid.
   Then deliver with `deliver4.py` under the naming convention.
4. This is **not** approval. The dashboard row for the verticals stays unchecked until Dan says so.

Model: Opus 5, effort high (a gate exception is a gate change). Starter prompt:
> Execute job J1 in `Handoffs/handoff-20260913-ad-variants-master-queue.md`: deliver the held Ad 4 9:16 masters from
> `/Volumes/Extreme/_edit_work/ad4-vert/`, recording Dan's 09-11 acceptance of −0.9 dBTP as an auditable exception
> (never a bound change; corpus must pass), refreshing the stale caption tools, re-gating at the current gate version.
> Model: Opus 5, effort high.

### J2 — Ad 1 (Muhammad): the 9:16 ≤0:59 cutdown

**Why it is missing.** The only vertical cutdown, `ad1-8-14/vert9x16/ad1_vertical_59s.mp4` (Aug 25, 0:50.75), came from an
earlier attempt. It predates the attempt-3 vertical Dan approved on 09-10, the "Real picture of me" label (09-11), the
label placement rule (09-12) and the current gates. **Do not deliver it.**

**Build.**
* Source: the approved attempt-3 vertical build `/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/`. Copy it to
  `ad1-vert59/`. The approved file has **6,977 frames, one more than Muhammad's 6,976**, so map every cut accordingly.
* Selection: reuse the ≤0:59 selection the Ad 1 square already proved (`/Volumes/Extreme/_edit_work/ad1-sq/`,
  `cutdown.py` → 1,493 frames / 49.82 s, three audits). It is on Muhammad's 6,976 grid, so account for the one-frame
  offset at every seam. Read `/shortad-from-longform` **[S1] 22–24** and `reference/a11_sq_ad1/` first: that cutdown
  shipped only after six seam defects were fixed (picture one frame late at seams, a word dropped from captions, a
  seam through the "s" of "abs"). Memory `cutdown-seams-single-source`: prove every seam's picture against the master.
* Picture: every real after picture of Dan in the selected ranges gets the **"Real picture of me — not AI-generated"**
  chip, **never over his face or abs** (`AGENTS.md` 09-12, measured per rendered frame). The approved vertical has no
  chip, so those beats are re-rendered, not just cut. AI images keep AI-GENERATED.
* **Before/after = same person** (`AGENTS.md` 09-12): the app recording uploads a man who is not Dan (memory
  `app-recording-before-after-pair`). If the selection includes the demo, its before and after must be the same man.
* Audio: the approved vertical's AAC stream, cut at the seams only (the Ad 1 square did the same). No loudness change.
* Gates on the delivered file: `qc.py`, watch pass, hair gate, `caption_sync_check.py`, `audio_gate.py`,
  `_shared/deliver/gate.py`, then the independent audit (7b). Expect "does not ship" the first time.
* Deliver `this picture got me abs | claude | 9x16 59s | ad 1.mp4` + review copies + stamps into
  `Muhammad Ad Videos/this picture got me abs - ad 1/`, and send Dan the 540p copy.

Model: Fable 5.1, effort high. Starter prompt:
> Execute job J2 in `Handoffs/handoff-20260913-ad-variants-master-queue.md`: build Ad 1's (Muhammad) 9:16 ≤0:59 cutdown
> from the approved attempt-3 vertical, reusing the Ad 1 square's proven cutdown selection (mind the 6,977 vs 6,976
> frame offset), adding the real-picture label off face and abs, the vertical's audio cut at the seams only. Every gate,
> the independent audit, deliver, send Dan the review copy. Model: Fable 5.1, effort high.

### J3 — Ad 2: the ≤0:59 cutdowns, vertical and square

**Why it is missing.** Ad 2's vertical never had a cutdown (`notes-square.md`: "no `cut_plan.json` exists"), so the
approved square went out full length only.

**Build.**
1. **Cut plan first.** Build a `cut_plan.json` on Muhammad's 8,275-frame timeline with the cutdown method in
   `/shortad-from-longform` (the Ad 3/4/5 `zcutdown` step: hook, problem, the AI demo, the payoff, CTA; seams snapped to
   silence and to HIS picture cuts, and never inside a light leak (A8.13)). **Exclude the app's email-capture screen**,
   which Muhammad's Ad 2 shows at 3:11, 3:12 and 3:23. Before/after = same person in any demo kept.
2. **9:16 59s** from `/Volumes/Extreme/_edit_work/ad2-vert-v2/`. **1:1 59s** from `/Volumes/Extreme/_edit_work/ad2-sq/`
   (the approved square). Use the same plan for both. Copy each directory first. Every real picture of Dan in range carries
   the real-picture chip off face and abs. The approved vertical predates the label; check what the approved square
   already carries and match it.
3. Audio: the approved vertical's AAC stream (the square carries the same stream bit for bit), cut at the seams only. No
   further lift. Ad 2's mix already has the approved +5.2 dB.
4. Check the closing CTA-pill caption overprint ([S1] 22–24) on both. The approved Ad 2 vertical is known to carry it.
5. Gates on both delivered files, the independent audit on each, then deliver
   `stop wasting money on nutritionists | claude | 9x16 59s | ad 2.mp4` and `… | 1x1 59s | ad 2.mp4` + review copies
   + stamps into the Ad 2 folder. Send Dan both review copies. Two renders in sequence, not in parallel.

Model: Fable 5.1, effort high (may need two sessions; if so, deliver the 9:16 first and update this row). Starter prompt:
> Execute job J3 in `Handoffs/handoff-20260913-ad-variants-master-queue.md`: build a ≤0:59 cut plan for Ad 2 on
> Muhammad's 8,275-frame timeline (no email-capture screen), then render the 9:16 59s from `ad2-vert-v2/` and the 1:1 59s
> from `ad2-sq/` off that one plan, with the real-picture label and the approved audio cut at the seams. Every gate, an
> independent audit on each, deliver, send Dan both review copies. Model: Fable 5.1, effort high.

### J4 — Ad 5: vertical round-2 revisions

Spec: **`Handoffs/handoff-20260912-ad5-vertical-revisions-round2.md`** (Dan's two asks: the app demo ends on the same man's
after picture, which Dan named on 09-12, and the real-picture label on every real picture of Dan, off his abs and larger).
Rebuilds both the full length and the 59s. Model and starter prompt are in that doc.

### J5 — Ad 5: square full + 59s

Spec: **`Handoffs/handoff-20260911-square-ad5-muhammad.md`** + **`…-square-ads-00-shared-rules.md`**. Fire only after J4 is
delivered and Dan approves. Its doc was written before round 2, so take the pictures, labels and demo pairing from the
**round-2** vertical, not the round-1 beats it lists.

### J6 — Ad 3: vertical full + 59s (in progress, not a handoff)

Owned by the Ad 3 vertical session (`/Volumes/Extreme/_edit_work/ad3-vert/`, section [A12]). Draft review copies were
built 09-13 14:19 in `ad3-vert/review/`. **Do not touch.** When it delivers into `Muhammad Ad Videos/stop paying human
trainers - ad 3/` and Dan approves, mark J6 done and re-check J7.

### J7 — Ad 3: square full + 59s

Spec: **`Handoffs/handoff-20260911-square-ad3-muhammad.md`**. Two blockers: J6 approved, and Muhammad's corrected Ad 3 HD
(the filed v6 HD is missing "back in my 20s, as a 38 year old dad running a successful ad agency." at 2:14.1–2:23.1)
passing `hd_vs_draft.py` VERDICT IDENTICAL. When the corrected HD lands, `/editor-deliveries` files it, and the 16:9 in the
Demand Gen campaign (`QWW1oumpNg4`) needs replacing via `/ad-setup`.

### J8 — Ad 4: square full + 59s

Spec: **`Handoffs/handoff-20260911-square-ad4-muhammad.md`**. Fire after Dan approves the Ad 4 vertical. J1 should run first
so the folder holds the masters the square is checked against.

### J9 — Ad 1 (Zeeshan): square full + 59s

Spec: **`Handoffs/handoff-20260911-square-ad1-zeeshan.md`**. Fire after Dan approves the Zeeshan Ad 1 vertical, re-delivered
09-10 with his audio untouched. 24 fps, the email-capture screen at 188.75–190.33 s replaced, his audio verbatim.

---

## When a new ad goes final (Ads 6–15, Waleed's Video 1)

When `/editor-deliveries` files a new 16:9 final, the session that files it adds one row per missing variant to the
matrix and two jobs to the queue:
* **Jn — Ad N: vertical full + 59s** via `/shortad-from-longform` (READY once filed; it includes Step 0b, proving the HD is
  the approved draft).
* **Jn+1 — Ad N: square full + 59s** via `…-square-ads-00-shared-rules.md` (BLOCKED on Dan approving Jn).

Rules that already bind these ads: the before and after in any pair are the same person. Every real picture of Dan
carries the real-picture label, off face and abs. No email-capture or side-by-side before/after app screen
(`compliance:banned_screen`). Editor audio stays untouched. Ads 6, 8, 9, 10, 13, 14 and 15 use the stranger's app recording
(09-10 finding), so their demos need the matching after picture.

## Closing out

* Each job: update its row (DONE + date + delivered file names) and the matrix. When a spec doc is fully executed, remove
  it from `Handoffs/README.md` and the HANDOFFS section of `AI_COORDINATION.md` in the same session.
* No dashboard rows (Dan's 09-08 rule). Check off an existing dashboard task only if one exists for that exact variant.
* Delete this doc and its board and README entries when every cell in the matrix is ✅ and no new final is pending.

## Found while auditing (for Dan, not jobs)

* **Approved Ad 1 and Ad 2 verticals print a caption over the closing CTA pill for about 7 frames** (memory
  `caption-trailing-entry-overprint`). The fix is a caption rebuild + mux with no re-render, but the files are live on YouTube, so a fix
  means new video ids swapped into the Demand Gen ads. Dan decides.
* **Muhammad's Ad 2 16:9 (live, `Dtk5knWM7c8`) and its approved square/vertical show the email-capture screen** at 3:11–3:23
  (Phase 2 compliance finding, still open on the board). J3's cutdowns exclude it. The full-length files are Dan's call.
