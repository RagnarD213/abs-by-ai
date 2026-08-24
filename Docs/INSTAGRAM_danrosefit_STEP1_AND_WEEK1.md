# @danrosefit — profile copy, archive split, and week one

Companion to `Handoffs/handoff-20260824-instagram-migration-danrosefit.md`.
Steps 1 and 6. Steps 2–5 are built and dry-run-verified but **blocked** — see the
bottom of this file.

Image assets live in `Short-form video content/instagram-danrosefit/`
(gitignored — Dan's personal photos, and the repo is public).

---

## Step 1 — profile copy

### Bio — 139 characters, under Instagram's 150 limit

```
200 lbs at 38. Real six-pack at 40.
No trainer. No coach. I used AI.
Ab tactics + fat loss for men 35+.
See YOUR abs before you have them ↓
```

### Links

| Slot | URL |
|---|---|
| 1 | `https://absbyai.com/?utm_source=instagram&utm_medium=bio` |
| 2 | the YouTube channel |

The profile currently has **no website link at all** — the "AbsbyAI.com" in the bio is
unclickable plain text. This is the highest-value ten seconds on the account.

### Name field — leave it as "Daniel Rose"

Meta Verified requires it to match the government ID. Do not turn it into a keyword
string, and leave the "AI creator" label **off**.

### Profile photo

`profile-photo_danrosefit_1080.jpg` — a face-and-shoulders crop from
`photo-223_FINAL_PRIMARY.jpg` (pool shoot, already retouched). Checked at 40 px, which
is the size it actually renders at next to a comment: the face still reads, which the
current full-body shot does not. Shoulders are in frame, so it still says fitness at a
glance, and the face is unobstructed for Meta Verified's photo-matching check.

### Four Highlight covers

`highlight-cover_{my-story,see-your-abs,ab-workouts,the-app}_1080x1920.png`, J2
tactical system (`MIL` palette — near-black field, olive rule, Impact caps).

Instagram crops a highlight cover to a **circle taken from the centre** and renders it
at about 64 px. Every word was sized against that: the build script asserts each corner
of the type block falls inside the visible circle, and all four were proofed at 64 px
before delivery. Rebuild with `_build-highlight-covers.py`.

### Archive split — the recommendation, since no list came back

Roughly 19 posts down to 9–10. **Keep:** the physique shots, the "GENERATED MY DREAM
BODY, THEN I BUILT IT" transformation graphic, the three jiu-jitsu posts. **Archive:**
the family ski trips, the photo collage, the ziplining, the hot tub, the group shots.

Two of the archived posts contain children's faces. That is a reason to archive before
pointing paid traffic at the account, independent of how the grid looks. Archiving is
reversible — nothing is deleted.

---

## Step 6 — week one

### Delivered: the Wednesday carousel

`carousel-week1_skip-list_01…09.jpg` — 1080×1350 (4:5, the tallest ratio Instagram
shows uncropped), cover + 7 numbered slides + closer. **"7 things I'd skip if I started
over at 40."**

Saves are the one engagement signal the account has almost none of, and a carousel is
the format that earns them. The topic deliberately avoids the queue: the four-ab-muscles
idea is already both a scheduled reel (17 Oct) and a backfill reel (21 Sep), so it could
not also be week one's carousel.

Caption:

```
7 things I'd skip if I started over at 40.

Every one of these cost me time, money or both. The last one is the one that
actually changed the result.

Save this before you spend another dollar on the first one.

Comment ABS and I'll send you the free AI preview 👇

#over40 #sixpackabs #fatloss #fitnessover40 #aifitness
```

### Not delivered: the four reels — and why

The Mon / Tue / Thu / Sat reels are **specified below, not cut.** Cutting them is
`/shorts`, which picks segments with Dan in the loop rather than guessing, and four
video builds is its own session. Each slot below names its source so that session
starts from a decision, not a search.

| Slot | Format | Source | The specific ask |
|---|---|---|---|
| **Mon** | Myth-kill, 15–25 s | `03 - The Supplements I Actually Take` | The "your supplements are 3% of your results" beat. Hook in frame one, no windup. Best-performing shape in the data. |
| **Tue** | AI in action, 20–30 s | **screen recording — does not exist yet** | The app generating a real abs preview, start to finish. See below. |
| **Thu** | One exercise, one cue, 10–15 s | `Media/exercise-demos/` (33 finished) | One demo video, one J2 title card, one cue. Cheapest slot in the week and it lifts completion rate for whatever posts next. |
| **Sat** | Over-40 / real life, 20–40 s | `04 - Why You Should Invest More In Your Health` | Identity, not tactics. Currently missing from the account entirely, and it is what converts. |

**Friday is deliberately empty** — Stories and 30 minutes of outbound commenting.

**The Tuesday slot is the important one.** Nothing in the 176-post queue is a screen
recording of the app generating someone's abs preview, and it is the only asset no
competitor can copy. It also has a hard rule attached: **the email-capture screen must
never appear**, in this or any demo.

---

## Steps 2–5 — built, dry-run clean, blocked on one OAuth click

`scripts/blotato/danrosefit_migration.py` executes the whole queue rebuild. It ran
against the live queue today and **all nine plan invariants passed**; nothing was
written, because `@danrosefit` is not connected to Blotato.

**Dan:** Blotato → Settings → Social accounts → add Instagram, signing in with the
**Instagram** credentials rather than through Facebook. If it errors, link the Instagram
account to the Abs by AI Facebook Page and retry. Then:

```bash
python3 scripts/blotato/danrosefit_migration.py --apply
```

It resolves the account id itself, refuses to write if any invariant fails, and records
every write to a state file so a re-run resumes instead of double-posting.
