# Handoff: Google Flow Music: interview Dan, then make a channel theme and background music (2026-11-07)

**Owner:** Claude, Opus 5.5 high (creative work).
**Authorization:** Dan, 2026-11-07: "I noticed we have Google Flow Music. I think that's included in here. Let's try to use this for something too. I'm thinking maybe we could generate good background music. Maybe we could make a theme song for the channel. Make me a handoff for the new task: interview me about what I want, and then generate some music while we're on this." Generating on his subscription is authorized. Never pay.
**Deadline:** Dan's Google AI Ultra drops from the $199.99 tier to the $99.99 tier on **Nov 29, 2026**, so do the bulk of the generating before then. Flow Music may have its own limits; read them in the app.

## Where it is

- **Address:** https://www.flowmusic.app in Dan's Chrome, signed in as Dan's account (the profile shows "TwilightWagon, MEMBER").
- **Features:** chat with a "co-producer", a Compose view, presets (Music for video, Songs for fun, Remix a track, Make a plugin), Songs, Playlists, Spaces, Music videos and Projects. The home page says downloads are "free unlimited".
- **Access banner:** on 2026-11-07 the page showed "Grant access to your Google One subscription to use your benefits." That is an account permission grant, so get Dan's clear yes in chat before clicking it, or ask him to click it himself. His request for this task is not that yes.
- **Other Flow work:** two Flow-credit handoffs are running in the same Google account (`handoff-20261107-flow-credits-*.md`). Use your own Chrome tab and never close tabs you didn't open.

## Step 1: interview Dan (before generating anything)

Keep it short, one question at a time where the answer changes the next question. Offer concrete options as buttons where possible. Cover:

1. **Theme song: what and where.** Pick one:
   - a 3 to 5 second sting for the video open and end card;
   - a 10 to 20 second intro;
   - a full song (for the channel trailer, ads, a playlist).
   Ask whether it has vocals, or the "Abs By AI" name sung or spoken.
2. **The feel.** Ask for genre and energy, and for reference artists, channels or songs he likes, for example the music under the fitness channels he watches. Ask what he never wants. Ask whether it should suit a 41-year-old guy getting shredded with AI: confident, funny, serious, gym-hype.
3. **Background beds.** Which videos need them: long-forms (talking head, studio or kitchen), Shorts, ads, the VSL and website video. How many tracks per mood, for example talking-calm, upbeat workout, story or emotional, comedic gag, reveal or payoff. Ask how long each should be: loopable 2 to 3 minute beds, or full tracks.
4. **Whether it should sound "branded".** One recurring motif across the theme and the beds, or separate tracks.
5. **AI-music flag.** Our standing rule (`.claude/skills/_shared/VIDEO-RULES.md`, the synthetic-media flag) marks a YouTube or TikTok upload as AI-altered when it contains AI-generated music. Tell him this in one line and ask whether he still wants AI music in content videos, or only in places like ads, the website and the trailer.

Write his answers into `Docs/FLOW_MUSIC_BRIEF_20261107.md` (his words quoted) before generating.

## Step 2: generate

- **Set up first.** Read what the app offers in the Compose and co-producer views: song length, stems, instrumental, extend or remix, download format. Also read its plan limits and the usage terms for commercial and YouTube use. Note anything that limits using the tracks in monetized videos and ads, in one line in the brief.
- **Make the theme.** 3 to 4 distinct directions, 2 to 3 takes each, picking the best take per direction before Dan hears anything. Then make short cut-downs of the winning takes: a 3 to 5 s sting and a 10 to 15 s intro.
- **Make the beds.** For each mood Dan named, 2 to 3 instrumental tracks with no vocals, at a steady level that sits under speech. Prefer tracks that loop cleanly.
- **Check them offline.** Use offline audio checks only, never play them out loud. This is the silent-checks rule in AGENTS.md. Measure loudness, true peak, clipping, silence, and stereo width. For a bed, check a clean loop point. Use `.claude/skills/_shared/audio/` tools where they fit. Say what actually ran; numbers are not a listening pass.
- **Download** everything to `Media/flow-music/<date>/` on the internal drive (the work drive order) with clear names: `theme-<direction>-take<N>.wav|mp3`, `bed-<mood>-<N>`. Keep a `catalog.json` with the prompt, settings, length, LUFS and mood for each.

## Step 3: Dan reviews

- **Review page.** One page using `.claude/skills/_shared/review_server.py` and the shared review player, phone layout first.
  - **Theme section:** one row per direction, with the take and its cut-downs.
  - **Beds section:** grouped by mood, each bed also played under a 20 s clip of Dan talking from a finished long-form, ducked the way an edit would mix it, so he hears it in context.
  - **Picks:** a pick button on each.
- **Playback.** Open the page with `?review_mode=automation`, check it silently, then call `AbsReviewAudio.handoff()`, so it is left paused with sound ready.
- **In chat:** give him the link, the directions in one line each, and the two wrap-up boxes. Stop for his picks.
- **After his picks:**
  - Make revisions he asks for in the same task.
  - File the approved tracks in `Media/music beds/` with their own README row (source: Google Flow Music, date, prompt).
  - Note the theme in the edit skills' music step: `/longform-edit` Step 7.5 and `/shorts`. Say it is an option, not a replacement for the Pixabay rule, until Dan says otherwise.
  - Commit with `safe-push.sh`.
