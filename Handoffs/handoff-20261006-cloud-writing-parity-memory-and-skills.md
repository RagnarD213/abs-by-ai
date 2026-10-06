# Handoff: make cloud Claude write like local Claude (memory, skills, test)

**EXECUTED 2026-10-06 (local, Opus 5.5).** Memory is in `Docs/memory/`, shared rules in `.claude/skills/_shared/WRITING-RULES.md`, test and local baseline in `Docs/CLOUD_WRITING_PARITY_TEST.md`. Left open: Dan runs the three cloud prompts and scores them.

Written 2026-10-06. Category: writing setup, no video work. Run this LOCALLY (on Dan's computer), not in the cloud.
Recommended: Opus 5.5, high effort. Never max.

## Why this exists

Dan wants to run writing tasks (scripts, outlines, copy, articles) in cloud Claude sessions. A cloud session starts from a
fresh copy of the GitHub repo. It therefore has the 32 skills, `CLAUDE.md`, `AGENTS.md`, `Docs/` and `Handoffs/`, plus the
Google Docs, Drive, Gmail, WordPress and Blotato connectors. It does NOT have:

1. Claude's local **memory folder** (lives on Dan's computer, not in git). Skills and `AGENTS.md` cite 21+ memory entries by name,
   for example `no-em-dashes`, `dan-personal-facts-for-scripts`, `ad-copy-no-unbelievable-claims`, `no-ad-agency-mention`,
   `model-routing-plan`, `drive-always-public`. In the cloud those references point at nothing.
2. Rules Dan taught Claude in earlier chats that never got written into a skill or memory.

Result today: cloud writing is competent but generic, and can break rules already settled.

## Goal

Cloud Claude and local Claude produce equivalent writing. Three jobs, in this order.

## Job 1: Copy the memory folder into the repo

1. Find the local memory folder: `~/.claude/projects/<this-project>/memory/` (check `ls ~/.claude/projects/`). Read `MEMORY.md` (the index) first.
2. Copy it to `Docs/memory/` in the repo, same filenames. Keep `MEMORY.md` as the index.
3. **Scan every file before committing.** The repo is public until Dan makes it private. Remove or replace with a pointer
   ("value lives in `~/.absbyai-secrets.env`") anything that is: an API key, token, password, subscriber email address, home
   address, ID number, or financial detail. Personal facts that scripts legitimately use (age, weight history, story beats in
   `dan-personal-facts-for-scripts`) stay, but list them in your report so Dan can veto any.
4. Split if useful: writing-relevant entries stay in `Docs/memory/`; entries that are purely about machine setup (Extreme drive,
   rclone, local launch agents) may stay too but are low priority.
5. Add to `CLAUDE.md`, near the top, one short rule: "Memory entries are in `Docs/memory/`. When a skill or rule says
   'memory `name`', read `Docs/memory/name.md`. Local sessions also have the same entries in the auto-memory folder; the repo copy
   is the cloud copy." Keep it under 3 lines; CLAUDE.md loads into every message.
6. Add a keep-in-sync step: whenever a session writes a new memory entry, it also copies it to `Docs/memory/` and pushes
   (or: add a small script `scripts/sync-memory-to-repo.sh` that copies and runs the secret scan, and note it in CLAUDE.md).
   Pick the script option; it is less likely to be forgotten.

## Job 2: Move chat-only rules into the skills

Goal: any rule Dan ever corrected Claude on, for writing, lives in a skill or memory, not only in an old chat.

1. Writing skills to sweep: `scriptwriting`, `scriptfromoutline`, `shorts-scripting`, `shortsideas`, `ad-copy`, `ad-outlines`,
   `copy-edit`, `teleprompterscripts`, `youtube-packaging` (titles and descriptions), `video-setup` (descriptions), and the
   sixpackabs.com article rules (`sixpackabs/articles/README.md`).
2. Mine the evidence:
   - Local past-session transcripts: `~/.claude/projects/<this-project>/*.jsonl`. Search Dan's messages for corrections:
     "don't", "never", "stop", "I don't like", "too", "sounds like", "that's not how I", "change", "rewrite", "why did you".
     Also his accepted and rejected edits in script Google Docs (suggestion-mode changes from `/copy-edit`).
   - Dan's own finished scripts and posts as the voice reference (finalized-scripts Google Doc, `Docs/`, `sixpackabs/articles/`).
3. For each candidate rule, check if it is already in a skill or memory. Only add what is missing.
4. Write each new rule into the single most relevant skill (a short, dated, imperative line with the reason). If it applies to
   more than one writing skill, put it in a shared file `.claude/skills/_shared/WRITING-RULES.md` and have each writing skill
   link to it in one line. Create that file if it does not exist. Do not copy the same rule into many skills.
5. Resolve every "see memory X" reference in the writing skills: either the entry now exists in `Docs/memory/`, or inline the
   rule. Produce a table in your report: skill, reference, resolved how.
6. Apply the no-em-dash rule to everything you write. count the em dash character in each new or edited file with grep -c; it must be 0.
7. Do not retrofit existing copy. Only add and fix rules.
8. Report the full list of rules found and where each went, so Dan can reject any in one pass.

## Job 3: Write and run a parity test

Put it in `Docs/CLOUD_WRITING_PARITY_TEST.md` (the test) plus results in the same file.

Design:
1. Pick 3 inputs with known good outputs Dan already approved: one ad outline to script (`/scriptwriting`), one dedicated
   short idea to script (`/shorts-scripting`), one rough paragraph to polish (`/copy-edit`). Use the approved finished versions
   as the answer key.
2. Write the exact starter prompt for each, written so it runs unchanged in a cloud session.
3. Add a checklist per output, scored yes/no: voice match (word count target of 172-185 for shorts, 66 second ceiling), no em
   dashes, no banned claims, no ad agency mention, Dan's personal facts used correctly, correct format and doc placement.
4. Run the same 3 locally first to get the baseline. Then tell Dan the three starter prompts to paste into cloud tasks,
   and the checklist to score them against the baseline. Cloud runs need to be started by Dan or a cloud session; do not
   claim they passed until they ran.
5. For every checklist miss on the cloud run, the fix is a missing rule: add it to a skill or `Docs/memory/` and re-test.
   Repeat until the cloud output passes the same checks as local.

## Ship it

1. `scripts/git/safe-push.sh -m "message" -- <files>` for every shared file (CLAUDE.md, `.claude/skills/_shared/*`, `Docs/`).
2. Confirm the push reached GitHub main (`git log origin/main -1`). Cloud sessions read from the repo, so unpushed means not
   there.
3. Delete this handoff's row in `AI_COORDINATION.md` and `Handoffs/README.md` when done. No dashboard step (paused).

## Done means

- `Docs/memory/` exists, secret-scanned, pushed, referenced from CLAUDE.md, with a sync script.
- Every "memory X" reference in writing skills resolves.
- New rules from chat history are in skills or `_shared/WRITING-RULES.md`, with a report Dan can veto.
- Parity test file exists with local baseline recorded and cloud starter prompts ready.
- Dan has the exact next action: paste the 3 prompts into cloud tasks and score them.

## Cautions

- Do not put keys, tokens, subscriber emails or home details in the repo. When unsure, leave it out and note it.
- Keep CLAUDE.md additions to a few lines. It costs context in every message.
- Do not rewrite skills wholesale. Add rules, fix dead references, nothing more.
