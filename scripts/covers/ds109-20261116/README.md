# DS-109 approved cover and publishing recipes

Current publishing config: scripts/blotato/configs/ds109-hungry-or-bored.json. Exact title: Hormozi: You're Not Hungry, You're Bored. Dan approved R4 and revised B. Four actual schedules exist for Jan14,2027 at6PM America/Chicago. Do not re-run schedule creation unless reconciling a real saved-post failure.

The build/media scripts run on M2 against its existing /Volumes/Extreme/_edit_work/DS-109/ assets, through SSH/resume; they do not reserve editcap slots. Approved movie and original paired files remain immutable. Main proof and private sources are retained under setup/publish/ and setup/r3/. `publishing_media.py` builds one cover-first TikTok derivative using shared tiktok_cover and preserves all original picture/audio packet payloads; uploads use the shared guarded Blotato client and full byte/hash downloads. `verify_schedules.py` reads the four saved targets/captions/times, and `verify_hosted_posts.py` downloads actual saved post URLs and compares full SHA256. They do not claim future public tile verification.

See Docs/DS109_SETUP_RECEIPT_20261116.md for approvals, hashes, backups, four schedule IDs, and future shared release-check responsibilities. Media stays out of git.
