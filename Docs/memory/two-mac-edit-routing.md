---
name: two-mac-edit-routing
description: Two Macs share video edits (M6 Dan's Mac 2 slots, M2 Pro headless 3 slots); run editroute.py pick before editcap acquire on every new edit
metadata:
  type: project
---

Since 2026-11-14 video edits run on two Mac minis on a Thunderbolt cable: the M6 (Dan's daily Mac, `m6`, 10.66.0.1, 2 edit slots, 6 of 12 cores while Dan is at it, 10 when away or 10 PM to 7 AM) and the M2 Pro (headless, `m2`, 10.66.0.2, 3 slots, 8 cores, holds the Extreme and Seagate drives). Numbers live in `.claude/skills/_shared/editroute/hosts.json`.

**Why:** Dan bought the M6 as his own machine; the M2 takes the overflow (handoff `Handoffs/two-mac-setup-20261112/03-two-mac-edit-routing.md`, receipt `Docs/TWO_MAC_EDIT_ROUTING_RECEIPT_20261114.md`). The exFAT drives cannot be shared to the M6 over SMB, so M6 edits pull footage with `editroute.py fetch` and M2 edits use the drives in place.

**How to apply:** before the first `editcap.py acquire` of a new edit run `editroute.py pick <JOB> --kind <K> --round <N>`; if it names the other Mac, start the edit there (Claude: app SSH connection `m2`; Codex: `ssh m2 codex exec`). Review pages made on the M2 open on the M6 at the same `http://127.0.0.1:PORT/` link. Finals from the M2: `editroute.py push`. The M2 has its own git checkout (not a share). See [[render-queue]] and the edit cap rule in VIDEO-RULES.md.
