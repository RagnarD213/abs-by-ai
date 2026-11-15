# What To Cut Shorts (SL-21): setup complete, shared waitlist

Dan approved all three films and final covers. All publishing assets are uploaded and verified. **HOLD for shared queue capacity: these are planned dates, not live schedules.** Blotato reads 199/200; a Short requires four posts.

| Short | Approved cover | Planned date, 9 a.m. Central | Platforms |
|---|---|---|---|
| Restaurants Don't Care About Your Fitness Goals | Restaurant R4 X2, Why Restaurants Make You Fat | Monday February 8, 2027 | YouTube, Facebook, Instagram @danrosefit, TikTok |
| You Don't Deserve A Vacation Until You're Ripped | Original X7 | Wednesday February 10, 2027 | All four |
| If You Can't Afford A Gym, You Can't Afford Therapy | Final therapy R4 X3, large bubble: Therapy makes you fat and depressed. | Friday February 12, 2027 | All four |

## Approvals and files

Therapy final approval, November 15: “This looks good. Approved. Go ahead and finish the setup for all three Shorts.” The chosen cover has no separate title, black text over three lines, and one continuous bubble/tail. Exact Instagram/YouTube PNGs and the existing YouTube JPEG were installed byte for byte. Restaurant and vacation covers stayed unchanged. `Short-form video content/covers/approved-sl21/picks.json` records all selections and hashes. The source-blind X3 pick was already logged, so it was not counted twice.

Approved films remain byte for byte:

- Short 1: `544f74b7bb182d5a4350a8ffa740b2d6c8529a3259b82fb271b71cb311ea85d5`, 72,626,250 bytes.
- Short 2: `2c05d70ccc2055da840be8fe57b158e649bd90e94f62430dd49906b1997bce81`, 72,253,137 bytes.
- Short 3: `b6bd0e5666ab58497e36bc31acc11f3349f53e7b8ed6b81cb5963818965ec2fa`, 69,715,138 bytes.

No original was re-rendered or re-edited. All inherited review/gate exceptions remain accepted. Shorts 1 and 2 carry the realistic-AI-video flag; Short 3 does not. An AI cover does not change that video flag.

## Backups and media verification

- [Google Drive backup](https://drive.google.com/open?id=1kDgQu3I9RwS4vRJjeYPlsrFaX97fyVBY): 36 files, 442,966,395 bytes. Every file MD5 and byte count matched; Drive permission read back as anyone/reader.
- Project finished package: `Short-form video content/whattocut SL-21/`. All 36 files SHA-256 reread verified.
- Extreme on M2: `/Volumes/Extreme/Short-form video content/whattocut SL-21/`. All 36 files SHA-256 reread verified.
- Twelve Blotato media assets fully downloaded and SHA-256 matched: three exact masters, three TikTok cover-first copies, three Instagram PNGs and three YouTube JPEGs. Cover URLs decode; YouTube covers remain under 2 MB.
- TikTok copies prepend one checked cover frame. Full decoding found no errors; every original picture frame after the cover is identical, and all audio packet payloads are identical. This was silent/offline verification, not an audible listening pass.
- Facebook approved covers and matching first caption lines are installed in both Macs' source registries and live installers; hashes read back.

## Metadata and queue readback

One organic config per Short, with approved video title, descriptions, platform captions, tags, root-site UTMs, ManyChat keyword, AI flag and pinned question:

- `scripts/blotato/configs/sl21-short1-restaurants-dont-care-about-your-fitness-goals.json`
  Pinned comment: “Quick question for you guys. How many times a week do you eat at restaurants?”
- `scripts/blotato/configs/sl21-short2-you-dont-deserve-a-vacation-until-youre-ripped.json`
  Pinned comment: “Do you work out when you're on vacation, or do you take the week off?”
- `scripts/blotato/configs/sl21-short3-if-you-cant-afford-a-gym-you-cant-afford-therapy.json`
  Pinned comment: “How much do you pay for your gym membership every month?”

All twelve planned platform targets passed cover/ad preflight on M6 and M2. `organic_short_queue.py` dry runs refused 203/200 for each Short as expected. Three unique shared-waitlist entries were reread on both Macs, in restaurants/vacation/therapy order, with `kitchen: true`, `after` and `parent_config` pointing to `ro20b-what-to-cut.json`. That parent config still plans Friday December 11, 2026. Dates respect phase 4, existing February 1/3/5 SL-20 reservations, content restrictions and all current slots. The shared top-up dry run preserves the waitlist and reports no room.

No live SL-21 schedule exists yet. No direct YouTube/holding upload or native schedule was created. Before/after ad scan is CLEAN; live cover audit has zero issues at 199 posts. Nothing belonging to another queued video was moved or deleted.

SL-21 stays **finalized**, revision 8, with a truthful setup-complete/waitlist note. The Drive Edit Queue status was uploaded and reread. It will become `uploaded` only after all actual Blotato posts exist and read back. Native artifact fallback sync remains for the next native writer; no mark-synced claim. No dashboard pause/resume control was changed.

## Existing post-release work

The shared top-up routine queues these four-platform packages when capacity frees, after the parent dependency. The parent is not public yet, so no public-release verification or Related Video link is claimed. After release, existing shared checks verify actual public covers, Facebook cover application, pinned comments and the Shorts article/skip. Add YouTube's Related Video link to the public RO-20B then. Prepared YouTube tags require the released id for native application/readback. No new per-video automation was created.

Evidence: `/Users/danrrose/Projects/_edit_work/sl21-covers/setup/` and the backed-up setup package. Paid API spend in this completion phase: $0. Dan has no remaining setup choice or action.
