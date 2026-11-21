# The ad study behind /ad-edit (2026-08-20)

Eleven winning direct-response ads downloaded, scene-detected, and read frame-by-frame
(per-shot contact sheets) before this skill was written. Raw media, contact sheets, scene
lists and `shot_stats.json` are preserved at **`/Volumes/Extreme/ad-edit-research/`**.
Dan's full performance archive is the Google Sheet **"Copy of SixPackAbs.com Channel YouTube
Commercials"** (`1Hot1_JQiKIAfvaqQ5t92YCK6IOV28GlFR5SRgE52rck`, 40 product tabs) — **green
fill `FF00FF00` = his best performers, red `FFFF0000` = worst, ignore every other color.**

## How to download a reference ad (SABR workaround, verified 2026-08-20)

Plain yt-dlp fails ("YouTube is forcing SABR streaming"). The android player client works:

```bash
~/Library/Python/3.9/bin/yt-dlp --extractor-args "youtube:player_client=android" \
  -f "b[height<=720]/18" -o "vids/%(id)s.%(ext)s" \
  --write-auto-sub --sub-lang en --sub-format vtt "https://www.youtube.com/watch?v=<ID>"
```

You get format 18 (640×360) — enough for cut analysis and reading big graphics. Then
scene-detect (`select='gt(scene,0.25)'` with the static ffmpeg at `Media/video_edit/bin/`)
and tile per-shot midpoint frames into contact sheets (PIL — `drawtext` is broken in the
static build). A ~5 min ad reads completely in 2–3 sheets.

## The study set — measured shot statistics

| ad | what | dur | shots | median shot | first-30s median | notes |
|---|---|---|---|---|---|---|
| ZkUn5LvheGg | Green Detox "5 Key Superfoods" (Dan: "good pacing and editing") | 5:24 | 70 | 4.2s | 2.0s | set-based content lecture |
| JITLCor5dQ4 | TestMax "Have A Seat Pool" — Clark read, mark&amy hook (GREEN) | 5:02 | 69 | 3.5s | **0.71s** | skit hook → replay commentary → teal studio |
| XfWY3DAXC0o | Test Reload pool version — "CURRENT TOP VARIATION" (GREEN) | 4:45 | 66 | 3.1s | 0.83s | same format as above |
| ooeWA3covSw | TestMax "10 lbs lard" visceral-fat hook (FINALIZED WIN) | 4:19 | 42 | 5.2s | 5.1s | prop-anchored kitchen lecture |
| X1fi2ScpCQc | Test Reload "estrogen molecule" interview — DAN'S PICK (GREEN) | 7:18 | 65 | 6.5s | 8.1s | two-presenter whiteboard, uniform pace |
| vAAISx7k1jY | TestMax "Eat Like A Pig" (FACEBOOK WIN) | 6:58 | 63 | 4.1s | 1.7s | spectacle-feast hook, food macro b-roll |
| nhWPCLmnDqg | SBSP "vacuum abs" (ADWORDS WIN) | 5:38 | 62 | 5.0s | 3.0s | |
| lfa71t4RAyw | MadMuscles "New Respect" $224.8k/30d | 1:48 | 31 | 2.3s | 2.0s | AI podcast-interview, every shot captioned |
| oxP-KvqWQAg | V Shred $306k Dr. Drew remix | 4:50 | 118 | **1.8s** | 16.4s* | *one long opening take, then firehose |
| iTkCystNwcM | V Shred #1 ALL-TIME, $5.3M lifetime (2020) | 4:27 | 48 | 4.0s | 4.3s | white-studio designed-typography listicle |
| L-nkqqiO0b8 | V Shred "How to get in shape fast for 2026", $2M (the shared VidTao link) | 1:24 | 44 | 1.7s | 1.7s | 9:16, caption-on-every-shot remix |

**Pacing conclusions baked into the skill:** Dan's winners run 4–7 min and settle into a
4–7s median shot length in the body — but several cut the hook at sub-1s pace. Nothing sits
unchanged longer than ~25–30s, and in pitch sections *something* on screen changes every
10–15s even while the take runs long (that's what the side inserts are for).

## The SPS house formats (what Dan's own winners actually are)

1. **Skit/spectacle hook → replay commentary → studio pitch** (TestMax pool, Test Reload
   pool, Eat Like A Pig). The hook is a self-contained scene cut fast (0.7–1.7s median);
   then the presenter narrates OVER a replay of the hook using **player-UI motifs — pause
   icon, rewind ⏪ with dissolve, red circle around the subject**; then a clean flat-color
   studio carries the rest.
2. **Prop-anchored lecture** (10 lbs lard). One physical prop is the visual anchor; macro
   close-ups of the prop replace b-roll variety.
3. **Set-based content listicle** (Green Detox). Numbered-list text cards ("3.) DARK LEAFY
   GREEN"), fact cards, split panels; reads as content, sells the whole time.
4. **Two-presenter whiteboard/authority** (estrogen interview). Uniform ~6.5s pace,
   citation cards (UCSF quote), metaphor graphics (testosterone battery, speedometer),
   labeled BEFORE|AFTER physique comparisons.

## The graphics playbook common to ALL the winners

- **Persistent CTA lower-third for most of the ad.** Green Detox: blue "Go To:
  GetGreenDetox.com" bar from 0:22 to the end. TestMax: "Click Here Or Go To
  TestMaxTips.Com" pill from ~1:31 (right after the first CTA card at 1:25) on literally
  every frame to the end card.
- **Side-panel inserts beside the talking head every ~10–15s** in pitch sections: a b-roll
  clip in a rounded rect, a text card, a graph, a physique photo, a red ✗ over an image.
- **Big text cards: white + red emphasis words, bold, drop shadow** ("YOU'VE BEEN LIED TO",
  "THE ONE THING", "GAINS ABOUT 17–20 lbs"). V Shred 2020 evolves this into designed
  typography (mixed color/weight highlights: "SIMPLE WAY to completely TRANSFORM your
  PHYSIQUE") plus a **persistent numbered-step chip** ("#3 Cut the fluff") pinned
  bottom-left through each listicle section.
- **Metaphor/anchor visuals** for the core mechanism: battery, speedometer, valve cartoon,
  molecule, 3D medical animation, physical prop.
- **Annotation motifs:** red circle, yellow arrows, pointing-hand cursor (animated "click
  below" hand near CTAs), pause/rewind overlays.
- **End card = physique + "CLICK BELOW or go to [URL]"** (teal/flat background, product-ish
  panel, persistent URL bar still visible).
- **Punch-in alternation everywhere:** the same talking-head setup alternates wide ↔ tight
  framings between takes so no cut ever reads as a jump cut.

## Competitor findings

- **V Shred** ($101.4M lifetime, avg ad 2:49): ad names document the process — `AP3749 04
  MIX 2 tips AP3243 + 3 tips AP2919`, `winner structure`, `(timer)`. **They literally
  remix sections of prior winners into new ads** and re-cut winner structure with new
  footage. The 2026 wave: every shot captioned (yellow-marker keyword style), ~1.7s cuts,
  whip/motion-blur + full-frame color-strobe transitions, glitch repeats on the key phrase
  (×3), Dr. Drew authority footage, prop + arrow annotations. Their all-time #1 is the
  OPPOSITE: clean white studio, designed typography, 4:27 listicle — proof both slow-format
  and fast-format work when the structure is right.
- **MadMuscles** (top lifetime creatives $6–17.7M): 0:47–2:16, podcast/interview framing,
  caption-every-shot (the /make-ad caption spec was measured from their ad), burned
  micro-disclaimer on every ad, and — important for us — **every winning creative ships in
  BOTH 9:16 and 16:9** (`9x16`/`16x9` in the filenames).
- VidTao mechanics: Dan is logged in in Chrome; the free tier hides direct YouTube links,
  but **the embed/thumbnail HTML leaks the video id** — regex the page HTML for
  `(?:embed/|vi/)([A-Za-z0-9_-]{11})`. Brand pages are reached by clicking the brand name
  on any ad page (the Brands search box returns nothing for "V Shred"). Judge ads by
  **lifetime spend first, then 30-day spend**; only study direct-response advertisers.

## Still-watchable green-row ads not yet studied (future reference pool)

bhHlB6jAkRg, MFcGCikA2Wo, h5h1wSE1d_0, tq96OGXAJfA, mKxbD17nnsI, 8-7dqSkjwus,
i4aN-typhlo, lU_-uBEWLI0, k6KoLySNgfo, irhcg1OPQdQ, 5i30KDjihrs, mT2u0dP1apU,
pwc59legbkU, yw_ATh6AVTU, vB9NIm0SZRg. Most SPS-era Mike Chang classics and both
Abs-After-40 links Dan named (avS9tt2iYXc, FK-ne_Lok8w) are now private (403) and no
reuploads were findable by search.
