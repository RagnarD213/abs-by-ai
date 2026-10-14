Tooling task (no video category). Sidebar name for the next task: `Frame QC Motion Takes`.

**Steps 1 to 3 DONE 2026-10-14 (Frame QC Upgrade session, commit 777a5e6):** `.claude/agents/frame-reviewer.md`, the frame spec
(`_shared/framecheck/spec.example.json`), `_shared/framecheck/gate.py` with stamps and `--verify`, wired into `PRE-RENDER-APPROVAL.md`,
`VIDEO-RULES.md`, `/ad-edit` and `/longform-edit`. Proof: the five rejected RA-04 pairs fail, F4h/F5p passes, also with every box
shifted 4 to 5 px (`_shared/framecheck/README.md`, Proof). Open: steps 4 and 5 below.

# Catch impossible AI frames and clips before Dan sees them: the frame-QC upgrade

**Written 2026-10-14 by the RA-04 round 2 session (Claude, Opus 5.5)**, at Dan's request after he rejected a leg press frame pair:
*"This is something which should have been caught in quality control... do some research and see if there are some kinds of skills,
repos, or modifications for Claude where we can do better QC on these start and end frames. If we get start and end frames that make
no anatomical sense like this or no physics sense, we reject it and regenerate."*

## What already exists (built 2026-10-14, works)

`.claude/skills/_shared/framecheck/` (README there): `posecheck.py` (MediaPipe pose: joint angles, bone lengths, body line against a
machine's guide), `rigid.py` (local template tracking: do rigid parts move together and along their guide; does anything static
drift), `lockstill.py` (copies static pixels from START). Plus a fresh independent reviewer subagent given only the pictures and a
measured checklist (A to I: machine realism, contact, body line, anatomy and bone lengths, continuity, hands and props, expression,
AI slop, animate test). On RA-04's leg press that reviewer failed six pairs and passed the seventh; every fail was real. What made it
work: the reviewer must MEASURE (angles, lengths, displacements, diffs), never just look; and each check was first proven on the
frames Dan had rejected.

## Research findings (2026-10-14)

* **No Claude skill, plugin or MCP server does this.** The closest is a generic Ultralytics MCP (detection, segmentation, YOLO pose)
  with no quality rules ([CVDLT MCP](https://mcp.so/servers/mcp-server-cvdlt)); others only describe images. We build it ourselves.
* **Vision-language models alone are weak judges of physics violations** ([TRAVL, 2025](https://arxiv.org/abs/2510.07550)), which
  matches today: an eye check passed faults that measurement caught. Keep the reviewer, but keep it measuring.
* **3D body fitting** fixes the weak spot of our 2D bone-length check (foreshortening): [SMPLest-X](https://arxiv.org/abs/2501.09782)
  (2025, code and weights public on Hugging Face) or [Multi-HMR](https://arxiv.org/abs/2402.14654) (ECCV 2024, code public).
  They fit a full skeleton, so bone lengths and joint limits compare in 3D. ⚠ Both use the SMPL-X body model, whose standard licence
  is non-commercial; check the commercial terms before relying on it for ads.
* **Point tracking for motion takes:** [CoTracker3](https://github.com/facebookresearch/co-tracker) (Meta, ICCV 2025, checkpoints
  public) tracks points through a generated clip with visibility. Points on an object that vanish mid-frame flag RO-08's
  "donuts vaporize" class; points on feet that leave a platform flag slipping contact. Object-permanence scoring along these lines:
  [World Consistency Score](https://arxiv.org/pdf/2508.00144).
* **Watch, not usable yet:** a body-distortion detector ([Distortion-5K / ViT-HD](https://arxiv.org/abs/2503.00811), F1 0.899 at
  locating malformed body parts; release promised, not confirmed) and Google's artifact-heatmap model
  ([RichHF](https://arxiv.org/abs/2312.10240); dataset public, model weights not confirmed).
* **Not useful here:** [VBench-2.0](https://arxiv.org/abs/2503.21755)'s anatomy and mechanics dimensions do not run on custom inputs.

## The plan (recommended, in this order)

1. **A permanent reviewer agent** `.claude/agents/frame-reviewer.md` (Opus 5.5, high): the A-to-I checklist from today, generic for
   any AI pair or clip, required to measure with `framecheck` and report PASS or FAIL per item with numbers. Fresh agent per review.
2. **A frame spec written before generating** (`spec.json` per pair): who is in it, what moves and along what (a rail, a hand path),
   what must stay still, what each hand holds, contact points (feet on platform). The checks read the spec, so they know what to test.
3. **One gate command** `framecheck/gate.py START END --spec spec.json` that runs pose (angles, bone lengths within 8 %), hands
   (MediaPipe Hands, already installed: five fingers, which hand holds what), rigid tracking for declared parts, static-pixel diff,
   and writes a PASS stamp with both hashes. Review pages refuse AI frames without a stamp and a reviewer PASS, the way the delivery
   gate refuses unstamped videos. Prove it on today's rejected pairs (`/Volumes/Extreme/_edit_work/ra04/round2/frames/`: F4c_a/F5c_b,
   F4d_b/F5e_b, F5h2, F5j, F5m must fail; F4h/F5p must pass).
4. **Motion takes:** `framecheck/clipcheck.py` with CoTracker3: track a grid plus spec'd parts through each AI take; flag mid-frame
   disappearances, contact slips and parts leaving their guide; strips of the flagged frames for the reviewer. Prove it on RO-08's
   rejected donut take (`longform-edit/reference/ro08/`) before trusting it.
5. **Then 3D:** add SMPLest-X (or Multi-HMR) as a second opinion on bone lengths and joint limits, after the licence check.

Cost: open-source and local (Mac M2 Pro), no API spend. Steps 1 to 3 fit one session; 4 and 5 another. Update the ad-edit and
longform-edit skills and `VIDEO-RULES.md` (the 2026-10-13 AI clip section) to point at the gate once it exists; push each shared file
with `safe-push.sh` as it is edited.

## Starter prompt

> Read `Handoffs/handoff-20261014-frame-qc-upgrade.md` and `.claude/skills/_shared/framecheck/README.md`, then build step 4 of the
> frame-QC plan: `framecheck/clipcheck.py` with CoTracker3 for AI motion takes, reading the same frame spec as `gate.py`, proven on
> RO-08's rejected donut take. Then step 5 (3D body fitting) only if the licence check clears it. Name this task `Frame QC Motion Takes`.

**Recommended model and effort: Opus 5.5, high.**
