# 02: Set up the new M6 from the M2, over the cable (Claude, on the M6)

Category: ops. Read `README.md` in this folder first (decisions, inventory). You are running on the brand-new M6. The old machine (M2) is at `10.66.0.2` on the Thunderbolt Bridge and holds everything. Dan's rules: do every step yourself, no asking for reversible work, explain in plain words. He does only logins and passwords.

Model: Claude Opus 5.5, high.

## What Dan has already done before firing this

Created the account `danielrose` on the M6, signed in to his Apple ID, installed Claude, plugged in the Thunderbolt cable, and handoff 01 has run on the M2. Check each; if one is missing, say which in one line and carry on with what does not depend on it.

## Hard rules

- **Copy, never move.** Nothing is deleted or changed on the M2 in this handoff. The M2 keeps its full copy until Dan approves cleanup later.
- The repo is public. Secrets and private files go machine to machine over the cable only, never into git, chat or an artifact.
- You cannot type passwords or change system settings. When a step needs one, open it for Dan (Terminal tab or the settings pane), tell him the one thing to type or click, and continue other work meanwhile.
- Verify every copy: `rsync -a --checksum --dry-run` (or file counts plus sizes) must show nothing left to send.

## Steps

1. **Link.** The M6 needs `10.66.0.1` on its Thunderbolt Bridge. Give Dan the one command to run in the Terminal panel (it asks for his Mac password): `sudo networksetup -setmanual "Thunderbolt Bridge" 10.66.0.1 255.255.255.0; sudo scutil --set ComputerName M6; sudo scutil --set LocalHostName m6; sudo scutil --set HostName m6; sudo pmset -a sleep 0 autorestart 1`. Then `ping -c 3 10.66.0.2`.
2. **SSH both ways.** `ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519` if absent. Write `~/.ssh/config` with hosts `m2` (10.66.0.2) and `m6` (10.66.0.1), user `danielrose`. Have Dan run `ssh-copy-id m2` in the Terminal panel and type his M2 password once. From then on no passwords: over that connection create the M2's own key and append its public key to the M6's `~/.ssh/authorized_keys`, and copy the same `~/.ssh/config` to the M2. Dan turns on Remote Login on the M6 (System Settings > General > Sharing), needed so the M2 can reach back. Test `ssh m2 hostname` and `ssh m2 ssh m6 hostname`.
3. **Check room.** `df -h /`. The copy needs about 260 GB. If the M6 would be left with under 150 GB free, skip old session transcripts under `~/.claude/projects/*/` (keep every `memory/` folder) and `~/.codex/archived_sessions`, and say so.
4. **Command line tools first** (the copy does not need them, the checks do). Trigger Apple's command line tools (`xcode-select --install`; Dan clicks Install). Install Homebrew only if Dan is present to type the password; otherwise install node without admin rights (official tarball into `~/.local`, on the PATH in `.zshrc`). Find how the M2 gets ffmpeg (`ssh m2 'which -a ffmpeg; mdfind -name ffmpeg | head'`, and grep the skills) and reproduce the same path on the M6.
5. **Copy the home state** with `rsync -aE --info=progress2` from `m2:` to the same paths: `~/Projects/Claude`, `~/Projects/Codex`, `~/Projects/_research`, `~/.claude`, `~/.claude.json`, `~/.codex`, `~/bin`, `~/.local`, `~/.npm-global`, `~/.npmrc`, `~/.venvs`, `~/.zshrc`, `~/.gitignore`, `~/.gitconfig`, and every private item listed in the README inventory. Do NOT copy `~/Projects/_edit_work` (stays on the M2) or `/tmp/absbyai-*`. Do the `~/.claude` copy before Dan opens other sessions on the M6, and exclude this chat's own live session files so the copy never overwrites them.
6. **Apps.** Copy from `m2:/Applications/` every app in the README inventory that is a plain drag-install app (`rsync -aE`), AI apps first: ChatGPT, Gemini, Grok Bot, Comet, Manus Studio, Cursor, Wispr Flow, Google Chrome, Descript, Slack, zoom.us, Telegram, Shottr, Cinch, VLC, The Unarchiver, Google Ads Editor, Android Studio, iMazing, the other browsers, and Dan's personal apps. Open each once and confirm it launches. Apps that need their own installer (Adobe, NordVPN, Xcode from the App Store, printer software, any that fail to launch) get a fresh download from the vendor's official site; list for Dan any that need his login to download.
7. **Rebuild what does not copy cleanly.** Recreate `~/.venvs/*` if their Python is missing; `npm rebuild` in `~/.npm-global` if a native module fails; check `railway whoami`, `claude --version`, `node -v`, `python3 -V`, `ffmpeg -version`, `rclone version`, `yt-dlp --version`.
8. **Mount the M2's drives.** Dan connects once in Finder (Go > Connect to Server, `smb://10.66.0.2`), picks Extreme and Expansion, ticks "Remember this password". Then add both to Login Items so they mount at login, and confirm `/Volumes/Extreme` and `/Volumes/Expansion` resolve. Read only a test file; write nothing to the Seagate.
9. **Project checks.** In `~/Projects/Claude/Projects/Abs By AI`: `git status` matches the M2's, `scripts/git/drift-check.sh`, `python3 .claude/skills/_shared/renderq/selftest.py`, `renderq.py status`, `editcap.py status`, hooks in `~/.claude/settings.json` fire (wrap-up hook), the memory folder is present, and the `task-wrapup` mod loads.
10. **Scheduled tasks and routines run on one Mac only.** List the Claude scheduled tasks and the `com.absbyai.*` / `com.danrose.*` LaunchAgents. Install on the M6 the ones that belong to the daily driver (review hub, edit queue pages, claude-cleanup, fb-reel-covers). `com.absbyai.nightly-footage` stays on the M2. Do not switch the scheduled tasks over yet: write the exact switch list (enable on M6, disable on M2) into the receipt and do the switch only when Dan says he has stopped opening Claude on the M2, so nothing fires twice.
11. **Sign-in list for Dan.** One numbered list of every app and CLI that needs him: Claude in Chrome extension, Chrome profile, ChatGPT/Codex, Gemini, Grok Bot, Comet, Manus, Cursor, Wispr Flow, Slack, Descript, `gh`/git credentials for safe-push, `railway login`, rclone remotes (copied config normally works), Google Drive connectors. Mark which ones copied their login and need nothing.
12. **Receipt.** `Docs/TWO_MAC_M6_SETUP_RECEIPT_<date>.md`: what copied and verified, what was reinstalled, what failed, the sign-in list, the scheduled-task switch list. Push with `scripts/git/safe-push.sh`. Update `Handoffs/README.md`.

## Done looks like

On the M6: the project opens in Claude with memory, skills, hooks and mods working; every AI app launches; `git`, `node`, `python3`, `ffmpeg`, `railway`, `rclone` work; `ssh m2` works without a password; the M2's two drives are mounted at their usual names; the M2 is untouched and still running its edits. Then tell Dan to fire handoff 03, with its starter prompt.
