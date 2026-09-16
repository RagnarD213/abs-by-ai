# Edit queue status: keep Dan's Abs By AI Edit Queue current

Dan's pinned page **https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs** lists every video-editing job
(`Handoffs/video-editing/`, IDs like `RA-01`, `DS-04`, `RO-02`, `SL-01`, `AV-05`, `AS-04`). It reads each job's
status live. **Any skill or agent (Claude, Codex, Grok Bot) that edits, finalizes or uploads a video on that list
updates its status at the moments below.** The record lives in three places, and `queue.py` keeps the first two equal:

* `Handoffs/video-editing/jobs.json`: the source of truth in git
* **Google Drive `Abs By AI automation/edit-queue-status.json`** (file id `1RX-GqepEKqB1LgJqJFRyRU2lOJMnRFgg`): uploaded
  by `queue.py` on every change via `~/bin/rclone`. The page reads it through Dan's Google Drive connector and
  re-checks every minute, so **any agent's update shows within about a minute of the page being open**
* the artifact db `jobs/<ID>`: a mirror Claude sessions write, used when the Drive read isn't available

## When to set which status (Dan, 2026-09-16)

| moment | state | who sets it |
|---|---|---|
| a session starts building the job | `in_progress` | the editing session |
| the review copy is delivered to Dan | `delivered` | the editing session |
| **Dan says the video is finalized / approved / done** | `finalized` | the session Dan says it to |
| **the finished video is uploaded and set up**: ads uploaded Unlisted and added to Google Ads (`/ad-setup`); organic uploaded Private + queued in Blotato (`/video-setup`) | `uploaded` | the setup session |
| Dan answers a "needs your call" question, or a blocker clears | `ready` (or `blocked` with the new reason) | whoever learns it |

**`finalized` means Dan's words, never a passed gate.** **`uploaded` only after the upload's visibility was read back
(Unlisted for ads, Private for organic) and, for ads, the Google Ads entry exists.** Never set `uploaded` at finalize time.

**Which job does a video belong to?** Match by the job's title or file in `Handoffs/video-editing/00-MASTER.md`. A
square/vertical of an ad maps to its `AV-`/`AS-` job. If the video isn't on the list (e.g. an editor's own 16:9 final),
there's nothing to update. If a finalized ad now owes variants (Ads 8, 9, 13, 15), add its AV/AS jobs (below).

## How (Claude session)

```bash
python3 scripts/edit-queue/queue.py set AV-05 finalized --by "Claude" --note "Dan finalized 09-18"
```
It updates `jobs.json` + the row in `00-MASTER.md`, uploads the Drive status file (this is what updates the page), and
prints one write entry. Mirror it to the artifact db:

* `Artifact` → `action: "write_db"`, `url: "https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs"`, `db_op: "set"`,
  `collection: "jobs"`, `doc_id: "<ID>"`, `file_path: <the printed file_path>`
* then `python3 scripts/edit-queue/queue.py mark-synced <ID>`
* commit `Handoffs/video-editing/jobs.json` + `00-MASTER.md` with the task's other changes. Other sessions often leave
  unrelated uncommitted edits; stage only these files.

**Catch up on anything Codex changed:** `python3 scripts/edit-queue/queue.py pending` prints the write entries for every
job whose status changed since the last sync. Send them in one `write_db` `db_op: "batch"` (≤ 50 per call), then
`mark-synced` those IDs. Run it whenever you touch the queue.

**New jobs** (a newly finalized ad's AV/AS pair, a new SL job): write the handoff doc and the `00-MASTER.md` row, put the
job record(s) in a JSON file (same fields as an existing record in `jobs.json`: `id, list, group, sub, title, roll,
size, file, claudeModel, claude, codexModel, codex, state, note`), run `queue.py add <file>`, and send the printed
entries with `write_db` batch. The page shows new IDs automatically.

## How (Codex or Grok Bot session)

Run the same `python3 scripts/edit-queue/queue.py set <ID> <state> --by "Codex"` (or `"Grok Bot"`) and check it prints
`Drive status file … uploaded`. That alone updates Dan's page. Then commit `jobs.json` + `00-MASTER.md`. If the upload
failed, run `queue.py push` once rclone works again, and tell Dan. Skip the `write_db` step: you can't reach the
artifact, and the next Claude session's `queue.py pending` mirrors it.

## If a write fails

A failed `write_db` or Drive upload never blocks the repo update: `jobs.json` still changes. For Drive, `queue.py push`
re-uploads everything. For the db, `syncedRev` stays behind and `pending` picks it up later. ⚠ rclone uses a shared
Google client id that Google is retiring during 2026 (memory `drive-backup-capability`). If uploads start failing
with quota or auth errors, that's why, and Dan needs his own client id set up.
