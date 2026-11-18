AD (Great Again T upsell video). GAT Upsell 4 AD R1. Job WV-07 "Great Again T Upsell 4: Abs By AI", round 1, Claude owner (Opus 5.5, high effort; Fable 5.2 high for the independent reviewer only if the trial in memory `fable-5-2-release` is still running).

Dan requested this edit on November 18, 2026 in the original chat titled "GAT Upsell 4 AD R1" (his words: "Use /ad-edit. Key with the approved house chroma key. Best take of every line, first-review approvals before the full render, every gate, independent audit, deliver, send me the review copy, update the queue."). That chat did no production: routing returned wait (M2 3 of 3 slots full with DS-98, RO-39, WV-03; M6 internal drive below its 80 GB reserve after Upsell 2's 53 GB reservation; WV-06 Upsell 3 queued just ahead). This immutable brief transfers the same authorized request to the capacity queue; it is not a second competing edit. Queue row WV-07 was READY; the submitting chat set it in_progress. Dan's explicit request covers this video even though it sells the Abs By AI app: it is a Great Again T funnel upsell, not one of the cancelled Abs By AI ads.

## Read before production

- AGENTS.md, CLAUDE.md, `.claude/skills/_shared/VIDEO-RULES.md` in full, `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`.
- `Handoffs/video-editing/WV-07-great-again-t-upsell-4-abs-by-ai.md` (the job doc) and `Docs/SHOOT_1113_FOOTAGE_REPORT.md`.
- `/ad-edit` skill (`.claude/skills/ad-edit/SKILL.md`), `.claude/skills/_shared/chroma-key/README.md`, `.claude/skills/_shared/hyperframes/README.md`, `.claude/skills/_shared/CUT-CONTINUITY-QC.md`.
- Dan's upsell style direction: `Handoffs/video-editing/WV-04-round-2-revisions.md` sections 1 and 2, memory `gat-upsells-cleaner-more-camera`. Cleaner, less busy, more trustworthy than the VSL; more Dan on camera, fewer AI clips (two or three at most in the whole upsell); graphics and clips only on a key point, about one a minute outside the offer section; high production value from the camera scene itself; key-point cards slightly larger than the VSL's (taller; clearly wider with a lot of text).
- `scripts/edit-queue/README.md` for batch execution, durable outcomes and approval stops.

## Sister upsells to reuse (same roll, same lighting, same day)

- Upsell 1 (WV-04) on the M2: `/Volumes/Expansion/_edit_work/WV-04/`. Round 2 delivered on http://127.0.0.1:9813/; notes `round2/ROUND-2-NOTES.md`. Reuse its C1904 key calibration (`key/`), look and voice recipes (`look/LOOK_WV04.json`, `look/VOICE_WV04.json`, `recipe/`), Wood Kitchen 1 background, card geometry and review-page builders, copying into this job's own folder. Never run a script inside another job's folder.
- Upsell 2 (WV-05, M6 `~/Projects/_edit_work/WV-05`) and Upsell 3 (WV-06, queued on the M2) are separate live jobs. Read only; never touch.
- Great Again T VSL (WV-03, `/Volumes/Extreme/_edit_work/WV-03`): approved bottle render and graphics in `round7/graphics/`. Copy, never run inside it. Bottle and label only from the locked design (`Contest/approved/DESIGN-LOCK.md`), never an AI-drawn label.
- Recommended options on the page: Colour Matched and voice House bass (Dan's Upsell 1 picks). Still show the alternatives, level-matched.

## Source

M2 raw: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/C1904.MP4`, approx 44:43-54:50 is Upsell 4 (Abs By AI); 31:18-44:43 is Upsell 3. Second copy on the Expansion. Never modify originals. Portrait: stored 3840x2160 rotation -90, decode to 2160x3840, add no transpose. FX30 29.97p, S-Cinetone / Rec.709, grade as Rec.709, decode BT.709. One stereo LPCM stream: read the roll sidecar first (`roll_sidecar.py show`) for word timings and mic pick. Mark used ranges after the final EDL.

Script: Great Again T upsell scripts, Google Doc `1lOl-CdLLIkvMQmECAmHz2WmrHfbpDOzxMuKlTMtXRcc`, section "UPSELL 4: ABS BY AI" (copy at `/Volumes/Expansion/_edit_work/WV-04/script/doc_full.txt` line 275 on; refresh from the live Doc). Offer: $67 one time, lifetime access, one-year guarantee; members normally pay $19.99 a month. Filmed wording wins where Dan departed from the script. Watch the whole range: hook restarts and retakes are common. Pick the best (normally last clean) take of every line; fix stumbles inside kept takes; zoom cuts, never naked jump cuts; hair-anchored NEAR/FAR fixed framing with verified hair clearance.

The script's own on-screen cues (build these first; they are the graphics that earn their place):
- The four "signs you're holding your testosterone back" list, each sign appearing as Dan says it.
- The app on a phone next to the Great Again T bottle (real approved bottle render; real app screens).
- Study card: Leproult and Van Cauter, 2011, JAMA: one week of 5-hour nights, testosterone down 10 to 15%. Print only what the study and Dan's line support.
- App screen recording, each feature shown as Dan names it: custom workouts, custom meal plans, photo calorie tracking, Sleep Coach, future-body picture.
- Price card: "$19.99 A Month" crossed out, "$67 One Time. Lifetime Access". Title capitalization, no em dashes.

Abs By AI app footage rules (they bind this upsell):
- Reuse approved app assets first: the RO-06 phone-beside-Dan feature tour (`B0544` phone screen, method `longform-edit/reference/ro06/phone_side.py`, captures from `appcap6.py`), the WV-01 workout-app format, existing VSL/app recordings. Leading with calorie tracking and workouts is Dan's stated preference.
- Meals: never the rejected chicken-and-broccoli plate (`B0035` and its sources/stills); salmon with Brussels sprouts or another appetizing verified dish; a food photo stays visible; calorie tracking shows the real app action and its matching result after the photo (memory `meal-showcases-appetizing-photo-first`).
- Workouts: real AI-Dan or real exercise demo videos only, never stick figures.
- Future body: before and after are the same person, shown on separate screens, never side by side; the only real app upload is a man who is not Dan (memory `app-recording-before-after-pair`); no "Meet the new you" or email-capture screen; AI-generated physiques carry the AI label, placed on the picture, clear of faces and abs.
- No unbelievable numbers or comparisons in on-screen graphics.

## Deliverable: one native 1080x1920 upsell for the phone funnel. No 16:9, no square, no cutdowns.

## First review, then stop

1. `editcap.py acquire WV-07` on the M2, then `renderq.py workdir WV-07 --need <honest GB>` (submitted estimate 150 GB; WV-04 used 316 GB over two rounds). All heavy steps through renderq; chains under `stallwatch.py run`.
2. House key (Bill Maher R2) calibrated to this range with `calibrate.py` on hard-motion excerpts (hair, hands, watch), each piece keyed once through `keyonce.py`. Measure rim, edge flicker, transparency, specks against the source on light, dark and pink backgrounds. If WV-04's calibration measures as valid on this range, reuse it and say so.
3. Take map and tight EDL of the whole read. This is a short ad: if every item in the rest of the film is a kind Dan has already seen moving (key, look, voice, cards, bottle, app scenes), build and show the WHOLE upsell at 1080p in round 1 (VIDEO-RULES, "Short-form and ads: build the whole video"); otherwise the first 60 seconds, with the camera scene in any slot that waits on a pick.
4. Colour options on identical frames; playable level-matched voice options on the same continuous passage starting on speech (House bass recommended). Shared mic pick and voice_chain, no unproved dereverb.
5. Every proposed graphic, app scene, product shot and clip in timeline order on its actual frame with 3-5 s of real narration around it, in the floating scrubbable context player. Soft Blue Light HyperFrames motion throughout each graphic's screen time. Library first; any new AI clip shown as complete START+END pairs (Google subscription attempt plus Codex, blind, frame gate and fresh frame-reviewer) with motion waiting for Dan's pick. Archive every generated take per the clip-library filing rule before pausing.
6. Correct and inspect every B-roll insert in the final rendered frame.
7. Managed review page (`review_server.py`, film at top, "What I decided" list, colour/voice controls, asset cards, short questions). Test in the side pane at 800 and 1150 px. Silent checks, then Finish checks for owner (paused, sound ready). Copy review videos of 45 s or more to `Videos to Review/` on the M6 with task-first names (`GAT Upsell 4 AD R1 - ...`). Mirror the page to the M6 and prove link 200, media range 206 and seeking at the same http://127.0.0.1:PORT/ link.
8. Release the slot at the review stop (`editcap.py release WV-07 --review`). Record a needs-dan outcome with the link, hashes and remaining work.

After Dan's picks (same chat continues): full render, every gate at current GATE_VERSION on the exact file (audio gate with seamscan on every join, delivery gate, hair, caption proof, sync, watch pass), independent ra-reviewer audit (expect DOES NOT SHIP first), fix, deliver to `Claude Ad Videos/Great Again T Upsell 4 Abs By AI - WV-07/` with notes, recipe and stamps, review copy to Dan with timestamps, `queue.py set WV-07 delivered` and mirror to the Edit Queue page. Final approval then gets the setup handoff (Codex owns setup). No covers, uploads or scheduling in this job.

## Recording

Update only WV-07's queue row, job doc and own board entry. Keep "first review delivered", "full film delivered", "Dan approved" separate. Never claim approval from silence. End every report to Dan with the two wrap-up boxes.
