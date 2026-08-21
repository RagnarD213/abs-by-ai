# HANDOFF: "Why You Should Invest More In Your Health" — cut-down variants

**From:** Claude Code (Fable 5, 2026-08-20) · **To:** fresh session, AFTER the v3 revisions
(`Handoffs/HANDOFF_invest_health_v3.md`) are executed AND Dan has approved v3.
**Do not start until Dan says v3 is approved** — variants cut from an unapproved base inherit
its junk three times over.
**Skill:** `/longform-edit` (read the Junk-footage detection + Whisper-timestamp sections first).
Opus 5 / medium effort is sufficient — the editorial judgment is pre-baked in the beat map below.

## Deliverables

1. `INVEST_HEALTH_conservative.mp4` + `.srt` — target **40–44 min** (cut ~10–13 min from v3's ~53).
   Remove repetition and belaboring only; EVERY outline point survives.
2. `INVEST_HEALTH_sub30.mp4` + `.srt` — target **< 30:00 hard**. Keep outline points wherever
   possible; the three big levers (below) are approved drops.
3. Dan then picks ONE variant; b-roll / AI-clip / graphics dressing happens only on the winner
   (separate future task). Do NOT dress the variants.

## Method

- Derive each variant from the FINAL v3 `edit/edl.json`: copy `build_edl.py` →
  `build_edl_cons.py` / `build_edl_sub30.py`, add a per-variant list of extra cut spans, keep all
  existing cuts/capper/zoom logic. Same word-snapping rules; same stretched-word caution
  (re-transcribe from source before cutting near any word >1.5 s).
- **Dan's repetition pattern: statement → restatement → example → restatement. Keep the FIRST
  statement + the STRONGEST example; cut restatements.** When a claim appears with and without a
  concrete number/story, keep the one with the number/story.
- **Never cut:** the sentence each J2 chip anchors to (chip source-times in `edit/build_gfx.py`);
  the Abs-By-AI plugs (photo-tracking mention ~src 1522–1565, full outro ~src 4062–4127); the
  v2/v3 inserts' beats (soup split ~1531–1537, placeholders ~1857–1911, Oura/Whoop ~2664–2779,
  Bryan Johnson ~3798+, supplements-joint graphic ~3056–3063); every hedge/disclaimer in the
  therapy-meds and steal sections if those sections are kept (the disclaimers are load-bearing).
- Overlays/chips/SRT are source-time-keyed and follow automatically. If a beat carrying an insert
  or chip is DROPPED (sub30 levers), delete that overlay from `composite.py` / that chip from
  `build_gfx.py` for that variant. Keep per-variant copies of `chip_timings.json`.
- Zoom parity re-shuffles per variant — full render each (~35 min), that's expected. Render each
  variant ONCE after all its cuts are final.
- QC per variant: the full v3 gate (duration/loudness/joint re-transcription on EVERY new cut,
  phrase-shingle repeat scan, contact sheets at new joints, chips on/off, `grep -c GOP` = 0).

## Beat map (src-time anchors; per-section duration targets in seconds)

| # | Section (src anchor) | v2≈ | Cons. | Sub30 | Editorial notes |
|---|---|---|---|---|---|
| 1 | Intro + halo setup (2.8–104) | 56 | 40 | 25 | Collapse the triple "halo effect" naming + "fat guy with money" riff to one pass |
| 2 | Job/partnership (111–156) | 45 | 40 | 25 | Keep job odds; partnership → one line |
| 3 | Relationship/divorce (178–268) | 90 | 60 | 35 | The "she won't say X, she'll think Y" mirror runs both directions — keep negative direction + one positive line |
| 4 | Dating (274–378) | 88 | 65 | 40 | Keep: 70% online, looks paramount, "10Xed my matches", winner-take-all. Cut the real-world-vs-online mechanics |
| 5 | Productivity + meal service (387–495) | 90 | 70 | 45 | Keep Taco Bell slump example; cut the "first few days" hedging repeat |
| 6 | Doctor time-cost (500–549) | 42 | 30 | 20 | The appointment-logistics listing (make/wait/go/fill/drive) → 2 items |
| 7 | Long-term thinking (555–614) | 52 | 45 | 25 | "Short-term thinking is why you're poor" is the keeper line |
| 8 | Mental health spiral (624–730) | 90 | 70 | 40 | Keep the spiral (meds→fat→worse); cut the second "trapped" pass |
| 9 | Bad health expensive (738–805) | 62 | 45 | 30 | |
| 10 | Diabetes friend story (811–916) | 103 | 90 | 60 | ANCHOR story — trim only the doubled dollar-figures and eye-injection restatement |
| 11 | Money-dead + inheritance (921–1002) | 68 | 50 | 35 | Keep "money does you no good if you're dead" + inheritance-lawsuit line |
| 12 | Not-dead-but-sick hypotheticals (1007–1149) | 122 | 85 | 45 | Four parallel hypotheticals (vacations/vision/stairs/kids/wife) → keep stairs "first floor like an old person" + kids |
| 13 | Brokie pivot + cut-bullshit (1174–1222) | 45 | 40 | 35 | Pivot point — light touch |
| 14 | Never-cut list (1227–1293) | 60 | 50 | 35 | Outline list — compress commentary, keep all 3 items |
| 15 | Bars & clubs (1306–1458) | 115 | 80 | 50 | Intro + "you don't need entertainment" + "not forever" all restate — one pass each |
| 16 | Restaurants (1464–1565) | 88 | 70 | 45 | KEEP the Abs-By-AI tracking plug intact |
| 17 | Junk food (1570–1606) | 36 | 32 | 28 | Already tight |
| 18 | Vacations (1612–1690) | 68 | 55 | 35 | Keep his 2-3 lb/week number |
| 19 | Therapy & psych meds (1694–1754) | 55 | 50 | **0** | **SUB30 LEVER 1: drop wholesale** — not in the outline, highest policy risk, saves ~55 s. If kept (cons.), keep every hedge |
| 20 | Sacrifice recap: subs/dates/clothing/car (1767–1817) | 45 | 30 | 25 | Outline items live HERE — compress, don't drop |
| 21 | Brokie tier: setup + food + Costco (1844–2077) | 195 | 150 | 100 | Placeholders live here (keep beats). "Beg/borrow/steal" + disclaimer block → the softened retake only |
| 22 | Premium protein + 401k-vs-salmon (2089–2257) | 155 | 120 | 80 | 401k-vs-salmon is a signature take — keep |
| 23 | Mattress + Purple + fluids (2269–2490) | 195 | 145 | 70 | **SUB30 LEVER 2: drop the fluids riff (2416–2490, ~70 s)** — polarizing, demonetization-adjacent; cons. trims it to ~30 s. Keep the mattress case + Purple rec |
| 24 | Gym membership / best people (2498–2629) | 115 | 90 | 60 | Keep "best people not best equipment" + osmosis in one pass |
| 25 | Sleep tracker (2664–2779) | 100 | 80 | 55 | Oura/Whoop graphics beats must survive; Apple-Watch cons-list → one line |
| 26 | GLP-1 (2784–2962) | 165 | 130 | 90 | Core Dan content; "cash out the college fund" stays (engagement) |
| 27 | TRT (2967–3047) | 72 | 55 | 35 | He hasn't started TRT — weakest tier-2 item; keep the outline mention |
| 28 | Supplements big-3 (3056–3219) | 145 | 110 | 70 | Supplements graphic joint stays |
| 29 | Baller: home gym + both-worlds (3234–3405) | 150 | 115 | 70 | **SUB30 LEVER 3: drop the COVID shed story (3275–3313, ~35 s)**; keep "gym membership AND home gym" |
| 30 | Meal prep / chef (3415–3537) | 105 | 85 | 55 | Keep Clean Eats + $120/wk numbers |
| 31 | Outsource chores (3546–3587) | 40 | 35 | 25 | |
| 32 | Trainer & nutritionist (3595–3682) | 85 | 65 | 40 | Keep the top-1%-only argument (sets up AI pitch) |
| 33 | Mega-baller + Bryan Johnson (3695–3834) | 118 | 90 | 60 | BJ clip beat survives |
| 34 | Summary (3839–3963) | 108 | 70 | 40 | Retention dies in recaps — cut hardest here |
| 35 | Outro CTA (4062–4127) | 64 | 64 | 50 | Conversion — light touch only |

Approx totals: conservative ≈ 42–43 min; sub30 ≈ 28–29 min (with the three levers). If sub30 lands
over 30:00 after QC, take the overage from sections 3, 12, 15, 34 (in that order) — never from 10,
16, 22, 26, or 35.

## After both variants pass QC

Deliver both files + SRTs to Dan (SendUserFile the SRTs + a per-variant duration/QC summary),
update `AI_COORDINATION.md`, check off the dashboard Key task for THIS handoff, and stop —
the pick and the dressing are Dan's next call.
