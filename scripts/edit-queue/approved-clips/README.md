# Approved clip registry

The live, append-only registry belongs at `/Volumes/Extreme/_edit_work/_approved_clips/index.json`.
It starts as `{"schema_version":1,"clips":[]}` and is deliberately not stored in Git because it
contains machine-specific paths and content hashes for rendered media. Frame or asset approval alone
never adds a row. A clip becomes eligible only after it appears unchanged in the delivered video and
Dan later finalizes that video; the row then binds the clip to that finalized video's SHA-256.

Each row follows `registry.schema.json`. A later edit may reuse a clip only when its file hash still
matches and `selection_fingerprint` matches the current choice. Changing the frame pair, source trim,
crop, rights note, duration, scene, boundary join, spoken beat, or intended action invalidates reuse.

Tests create their own empty registry under a temporary directory. They never read or write this live path.
