# 01: Prepare the M2 to run headless (Codex or Grokbot, on the M2)

Category: ops. Read `README.md` in this folder first. Dan authorizes every step here, including typing his Mac login password at the admin prompts (it is in his password vault; never write it into a file). These are the steps Claude cannot do because they change system settings and need the admin password. Do the whole thing; do not stop to ask Dan.

Nothing here interrupts running edits. Do not restart the Mac while `python3 .claude/skills/_shared/renderq/renderq.py status` shows active holders.

## Steps (System Settings, or the commands shown with `sudo`)

1. **Names.** Computer name `M2`, local hostname `m2`: `sudo scutil --set ComputerName M2; sudo scutil --set LocalHostName m2; sudo scutil --set HostName m2`.
2. **Sharing** (System Settings > General > Sharing): turn on **Remote Login** (allow user `danielrose`), **Screen Sharing**, and **File Sharing**. In File Sharing add `/Volumes/Extreme` and `/Volumes/Expansion` as shared folders named exactly `Extreme` and `Expansion`, read and write for `danielrose`.
3. **Thunderbolt link address.** System Settings > Network > Thunderbolt Bridge > Details > TCP/IP: Manually, IP `10.66.0.2`, mask `255.255.255.0`, router empty. Or `sudo networksetup -setmanual "Thunderbolt Bridge" 10.66.0.2 255.255.255.0`.
4. **Never sleep, come back after a power cut:** `sudo pmset -a sleep 0 disksleep 0 displaysleep 10 autorestart 1 womp 1 powernap 0`.
5. **Log in by itself after a restart** (System Settings > Users & Groups > Automatically log in as: Daniel Rose). The background routines and the review pages only run when the account is logged in. This needs FileVault off; if FileVault is on, turn it off and note that in the receipt.
6. **Keep external drives awake:** confirm "Put hard disks to sleep when possible" is off (Energy settings).
7. **SSH folder ready:** `mkdir -p ~/.ssh && chmod 700 ~/.ssh && touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys`.

## Verify, then report

- `systemsetup -getremotelogin` says On; `ssh danielrose@localhost true` works after accepting the key; `sharing -l` lists Extreme and Expansion; `ifconfig bridge0` shows `10.66.0.2`; `pmset -g` shows `sleep 0` and `autorestart 1`.
- Write `Docs/TWO_MAC_M2_PREP_RECEIPT_20261112.md` (what was set, what was already set, anything refused), push it with `scripts/git/safe-push.sh`, and move this handoff's line in `Handoffs/README.md` out of OPEN.

Done looks like: the M2 can be reached by SSH, screen sharing and file sharing, holds `10.66.0.2` on the Thunderbolt Bridge, never sleeps, and logs itself in after a restart.
