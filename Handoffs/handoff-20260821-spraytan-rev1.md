# HANDOFF — Spray Tan longform, revision 1 (clip/graphic pass + fixes)

**Created:** 2026-08-21 · **Status:** NOT STARTED · **Skill:** `/longform-edit`
**Recommended model/effort:** **Opus 5, Extra High.** Justification at the bottom.

---

## What you are revising

`claude edited long form content/01 - My First Spray Tan/FINAL_spraytan.mp4` (19:00, QC PASS).

**Everything you need is already built — do not re-cut from scratch:**

| file | in |
|---|---|
| `ranges.py` · `chips.py` · `edl.json` | the delivery folder AND `.claude/skills/longform-edit/reference/` |
| working dir, transcripts, silences, **segment cache** | `/Volumes/Seagate 4TB/_edit_work/spraytan/` |
| generic scripts | `.claude/skills/longform-edit/reference/*_generic.py` |

**READ `.claude/skills/longform-edit/SKILL.md` FIRST.** It carries every trap this pipeline
has paid for. The two that matter most here: work on the Seagate, and **never delete
`_edit_work/spraytan/clips_graded/`** — it is the segment cache. A revision re-extracts only
changed beats (last run: 40/42 reused).

**Source roll:** `/Volumes/Seagate 4TB/abs by ai 8:3 jeff chagrin shoot/main camera/C1512.MP4`
**Grade (already correct, do not change):**
`curves=all='0/0 0.079/0.006 0.25/0.262 0.50/0.552 0.80/0.862 1/1'` — and **no white-balance
correction**, deliberately: the warm cast IS the spray tan, which is the subject.

---

## Dan's notes, in his words, with the work already scoped

### 1. `0:03–0:11` — before/after stills, left and right

> *"when I say 'here on the left' and 'here on the right,' insert the pale image, the 844C5D1,
> that one, insert that on the left. And insert the tanned image on the right. Crop this,
> though, so that it only shows me, and eliminate all that unnecessary space on the sides and
> the top of the picture before inserting it into the video."*

- **PALE (left):** `photos/Dan Before Pictures/844C5D19-B13D-41E8-AE31-7BCC8A72D709_1_105_c.jpeg`
  — verified present, 442 KB.
- **TANNED (right):** a finalized social-media pick from the 7/31 pool shoot,
  `photos/finalized social media photos/photo-*_FINAL_PRIMARY.jpg`. **Match the pose to the
  pale shot** if you can — a direct comparison is the whole point.
- **Crop both tight to his body** before compositing. Dead space kills the comparison.
- Beat is `intro`, final `0:00.00–0:25.72`, source `135.76–161.48`. His line lands: "Here on the
  left…" ≈ `0:03`, "And here on the right…" ≈ `0:07`, "And here on video…" ≈ `0:11` (that last
  one is him on camera — leave it clean).
- Suggested treatment: two-up split with the J2 olive rule between, or L then R timed to the
  words. Either way it must be **off screen by `0:11`**.

### 2. `4:00` — junk footage / repeated take

> *"junk footage and repeated takes were kept in here. Eliminate this junk footage."*

He is right, and this was a known kept stumble — `ranges.py` comments it as
`# self-correction kept (no clean internal cut)`. The exact words, from the source roll:

```
…get your back,[463.28→464.08]  then[464.08] this[464.20] if[464.68] you[465.38~] have[466.98] someone who can help you apply the tan…
```

`you`[465.38] is a **stretched word** (1.6 s) — Whisper folded the pause into it, so its `end`
is fake. Two ways to kill it, in preference order:

1. **Cover it with a cutaway** (he wants clips everywhere anyway — this beat is literally about
   *someone helping you apply the tan*). Cleanest, zero cut risk.
2. Split `diy-helper` into `459.18→464.10` + `466.90→483.24`. Reads "…get your back, → have
   someone who can help you apply the tan…". Slightly abrupt; listen-QC it.

**Do NOT** create an adjacent pair under 0.20 s apart — the builder and QC both assert against
it now (an artificial split mid-speech makes render.py's 30 ms fades dip audibly).

### 3. `9:24–9:40` — three before/after pairs

> *"Insert 3 different pairs of pictures (6 total) comparing before and after the spray tan…
> try to get two that are in the same pose so you can do a direct comparison. Also, make sure
> to crop these images…so that there's not excessive space around me and the extent of the tan
> is more visible."*

- **TANNED:** `photos/finalized social media photos/` (7/31 pool shoot — that shoot was 2 days
  after the tan, which is why it is the "after").
- **PALE:** search **Apple Photos for "Daniel Rose"** — his screenshot shows the pool-side set
  he means. **Not** the tanned/retouched ones; pick clearly pale frames. Same pose as the
  tanned pick wherever possible.
- Beat is `before-after-photos`, final `9:21.07–9:54.64`. His narration there explicitly
  invites judgement ("I'll let you judge for yourself"), so give each pair ~4–5 s.
- Crop tight, same framing on both halves of a pair, consistent treatment across all three.

### 4. `11:08` — dead pause

> *"Slight pause here, cut this and cover with a stock clip"*

Confirmed: source silence **`1010.79→1011.89` (1.10 s)**, between "…and is aging you." and
"Not only does sun damage give you cancer…". Final-edit `11:08.9`. Cover it, or tighten the
range; covering is what he asked for.

### 5. THE BIG ONE — clips and graphics throughout

> *"I think it's too much on the camera scene, not enough breaking that up… insert a large
> amount of stock footage and graphics… generally there shouldn't be more than 30 seconds
> without a clip or some kind of graphic… I'd rather have a little bit too much and eliminate
> them than not enough."*

**This is the bulk of the job.** 19:00 at a ≤30 s gap ⇒ **~40 inserts minimum**. There are 26
J2 chips already; they count toward the rule, so **map the existing chip timings first and
fill the gaps** rather than starting from zero.

- **Sourcing: Pexels first, free, no API key** — `https://www.pexels.com/download/video/<ID>/`
  curls straight to the CDN. AI-generate only where nothing suitable exists. This is the
  documented convention in `.claude/skills/ad-edit/SKILL.md` (Ad #1 filled every slot from
  Pexels for $0). Check `Media/B roll/` for anything reusable before sourcing.
- **Budget:** $25/session standing authorization. Pexels should keep this near $0; state the
  estimate before any AI generation batch.
- Obvious content beats to illustrate: cameras flattening definition, fitness models/stage
  tan, the studio booth, aerosol/wipes, the $80+$20 cost breakdown (graphic), the 8-hour dry
  window (graphic/timer), shower rules (graphic list), the 7-day fade (graphic), water/pool,
  sun damage & skin cancer, pale/ginger skin, the $50–$100 con (graphic), golden-hour lighting,
  the pump, fasted shooting, posing.
- **Keep him on camera for the personal/story beats.** The point is to break up monotony, not
  to bury him.
- Full-frame AI-generated clips need the **AI-GENERATED tag** per the ad-edit rule if any are
  generated rather than stock.

### 6. Jump cuts → 10 % zoom cuts

> *"this video contains many jump cuts. Eliminate the jump cuts with a zoom cut. I believe a
> 10% zoom cut was what worked best in our last try."*

Correct — 10 % is the value the invest-health v3 revision settled on (6 %→10 %). There are
**41 joins**. Alternate in/out so it doesn't creep, and skip any join you have covered with a
clip (a cutaway already hides the jump — a zoom there is wasted). Supersample the scale to
avoid the shimmer that bit the earlier Ken Burns pass.

---

## 7. Deodorant marks — TESTED, here is the recipe

He asked whether editing can reduce the white underarm residue. **Yes — I built and measured a
fix before writing this. Do not re-derive it.** Full reasoning is in the chat; the working
numbers:

- Residue signature: **saturation ≈ 0.24, value ≈ 0.35** (desaturated grey on dark hair).
- Neighbouring armpit hair: sat **0.61** · arm skin: sat **0.79** · chest skin: sat **0.56**.
  Background fridge/wall: value **> 0.85**. So a saturation key with a value ceiling separates
  the residue from *everything else* — **0 % false positives on skin** in the test frame.

**The filter (verified working):**

```
geq=r='r(X,Y)*(1-0.28*(W))':g='g(X,Y)*(1-0.45*(W))':b='b(X,Y)*(1-0.63*(W))'

W = box * clip((0.45-sat)/0.20,0,1) * clip((0.62-val)/0.15,0,1)
sat = (max(r,g,b)-min(r,g,b))/max(max(r,g,b),1)
val = max(r,g,b)/255
box = feathered rectangle around the armpit (18 px feather)
```

The multipliers map the residue colour (88,76,67) exactly onto the neighbouring hair colour
(63,42,25) at full weight, so **texture is preserved** — it re-tints rather than paints over.

**Measured on the test frame (`t=14.0 s`, box `1225,675→1320,790`):**

| | result |
|---|---|
| residue-signature pixels | **482 → 191 (60 % reduction)** |
| pixels altered outside the box | **0** (max delta 0) |
| same filter at other arm positions | near-inert — 23 px / delta 1 at `t=12.5`, delta 7 at `t=11.0` |

That last row is the important one: **the filter is self-limiting.** It only acts where the
signature exists, so a generous static box per shot is safe — no tracking, no keyframes, and
because it is deterministic per-pixel with no temporal term, **it cannot flicker.**

**Recommended approach (combination):**
1. **Cover the worst moments with cutaways** — the arms-raised gestures at ≈`0:13` and ≈`1:00`
   score highest, and he wants clips there anyway. Free and perfect.
2. **Apply the filter to the remaining arms-raised beats**, per-beat box, in the extraction
   filter chain alongside the grade so it costs no extra pass.
3. **Stop at ~60 %.** Pushing harder starts reading as a dark smudge, which is worse.

**Do not** attempt per-frame AI inpainting — 34,000 frames, and frame-to-frame inconsistency on
a moving arm looks far worse than the stain.

**Production note for Jeff/Dan:** the real fix is at the shoot — clear/invisible-solid
deodorant, or wipe the underarms down before rolling. Worth adding to the shoot checklist.

---

## Order of work

1. Re-read `SKILL.md`. Set `PATH` to the static ffmpeg (`Media/video_edit/bin/`).
2. Fix the cut first — items **2** and **4** — in `ranges.py`, rebuild the EDL, check flags.
3. Map existing chip times, list every gap > 30 s, and plan the insert list. **Show Dan the
   plan before sourcing 40 clips** if anything is ambiguous; otherwise proceed.
4. Source stock (Pexels first), build the still composites (items **1** and **3**).
5. Zoom cuts on remaining uncovered joins.
6. Deodorant filter on the arms-raised beats not covered by a cutaway.
7. Render (cache makes this cheap) → composite → **rebuild the SRT and chapters**, because
   every timing shifts.
8. **QC: `qc_generic.py` must PASS all six checks**, then `srt_validate.py` ≥ 10 windows.
9. Deliver **into the same folder** (`claude edited long form content/01 - …`), keeping
   `FINAL_spraytan.mp4` as the name so nothing downstream breaks. Update the folder README.
10. Update `AI_COORDINATION.md` — **re-read it from disk immediately before writing**, a
    concurrent session wiped an entry today. Check this handoff's dashboard task off (Rule 9).

## Watch out for

- **The repo is public** and the delivery folder is now inside it. `.gitignore` has
  `claude edited*/` plus a global `*.mp4` rule, but run `git check-ignore -v` anyway.
- **Boot disk is ~98 % full (19 GB).** Render on the Seagate; only the finished file comes back.
  ~51 GB of safe reclaim is listed in the folder README if you need room.
- Timings shift the moment the cut changes — **SRT and chapters must be regenerated**, never
  hand-patched.
- Dan kept seven flagged lines deliberately (profanity, the Donald Trump tan joke). **Leave
  them in** unless he says otherwise.

## Why Opus 5 / Extra High

Volume plus precision. ~40 insert decisions need genuine editorial judgement about what
illustrates each point; the cut surgery needs millisecond accuracy against stretched-word
traps that have already produced clipped audio twice; and the deodorant work is a signal-
processing problem where a wrong threshold silently damages skin. Mistakes are expensive —
each one costs a render and a QC cycle. **Opus 5 High is acceptable if usage is tight**,
since the segment cache makes iteration cheap, but Extra High is the better trade here.
