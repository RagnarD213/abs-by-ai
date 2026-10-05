# Ad 13 round 4 setup receipt, 2026-10-05

Session: The Cost Of Getting Abs S/Sh Ad Setup.

Daniel approved and authorized these exact exports in `Handoffs/ad13-round4-approval-20261005.json`. All three movie hashes were verified before upload and again after setup. Every matching delivery stamp is PASS with 39 passing rows. The movies were uploaded without edits, encoding, trimming, padding or remuxing.

## YouTube uploads

| Format | YouTube | Runtime | Exact SHA-256 | Video asset |
|---|---|---|---|---|
| 16x9 | https://youtu.be/NQeyZ2jylVU | 244.877967 s | `e7b5ff4597c10539d25d737806056a2c209b5c02899b54419cff50a242ce1ed3` | `428010559636` |
| 1x1 | https://youtu.be/2-S3WVLhDsI | 244.877967 s | `43fe4f707ac41759fd94c6353289396cce967b1e97d30560df373a6c9c2d45f1` | `428100028746` |
| 1x1-59s | https://youtu.be/W1xLK5W9l_0 | 54.287567 s | `d59a126976bb12ec25e8ff6c12520bcf32dbfd4b6d99c9162859efa736f51c12` | `428100028503` |

All three read back on channel `UC236gjadarHAhEhOMYNGJ9g`: Unlisted, processing succeeded, HD, embeddable true, not made for kids. Synthetic media true was submitted on each upload; this channel token does not expose `containsSyntheticMedia` in videos.list, so it is a submission confirmation rather than an independent setting readback. Upload logs and configs remain in the setup folder. No duplicates existed in the channel inventory before upload.

Descriptions and topic tags were read from the current verified vertical uploads, preserving the /start 7-day trial offer. Both full movies have the same valid chapters, starting at 0:00 and with every chapter at least 10 seconds; the last is 13.878 seconds. The short has no chapters and stays at its approved 54.287567-second duration.

Classification: AD. Full closing words from the round 4 finished word transcript: "Then our powerful AI engine builds the exact plan to get you there. Tap the button below to get started." The short transcript has the same closing words. Transcript sources: `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/round4/h16x9/words_out.json` and `/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/cut/words_ctc.json`.

## Thumbnails

Locked design 13-R3B, "HUMAN TRAINERS HATE THIS AI". Reused the approved horizontal final. Built a matching 1080x1080 square from the original photo-10, original mask and existing repaired robot plate. Original real photo pixels were not redrawn. No new image generation was needed, no paid image API was used. Reproducible builder: `scripts/covers/trial-campaign-20261001/ad13-square/build.py`, also saved beside the finals. New final copied to `social media graphics/youtube/thumbnails/_trial-campaign-20261001/FINAL APPROVED/`.

Square inspected at native 1080x1080 and 320x320 phone size. Complete wording, original hair and face retained; text-person overlap is zero. Every served maxres thumbnail was fetched and opened. YouTube serves the square centered within 1280x720 with black sides; the full square image is intact. Both square served thumbnails are byte-identical.

| Format | Thumbnail path | Final SHA-256 | Served evidence SHA-256 |
|---|---|---|---|
| 16x9 | `/Users/danielrose/Documents/Claude/Projects/Abs By AI/social media graphics/youtube/thumbnails/Ad 13 What Getting Abs Cost/trial-20261001/Ad 13 | 16x9 | FINAL.jpg` | `c7a658be24588ed648a385dd689995c1cef44accf86e37e30978c9fb4ed53222` | `91931b6974752a000f6af5206deb4b85efecd226526e96c182557f6506b047b0` (`readback-NQeyZ2jylVU.jpg`) |
| 1x1 | `/Users/danielrose/Documents/Claude/Projects/Abs By AI/social media graphics/youtube/thumbnails/Ad 13 What Getting Abs Cost/trial-20261001/Ad 13 | 1x1 | FINAL.jpg` | `c9930509d8d25a8c806863ade01d64ee3ad7df5eb2159e6cf905163240c0d940` | `28d14ca363cea3d5400081dbc87bdcd68cf5c21392e6fa2b3f0874ffa8cd4a60` (`readback-2-S3WVLhDsI.jpg`) |
| 1x1-59s | `/Users/danielrose/Documents/Claude/Projects/Abs By AI/social media graphics/youtube/thumbnails/Ad 13 What Getting Abs Cost/trial-20261001/Ad 13 | 1x1 | FINAL.jpg` | `c9930509d8d25a8c806863ade01d64ee3ad7df5eb2159e6cf905163240c0d940` | `28d14ca363cea3d5400081dbc87bdcd68cf5c21392e6fa2b3f0874ffa8cd4a60` (`readback-W1xLK5W9l_0.jpg`) |

## Horizontal replacements

Account-wide ad and asset-binding inventory found five configured ads using `-SuKGXGcbIg` / asset `423865478571` and one PMax binding. The earlier `hrQf1240kQA` historical ads were already REMOVED and remain unchanged.

| Campaign | Group | Old ad | Old status before / after | Replacement ad | Replacement status |
|---|---|---|---|---|---|
| `24243839443` | `197465035822` | `825601774244` | ENABLED / PAUSED | `826990035741` | PAUSED |
| `24243839443` | `200980520340` | `825601774247` | ENABLED / PAUSED | `826990035744` | PAUSED |
| `24305381214` | `201604959278` | `826637064697` | ENABLED / PAUSED | `826990035747` | ENABLED |
| `24305381214` | `206411886211` | `826720144451` | ENABLED / PAUSED | `826990035750` | ENABLED |
| `24316364155` | `204553316830` | `826635661894` | ENABLED / PAUSED | `826990035753` | ENABLED |

The legacy campaign `24243839443` was PAUSED and remains PAUSED, with both replacement ads PAUSED. Trial and conversion remarketing campaigns were already ENABLED and remain ENABLED. Old ads were paused, never deleted. The old horizontal upload remains Unlisted. Each replacement clones its own live source copy, logo, business name, CTA, landing page and tracking convention, with only the version in `utm_content` changed.

PMax campaign `24308574894`, asset group `6754766656`: old binding `6754766656~423865478571~YOUTUBE_VIDEO` read back REMOVED, new binding `6754766656~428010559636~YOUTUBE_VIDEO` ENABLED. Active video count remains five. All other binding records and assets are preserved. The removed binding remains in API history, so historical record count increases by one while active asset count stays unchanged.

Google validateOnly passed before one atomic 17-operation apply: three video assets, seven ads, five old-ad pauses and two PMax binding operations. Readbacks verified every new video reference, copy, URL and status, the five PAUSED old ads and removed PMax binding. Final account scan has zero enabled paid uses of either old Ad 13 horizontal. Unfinished replacement references: none.

## Square additions

| Format | Trial group | Ad | Asset | Final URL |
|---|---|---|---|---|
| 1x1 | `204553316830` | `826990035756` | `428100028746` | https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad13&utm_content=codex-1x1-vsl |
| 1x1-59s | `204553316830` | `826990035759` | `428100028503` | https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad13&utm_content=codex-1x1-59s-vsl |

Both square ads are ENABLED, with exact current trial copy/settings. They were added only to group `204553316830`. Existing vertical videos `f792V7H1Vkc`, `VPyHyxEkHjo` and trial ads `826888334290`, `826888304284` are preserved. YouTube vertical metadata/status and all pre-existing ad records were compared; only the five authorized old-horizontal ad statuses changed. No extra square or vertical formats were added to remarketing. Subscriber engagement untouched.

## Budgets, policy and records

| Campaign | State preserved | Daily budget before / after | Budget ID |
|---|---|---|---|
| Trial `24316364155` | ENABLED | $50 / $50 | `15911255930` |
| Conversion remarketing `24305381214` | ENABLED | $10 / $10 | `15911284202` |
| PMax `24308574894` | ENABLED | $50 / $50 | `15923601274` |
| Legacy Demand Gen `24243839443` | PAUSED | $50 / $50 | `15862488218` |

Live budgets supersede older $30/day trial and $5/day PMax notes. No budget operation was sent. Campaign/group states, bids, audiences, criteria, goals and asset-group settings compared exactly before/after. All 230 pre-existing ads preserved except the five authorized pause statuses.

All seven new ads and the new PMax video binding read back REVIEW_IN_PROGRESS / UNKNOWN. Setup and replacement are verified; Google approval remains pending. Policy recheck date: 2026-10-06. No automation created. Existing vertical trial ads now read APPROVED / REVIEWED.

Durable evidence: `scripts/ads/api/dgen-ads/ad13-round4-20261005.*`. Full before/after resource snapshots and upload logs: the ad folder `setup-round4-20261005/`. Google readback retains removed historical bindings; verification uses their actual status.

AS-10 set FINALIZED from Daniel's approval, then UPLOADED only after YouTube and Google Ads readbacks. Queue synchronization is recorded separately from media receipts. No organic posting, Public upload or scheduling. Paused Victory Dashboard skipped.
