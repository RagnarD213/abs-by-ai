# M6 setup receipt (handoff 02)

Executed: November 13, 2026, about 6:40 to 8:30 p.m. America/Chicago.
Owner: Claude (Opus 5.5) on the M6, Dan at the keyboard for passwords and sign-ins.
Source: `Handoffs/two-mac-setup-20261112/02-m6-setup.md`.
Machine: Mac mini M6, macOS 27.2.1, Thunderbolt Bridge `10.66.0.1`. Old Mac: M2 at `10.66.0.2`.

**Status: handoff 02 is done except three known gaps:** (1) the M2's Extreme and Expansion drives cannot be mounted or read from the M6; (2) the scheduled-task switch waits for Dan to stop using Claude on the M2; (3) Dan's past Claude sessions appear in the sidebar only after Claude is restarted. Nothing on the M2 was deleted, moved or changed except what the handoff ordered: its own SSH key, `~/.ssh/config`, and the M6 key in `authorized_keys`.

## Correction to the handoff: the account name differs

The handoff assumed the M6 account is `danielrose`. It is **`danrrose`** (home `/Users/danrrose`). Dan chose a path alias: `/Users/danielrose` is a symlink to `/Users/danrrose`, so every copied path, LaunchAgent, scheduled task `cwd` and script works unchanged. Over SSH the M6 user is `danrrose` (set in `~/.ssh/config` on both Macs). `~/Documents/Claude` links to `~/Projects/Claude` as on the M2.

## Link and SSH

| Item | Result |
|---|---|
| Cable | First check: no device on any M6 Thunderbolt port. After Dan reseated it: `en2` active, M2 (Mac14,12) seen, ping 0% loss, ~0.3 ms |
| M6 settings | Bridge `10.66.0.1/24`, names `M6` / `m6` / `m6`, `pmset sleep 0 autorestart 1` (Dan ran the one sudo line) |
| SSH | `ssh m2 hostname` → `m2` and `ssh m2 ssh m6 hostname` → `m6`, both with no password (BatchMode). M2 got its own ed25519 key; same `~/.ssh/config` on both Macs |
| Remote Login on M6 | On (Dan, System Settings) |
| Note | The Claude app's built-in terminal panel is blocked from the cable network by macOS local-network privacy ("No route to host"); the Terminal app and Claude's own shell are not. Use Terminal.app for interactive commands that need the M2 |

## Room

852 GB free before the copy, about 520 GB after. No transcripts were skipped.

## What copied, and how it was verified

Copied with `rsync -a` from `m2:` to the same paths (the macOS 27 `openrsync` mishandles `-E`, so apps went with `ditto`, which keeps signatures and extended attributes). Verified with a checksum dry run (`rsync -ac --dry-run`), plus `shasum` on `~/bin`, `codesign` on every app and a launch of every app.

| Item | Size | Checksum verify |
|---|---|---|
| `~/.claude` (live M6 session folders excluded) | 57 GB | Differences only from the M2 still running sessions (101 transcript files) and the M6 Claude app refreshing its plugin marketplace list (1,062 files) |
| Private state: `.absbyai*` (all 13), `.srm-secrets.env`, `.env.local`, `.railway`, `.appstoreconnect`, `.config`, `.gemini`, `.grokbot`, `.hyperframes`, `.twc`, `.vercel`, `.android`, `.cursor`, `.npmrc`, `.gitignore`, `.zsh_history` | small | Differences only from tools run on the M6 during the checks (rclone token refresh, railway, hyperframes, Grok Bot and Android Studio first launches) and the M2 adding to the Veo ledger |
| `~/.zshrc` | | Copied, then one block appended on the M6 (node, npm globals, `~/bin` on the PATH). The top-up script no longer re-copies it |
| `~/.claude.json` | | Merged, not overwritten: the M6 sign-in kept, all 72 M2 project entries added under both `/Users/danielrose/...` and `/Users/danrrose/...` keys. M6 original kept in `~/M2-transfer/m6-original/` |
| `~/.claude/projects` memory | 338 memory files | `-Users-danrrose-*` links to every `-Users-danielrose-*` folder (74), so memory loads whichever path a session opens |
| `~/bin`, `~/.local`, `~/.npm-global`, `~/.venvs`, `~/Library/Python` (pip user packages for `/usr/bin/python3` 3.9.6, incl. imageio-ffmpeg, yt_dlp, torch) | 3.2 GB | 0 differences |
| `~/Projects/_research` | 3.2 GB | 0 differences |
| `~/Projects/Claude` | 102 GB | The first pass missed commit 4e42754, made on the M2 mid-copy; a top-up pass fixed it. Final differences: 4 files the M2 changed afterwards (git index, `Media/flow-credit-log.md`, review snapshot) |
| `~/Projects/Codex` | 12 GB | 0 differences |
| `~/.codex` | 74 GB | Differences only in live files: 285 session files and logs written by Codex still running on the M2, and 324 plugin files plus state databases refreshed when ChatGPT was first opened on the M6 |
| `~/Library/Application Support/AbsByAI`, `AbsByAI Review Hub`, `AbsByAI Reviews` | 28 GB | Checksum verified |
| Claude desktop app data | 18 GB | Full copy kept in `~/M2-transfer/staging/Claude-AppSupport/` (not live); its checksum check shows only caches and session files the running Claude app on the M2 keeps changing. Merged into the live app: 2,479 Claude Code session records and all Cowork sessions (`--ignore-existing`, no M6 file overwritten). `scheduled-tasks.json` deliberately not merged |

Not copied, as ordered: `~/Projects/_edit_work` (stays on the M2), `/tmp/absbyai-*`. Logs and scripts: `~/M2-transfer/` on the M6 (`copy-home.sh` re-runs the copy; `copy-home.sh verify` repeats the checksum check).

**The M2 is still being used.** Claude sessions there committed as late as 7:00 p.m. and keep writing. Run `~/M2-transfer/copy-home.sh` once more after Dan stops using Claude on the M2, then `copy-home.sh verify`.

## Command line tools

| Tool | Result |
|---|---|
| Apple command line tools | Installed (Dan clicked Install): git 2.54.0, `/usr/bin/python3` 3.9.6 |
| node / npm | v24.16.0 / 11.13.0, the M2's own official build copied to `~/.local/node` (no admin install). Nothing in the project calls `/usr/local/bin/node` |
| Homebrew | Not installed. The M2's Homebrew holds only smartmontools |
| ffmpeg | The skills call the project's own `Media/video_edit/bin/ffmpeg` (render queue shim over `ffmpeg.real`). Works on the M6: `ffmpeg version 6.0`, `ffprobe version 6.0`. Not on the PATH, same as on the M2 |
| claude | 2.1.318 |
| railway | Logged in (copied login works) |
| rclone | v1.75.1; remotes `gdrive:` and `gdrive_backup:` copied and working. rclone warns that its shared Google Drive client ID is being retired during 2026 |
| yt-dlp | 2026.10.26 |
| shopify / hyperframes | 5.0.1 / 0.7.7 |
| `~/.venvs/voice-pilot` | Python 3.12.15 runs (its uv Python came with `~/.local`); no rebuild needed |
| gh | v2.104.0, official release, checksum and GitHub signature verified, in `~/.local/bin`. Signed in as RagnarD213; `gh auth setup-git` makes git push work |
| Rosetta 2 | Installed (Dan), needed by the Intel-only apps below |

## Apps

**Copied from the M2 and launched once (all open):** ChatGPT (holds Codex and the Codex CLI), Gemini, Grok Bot, Comet, Manus Studio, Cursor, Wispr Flow, Descript, Slack, zoom.us, Telegram, Shottr, Cinch, VLC, The Unarchiver, Google Ads Editor, Android Studio, iMazing, Brave, Firefox, Microsoft Edge, Opera, Grammarly Editor, GIMP, AnyDesk, Onigiri, CopyMyData, PhoneRescue, Steam, PokerStars, Thunderbird, Skype, Teams classic; in `~/Applications`: Civilization VI (Steam shortcut), Trader Workstation. Already on the M6: Claude, Google Chrome, Safari, Keynote/Numbers/Pages (Creator Studio versions), GarageBand, iMovie.

- Intel-only (run through Rosetta): Cinch, GIMP, Grammarly Editor, Opera, PhoneRescue, PokerStars.
- Strict `codesign` fails on Google Ads Editor, Brave, CopyMyData, PhoneRescue and PokerStars **exactly as on the M2**; all five launch.
- Dock: ChatGPT, Grok Bot, Gemini and Shottr added next to Claude (Dan's request).

**Need a fresh install from the vendor (not done; each needs Dan's password or login):**

| App | Where | Needs |
|---|---|---|
| Adobe Creative Cloud, Acrobat DC | adobe.com (Creative Cloud installer) | Adobe login, Mac password |
| Adobe Acrobat Reader | get.adobe.com/reader | Mac password |
| NordVPN | App Store | Apple ID, then Nord login; approve its network extension |
| Xcode | App Store | Apple ID. Optional now: the M6 LaunchAgents use `/usr/bin/python3` instead of Xcode's Python |
| HP Smart | App Store | Apple ID |
| Brother and Epson printer software | brother-usa.com, epson.com support pages | Mac password |

## Shared drives (step 8): not working

- SMB itself works from the M6: Dan's password is saved in the keychain and the M2's home share mounts and reads.
- `Extreme` and `Expansion` are listed by the M2 but every mount fails with `No such file or directory`. Both are exFAT, handled on the M2's macOS by the FSKit user-space driver; the M2 cannot serve them over SMB. Same failure as the M2 prep receipt (`STATUS_INTERNAL_ERROR` there).
- Fallback over SSH is also blocked: `ls /Volumes/Extreme` over `ssh m2` returns `Operation not permitted` (macOS privacy protection for removable volumes). The fix is one switch **on the M2**: System Settings > General > Sharing > Remote Login (i) > *Allow full disk access for remote users*. Not changed, because the handoff forbids changing the M2; decide it in handoff 03.
- No Login Items added (nothing mounts). Nothing was written to either drive. The drives stay plugged into the M2.

## Project checks (`~/Projects/Claude/Projects/Abs By AI`)

| Check | Result |
|---|---|
| `git status` vs the M2 | Identical: HEAD 4e42754 on `main`, the same 1,202 uncommitted lines (sorted diff empty) |
| `scripts/git/drift-check.sh` | `Git drift OK: ahead 0 / behind 0` |
| `renderq/selftest.py` | 61 of 61 pass |
| `renderq.py status` / `editcap.py status` | Both run: 0 of 5 edit slots in use |
| Hooks | The Stop hook `~/.claude/hooks/wrapup-check.py` fires on the M6 (it enforced the wrap-up boxes during this session) |
| Memory | 338 files present, reachable under both path spellings |
| Plugins and mods | hyperframes, frontend-design and nateherk-design skills loaded in this session as soon as `~/.claude` arrived; `task-wrapup@dan-mods` is enabled in `settings.json`; confirm the mod after Claude restarts |
| Push | `gh` sign-in works; this receipt was pushed with `scripts/git/safe-push.sh` |

## LaunchAgents (step 10)

Installed in `~/Library/LaunchAgents` on the M6 with two path changes: Xcode's `python3` → `/usr/bin/python3` (no Xcode on the M6) and `~/Documents/Claude/...` → `~/Projects/Claude/...` (launchd cannot read `~/Documents`). M2 originals kept in `~/M2-transfer/launchagents-m2-originals/`.

| Agent | M6 state | Check |
|---|---|---|
| `com.absbyai.review-hub` | **Running** | port 8797 answers 200 |
| `com.absbyai.edit-queue-review` | **Running** | review page `127.0.0.1:8830` answers 200 |
| `com.danrose.claude-cleanup` | **Loaded** (every 30 min) | dry run: kept 3, closed 0 |
| `com.absbyai.edit-queue` (dispatcher) | Installed, **disabled** (`Disabled` key + `launchctl disable`) | Launches render jobs; running on both Macs would start jobs twice. Decide in handoff 03 |
| `com.absbyai.fb-reel-covers` | Installed, **disabled** | Posts covers to Facebook every 20 min; the M2 still runs it. Enable on the M6 at the switch |
| `com.absbyai.nightly-footage` | Not installed | Stays on the M2. It is **not loaded on the M2 either** (`launchctl list` shows nothing); check that in handoff 03 |

The stale review agents (`com.absbyai.review.*`, `ro0*`, `wv01`, `row16`, `roll-sidecar`, `test-extreme-access`, `hyperframes-codex-review`) were not installed.

## Scheduled-task switch list (do only when Dan says he has stopped opening Claude on the M2)

Today **all 40 registered tasks on the M2 are already off** (`enabled: false`, file last changed Nov 11 1:06 p.m.), and the M6 has none registered, so nothing fires twice. All 45 task folders are on the M6 in `~/.claude/scheduled-tasks/`, plus the 3 older ones in `~/Projects/Claude/Scheduled/`.

**Enable on the M6** (the recurring tasks that were running until Nov 11):

| Task | Schedule |
|---|---|
| social-queue-daily-refresh | 6:20 daily |
| fb-ig-follow-matches-daily | 6:45 daily |
| upwork-proposals-daily | 7:00 daily |
| fb-tiktok-follow-matches-daily | 7:30 daily |
| youtube-pinned-comment-daily | 9:40 daily |
| sixpackabs-article-gap-daily | 10:30 daily |
| house-sale-followup | 8:00, 12:00, 17:00 Mon-Sat (last ran Nov 5; confirm with Dan) |
| video-model-watch-monthly | 8:00 on the 1st |

**One-time tasks still due** (enable on the M6 only if Dan still wants them): ro08-tiktok-direct-upload Nov 19 12:05, ro20-tiktok-direct-upload Nov 23 12:05, ro20c-tiktok-direct-upload Dec 7 12:05.

**Decide in handoff 03:** edit-stall-watchdog (every 15 min; it watches edit runs, which stay on the M2).

**Leave off** (stale since Aug to Oct, or past their window): abs-by-ai-morning-brief, daily-watch-history-review, editor-deliveries-daily, twc-work-search, unemployment-payment-reminder, android-play-review-watch, ro26-release-after-ro25-public, and every past-due one-time task. Unregistered folders (no schedule on either Mac): abs40-vs-25-blotato-queue, fire-vqc-phase3-watch-pass, ro07-blotato-queue-when-room, sl03-queue-shorts-2-3-6, verify-828-drive-backup-2.

**Disable on the M2:** nothing to do today (all off). At the switch, re-check the M2's `scheduled-tasks.json` shows `enabled count: 0` and unload `com.absbyai.fb-reel-covers` there only if Dan approves changing the M2.

**Switch steps:** (1) Dan confirms he has stopped opening Claude on the M2; (2) `~/M2-transfer/copy-home.sh` then `copy-home.sh verify`; (3) re-check the M2 task count is 0; (4) register and enable the tasks above on the M6 through Claude's scheduled-tasks tools (`cwd` `/Users/danielrose/Documents/Claude/Projects/Abs By AI` works through the alias); (5) enable `com.absbyai.fb-reel-covers` on the M6.

## Sign-in list for Dan

Copied logins that already work (nothing to do): **railway**, **rclone** (Google Drive), **Codex** inside ChatGPT (via `~/.codex/auth.json`), **gh / git** (signed in today), **Google Drive, Gmail and Calendar connectors** in Claude (account-level, already connected).

Needs Dan:

1. Claude in Chrome extension: install it in Chrome on the M6 and sign in.
2. Chrome profile: sign in to Chrome (passwords and bookmarks sync; cookies do not move between Macs).
3. ChatGPT app (Codex is inside it).
4. Gemini.
5. Grok Bot.
6. Comet.
7. Manus Studio.
8. Cursor.
9. Wispr Flow (also grant microphone and accessibility when it asks).
10. Slack.
11. Descript.
12. `claude` in the terminal: run `claude` once in Terminal and sign in (the desktop app is signed in; the terminal tool is not).
13. shopify CLI: `shopify auth login` when next needed.
14. Zoom, Telegram, Thunderbird, Steam, Android Studio, iMazing, AnyDesk, Grammarly and the other browsers: sign in when first used.
15. Restart Claude once so the copied past sessions appear in the sidebar. If they still do not appear, the chats remain on the M2 and in the staging copy.

## Next

Fire handoff 03 (`Handoffs/two-mac-setup-20261112/03-two-mac-edit-routing.md`, Claude Fable 5.2, high). It owns the edit-queue dispatcher, the edit-stall watchdog, the drive access decision and the nightly-footage check above.

## Update, November 14, 2026 (morning)

- **Codex automations were running on both Macs.** Copying `~/.codex` and opening ChatGPT once on the M6 for the launch test made Codex's 8 active automations run here as well as on the M2 (check-youtube-shorts-covers, finish-ro-25-article-and-captions-check, keep-your-muscle-release-check, nightly-seagate-copy-verification, publish-daily-morning-brief-locally, release-ro-25-tiktok, upwork-follow-up-drafts, verify-ro-25-after-9-am-release). Codex on the M6 flagged it itself in `AI_COORDINATION.md` ("M2/M6 duplicate publishers"). Its M6 runs made four commits that only touched notes (`AI_COORDINATION.md`, `Docs/MORNING_BRIEF_LOCAL.md`, the M2 prep receipt); nothing posted outside the repo was found. **Fixed at 7:27 a.m.:** ChatGPT quit on the M6 and all 8 set to `PAUSED` in `~/.codex/automations/*/automation.toml` **on the M6 only** (originals in `~/M2-transfer/codex-automations-before-pause/`). The M2 keeps running them, unchanged. Moving Codex automations to the M6 is a separate switch for Dan; it was not part of the Claude-task switch.
- **Claude is still busy on the M2.** Six Claude Code sessions are open there and delivered DS-41 R1 and SL-21 round 2 overnight. Dan was told to leave Claude running on the M2; the plan's condition is that *Dan* no longer opens Claude there, which he confirmed.
- **Scheduled-task switch, approved by Dan:** the 8 recurring tasks in the switch list (house-sale-followup included) are written into the M6 registry, enabled, with `missedRunScanFloor` set to now so no Nov 11-14 catch-up runs fire. The running app keeps its list in memory, so a one-time helper (`launchctl` job `com.danrose.m6-task-switch`, script `~/M2-transfer/switch/`) re-applies them the moment Claude quits; they load when Claude reopens. The M2 registry still has 0 enabled. Task files re-synced from the M2 (0 differences). One-time TikTok uploads (Nov 19, Nov 23, Dec 7) and edit-stall-watchdog stay off. `com.absbyai.fb-reel-covers` stays disabled on the M6 because the M2 still runs it.
- **Past sessions** now appear in the M6 sidebar (no restart was needed).
- **Dock:** auto-hide on, size and magnification copied from the M2. **Wallpapers:** the M2 uses two ChatGPT images from its `~/Downloads` plus `image (6).png` from iCloud Drive. The iCloud one is in `~/Pictures/Wallpapers` on the M6; the two Downloads images are blocked by the M2's privacy protection over both SSH and the SMB home share (the share lists Downloads as empty), the same block as the drives and Shottr's settings.
- **M2 change approved by Dan (7:37 a.m.):** at the M2's own keyboard Dan turned on Remote Login > *Allow full disk access for remote users* and switched Screen Sharing off and on (remote Screen Sharing had failed with "not permitted" because it was enabled from the command line during prep). Verified from the M6: `ssh m2 ls /Volumes/Extreme` and `/Volumes/Expansion` now list (read only; nothing written), and the M2's `~/Downloads` and app containers are readable. Mounting the exFAT drives over SMB is still not possible. The two wallpaper images were then copied to `~/Pictures/Wallpapers` and the first set as the M6 wallpaper. Shottr's settings cannot be written from outside Shottr (macOS app-data protection); the M2 values are afterGrabCopy on, editor window off, area Ctrl+Shift+Cmd+Space, full screen Cmd+Shift+Space, OCR Ctrl+Opt+Cmd+O.


## 02b: Claude desktop SSH connection completed (Codex, November 14, 2026)

- Added the SSH connection **`m2`** through Claude Desktop **5.11492.5**, Code > new session > Environment > New environment > SSH > Host > Add SSH connection. The current layout puts SSH inside New environment, rather than directly in the environment menu.
- Entered connection name `m2`, SSH host `m2`, and SSH key `~/.ssh/id_ed25519`. Left the port at the SSH-config default and the worktree folder at its host default. The form has no separate user field: `ssh -G m2` confirms user `danielrose`, resolved host `10.66.0.2`, and the requested identity file.
- Accepted the requested connection prompt. **Test connection** reported **“Connected. This host is ready to use.”**, using **OpenSSH 10.5 /usr/bin/ssh**. No new host-key prompt, password, or Claude sign-in was required. Nothing was refused.
- Claude installed its remote helper and Claude Code on the M2. Verified files: `~/.claude/remote/srv/87375cc7c944eb9d45c8d9267edc70a4b4827961/server` (8.2 MB) and `~/.claude/remote/ccd-cli/2.1.325-1b2c3c6aecdd` (331 MB). The app displayed the CLI download completing at 114/114 MB.
- Saved an SSH **environment also named `m2`**, with folder `/Users/danielrose/Projects/Claude/Projects/Abs By AI`, Worktree unchecked. Accepted the trust prompt for that exact folder on `m2`.
- Started only a verification session, **Hostname**, ID `local_e643e097-5d87-466c-a9a5-c4055e4e0e6e`. Its `!hostname` command returned **`m2`** with prompt `danielrose@m2 Abs By AI %`. In its integrated remote terminal, `pwd` returned **`/Users/danielrose/Projects/Claude/Projects/Abs By AI`**. No edit was started.
- Closed the terminal and archived only that disposable test session. Opened New again and verified **Recent environments: m2 m2** and **Environment: m2** remain available. Other sessions were not archived or deleted.
- Verification used the actual desktop UI and remote shell. Codex does not expose Claude's `list_start_targets` tool, so that API was not called here; the saved SSH host, saved project environment, and successful app session were verified directly. Handoff 03 can now select `m2`.
