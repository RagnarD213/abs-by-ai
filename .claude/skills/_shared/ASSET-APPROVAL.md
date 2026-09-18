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
  "items": [{
    "id": "clip-01",
    "type": "ai_motion",
    "in": 12.4,
    "out": 16.4,
    "spoken_beat": "...",
    "intended_action": "...",
    "start_frame": {"path": "/absolute/start.png", "sha256": "..."},
    "end_frame": {"path": "/absolute/end.png", "sha256": "..."},
    "preview": null,
    "source": null,
    "placeholder": {"label": "PLACEHOLDER — clip-01", "sha256": "..."},
    "estimated_usd": 0.90,
    "approval": {"status": "pending", "selected_hashes": [], "words": null},
    "final_clip": null
  }]
}
```

For `stock` and `existing_broll`, use `preview` and `source` records instead of start/end frames. Include the exact proposed trim/crop hash and source-rights note. Record Dan's exact approval/rejection words and the selected hashes. A materially changed frame, source, trim, action or duration becomes `pending` again; other approved items stay approved.

## Placeholder draft

Build the rest of the video normally. Each unresolved slot has its exact planned duration and a conspicuous internal label such as `PLACEHOLDER — clip-01 — intended action`; AI slots may hold the proposed start frame. Keep the voice, timing and surrounding edit reviewable.

Name the review copy `DRAFT - ...`. It may run diagnostics, but its overall status stays DRAFT while any item is pending or any placeholder remains. Never grant or copy a delivery PASS, present it as final, upload it, or ask the independent final reviewer to review it as a complete candidate.

## Resume after Dan's decision

Do not keep an AI session alive while waiting. Persist the packet and exit. For a queue job, use `draft_review`/`frames_approved` only after those states exist; until then use a supported waiting state and include the packet path in the note.

On approval, verify the stored hashes. Generate AI motion only from the approved frame pair and within the remaining per-video budget. Insert the exact approved stock/B-roll trim. Rebuild affected scenes and boundary joins only, remove all placeholder labels, and set the packet to `complete` only when every item has an approved final clip hash.

Then perform the ordinary full-file gates, chronological picture/audio review and one independent complete-candidate review. Report revision count, available editor/reviewer model usage, itemized paid-provider charges, and every unavailable measurement as `null` with its reason.
