# Handoff — put the newly finalized ads on YouTube and into Google Ads (Ads 6 and 14, plus 7 and 10)

**Written 2026-09-15** by the session that reviewed Muhammad's 09-14 batch of seven cuts. Dan's instruction that
session: *"Two of them are finalized and don't need revisions… create a handoff document to set up the finalized ads
in Google Ads and YouTube in a new task."*

This is **ops, which is Codex's lane since Dan's 2026-09-15 decision** (memory `codex-owns-non-core-work`). Model
recommendation is at the bottom.

**Goal:** every finalized 16:9 ad master is unlisted on the Abs by AI YouTube channel with a real description,
chapters, tags, the AI-content disclosure and a clean thumbnail, and is running in the Demand Gen conversion
campaign `24243839443` on its own ad groups, with the ids recorded. Nothing organic is published.

---

## What is finalized and what state it is in

| ad | title (script title, use verbatim as the YouTube title) | master | YouTube | Google Ads |
|---|---|---|---|---|
| **6** | You're Not Too Old to Get Abs. I'm Proof. | **filed 09-15** — `Muhammad Ad Videos/you're not too old to get abs i'm proof - ad 6/you're not too old to get abs i'm proof \| muhammad \| 16x9 \| ad 6.mp4`, 363,314,897 bytes, 1920×1080, 29.97, 8,208 frames, **4:33.9**, 10.3 Mbps. Drive `1jO-re15wKmdzD6SQsQLHkSbnVXdDUPOI` ("Daniel HQ Ad 6 V4 HD.mp4") | ❌ | ❌ |
| **14** | I Watched 400 Workout Videos and Gained Weight | ⚠ **not filed** — only "Daniel HQ ad 14 V3.mp4", Drive `1VQuOxzfbmXv_TgO5GgURXrLkkwusU6_k`, 79,337,649 bytes, 1920×1080, 29.97, 5,924 frames, **3:17.7**, but only **3.0 Mbps** (every other final is ~10 Mbps). See "Ad 14's export" below | ❌ | ❌ |
| **7** | In 2010 I Photoshopped My Face on a Fitness Model. AI Just Did It for Real. | filed 09-13 — `Muhammad Ad Videos/in 2010 i photoshopped my face on a fitness model ai just did it for real - ad 7/… \| muhammad \| 16x9 \| ad 7.mp4`, 1920×1080, 6,358 frames, 3:32.1. ⚠ **Muhammad re-exported it on 09-14** (Drive `1D7sc0Nyq_ViM1bEJGP4xXStMphpVzmFs`, 283,996,801 bytes, identical audio stream, same frame count, new picture encode) — see below | ❌ | ❌ |
| **10** | My Dad Bod at 38. My Dad Bod at 40. | filed 09-13 — `Muhammad Ad Videos/my dad bod at 38 my dad bod at 40 - ad 10/… \| muhammad \| 16x9 \| ad 10.mp4`, 1920×1080, 5,443 frames, 3:01.6. Drive `1582XKVpH-6LYq8fEJlFQksMZE0HL1Ct5` | ❌ | ❌ |

Ads 7 and 10 were finalized by Dan in the Upwork room on 09-12 (*"Both HD videos at 7 and 10 are looking good, and
those are finalized"*) and filed on 09-13, but nobody has uploaded them — the master queue notes *"Neither ad is on
YouTube or in Google Ads yet."* They belong in this job: same skill, same campaign, four ads in one session.

**Already live, do not re-do:** Ads 1, 2, 3, 4 and 5 (`Docs/AD_VIDEO_IDS.md`, `Docs/DGEN_CONVERSION_CAMPAIGN.md`).

### Ad 7's 09-14 re-export — resolve this first

The 09-13 filed file and the 09-14 Drive file have **byte-identical audio** and the same frame count and duration;
only the video stream differs (creation times 09-12 13:49Z vs 09-14 06:58Z). The 09-15 review session diffed all 6,358 frames. **The re-export
is a real picture fix, and it introduced one small defect:**

* **Fixed:** the panel at **2:48–2:51** ("GENERATING YOUR GOAL IMAGE / Is just the first step"). In the filed 09-13
  copy the header ran off the LEFT EDGE of the frame and the line under it was cut to "is just the first".
* **Broken:** on that same beat the AI label now reads **"AI-GENERATEd"** — lowercase final letter — for the panel's
  whole duration. Every other AI label in the ad is full capitals. Verified at full resolution at 2:49 and 2:51.
* Everything else is frame-identical (0:00–2:47, 2:52–3:32 unchanged; the sub-second differences at 0:00–0:01,
  0:20, 2:23 and 3:26 are animation/encode noise, checked at full resolution).

**So neither file is shippable as-is:** the filed one has a title running off screen, the new one has the typo.
A one-item round-5 note asking for the capital D went into Muhammad's doc on 09-15. **Wait for his corrected export**,
file it with `/editor-deliveries` as the Ad 7 master (replacing the 09-13 file) and upload that. If Dan wants Ad 7
live before that lands, the 09-14 file is the better of the two — the typo is a small chip, the cut-off title is a
whole header — but say so in the report and swap the video when the fix arrives.

### Ad 14's export

3.0 Mbps at 1080p is a review-grade export, not the ~10 Mbps HD Muhammad sends when an ad is done, and `/ad-setup`
step 0 refuses a draft-size file on purpose. **Do this:** tell Dan in your first report that Ad 14 needs the HD
export, and ask him to request it from Muhammad in the Upwork room (never message the editor yourself). The doc
section written for Ad 14 on 09-15 already says *APPROVED - FINALIZED - READY FOR HIGH QUALITY EXPORT*, so the ask is
expected. If Dan says to go with the 3.0 Mbps file, upload it and note the bitrate in `Docs/AD_VIDEO_IDS.md`; swap
the video later when the HD lands (a new video id + one more `videos` entry, the old ads paused — the skill covers it).

---

## How to run it

**Follow `.claude/skills/ad-setup/SKILL.md` end to end, per ad.** It is written for exactly this and every step in
it was run on Ads 3, 4, 5 and 3-again. Do not improvise around it. The parts that matter most here:

1. **Step 0 preconditions** — the latest `revision docs/adN-revisions-muhammad-round*.md` reads finalized, nothing
   newer exists, the file is 1080p-class, and nobody else owns the ad in `AI_COORDINATION.md`. For Ads 6, 7, 10 and
   14 the finalization records are: Ad 6 — the 09-15 doc section; Ad 7 and Ad 10 — Dan's 09-12 Upwork message, also
   recorded in `.claude/skills/editor-deliveries/state.json`; Ad 14 — the 09-15 doc section.
2. **Step 1 file the master** (curl from Drive, verify size, `ffprobe`, `state.json` row) — needed for Ad 14 only;
   Ads 6, 7 and 10 are already filed. Measure and report loudness/true peak; the editor's audio is never processed.
3. **A compliance pass before upload, on the delivered master.** Ad 2 is live in the campaign with the app's
   email-capture screen at 3:11–3:23 and a before/after screen at 3:11, found long after upload. For each of these
   four masters, scan every frame for the banned screens (the `compliance:banned_screen` check used by the video
   gates, or a frame sweep of the app-demo stretches at full resolution) and confirm: no side-by-side before/after,
   no "Meet the new you" reveal, no email-capture form. If one turns up, **stop and report it — do not upload it**.
4. **Steps 2–5** — title = the script title above, verbatim; description from the transcript with chapters + the UTM
   link; tags; "altered or synthetic content" = yes; thumbnail built the clean way, set and read back. ⚠ Two large
   uploads in parallel is the ceiling, and a failed upload still leaves an empty husk video that Dan has to delete
   in Studio (09-14 lesson at the bottom of the skill).
5. **Step 6 Google Ads** — one `scripts/ads/api/dgen-ads/adN.json` per ad (copy `ad3.json`), dry run, `--apply`,
   then `node scripts/ads/api/client.js policy 24243839443` the next day. Campaign `24243839443`, $30 target CPA on
   the ad group, two groups per ad (`/start` and home), $20/day budget shared across everything — say that in the
   report. **Never enable a campaign.**
   **Copy:** Dan's approved shapes *How I Got Abs At 40* and *How AI Got Me Abs* on every ad, plus plain lines about
   what that ad shows. No questions, no withheld payoff, no "trick", nothing medical. Ad 5's *Why My Diets Kept
   Failing* is DISAPPROVED as clickbait — do not write anything of that shape (memory `ad-copy-no-unbelievable-claims`).
   Ad-specific angles that are safe: Ad 6 age ("I got abs at 40"), Ad 7 the Photoshop story, Ad 10 the dad bod,
   Ad 14 the 400 workout videos — state them flatly, never as a tease.
6. **Step 7 record it** — a row per video in `Docs/AD_VIDEO_IDS.md`, a dated section in
   `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the `state.json` filed rows, commit and push, and check off the dashboard row
   *"Add the new finished ads to the Google Ads campaigns…"* only if every ad it names is in.

## When you are done

* Report to Dan in plain language: the four video links, what each description and thumbnail says (send the
  thumbnail review sheet with SendUserFile), the ad groups and their landing pages, that Google is reviewing, the
  shared-budget note, Ad 14's bitrate question, anything the compliance pass found, and that organic posting was not
  done — **an ad is never published organically** (Dan, 2026-09-17; `AGENTS.md`), and asking to "set it up on
  all platforms" does not change that.
* Tell the variants session it can start: **`Handoffs/handoff-20260915-ads-6-14-variants.md`** (jobs J15–J18 in the
  master queue) builds the vertical, square and ≤0:59 versions of Ads 6 and 14; Ads 7 and 10 are J10–J13 there.
  Uploading a variant later is the same skill with one more `videos` entry on the ad groups this job creates.
* Delete this doc, its row in `Handoffs/README.md` and its line in `AI_COORDINATION.md` when all four ads are live.

## Model and starter prompt

**Codex (GPT-6 Astra), effort high** — ops work, Dan's 09-15 lane decision. It reads the Claude skill file directly;
everything it runs is `curl`, `node` and the Ads/YouTube scripts in this repo. If Dan would rather run it in Claude,
Opus 5 at high effort does the same job.

> Execute `Handoffs/handoff-20260915-finalized-ads-6-14-youtube-and-google-ads.md`: upload Muhammad's finalized Ads
> 6, 7, 10 and 14 to YouTube unlisted with descriptions, chapters, tags, the AI disclosure and thumbnails, then add
> each to the Demand Gen conversion campaign `24243839443`, following `.claude/skills/ad-setup/SKILL.md` end to end.
> Resolve Ad 7's 09-14 re-export and Ad 14's 3.0 Mbps export question first, run the banned-screen compliance pass on
> every master before uploading, record the ids in `Docs/AD_VIDEO_IDS.md` and `Docs/DGEN_CONVERSION_CAMPAIGN.md`,
> commit and push, and report to Dan in plain language.
