# M2 headless preparation receipt

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
