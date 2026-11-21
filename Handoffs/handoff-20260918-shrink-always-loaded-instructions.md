# Handoff — cut the instructions that load into every session by about half

Written 2026-09-18 by Claude (Fable 5.1) at Dan's request. **Executor: Codex** (a careful text-moving job; no Claude allowance).

## Why

Every Claude session in this project — and every subagent it spawns — loads these before doing anything
(measured 2026-09-18):

| file | words |
|---|---|
| `AGENTS.md` | 5,120 |
| `AI_COORDINATION.md` | 2,500 (at its cap) |
| `memory/MEMORY.md` index | 2,134 |
| `CLAUDE.md` | 1,407 |
| **total** | **11,161 ≈ 15k tokens** |

About 3,300 words of `AGENTS.md` are video/photo production rules that load even for a dashboard check-off or a TWC run.
Two sections are in **both** `CLAUDE.md` and `AGENTS.md` word for word ("Video review refinements — C1652 R3" and
"Horizontal footage stays completely static"), and `CLAUDE.md` imports `AGENTS.md`, so they load twice.

## Goal

`AGENTS.md` + `CLAUDE.md` together ≤ **3,000 words**, with **no rule lost and no rule reworded**. Video sessions still
see every video rule, because the video skills point at the new file.

## The one hard constraint

These rules are Dan's words and several cost him real money when they were missing. **Move text verbatim. Do not
summarize, merge, "tidy" or rephrase a rule.** The only text you write is pointers.

## Steps

1. `git pull --rebase`. **`AGENTS.md` and `CLAUDE.md` had uncommitted edits from other sessions on 2026-09-18** — run
   `git diff AGENTS.md CLAUDE.md`. Those edits are other sessions' rule additions: keep them. Commit them first as their own
   commit ("AGENTS/CLAUDE: pending rule additions") so the move is a clean diff.
2. Create **`.claude/skills/_shared/VIDEO-RULES.md`**. Move these `AGENTS.md` sections into it verbatim, headings intact:
   - Standing authorization for thumbnail replacement
   - Video clip generation budget and frame approval
   - A before and after picture are the SAME PERSON
   - Video editing feedback — organic C1652
   - Reusing Dan's previously produced videos
   - Label Dan's real pictures
   - Don't default to frowning photos
   - Audio: one standard, enforced by a stamp
   - One delivery gate, versioned, on the delivered file
   - No gate change ships without the regression corpus
   - Video builds: never run more than two at once
   - Video review refinements — C1652 R3
   - Horizontal footage stays completely static
3. Delete the two duplicated sections from `CLAUDE.md` (they now live once, in VIDEO-RULES.md).
4. **Two publishing rules stay in `AGENTS.md` but shrink to their first bullet + a pointer**, full text moved to
   VIDEO-RULES.md: "An AD is never published organically" and "YouTube visibility — never upload Public". They bind
   non-video sessions too (Blotato, ad setup), so a one-paragraph version must stay always-loaded. Both are also enforced in
   code (`scripts/blotato/ad_guard.py`, the PreToolUse hook), which is the real safety net.
5. In `AGENTS.md`, where the sections were, add exactly one block:
   > **Video, photo, thumbnail, cover, audio and publishing work: read `.claude/skills/_shared/VIDEO-RULES.md` in full before
   > doing anything.** It holds Dan's standing production rules. Not having read it is not an excuse.
6. Make the pointer unmissable for the tools that need it:
   - Add a first-line "Read `_shared/VIDEO-RULES.md` first" to each video/photo skill's `SKILL.md`: `ad-edit`,
     `longform-edit`, `shorts`, `shortad-from-longform`, `website-video`, `coverimage`, `youtube-packaging`,
     `video-setup`, `ad-setup`, `revisions`, `photo-edit`, `background-removal`, `make-ad`, `exercisegeneration`, `findassets`.
   - Same line in `.claude/skills/_shared/EDITOR-CARD.md`, `Handoffs/video-editing/00-RULES.md`,
     `scripts/edit-queue/preamble.md` and `scripts/edit-queue/reviewer-brief.md`, and in the `ra-editor` / `ra-reviewer`
     agent definitions under `.claude/agents/`.
7. `CLAUDE.md` "Shared-workflow requirements" repeats most of `AGENTS.md` "Session coordination". Keep the `CLAUDE.md`
   copy (it has the two incident notes); reduce the `AGENTS.md` section to the bullets that are not in `CLAUDE.md`. If
   unsure whether a bullet is a duplicate, keep it.
8. **Verify nothing was lost:** for every sentence removed from `AGENTS.md`/`CLAUDE.md`, confirm it exists in
   VIDEO-RULES.md or still in one of the two files. A script that splits the pre-change files into sentences and greps the
   post-change trio is enough; paste its "0 missing" result in chat.
9. `wc -w AGENTS.md CLAUDE.md` — report before/after.
10. Commit + push to `main`. No deploy involved.

## Optional second pass (only if step 9 is done and clean)

- `memory/MEMORY.md` (2,134 words) at `~/.claude/projects/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/memory/`:
  it is an index, one line per memory. Shorten hooks to ≤ 12 words each; **do not delete or edit any memory file**, only
  the index lines. Target ≤ 1,400 words.
- `AI_COORDINATION.md`: do **not** restructure it — sessions own their entries. Only report to Dan which DAN'S DECISIONS
  entries are older than 14 days so he can kill them.

## Do not

- Do not reword, shorten or drop any rule. Do not touch gates, thresholds, the corpus, or any skill's technical content.
- Do not move the non-video standing authorizations, "Delivery and deployment", "Communication", "Context preservation",
  the Gemini-review and AI-spend authorizations, or the dashboard authorization — every session needs those.

## Done means

Before/after word counts, the "0 missing" proof, the list of files that got the pointer line, pushed commit hash, and a
two-sentence plain-English summary for Dan.
