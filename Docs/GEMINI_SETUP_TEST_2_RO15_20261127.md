# Gemini Setup Test 2 (Practice Run): Sleep Better With Glycine (RO-15)

**Date:** 2026-11-27  
**Type:** CONTENT · long-form (LFC) · RO-15 · Gemini audition 2 of 2 (practice run, nothing live changed)  
**Runner:** Antigravity CLI (`agy`) on M6, model `gemini-4-neon-high` (+ one internal `agy --model claude-opus-5-5-high` sub-call for blind copy comparison)  
**Blind review page:** `http://127.0.0.1:9640/` (served by durable shared `review_server.py` hub; verified HTTP 200)  
**Work folder:** `/Volumes/Extreme/_edit_work/GEMINI-SETUP-TEST-2/`  
**Locked blind manifest:** `/Volumes/Extreme/_edit_work/GEMINI-SETUP-TEST-2/PACKAGE-MANIFEST.json` (`SHA-256: 33980e00fc7662b950e67f34caaf672ae05605056b5fdd3744f8402e2389d563`, 122 files hashed)

> **Read after picking on `http://127.0.0.1:9640/`.** The review page keeps all five thumbnails labeled neutrally (`Option 1` to `Option 5`) and both copy sets labeled neutrally (`Set A` and `Set B`) with zero author hints or reference comparisons. The key and side-by-side comparison against the approved RO-15 package are below.

---

## 1. Blind Rule & Zero-Leak Attestation

- **Blind rule kept:** Until `/Volumes/Extreme/_edit_work/GEMINI-SETUP-TEST-2/PACKAGE-MANIFEST.json` was completely written, hashed, and verified on disk (`2026-11-27T10:01:13-05:00`), this session did **not** open, list, search, or read any of the forbidden RO-15 / glycine files: `scripts/blotato/configs/ro15-glycine.json`, `Docs/RO15_SETUP_RECEIPT_20261106.md`, `Docs/RO15_SETUP_RECHECK_20261114.md`, `social media graphics/youtube/thumbnails/Sleep Better With Glycine/`, `Sleep Better With Glycine - thumbnail FINAL.jpg`, `chapters.txt`, `sixpackabs/articles/TBD-ro15-glycine.md`, `BLOTATO_QUEUE_PROGRESS.md`, `AI_COORDINATION.md`, `Docs/LONGFORM_RELEASE_CALENDAR.md`, or `scripts/blotato/video_waitlist.json`. The master folder was never listed (`ls` was never run on it); only the two exact handoff-verified paths (`FINAL - Sleep Better With Glycine.mp4` and `.srt`) were read in place.
- **Verified inputs (read-only, untouched):**
  - Master MP4: `1,784,296,329` bytes, `323.990333 s` (`5:23.99`), `1920x1080`, `30000/1001 fps`, H.264 + AAC, SHA-256 `46dfc4240eeb08cb5a1e4c3e0d20680d1d0d03813fb1402a599d3e7aa13e290e` (exact match).
  - Captions SRT: `9,423` bytes, SHA-256 `99969ede25f8488f9e64708ee52a0fe6320de155a41b253f65ee72f6d67dc19c` (exact match).
- **Zero leak & stop lines kept:**
  - Zero Codex, zero Claude Code, zero `codex-image.sh`, zero `blind.py`, zero paid API (`GEMINI_API_KEY`, `GOOGLE_API_KEY`, and `ALLOW_API_IMAGE` all confirmed unset).
  - Nothing live changed: zero Blotato calls, zero config in `scripts/blotato/configs/`, zero calendar/waitlist/site/YouTube edits, zero edits to `AI_COORDINATION.md`, `BLOTATO_QUEUE_PROGRESS.md`, `.claude/skills/video-setup/SKILL.md`, `Docs/PINNED_COMMENTS.md`, `Handoffs/README.md`, or any Joint Vigor file.
  - Draft config carries `"release_hold"` and HTTPS placeholder URLs so `ad_guard.py` and `longform_queue.py` would refuse even an accidental run.

---

## 2. Blind Key (`BLIND-COPY-KEY.json`)

| Review Page Label | Author / Source |
|---|---|
| **Set A** | `claude-opus-5-5-high` (internal `agy` sub-call) |
| **Set B** | `gemini-4-neon-high` (primary runner) |
| **Option 1** | AI Dan #1: mixing white glycine powder into chilled water at night (dark left scrim, cyan bar, Impact white + cyan) |
| **Option 2** | AI Dan #2: peaceful deep restorative sleep in cool dark bedroom (midnight header fade, blue rule, white + gold Impact) |
| **Option 3** | Real photo Dan (`studio-white-49_CUTOUT.png`, untouched original pixels + white keyline) over AI nightstand scene (red bar, Arial Black) |
| **Option 4** | History-guided #1: AI Dan refreshed in bright morning bedroom + frosted glass card (`Top 1 Percent` style, Avenir Next Heavy) |
| **Option 5** | History-guided #2: AI Dan holding chilled glycine glass beside glowing `63°` thermostat + black/yellow top bar |

---

## 3. Side-by-Side Comparison: Practice Package vs Approved RO-15 Package

### A. Core Metadata, Description, Article & Config Fields

| Field / Area | Approved RO-15 Package (Nov 6 / Nov 14) | Gemini (Set B) | Opus Sub-Call (Set A) |
|---|---|---|---|
| **Recommended Title** | `Glycine Helped Me Sleep Better Than Any Other Supplement` (56 chars) | `Sleep Better With Glycine (3 Grams Before Bed)` (46 chars) *(Alt 2: `This Cheap Amino Acid Helped Me Sleep Better (Glycine)`; Alt 3: `Glycine For Sleep: My Oura Ring Results Taking 3g Every Night`)* | `Sleep Better With Glycine If You Sleep Hot` (42 chars) *(Alt 2: `This Amino Acid Helped Me Sleep Better Than Any Supplement`; Alt 3: `Glycine for Sleep: My Oura Ring Results After Taking It Every Night`)* |
| **Description Length & Structure** | 1,197 chars (~196 words): 3 tight hook/body paragraphs, AbsByAI UTM link, 9 bare chapters (no `Chapters:` heading), study DOI link (`10.1111/j.1479-8425.2007.00262.x`), AI clip note + subscribe line, 4 hashtags. No medical disclaimer, no SixPackAbs.com mention. | 1,924 chars (~329 words): 4 paragraphs covering mechanism, Japanese studies, Oura numbers & dose, AbsByAI UTM link, `Chapters:` heading + 9 timed chapters, engagement prompt, AI disclosure, general fitness disclaimer, subscribe + SixPackAbs.com line, 5 hashtags. | 1,546 chars (~261 words): 3 paragraphs (hook, overview, hot-sleeper callout), AbsByAI UTM link, `Chapters` heading + 10 timed chapters (9 matching + 5:05 CTA), engagement prompt, AI disclosure, general fitness disclaimer, subscribe + SixPackAbs.com line, 5 hashtags. |
| **UTM Link** | `https://absbyai.com/?utm_source=youtube&utm_medium=video&utm_campaign=longform&utm_content=ro15-glycine` | Exact match (`ro15-glycine`, organic root `/`) | Exact match (`ro15-glycine`, organic root `/`) |
| **YouTube Tags** | 15 tags (`glycine`, `glycine for sleep`, `glycine sleep`, `glycine supplement`, `best sleep supplement`, `sleep supplements`, `how to sleep better`, `sleep hot at night`, `waking up hot at night`, `night sweats sleep`, `core body temperature sleep`, `Oura Ring`, `Oura sleep score`, `amino acid for sleep`, `Dan Rose Fitness`) | 13 tags (strong overlap on core glycine/sleep/Oura/hot-sleeper terms; missed `night sweats sleep`, `core body temperature sleep`, and exact `Dan Rose Fitness` vs `Dan Rose`) | 15 tags (strong overlap including `glycine`, `glycine for sleep`, `best sleep supplement`, `how to sleep better`, `hot sleeper`, `sleep temperature`, `oura ring`, `glycine powder`) |
| **Hashtags** | `#Glycine #SleepBetter #SleepSupplements #SixPackAbs` (4) | `#Glycine #SleepTips #DeepSleep #SleepSupplements #AbsByAI` (5) | `#glycine #sleepbetter #sleepsupplements #supplements #absbyai` (5) |
| **Engagement Prompt** | Config has `"engagement_prompt": "Follow for more on what I've tried to improve my sleep."` (55 chars), while `pinned_comment` says `"Subscribe for more..."`, `close` asks bedroom temp, and Nov 6/14 receipts list `"How many nights a week do you wake up too hot or sweating?"`. Still has legacy `"keyword": "SLEEP"`. | `"Do you wake up hot at night, and have you ever tried glycine for sleep?"` (71 chars; passes `organic_engagement.treatment()` across all 4 platforms; zero legacy ManyChat keyword) | `"Do you wake up at night because you're too hot, or do you usually sleep cold?"` (77 chars; passes `organic_engagement.treatment()`) |
| **Site Article (`build.py --check`)** | `sixpackabs/articles/TBD-ro15-glycine.md`: **1,124 words**, excerpt **147 chars**, `OK`. Voice score **12.2** (line 17.4). Links to 2 sleep/supplement videos + Japanese study DOI. | `copy/gemini-article-TBD-ro15-glycine.md`: **1,069 words**, excerpt **149 chars**, `OK`. Voice score **12.6** (line 17.4). 0 hard fails, 0 em/en dashes. | `copy/opus-article-TBD-ro15-glycine.md`: **1,159 words**, excerpt **137 chars**, `OK`. Voice score **12.1** (line 17.4). 0 hard fails, 0 em/en dashes. |
| **Em/En Dashes & AI Stock Phrases** | 0 hard fails (`voice_check.py --hard` OK) | 0 hard fails (`voice_check.py --hard` OK across packaging, article, and draft config) | 0 hard fails (`voice_check.py --hard` OK across packaging and article) |
| **Schedule & Config Fields** | `content_type: "organic"`, `slug: "ro15-glycine"`, `main: "2026-12-23T15:00:00.000Z"` (Wed Dec 23 9 AM CT; socials Thu Dec 24 noon CT), `ai_generated: true`, `kitchen: false`, `facebook_media_type: "reel"`, real Blotato URLs, `thumbnail_approval`, `release_approval`. | All required `longform_queue.py` fields present with exact matching types (`content_type: "organic"`, `slug: "ro15-glycine"`, `main: "2026-12-23T15:00:00.000Z"`, `ai_generated: true`, `kitchen: false`, `gym: false`, `facebook_media_type: "reel"`, `engagement_prompt`, `platform_ctas`). HTTPS placeholder URLs + `"release_hold"` safety guard. Passes `ad_guard` (excluding intentional `release_hold`) and generates all 4 platform posts cleanly via `longform_queue.posts()`. | N/A (copy + article only per handoff) |

### B. Chapter Timestamps Against Real `chapters.txt`

| # | Real `chapters.txt` | Gemini (Set B) | Gemini Delta | Opus Sub-Call (Set A) | Opus Delta |
|---|---|---|---|---|---|
| 1 | `0:00` Why Glycine Helped Me Sleep | `0:00` The amino acid that helped me sleep | **0 s** | `0:00` The supplement that helped me sleep most | **0 s** |
| 2 | `0:24` What Glycine Is | `0:26` What is glycine? | **+2 s** | `0:26` What is glycine? | **+2 s** |
| 3 | `0:49` How It Helps You Sleep | `0:50` How glycine helps you sleep | **+1 s** | `0:49` How glycine helps you sleep | **0 s** |
| 4 | `1:16` The Research | `1:17` What the Japanese studies show | **+1 s** | `1:16` The research (and why I'm not 100% sure) | **0 s** |
| 5 | `1:49` Who It's Good For | `1:49` Who glycine is good for | **0 s** | `1:49` Who glycine is good for | **0 s** |
| 6 | `2:34` What Happened When I Took It | `2:34` What happened on my Oura Ring | **0 s** | `2:33` What happened when I took it | **-1 s** |
| 7 | `3:44` The Bigger Point | `3:44` Supplements are only 5% of your results | **0 s** | `3:44` Glycine is not a cure-all | **0 s** |
| 8 | `4:22` How To Take It | `4:23` How to take glycine (dose and form) | **+1 s** | `4:22` How to take glycine for sleep | **0 s** |
| 9 | `4:52` Wrap-Up | `4:53` Bottom line and the AI Supplement Audit | **+1 s** | `4:52` Is glycine worth trying? *(+ `5:05` The AI Supplement Audit)* | **0 s** |

- **Scorecard check (chapters within 2 seconds):** **PASS for both sets.** Every single one of the 9 chapters landed within `<= 2 s` of real `chapters.txt` (Gemini max delta `2 s`, mean `0.67 s`; Opus max delta `2 s`, mean `0.33 s`). Note that at chapter 2, cue 8 (`So,`) begins at `0:24.926` and cue 9 (`first of all, what is glycine?`) begins at `0:26.046`, explaining the exact `+2 s` offset on both blind sets.

### C. Thumbnail Comparison Against Dan's Approved Round-2 Final

- **Approved RO-15 Final (`Sleep Better With Glycine - thumbnail FINAL.jpg`, 1280×720, 335 KB, SHA-256 `655ccdee...`):**
  - AI shirtless Dan on the **right**, tight chest-up leaning next to a large glass of water while pouring a scoop of white powder into it, against a clean dark charcoal-navy background.
  - Left side 3-line Title Case Impact stack: `Sleep` (white) / `Better` (white) / `With Glycine` (dark text inside a bright mint-cyan highlight box).
- **Our Blind Five (`1280x720`, `125 KB` to `168 KB`, all well under 2 MB, zero text overlaps, Title Case set in code):**
  - **Option 1 (`thumb-1.jpg`, 126 KB):** Independently converged on the **exact same concept, headline, three-line break (`Sleep` / `Better` / `With Glycine`), left/right composition, pouring-powder-into-glass action, and dark-navy + white + cyan palette** as Dan's Round-2 approved final, completely blind. Difference: our Option 1 frames Dan wider (waist-up showing full six-pack abs and Oura-style ring in a moonlit bedroom), whereas Dan's approved final crops closer on his face and the swirling glass with a mint highlight box behind `With Glycine`.
  - **Option 2 (`thumb-2.jpg`, 138 KB):** Peaceful deep restorative sleep in a cool dark bedroom (showing good sleep per `ai-clip-gags-injury-and-sense`) with midnight top gradient, blue rule, and white/gold Impact headline.
  - **Option 3 (`thumb-3.jpg`, 168 KB):** Real untouched cutout of Dan (`studio-white-49_CUTOUT.png`, original person pixels preserved with crisp white keyline) composited over an AI-generated dark nightstand scene (iced water glass, powder bowl, spoon, smart ring) with red accent bar and Arial Black headline.
  - **Option 4 (`thumb-4.jpg`, 135 KB):** Refreshed morning Dan sitting on a crisp luxury bed on the left + `Top 1 Percent`-inspired frosted cool-slate glass card on the right with dark navy Avenir Next Heavy typography.
  - **Option 5 (`thumb-5.jpg`, 137 KB):** Dan holding a chilled glycine water glass next to a glowing `63°` Nest-style thermostat under a black top banner with bold golden-yellow Impact text (modeled on Dan's most-picked yellow-on-black header style).

---

## 4. Honest Gaps: What Real RO-15 Had That Ours Missed (and Vice Versa)

### What the real approved RO-15 package had that ours missed
1. **Verified study DOI citation:** The real description and real article link directly to Yamadera et al. (`https://doi.org/10.1111/j.1479-8425.2007.00262.x`, 11 participants with sleep complaints). Neither Gemini nor the Opus sub-call looked up or linked the paper because we stayed strictly inside the captions text.
2. **Oura Ring physiological nuance in the article:** The real article clarifies that the Oura Ring measures *finger skin temperature trend* rather than direct core body temperature, preventing an overstatement. Both blind drafts followed Dan's spoken wording ("tracks my body temperature") without adding that clarification.
3. **Tighter above-the-fold YouTube description:** The real description (1,197 chars) is punchier and faster to scan than Gemini's (1,924 chars) or Opus's (1,546 chars).
4. **Tighter topical internal article links:** The real article linked to `/videos/8-hours-in-bed-is-not-8-hours-of-sleep/` and `/videos/your-supplements-are-only-3-of-your-results/`. Because our blind directory scan filtered out any filename containing `sleep` and skipped shorter articles, our drafts linked to broader published Abs By AI long-forms instead.
5. **Larger face/glass scale on the pouring thumbnail:** Dan's approved Round-2 A thumbnail pushes closer on his smiling face and the oversized water glass with swirling powder, giving slightly stronger visual pop at tiny phone thumbnail sizes compared to Option 1's wider waist-up framing.

### What our practice package had that the real RO-15 package lacked
1. **Clean Nov 17 `engagement_prompt` alignment:** The real RO-15 config still carries legacy `"keyword": "SLEEP"` and three different engagement prompts across `close`, `pinned_comment`, `engagement_prompt`, and the Nov 6/14 receipts. Our draft config has one clean, consistent `engagement_prompt` validated by `organic_engagement.treatment()` across all four platforms and zero legacy ManyChat fields.
2. **Explicit medical/fitness disclaimer and `SixPackAbs.com` pointer in the YouTube description:** Present in both Set A and Set B descriptions; absent from the real RO-15 description.
3. **One-pass thumbnail speed and blind convergence:** Built all five genuinely distinct 1280×720 designs in one unattended pass (~1 minute parallel image generation, 0 refusals, 0 paid API, 0 Codex tokens), including an option that matched the approved Round-2 concept on the first try.
4. **Structured `Chapters:` heading** in the YouTube description (real description listed timestamps with no header).

---

## 5. Audition Telemetry & Scorecard Numbers

### Timing & Automation
- **Start time:** `2026-11-27T09:48:06-05:00`
- **Blind package locked (`PACKAGE-MANIFEST.json`):** `2026-11-27T10:01:13-05:00` (**13 min 7 sec** for the entire blind setup package + durable review page)
- **Opus sub-call wall-clock time:** `2026-11-27T09:57:21-05:00` to `2026-11-27T09:58:42-05:00` (**81 seconds**, exit code `0`, 9,889 bytes output)
- **Dan interventions needed:** **0** (fully unattended end-to-end)

### Image Generation
- **Tool:** Antigravity built-in `image-generator` subagent only (zero `codex-image.sh`, zero Codex, zero Flow credits, zero paid API)
- **Final raw images used:** 5 (4 AI Dan using `identity-reference.jpg`, 1 background-only for real cutout `studio-white-49_CUTOUT.png`)
- **Total internal generation attempts across the 5 subagents:** 9 (`thumb1` 2 tries, `thumb2` 2 tries, `thumb3` 1 try, `thumb4` 1 try, `thumb5` 3 tries)
- **Safety / policy refusals:** **0** (all shirtless lean physique generations succeeded cleanly)

### `/usage` Readings (Antigravity Subscription Allowance)

| Checkpoint | Timestamp (EST) | Gemini Weekly Rem. | Gemini 5-Hour Rem. | Claude & GPT Weekly Rem. | Claude & GPT 5-Hour Rem. |
|---|---|---:|---:|---:|---:|
| **Start of test** | `09:48:25` | `99%` | `99%` | `100%` | `100%` |
| **Before Opus sub-call** *(after thumbnails + Gemini copy)* | `09:57:21` | `99%` *(98% at 09:56:11)* | `97%` | `99%`* | `98%`* |
| **After Opus sub-call** *(alone)* | `09:58:42` | `98%` | `97%` | `98%` | `96%` |
| **Final (end of run)** | `10:02:01` | `98%` | `96%` | `98%` | `96%` |

*\*Note on the Claude & GPT pre-call shift:* At `09:48:25` and `09:56:14`, Claude & GPT read `100% / 100%` (reset `1970-01-01`). At `09:57:21` (immediately before the Opus sub-call ran) it read `99% / 98%` (reset `2026-12-04T14:56:44Z`, likely from a concurrent run or initial probe at `09:56:44`). The isolated Opus 5.5 high sub-call (`44,975`-char prompt producing full packaging + 1,159-word article) consumed **1% of the weekly** and **2% of the 5-hour** Claude & GPT allowance inside Gemini. The entire Gemini portion (planning, 5 thumbnails via 9 image generations, Gemini copy + article + config, review page, manifest, comparison report) consumed **~1% weekly** and **3% 5-hour** of the Gemini Models allowance.

### Self-Check Against Scorecard

| # | Area | Status | Evidence |
|---|---|---|---|
| 1 | Copy and voice | **Ready for Dan's blind pick** | Both Set A and Set B pass `voice_check.py --hard` (0 em/en dashes, 0 stock phrases), score inside Dan's band (`12.1` and `12.6` vs line `17.4`), and hit all 9 chapters within `<= 2 s` of real `chapters.txt`. |
| 2 | Thumbnails | **Ready for Dan's blind pick** | 5 clearly distinct 1280×720 JPEGs (`125–168 KB`, all `< 2 MB`), Title Case set in code, 0 refusals, 1 untouched real cutout, 4 face-checked AI Dan scenes; Option 1 independently matched Dan's approved Round-2 concept. |
| 3 | Technical accuracy | **PASS** | `ro15-glycine.DRAFT.json` passes every `longform_queue.py`, `organic_engagement.py`, and `ad_guard.py` (excluding intentional `release_hold`) check; both articles pass `sixpackabs/articles/build.py --check`; misses documented candidly above. |
| 4 | Zero leak | **PASS** | Zero Codex, zero Claude Code, zero `codex-image.sh`, zero paid API (`GEMINI_API_KEY`, `GOOGLE_API_KEY`, `ALLOW_API_IMAGE` unset); all four `/usage` checkpoints recorded. |
| 5 | Ran on its own | **PASS** | Blind rule kept until `PACKAGE-MANIFEST.json` was locked; 1 session; 0 interventions; 0 stop lines crossed; durable review server live at `http://127.0.0.1:9640/` (HTTP 200). |
