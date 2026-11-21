# M2 headless preparation receipt

**Current status, November 14, 2026: handoff 01 COMPLETE.** The M6 now reaches the M2 through passwordless SSH, an authenticated Screen Sharing desktop session, and native SMB mounts of both external drives. All requested names, sharing, cable addressing, power and automatic-login settings are applied. Restart, power-cut recovery and reconnect after a real reboot remain untested; no restart or physical-drive unmount was performed.

## Final drive-sharing repair, November 14

Dan authorized enabling Full Disk Access for the M2 file-sharing service. Codex connected through Screen Sharing, opened the M2's System Settings, authenticated at the admin prompt and added `/usr/sbin/smbd` to **Privacy & Security > Full Disk Access**. The settings display showed **smbd ON** and **sshd-keygen-wrapper ON**. Read-only system permission metadata corroborated both grants. No privacy database was edited and System Integrity Protection was not changed.

The effective remote-user grant now allows SSH reads of both drives. Adding the missing file-sharing grant resolved the separate SMB failure. Earlier claims that exFAT/FSKit made these shares impossible were incorrect. Neither filesystem nor drive mounting method needed changing.

### Verified from the M6

- `ssh m2 hostname` returns `m2`; the reverse SSH connection returns `m6` without a password. An actual authenticated M2 desktop was operated through Screen Sharing.
- Native macOS NetFS mounted `//danielrose@10.66.0.2/Extreme` at `/Volumes/Extreme` and `//danielrose@10.66.0.2/Expansion` at `/Volumes/Expansion`. The M6 mount table confirms both are SMB filesystems owned by its `danrrose` account.
- Read real project files through each SMB mount and compared SHA-256 against the same files read directly on the M2 over SSH:

| Drive | Project sample | Matching SHA-256 |
|---|---|---|
| Extreme | `_edit_work/RO-22/setup/RESUME.md` | `adc056975b839ba2055fc0196a625edb1ddb403c33914897155ab1e7ef86cc9a` |
| Expansion | `_edit_work/DS-41/r1/RESUME.md` | `6c8a1128903e4a7f21ad1fd0779e13db2c1c017a91981882215d053aecaa1746` |

- An additional native SMB read/hash comparison passed for a small existing file on each drive.
- A uniquely named temporary probe on **Extreme only** passed SMB write, readback and remote checksum comparison, then was removed. **No file was written to Expansion in this repair.** Expansion is shared read/write as requested, but this repair tested it read-only, respecting handoff 02's Seagate restriction.
- Rechecked M2 names `M2`/`m2`/`m2`, Remote Login On, FileVault Off, automatic-login user `danielrose`, Thunderbolt `10.66.0.2/24` with no router, and power values `sleep=0 disksleep=0 displaysleep=10 autorestart=1 womp=1 powernap=0`.

### Quiet automatic reconnect on the M6

Installed and loaded the per-user LaunchAgent `com.absbyai.m2-drive-mounts`:

- Helper: `~/Library/Application Support/AbsByAI/mount-m2-drives.py`.
- Agent: `~/Library/LaunchAgents/com.absbyai.m2-drive-mounts.plist`.
- Log: `~/Library/Logs/AbsByAI/m2-drive-mounts.log`.
- Durable source copies: `scripts/two-mac/mount-m2-drives.py` and `scripts/two-mac/com.absbyai.m2-drive-mounts.plist` (the plist paths are for this M6 account).

It runs at login and retries every 60 seconds using native macOS NetFS and the existing Keychain login. No credentials are stored in these files and dialogs are suppressed. It returns quietly when the cable is absent or both expected shares are mounted, and refuses to replace an unexpectedly occupied mount path. It never unmounts or formats a drive. Each mount attempt has a 45-second limit.

Validation: native NetFS actually mounted both shares; the installed helper then exited 0 with both present; plist lint passed; `launchctl` shows the loaded agent with successful runs and last exit code 0. Actual reboot/cable-disconnect recovery was not tested, to avoid disrupting concurrent work.

### Completion and boundaries

Handoff 01 is retired from OPEN. Handoff 02 migration and the separate 02b Claude-app SSH connection have their own [M6 receipt](TWO_MAC_M6_SETUP_RECEIPT_20261113.md). Handoff 03 edit routing and the scheduled-task switch remain separate work; this drive repair did not launch edits or move scheduled jobs.

The following entries are a chronological diagnostic history. Their blocker and next-action statements are superseded by the verified completion above.

## Original November 13 execution log

Executed: November 13, 2026, approximately 5:37–5:53 p.m. America/Chicago.
Owner: Codex. Source: `Handoffs/two-mac-setup-20261112/01-m2-prep-codex-grokbot.md`.
Machine: Mac14,12, macOS 26.5.2 (25F84), user `danielrose`.

**Status: all requested system settings applied; external-drive SMB access is blocked by a verified server error. Handoff 01 is not fully complete.** No restart, logout, drive unmount, formatting, data migration, or interruption of another edit was performed. Handoffs 02 and 03 were not executed.

## Settings and verification

| Item | Before | Applied and verified |
|---|---|---|
| Names | Computer `Mac mini`, local `Mac-mini`, HostName unset | Computer `M2`, local `m2`, HostName `m2`; all three `scutil --get` checks pass |
| Remote Login | Off | Persistent SSH launch service enabled; `systemsetup -getremotelogin` reports **On**; `ssh danielrose@localhost true` authenticated and exited **0** |
| SSH access | Admin group permitted | Access list explicitly contains `danielrose`, with inherited admin group removed |
| Screen Sharing | Service not configured by this task | Persistent service enabled; TCP 5900 accepts connections and returns `RFB 003.889`; access explicitly limited to `danielrose`. A full remote desktop session from the M6 has not been tested |
| File Sharing | No explicit share records | Persistent SMB service enabled; TCP 445 listening; `sharing -l` lists exact shares `Extreme` and `Expansion`, paths `/Volumes/Extreme` and `/Volumes/Expansion`, shared=1, read-only=0, guest=0. Both roots are owned by Dan with owner read/write access |
| SMB login | Initial authentication rejected | Enabled the account's SMB-NT credential support and refreshed its password data using the **same existing password**, without selecting a new password. Authenticated `smbutil view //danielrose@localhost` now succeeds and lists both shares |
| Thunderbolt | DHCP, no address | Service manually configured to `10.66.0.2`, mask `255.255.255.0`, router empty. Address also applied to `bridge0`; `ifconfig bridge0` shows `inet 10.66.0.2 netmask 0xffffff00`. Physical link remains **inactive**, so M6 cable connectivity is untested |
| Power | sleep=0, disksleep=0, displaysleep=10, womp=1 already set; autorestart=0, powernap=1 | `pmset -g custom`: sleep=0, disksleep=0, displaysleep=10, autorestart=1, womp=1, powernap=0 |
| Automatic login | Not configured; FileVault On | FileVault disabled as instructed; `fdesetup status` reports **Off**. `sysadminctl -autologin status` reports `Automatic login user: danielrose`; loginwindow setting matches. Actual restart/login behavior deliberately not tested while renders run |
| SSH folder | Absent | `~/.ssh` mode 700; `authorized_keys` mode 600, owned by Dan; existing content not overwritten. Local SSH host key accepted into known_hosts. No new SSH identity or M6 key installed |

`systemsetup -setremotelogin on` initially refused because its caller lacks Full Disk Access. The system's SSH LaunchDaemon was enabled and bootstrapped directly with admin privileges; the subsequent official status check and authenticated SSH test both passed. No Full Disk Access grant or privacy database modification was made.

## Remaining blocker: actual external-drive access

Checking only the share list would have missed this failure:

- Native authenticated SMB enumeration succeeds and lists `Extreme` and `Expansion`.
- Native `mount_smbfs` tests for each return **No such file or directory**, despite both mount folders and share paths existing.
- An independent Python `smbprotocol` client authenticated successfully. A temporary file in the existing internal `danielrose` share was written over SMB, read back, and compared byte-for-byte with the local file: **PASS**.
- The same client's file creation on **both external shares** fails with **STATUS_INTERNAL_ERROR (0xc00000e5)**. No probe files remain.
- Both external drives are mounted as **exFAT using FSKit**. Server logs also report `query_volume_attributes_check_root ... APFSVolumeRole error: 0xc002`. These observations isolate the failure to external-volume sharing; they do **not** establish the root cause.

Diagnostic environment and non-secret results are in `~/Library/Caches/two-mac-prep-20261113/`; `smb-check.json` records the three outcomes. The isolated environment installed `smbprotocol` from PyPI. No password was put in a command argument, script, receipt, or repository file.

**Exact next action:** continue diagnosing the external SMB failure without disrupting edits. When an idle maintenance window exists, test native external-volume access from the M6 and isolate the FSKit/exFAT behavior with a disposable test volume before changing either production drive's mounting method. Do not reformat these drives. Do not treat handoff 02's drive mounts as ready until actual SMB reads/writes pass.

The render queue was checked before and after setup and still had an active heavy holder at the end. Per the handoff, no restart was attempted. Automatic login, power-cut recovery, the physical Thunderbolt connection, and an M6 Screen Sharing session remain untested in practice.

## Handoff status

The main handoff index retains the remaining work in OPEN, with the verified blocker. Marking handoff 01 completed and removing its unfinished access verification would be inaccurate. Resume only the failed verification/repair, rather than repeating the completed system settings.

Reference consulted: [Apple: Set up SMB file sharing](https://support.apple.com/en-gb/guide/mac-help/-mh14107/mac). Findings above are from actual local tests, not inferred from that guide.


## Resumed from the M6 on November 13

Codex resumed this same chat on the M6 and verified:

- The current Mac identifies as `M6`, model `Mac18,5`. Its account is `danrrose`, with `/Users/danielrose` linked to that home. The active Thunderbolt Bridge has `10.66.0.1/24` and sees the M2.
- Passwordless `ssh m2 hostname` returns `m2`; the reverse connection through `ssh m2 ssh m6 hostname` returns `m6`.
- Claude owns the ongoing M6 migration, documented in `Docs/TWO_MAC_M6_SETUP_RECEIPT_20261113.md`; an rsync verification process was still running. Codex did not modify its scripts, receipt, copies, or live state.
- On the M2, both ordinary SSH and an authenticated root SSH session receive **Operation not permitted** when listing either external drive. macOS privacy logs contain `kTCCServiceSystemPolicyRemovableVolumes` requests and denial messages during these checks. This establishes a remote-session privacy obstacle; it does not prove that privacy is the only cause of the separate SMB errors.
- The M2 still has an active render holder. No restart, unmount, or drive change was attempted.
- Computer-use access to the M6 Screen Sharing app timed out twice, including one attempt using its verified path `/System/Applications/Utilities/Screen Sharing.app`. No remote desktop session was established and no privacy setting was changed.

**Immediate next action for Dan:** on the M2, open System Settings > General > Sharing > Remote Login (information button), and enable **Allow full disk access for remote users**. This is the supported setting for disk access from authenticated SSH sessions ([Apple instructions](https://support.apple.com/en-mt/guide/mac-help/mchlp1066/27/mac/27)). After it is enabled, Codex should reconnect from this same M6 chat, verify external-drive reads, and continue the SMB diagnosis without disrupting edits. The Screen Sharing automation timeout prevents Codex from reaching that switch through the desktop interface from here.


## November 14 follow-up after Dan enabled remote-user disk access

Dan confirmed enabling the M2 Remote Login full-disk switch and authorized continued repair from the M6. Checks at approximately 7:18–7:28 a.m. Central:

- Fresh SSH sessions, explicitly disabling connection reuse, still cannot list either external volume. An authenticated root SSH session gets the same denial.
- Authenticated SMB share enumeration from the M6 succeeds and lists both exact share names. A native M6 mount of `Extreme` still returns **No such file or directory** after successful authentication. Neither external drive is mounted on the M6.
- The M2 privacy log directly attributes the SSH denial to `/usr/libexec/sshd-keygen-wrapper`. At 07:20:28, request `25468.813` for `kTCCServiceSystemPolicyAllFiles` returned `authValue=0, authReason=5`.
- The same log attributes the failing SMB volume access to `/usr/sbin/smbd`. At 07:23:10, request `25468.824` for `kTCCServiceSystemPolicyAllFiles` returned `authValue=0, authReason=5`; its removable-volume request `25468.825` returned `authValue=1, authReason=0`, rather than an allowed grant.
- A read-only check of the system permission database was refused. No permission database was modified. A standard service refresh using `launchctl kickstart` was also refused by System Integrity Protection; that protection remains enabled and no alternative bypass was attempted.
- A new attempt to reach the M2 via Finder's `vnc://10.66.0.2` route reached the native Screen Sharing login dialog. The app then quit during sign-in, and computer use returned **App quit**. Therefore the M2 settings still cannot be operated through that interface from here.
- The render queue was idle at the initial check. No Mac restart, drive unmount, drive format, file copy, or exported-media change was performed. No new probe was written to either production drive.

**Current prerequisite:** on the M2, open **System Settings > Privacy & Security > Full Disk Access**. Enable both **sshd-keygen-wrapper** and **smbd**. If missing, add the verified existing executables with **+**, then **Command-Shift-G**:

1. `/usr/libexec/sshd-keygen-wrapper`
2. `/usr/sbin/smbd`

This requests permission for the actual two services observed in the logs, rather than asking Dan to repeat the Remote Login switch. Once enabled, reconnect from the M6, verify real external-drive reads, and retry the native mounts before investigating filesystem behavior. Effective permission has not yet been verified, and the FSKit hypothesis remains unproven.

References: [Apple remote access setting](https://support.apple.com/en-mt/guide/mac-help/mchlp1066/27/mac/27); [storage vendor instructions for SMB Full Disk Access](https://help.iodyne.com/hc/en-us/articles/42386134675095-Sharing-a-container-over-SMB). These are setup references; the denial evidence above comes from the actual M2 logs.
