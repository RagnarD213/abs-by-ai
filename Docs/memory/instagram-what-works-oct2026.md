---
name: instagram-what-works-oct2026
description: "Measured 2026-10-20 on @danrosefit (65 posts, Meta API): exercise mistake-and-fix Reels are the only growth format; talk-only Reels and physique photo posts don't reach strangers"
metadata:
  node_type: memory
  type: project
  originSessionId: e3206ffd-38e1-4f64-9e38-64498f514113
  modified: 2026-10-20T21:03:39.033Z
---

**Deep dive 2026-10-20** (Meta Graph API, every @danrosefit post Aug 20 to Oct 17; organic numbers only, ads excluded).
Plan page: see the session's published "@danrosefit Growth Plan" artifact.

- **Exercise mistake-and-fix Reels win.** Dan moving in second one, names a mistake ("most people jump rope with both
  feet"), shows the fix, 35-52 s. All top 7 Reels (868-2,243 reached, 12-16 s average watch). Median 589.
- **Talk-only Reels** (food, AI tools, habits said to camera): median 394, none above 538, viewers leave at 4-7 s.
- **Physique photo posts** with the tip only in the caption: median 336, mostly followers. In 30 days Reels reached
  9,565 non-followers vs 1,847 for photo posts. Same topic as photo vs demo Reel: jump rope 314 vs 2,243; towel back 261 vs 1,430.
- **Full long-form films posted as Reels**: 2-13% watched; deadlift film (1,374) the exception.
- **Shares** median 0 per Reel; comments 1-3. Followers ~5/day without ads, ~11/day during the $40/day test.
- Engaged audience 84% men, 25-44 (25-34 largest), US/CA/AU/UK. Follower list has an Austin cluster.
- Volume was not the problem (~10 posts/week). From mid-Nov the queue is mostly photos and generic "Saveable Series"
  checklist carousels (studio27 batch); exercise Reels drop to 1-2/week.
- **Trial Reels via Blotato need 1,000 followers** (`trial.graduationStrategy`); Blotato also supports `collaborators`.
- Reading the data: `GET /17841401601139982/media` + `/{media}/insights` with `META_ADS_TOKEN` + appsecret_proof
  (v21.0); account `insights` windows max 30 days. `profile_links_taps` is contact buttons, not the bio link.

**Dan's call, 2026-10-20:** the old pool-photo posts (shirtless photo, tip only in the caption) are retired; he called them
pointless "unless you're a personal friend". All of them were deleted from the queue on Instagram and Facebook. The Codex
studio batch (designed posts with the point on the image, carousels first) is the photo content now, and new photo posts
should be made like it. Receipt: `Docs/STUDIO27_BLOTATO_QUEUE_RECEIPT_20261003.md`, 2026-10-20 section.

Related: [[instagram-account-state]], [[shorts-organic-research]], [[shorts-reason-to-watch]], [[meta-ads-instagram-identity]].

**Template R1 (2026-10-20, Claude Opus):** Design canvas "Instagram Template R1", https://claude.ai/artifact/VxoxLtBBYkWLuKixTCSk3m :
5 carousels + 5 singles + a template sheet. Six series (The Fix, Receipts, Steal My, Swaps/The Math, Proof, Straight Talk),
ink/bone/red/yellow, Anton + Manrope, real footage stills first. Proposed 4-week test vs the studio batch in the M/W/F 5 PM
slots, judged on non-follower reach and saves at day 7. Awaiting Dan's picks; nothing queued.

**Template batch 1 (2026-10-21/22):** Dan approved The Fix, Receipts and Steal My Workout carousels plus the cheat sheet;
rejected Swaps, Timeline and the photo singles. C1-C3 queued, then his round 1 picks (4 Fix, 2 workouts) Oct 23-Nov 9;
all 26 Codex studio posts retired to `scripts/blotato/photo_reserve.json`. Generator: `/instagram-posts` skill. Receipts
needed more visuals; last slides always show a big shirtless cutout. Receipt: `Docs/IG_TEMPLATE_QUEUE_RECEIPT_20261021.md`.
