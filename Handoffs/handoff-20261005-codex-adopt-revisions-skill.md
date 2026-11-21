# Codex: adopt Claude's /revisions skill and review editors' cuts the same way

**Written:** 2026-10-05 by Claude (Opus 5.5) at Dan's request. **For:** Codex. **Model:** GPT-6 Astra, high (a review is
frame-level visual judgement plus writing in Dan's voice; Sol is not the place to save here).

## Why
Dan's Claude allowance for the week is nearly used, and editors keep delivering cuts. He wants Codex to review them with
the same skill, the same checks and the same document Claude produces, so an editor cannot tell which of us wrote it and
Dan forwards the doc without editing it.

## The one decision that matters: do not fork the skill
The skill is `.claude/skills/revisions/SKILL.md` (about 22,000 words). Most of it is nine "calibration passes": rules
taken from Dan's own edits to earlier docs. It changes every time Dan edits a doc. A Codex copy would be out of date
within a week, and the two of us would start writing different docs.

So: **Codex reads and follows the repo file itself, every review, in full.** What Codex installs is a thin adapter at
`~/.codex/skills/revisions/SKILL.md` (same pattern as `~/.codex/skills/abs-edit-ad/`, which is already "an adapter over
the existing production code"). The adapter holds only: the trigger description, "read the repo skill in full and follow
it", and the tool translation table below. No rules, no calibration, no format notes copied into it.

When Dan edits a doc Codex wrote, Codex writes the new calibration pass into the **repo** skill file (next pass number,
same format as passes 1 to 9), so Claude picks it up too.

## Read before the first review, in this order
1. `.claude/skills/_shared/VIDEO-RULES.md` (the skill's first line requires it).
2. `.claude/skills/revisions/SKILL.md`, all of it. Do not skim the calibration passes; they are the skill.
3. `.claude/skills/_shared/CUT-CONTINUITY-QC.md` (the jump-cut pass every review runs).
4. `.claude/skills/findassets/SKILL.md` and `DELIVERED_CLIPS.md` (how a clip named in an item gets cut, uploaded and linked).
5. `.claude/skills/revisions/reference/shorts-graphics-kit/BRIEF.md` (we build the graphics for an editor's shorts).
6. Claude's memory notes, which Codex does not load automatically. Folder:
   `~/.claude/projects/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/memory/`. Read: `revision-docs-in-dans-voice`,
   `revisions-zero-edit-goal`, `revision-status-check-live-doc`, `editor-message-voice`, `revision-task-naming`,
   `editor-shorts-graphics-kit`, `before-after-same-person`, `ai-clip-artifact-giveaways`, `editor-audio-untouched`,
   `zeeshan-delivery-includes-srt`, `no-em-dashes`, `swearing-never-cut-never-ask`, `clip-library`.
7. Two finished examples to match exactly: `revision docs/shorts-revisions-muhammad-10-2-26.md` with its `.summary.md`
   (shorts batch, round 2 and 3), and `revision docs/oura-review-revisions-zeeshan-round4-10-2-26.summary.md` (long-form).

## Tool translation (Claude's tools, and what Codex uses instead)
Every item below was checked on this Mac on 2026-10-05.

| The skill says | Codex does |
|---|---|
| Google Drive connector `create_file` with markdown | Convert the markdown to HTML, then import it as a Google Doc with rclone (recipe below) |
| Drive connector `read_file_content` on a doc id | `curl -sL "https://docs.google.com/document/d/<ID>/export?format=md"` (works with no login on any anyone-with-link doc; for a private doc use `rclone copyto` with `--drive-export-formats docx`) |
| Drive connector `search_files` in a folder | `rclone lsjson -R "gdrive:<path>"` or `rclone lsjson --drive-root-folder-id <FOLDERID> gdrive:` |
| `python3 -m gdown <FILEID>` | Same. gdown 5.2.2 is installed for python3.9 |
| ffmpeg / ffprobe | Not on PATH. `Media/video_edit/bin/ffmpeg` and `ffprobe`. Whisper shells out to `ffmpeg` by name, so run it with `PATH="$PWD/Media/video_edit/bin:$PATH"` |
| Local Whisper `small` | `python3 -m whisper` (installed for python3.9) |
| Rename the session to "<Editor> revisions" | Rename the Codex task the same way, first action of every review |
| Gemini second opinion on AI shots | Allowed under the standing authorization in `AGENTS.md` (up to $5 a batch). A Gemini "clean" never overrules your own frames |
| Chrome paste into an existing doc (`md_to_docs_clipboard.py`, lessons 20 and 24) | Same script, Codex's own Chrome or computer-use tools |

**Creating the Google Doc (the one real gap, tested end to end):**

    python3 - <<'EOF'
    import sys; sys.path.insert(0, '.claude/skills/revisions/reference')
    from md_to_docs_clipboard import to_html
    md = open('revision docs/<name>.md').read()
    open('/tmp/<name>.html', 'w').write('<html><body>' + to_html(md) + '</body></html>')
    EOF
    rclone copyto /tmp/<name>.html "gdrive:Revision Docs/<name>.html" --drive-import-formats html --drive-export-formats html
    rclone lsjson "gdrive:Revision Docs" --drive-export-formats html      # the ID of the new Doc
    rclone link "gdrive:Revision Docs/<name>.html" --drive-export-formats html   # sets anyone-with-link view

Both format flags are required; with only the import flag rclone refuses. `to_html` already handles the revisions
dialect: H2 headers, bullets nested to any depth, bold, Dan's literal `\*\*HEADER\*\*` look, and `<https://…>` links.
After creating the doc, read it back with the export URL and confirm the nesting, the links and the title (rename the
doc in Drive if the title kept `.html`). Use the Drive folder the recent docs live in if you can find it by listing;
otherwise `Revision Docs/` is fine. Every doc is anyone-with-link view (Dan's Drive rule).

⚠ rclone prints a notice that its shared client id is being retired during 2026. If doc creation starts failing with a
403 or an auth error, that is the cause: tell Dan in one line, and fall back to the Chrome paste route.

## What "the same way" means: the points Codex is most likely to get wrong
The skill is the authority. These are the ones that have cost a round before.

1. **The doc is Dan's.** First person, his format, his status words. Nothing says a review, a check, a tool or an AI was
   involved, in the Doc, the markdown copy or the message. Never send anything to an editor; Dan forwards it.
2. **Confirm the editor and the round before writing.** Several editors cut the same script; a new cut of a reviewed
   video is usually someone else's round 1.
3. **A status check starts from the live Google Doc**, not our markdown copy. Dan deletes and adds items after we write.
4. **Zero-edit goal.** Run the skill's step 7 self-check, pass by pass, before delivering. Items fix what is wrong; they
   do not upgrade what is acceptable.
5. **Every review produces three things:** the Google Doc, the byte-exact markdown copy in `revision docs/`, and a
   `.summary.md` beside it holding the table, what he did and did not do, "AI CLIPS FLAGGED, watch before forwarding",
   "Approved on your behalf", "For your call", and the paste-ready message to the editor in Dan's voice.
6. **Measure, do not eyeball:** the audio gate and `pick_lav --analyse` first, `framing.py`, `sets_level.py` on workout
   videos, full-resolution crops of every text panel read against the script, and the AI-artifact pass on consecutive
   frames with the false-positive protocol.
7. **Library first.** Our B-roll, then our existing AI clips, then stock, and a new AI clip last (step 6).
8. **We build the graphics** for an editor's shorts when his are off (step 6b), and link the files in the doc.
9. **No em dashes, anywhere.** The skill's older worked examples still contain them ("Hey Muhammad", "Ad 8", the
   2026-09-18 samples). Do not copy that punctuation. Use a comma, a colon or two sentences, the way the 10-02 docs do.
   Search the markdown, the summary and the message for the em dash character before delivering (the check in `AGENTS.md`); each count must be 0.
10. **No compliance commentary** in a review. Stay on the cut.
11. **Finalized queue jobs:** when Dan finalizes a cut that is a job on `Handoffs/video-editing/00-MASTER.md`, set it on
    the Edit Queue page per `.claude/skills/_shared/edit-queue/README.md`. The Victory Dashboard is paused; do not touch it.

## Steps for this handoff
1. Do the reading above.
2. Write the adapter at `~/.codex/skills/revisions/SKILL.md` (frontmatter name `revisions`, a trigger description taken
   from the repo skill's own, the "read the repo file in full" instruction, and the translation table). Add one line to
   `~/.codex/AGENTS.md` if that is where Codex records its project skills.
3. Prove the Doc route once with a three-line test file, read it back, then delete the test file.
4. **Parity check, one video only.** Take one short from Muhammad's 2026-10-02 delivery (the sent doc is
   `1AR_8AeBzwhTuGelBlz1IRPcvKi5MHr-HT2kUTQ29o6s`; his files are in the Drive folder he named "Daniel HQ"). Review it
   cold with the skill, without opening Claude's doc first. Then compare your item list with Claude's section for that
   video and report: items both found, items only Claude found, items only you found, and for each difference which
   rule in the skill decides it. Do not send or publish this; it is a private check. If Dan hands you a real new cut in
   the same session, skip the parity check and let the real review be the proof.
5. Report to Dan in plain language: the adapter is installed, the Doc route works, the parity result, and anything in
   the skill you could not do with Codex's tools.

## Not in scope
No changes to the repo skill's rules. No messages to editors. No re-rendering of any video. No reviews of our own
pipeline builds (those go through the round method in `_shared/PRE-RENDER-APPROVAL.md`).

## Deliver
Nothing in the repo changes in this handoff unless you fix a wrong path in the skill; if you do, push it with
`scripts/git/safe-push.sh`. Never commit media. When done, delete this handoff's line from the HANDOFFS section of
`AI_COORDINATION.md` and mark its row in `Handoffs/README.md`.

## Starter prompt (Codex, GPT-6 Astra, high) for adopting the skill
> Read `Handoffs/handoff-20261005-codex-adopt-revisions-skill.md` and execute it. Adopt Claude's /revisions skill
> without forking it: read `.claude/skills/revisions/SKILL.md` in full, install the thin adapter in
> `~/.codex/skills/revisions/`, prove the Google Doc route, run the one-video parity check, and report back in plain
> language. Do not message any editor.

## Starter prompt for every review after that (Codex, GPT-6 Astra, high)
> Name this task "<Editor> revisions". Use the revisions skill: read `.claude/skills/revisions/SKILL.md` in full and
> follow it exactly. Editor: <name>. Round: <n>. Cut(s): <Drive link or folder>. Write the Google Doc in my voice, save
> the markdown copy and the summary in `revision docs/`, and give me the doc link, the top findings, anything that
> needs my call, and the paste-ready message. Do not send anything to the editor.
