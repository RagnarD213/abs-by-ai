# Asset approval and placeholder editing

Use this after the scene plan and before paying for AI motion or committing a new stock/existing-B-roll choice. It preserves the normal quality bar; it moves a costly source-selection mistake earlier.

## One early approval package

The owning editor prepares and sends one compact package immediately, then continues the rest of the edit without waiting. Group items in timeline order and show enough context to judge each choice:

- slot ID, exact in/out and spoken line or beat;
- why the insert supports that beat;
- AI motion: one best start frame, one matching end frame, intended action, duration and estimated new/total per-video cost;
- stock or existing B-roll: a 0.5–15 second moving preview of the exact proposed source trim, crop and basic treatment, plus source ID/path, usage-rights evidence and hash;
- whether the choice is new, previously approved and hash-matching, or reused without another approval.

Prefer one strong AI frame pair. Offer alternatives only when a real creative choice cannot be resolved by the editor. Check the approved-clip library and exact existing assets before proposing new generation. Do not resubmit an unchanged approved asset merely because a later revision touches another scene.

## Durable packet

Write `placeholders.json` beside the internal draft. It is the authoritative resume record, not a chat transcript. Use schema version 1 and include:

```json
{
  "schema_version": 1,
  "video_id": "RA-00",
  "revision": 1,
  "status": "approval_required",
  "draft": {"path": "/absolute/DRAFT.mp4", "sha256": "..."},
  "prior_paid_spend_usd": 0.0,
  "generation_budget_usd": 5.0,
  "items": [{
    "id": "clip-01",
    "type": "ai_motion",
    "reuse_status": "new",
    "in": 12.4,
    "out": 16.4,
    "duration": 4.0,
    "spoken_beat": "...",
    "intended_action": "...",
    "affected_scenes": ["scene-07"],
    "boundary_joins": ["join-06-07", "join-07-08"],
    "start_frame": {"path": "/absolute/start.png", "sha256": "..."},
    "end_frame": {"path": "/absolute/end.png", "sha256": "..."},
    "preview": null,
    "source": null,
    "placeholder": {"label": "PLACEHOLDER — clip-01", "sha256": "..."},
    "estimated_usd": 0.90,
    "approval": {"status": "pending", "selected_hashes": [], "words": null,
      "timestamp": null, "selection_fingerprint": null},
    "final_clip": null
  }]
}
```

For `stock` and `existing_broll`, use `preview` and `source` records instead of start/end frames; `preview` also carries
`preview_seconds`, while `source` carries
`trim_in`, `trim_out`, `crop` and `rights`. Every path is absolute, contained by the work directory or an explicitly
configured source root, and hash-checked on every read. Record Dan's exact words, timestamp, selected hashes and the
derived selection fingerprint. A material change to timing, beat, action, scenes/joins, frame, source, trim, crop or
rights becomes `pending` again; unchanged approved items stay approved. Partial and duplicate submissions are refused.
The queue adds ISO-8601 `created_at` and `updated_at` fields. If prior spend is unknown,
`prior_paid_spend_usd` is `null` and `prior_paid_spend_reason` is required; new AI motion cannot be approved until that
cost is known. At completion, `delivery` records the final video's path/hash and the chronological watch log's
path/hash. Each `final_clip` records its path/hash and the approved `inserted_from_fingerprint`.
The queue also requires the existing `PRE_RENDER_CHECK.json` motion evidence for every stock/existing-B-roll preview;
a still or a preview outside 0.5–15 seconds parks stage one before it can wait for approval.

## Placeholder draft

Build the rest of the video normally. Each unresolved slot has its exact planned duration and a conspicuous internal label such as `PLACEHOLDER — clip-01 — intended action`; AI slots may hold the proposed start frame. Keep the voice, timing and surrounding edit reviewable.

Name the review copy `DRAFT - ...`. It may run diagnostics, but its overall status stays DRAFT while any item is pending or any placeholder remains. Never grant or copy a delivery PASS, present it as final, upload it, or ask the independent final reviewer to review it as a complete candidate.

## Resume after Dan's decision

Do not keep an AI session alive while waiting. Persist the packet, write the queue's `DRAFT-DELIVERY.json`, and exit.
The runner sets `draft_review`; a complete current approval batch sets `frames_approved`. Approval while stage one is
still running updates only the packet and never changes or steals its claim.

On approval, a fresh finishing session in the same work directory and logical revision verifies the stored hashes.
Generate AI motion only from the approved frame pair and within the remaining per-video budget. Insert the exact
approved stock/B-roll trim. Rebuild affected scenes and boundary joins only, remove all placeholder labels, and set
the packet to `complete` only when every item has an approved final clip hash plus hash-bound delivery/watch evidence.

Then perform the ordinary full-file gates, chronological picture/audio review and one independent complete-candidate review. Report revision count, available editor/reviewer model usage, itemized paid-provider charges, and every unavailable measurement as `null` with its reason.
