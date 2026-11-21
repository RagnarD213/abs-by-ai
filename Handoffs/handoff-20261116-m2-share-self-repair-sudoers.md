**DONE 2026-11-16 12:33 by Dan himself (both entries parsed OK); Claude restarted smbd (748% -> 0% CPU) and verified both shares remounted, read/write, and `sudo -n -l` on both Macs. Do not fire.**

# Handoff: let the M6 repair a stuck M2 drive share by itself (2026-11-16)

For **Codex and Grokbot**. Dan authorizes the whole step, including typing his Mac passwords: "I don't want to do this
myself" (2026-11-16). Do every step below yourselves; do not hand anything back to Dan. Never write a password into any
file, log, commit or chat. Passwords: Dan's password vault (Grokbot has access). The two Macs: the **M6** (Dan's Mac, user
`danrrose`) and the **M2** (headless Mac Pro-style edit machine, user `danielrose`, reachable from the M6 as `ssh m2`,
address 10.66.0.2 on the cable between them).

## What happened
The M6 shows the M2's two drives (`/Volumes/Extreme`, `/Volumes/Expansion`) over SMB file sharing. On 2026-11-16 at about 12:20
the M2's file server (`/usr/sbin/smbd`) stuck at 200-700% CPU and both shares dropped on the M6. The M6's reconnect job
(LaunchAgent `com.absbyai.m2-drive-mounts`, every 60 s, script `~/Library/Application Support/AbsByAI/mount-m2-drives.py`,
repo copy `scripts/two-mac/mount-m2-drives.py`) times out and cannot repair it, because restarting `smbd` and force-unmounting
a dead share need root. Claude already extended that script (committed c7bc5b1): when a reconnect times out it now runs
`ssh m2 'sudo -n /bin/launchctl kickstart -k system/com.apple.smbd'` (at most once per 15 min) and
`sudo -n /sbin/umount -f /Volumes/<share>` for a stale mount. Those two `sudo -n` calls only work once two narrow sudoers
entries exist. That is this job.

## The step (about 2 minutes)
1. On the M6, in Terminal (logged in as `danrrose`), run and enter the **M2's** password for `danielrose` when asked:
   ```
   ssh -t m2 "echo 'danielrose ALL=(root) NOPASSWD: /bin/launchctl kickstart -k system/com.apple.smbd' | sudo tee /etc/sudoers.d/absbyai-smbd >/dev/null && sudo chmod 440 /etc/sudoers.d/absbyai-smbd && sudo visudo -cf /etc/sudoers.d/absbyai-smbd"
   ```
2. On the M6, run and enter the **M6's** password for `danrrose`:
   ```
   echo 'danrrose ALL=(root) NOPASSWD: /sbin/umount -f /Volumes/Extreme, /sbin/umount -f /Volumes/Expansion' | sudo tee /etc/sudoers.d/absbyai-m2-shares >/dev/null && sudo chmod 440 /etc/sudoers.d/absbyai-m2-shares && sudo visudo -cf /etc/sudoers.d/absbyai-m2-shares
   ```
   Both must print "parsed OK". If `visudo -c` fails, remove that file at once (`sudo rm /etc/sudoers.d/<name>`) and report.
   Each entry allows exactly one command without a password; nothing else changes.
3. Repair the share now: `ssh m2 'sudo -n /bin/launchctl kickstart -k system/com.apple.smbd'`. This restarts only the M2's file
   sharing; renders and edits running on the M2 read its drives directly and are not touched.
4. Wait up to 3 minutes for the reconnect job (or run `/usr/bin/python3 "$HOME/Library/Application Support/AbsByAI/mount-m2-drives.py"`).
   Verify on the M6: `mount | grep -E 'Extreme|Expansion'` shows `//danielrose@10.66.0.2/Extreme on /Volumes/Extreme` and the
   same for Expansion, and `ls /Volumes/Extreme/_edit_work | head` returns within a few seconds.
5. Verify the M2's file server is calm: `ssh m2 'ps -o pcpu= -p $(pgrep -x smbd)'` under about 20.
6. Verify the self-repair permissions work without a password: `sudo -n -l` on the M6 lists the two umount commands, and
   `ssh m2 'sudo -n -l'` lists the kickstart command.

## Do not
- Eject, unplug or unmount the Extreme or Expansion on the M2 (renders are writing to them).
- Restart either Mac, change other sudo rules, sharing settings or accounts.
- Kill any process on the M2 other than through step 3.

## Report (short, plain words, for Dan)
Both entries installed and checked; share remounted (yes/no); M2 file server CPU before and after; anything that failed with
the exact message. Then remove this handoff's line from the OPEN section of `Handoffs/README.md` and commit with
`scripts/git/safe-push.sh` (Codex) or tell Claude to (Grokbot).
